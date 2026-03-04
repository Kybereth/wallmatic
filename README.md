# Wallmatic
**Wallmatic** is a lightweight CLI wallpaper manager for Wayland (tested on Hyprland) that supports mood-based themes and global randomization.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)  ![Hyprland](https://img.shields.io/badge/Hyprland-58C4DC?logo=hyprland&logoColor=white) ![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
## Features
- **Three Modes:**
	- `global`: Random wallpaper from your entire collection.
	- `mood`: Random wallpaper from specific theme(sub-folder). 
	- `static`: Lock a specific image.
- **Multi-Daemon Support:** Works with awww(swww) and hyprpaper.
- **Pywal Integration:** Automatically updates your color scheme by invoking Pywal on the current wallpaper
- **Waybar Support:** Auto-reloads Waybar to apply new CSS palette
- **CLI First:** Fully manageable via a clean Typer-based interface.

## Prerequisites
To use Wallmatic, you need at least one **wallpaper daemon** installed:
- [awww](https://codeberg.org/LGFae/awww) (formerly `swww`) — An efficient wallpaper daemon for Wayland.
- [hyprpaper](https://github.com/hyprwm/hyprpaper) — A simple and fast wallpaper utility for Hyprland

**Optional dependencies:**
- [pywal](https://github.com/dylanaraps/pywal) — A tool that generates a color palette from the dominant colors in an image.

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

## Configuration
Wallmatic stores its configuration in `~/.config/wallmatic/config.yaml`. You can manage it via the CLI:
```bash
# Enable or disable Pywal integration
wallmatic config set pywal true

# Change wallpaper daemon (default is "auto")
wallmatic config set wallpaper_daemon swww

# Reset configuration to default if something goes wrong
wallmatic config reset
```

## Wallpaper Directory Structure 
For **global** and **mood** to work correctly, organize your wallpapers into subdirectories(themes):
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
- [ ] **Automated Switching:** Systemd daemon (enable/disable, interval control).
- [ ] **Pywalfox Support:** Sync your browser colors with your wallpaper themes.
- [ ] **Multi-monitor Support:** Individual configuration for different monitors.

## License
This project is licensed under the **GPL-3.0 License**. See the [LICENSE](LICENSE) file for details.