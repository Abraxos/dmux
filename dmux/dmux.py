from pathlib import Path
from configparser import ConfigParser
import logging as log

from libtmux import Server, Session
import attr
from attr.validators import instance_of
import click


# set up configuration and logging
CONFIG_PATH = Path.home() / '.config' / 'dmux' / 'config.ini'
LOG_PATH = Path.home() / '.config' / 'dmux' / 'dmux.log'
SESSION_NAME = 'dmux'

LOG_PATH.parent.mkdir(exist_ok=True)
LOG_PATH.touch(exist_ok=True)
log.basicConfig(filename=str(LOG_PATH),
                format='%(asctime)s:%(levelname)s: %(message)s',
                level=log.DEBUG)


def get_session(session=SESSION_NAME):
    if not Server().has_session(session):
        Server().new_session(session)
    return Server().find_where({"session_name": session})


@attr.s
class DmuxWindow(object):
    name = attr.ib(validator=instance_of(str))
    incantation = attr.ib(validator=instance_of(str))
    tmux_window = attr.ib(None)
    session = get_session()

    def _link(self):
        self.tmux_window = self.session.find_where({'window_name': self.name})
        if not self.tmux_window:
            log.info("Creating new window: {}".format(self.name))
            self.tmux_window = self.session.new_window(self.name)
        self.primary_pane = self.tmux_window.panes[0]
        return self

    def stop(self):
        self._link()
        log.info("Stopping: {}".format(self.name))
        self.primary_pane.cmd('send-keys', 'C-c')
        return self

    def start(self):
        self._link()
        log.info("Starting: {}".format(self.name))
        self.primary_pane.send_keys(self.incantation, enter=True, suppress_history=False)
        return self

    def restart(self):
        log.info("Restarting: {}".format(self.name))
        self.stop()
        self.start()
        return self


def load_config(path):
    if not path.exists():
        path.parent.mkdir(exist_ok=True)
        path.touch(exist_ok=True)
    config = ConfigParser()
    log.info("Reading configuration at: {}".format(str(path)))
    config.read(str(path))
    log.info("Config loaded")
    return {w: i for w, i in zip(config.sections(), [config[s]['incantation'] for s in config.sections()])}


def windows_or_die(windows, config):
    for w in windows:
        if w not in config:
            log.error("There is no tmux window named '{}' in the configuration.".format(w))
            exit(1)
    return windows


@click.group()
def dmux():
    """An extremely simplistic service management system that contains all services inside of a tmux session called 'dmux' where every service gets its own window and is run as a simple command line program. Dmux is driven by a configuration file for a given user in ~/.config/dmux/config.ini and can be run at startup by adding the following line to the user's crontab (crontab -e): @restart dmux start"""
    pass


@dmux.command()
def attach():
    """Attaches the current shell to the tmux session named 'dmux'"""
    get_session().attach_session()


@dmux.command()
@click.argument('windows', nargs=-1)
def start(windows):
    """Starts either a particular service that exists in the configuration, or all of them."""
    config = load_config(CONFIG_PATH)
    windows_or_die(windows, config)
    if windows:
        log.info("Starting: {}".format(str(windows)))
        [DmuxWindow(w, i).start() for w, i in config.items() if w in windows]
    else:
        log.info("Starting all windows")
        [DmuxWindow(w, i).start() for w, i in config.items()]
    get_session().attach_session()


@dmux.command()
@click.argument('windows', nargs=-1)
def restart(windows):
    """Restarts either a particular service that exists in the configuration, or all of them."""
    config = load_config(CONFIG_PATH)
    windows_or_die(windows, config)
    if windows:
        log.info("Restarting: {}".format(str(windows)))
        [DmuxWindow(w, i).restart() for w, i in config.items() if w in windows]
    else:
        log.info("Restarting all windows")
        [DmuxWindow(w, i).restart() for w, i in config.items()]
    get_session().attach_session()


@dmux.command()
@click.argument('windows', nargs=-1)
def stop(windows):
    """Stops either a particular service that exists in the configuration, or all of them."""
    config = load_config(CONFIG_PATH)
    windows_or_die(windows, config)
    if windows:
        log.info("Stopping: {}".format(str(windows)))
        [DmuxWindow(w, i).stop() for w, i in config.items() if w in windows]
    else:
        log.info("Stopping all windows")
        [DmuxWindow(w, i).stop() for w, i in config.items()]


if __name__ == '__main__':
    dmux()
