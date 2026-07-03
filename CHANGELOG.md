# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/)

## [Unreleased]

## [0.3.1] - 2026-07-03
### Fixed
- Prevented the random selector from picking the same wallpaper consecutively when alternative images are available in the theme.

## [0.3.0] - 2026-07-03
### Added
- Logging subsystem (errors and stack traces are written to `wallmatic.log`).
- New `wallmatic config edit` command to modify settings directly via the system's default `$EDITOR`.
- Dynamic image format filtering applied to `Selector` based on the currently active wallpaper daemon.
- Introduced `daemon_options` nested dictionary structure in `config.yaml` for advanced backend configurations (e.g., `awww` transitions). 

## [0.2.0] - 2026-06-04
### Added
- Integrated `wallust` as a new alternative color palette generator.
- Implemented Factory and Strategy design patterns for both wallpaper daemons (`WallpaperEngine`)
and color backends (`ColorEngine`).
- Added defensive execution checks inside individual engine classes to prevent raw OS crashes.

### Changed
- Refactored `config.yaml`: replaced the old `pywal` (bool) toggle with a flexible
`color_engine` (str) selector (accepts `none`, `pywal`, `wallust`).
- Updated `wallmatic status` CLI output to display the active color engine instead of a boolean status.
- Restricted `ConfigEnum` and validators to support the new modular configuration keys.

## [0.1.1] - 2026-04-17
### Fixed
- Added explicit `pywal` dependency check in `Applier` (now raises clear error if `wal` is missing).
- Improved error handling when `config.yaml` is corrupted, missing or unreadable.
- Fixed theme handling in `set-mode mood` and `next` (no more fallback bugs when theme is `null`).
- Refactored `Selector`:
  - Empty themes (directories without images) are now filtered out everywhere.
  - `show-themes`, `global` mode and `rand_theme` show only usable themes.
  - Added defensive check against empty/invalid `theme` in `rand_mood_wallpaper`.
- Minor path and variable cleanups in `ConfigManager` and `Controller`.

### Changed
- `list_themes()` now returns only themes that actually contain supported images.

## [0.1.0] - 2026-04-10
### Added
- Initial MVP release with three modes: `global`, `mood` and `static`.
- Support for awww/swww, hyprpaper and optional pywal + waybar integration.
