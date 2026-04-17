# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/)

## [Unreleased]

## [0.1.1] - 2026-04-17
### Fixed
- Added explicit `pywal` dependency check in `Applier` (now raises clear error if `wal` is missing)
- Improved error handling when `config.yaml` is corrupted, missing or unreadable
- Fixed theme handling in `set-mode mood` and `next` (no more fallback bugs when theme is `null`)
- Refactored `Selector`:
  - Empty themes (directories without images) are now filtered out everywhere
  - `show-themes`, `global` mode and `rand_theme` show only usable themes
  - Added defensive check against empty/invalid `theme` in `rand_mood_wallpaper`
- Minor path and variable cleanups in `ConfigManager` and `Controller`

### Changed
- `list_themes()` now returns only themes that actually contain supported images

## [0.1.0] - 2026-04-10
### Added
- Initial MVP release with three modes: `global`, `mood` and `static`
- Support for awww/swww, hyprpaper and optional pywal + waybar integration
