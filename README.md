# dmux

A simple set of functions to manage services as running processes inside of tmux.

## Installation

Clone this repository (for this example: `~/repo/dmux`) and then execute the following with pip, prefersbly in a `virtualenv` if you plan on developing it.

```
pip install ~/repo/dmux
```

If you want it to start up all the processes when your computer boots up, add the following to your crontab: (`$ crontab -e`):

```
@reboot dmux start
```

## Usage

### Configuration

As of right now the configuration is fairly simple: You make a list of windows each of which has an incantation for a program to launch. Make sure that the windows are not named the same as the program being launched inside of them. You **must** save the configuration to: `~/.config/dmux/config.ini`

**Example:**

```
[htop-]
incantation = htop

[ncdu-]
incantation = ncdu -x /
```

### Running

To launch all processes:

```
dmux start
```

To launch a specific process:
```
dmux.py start htop-
```

To restart:

```
dmux restart
dmux restart htop-
```

To attach:

```
dmux attach
```