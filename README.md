# Wallmatic
**Wallmatic** is a lightweight CLI wallpaper manager for Wayland (tested on Hyprland) that supports mood-based themes and global randomization.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)  ![Hyprland](https://img.shields.io/badge/Hyprland-58C4DC?logo=hyprland&logoColor=white) ![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
## Features
- **Three Modes:**
	- `global`: Random wallpaper from your entire collection.
	- `mood`: Random wallpaper from a specific theme (sub-folder). 
	- `static`: Lock a specific image.
- **Multi-Daemon Support:** Works with awww (swww) and hyprpaper.
- **Automation:** Integration with native Systemd user units for background wallpaper rotation.
- **Color Engine Support:** Automatically updates your system colors by invoking Pywal or Wallust on the current wallpaper.
- **Waybar Support:** Auto-reloads Waybar to apply a new CSS palette.
- **CLI First:** Fully manageable via a clean Typer-based interface.

## Prerequisites
To use Wallmatic, you need at least one **wallpaper daemon** installed:
- [awww](https://codeberg.org/LGFae/awww) (formerly `swww`) — An efficient wallpaper daemon for Wayland.
- [hyprpaper](https://github.com/hyprwm/hyprpaper) — A simple and fast wallpaper utility for Hyprland.

**Optional dependencies:**
- [pywal](https://github.com/dylanaraps/pywal) — A tool that generates a color palette from the dominant colors in an image.
- [wallust](https://codeberg.org/explosion-mental/wallust) — A fast, Rust-based tool for generating color palettes from images (a modern alternative to pywal).
## Installation
It is recommended to use [pipx](https://github.com/pypa/pipx) to install Wallmatic globally in an isolated environment:
```bash
pipx install git+https://github.com/Kybereth/wallmatic
```

## Quick Start
```bash
# Initialize Wallmatic and set your wallpaper directory
wallmatic init --directory ~/Pictures/Wallpapers

# Choose a mode (default is global):
wallmatic set-mode mood --theme mountains

# Pick a random wallpaper
wallmatic next

# See your current settings
wallmatic status

# Not sure about commands? Use the built-in help:
wallmatic --help
```

## Automation (Timer)
Wallmatic integrates directly with Systemd User Units to handle background automation.
```bash
# Enable wallpaper switching every 15 minutes (and keep wallpaper on boot)
wallmatic timer enable --interval 15m --restore

# Enable switching at specific times (e.g., 9:00 and 18:00) and roll a new wallpaper on boot
wallmatic timer enable --hours "09,18:00" --change-on-boot

# Check the current background daemon status
wallmatic timer status

# Completely disable automation and remove systemd unit files
wallmatic timer disable
```

### Accepted Formats:
- `--interval (-i)`: Takes standard systemd time spans, e.g., `30s` (seconds), `15m` (minutes), `2h` (hours), `1d` (days).
- `--hours (-h)`: Takes standard systemd `OnCalendar` hour notation, e.g., `21:00` (every day at 9 PM), `06,12,18:00` (three times a day).

## Configuration
Wallmatic stores its configuration in `~/.config/wallmatic/config.yaml`. You can manage it via the CLI:
```bash
# Set the color generation engine (options: pywal, wallust, none)
wallmatic config set color_engine wallust

# Change wallpaper daemon (default is "auto")
wallmatic config set wallpaper_daemon awww

# Open the raw configuration file in your default system editor ($EDITOR)
wallmatic config edit

# Reset configuration to default if something goes wrong
wallmatic config reset
```
For advanced tweaks (like awww animation speed, transitions, or FPS), use `wallmatic config edit` to modify the `daemon_options` block inside the YAML file directly.


## Wallpaper Directory Structure
For **global** and **mood** to work correctly, organize your wallpapers into subdirectories (themes):
```
Wallpapers/
├── nature/
│    ├── forest.jpg
│    ├── mountains.webp
├── space/
│     ├── mars.png
│     └── milky-way.webp
└── cyber/
      └── neon-city.png
```

## Roadmap
- [x] **Automated Switching:** Systemd daemon (enable/disable, interval control).
- [ ] **Pywalfox Support:** Sync your browser colors with your wallpaper themes.
- [ ] **Multi-monitor Support:** Individual configuration for different monitors.

## License
This project is licensed under the **GPL-3.0 License**. See the [LICENSE](LICENSE) file for details.
