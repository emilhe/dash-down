# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 03-04-25

### Added

- Add (custom) m2d CSS classes to all elements (inspired by markdown2dash)

### Removed

- Removed all dependency on Python box library (dependency reduction)
- Removed references to CSS files from GITHUB

### Changed

- Updated to Dash 3
- Change build system to uv
- Updated dependencies, except for `mistune` (migration to v3 postponed due to breaking API changes)
- Change code highlighting from using `Prism` to `CodeHighlight`, thereby fixing [#2](https://github.com/emilhe/dash-down/issues/2)

## [0.1.4] - 26-11-24

### Changed

- Various version updates (now supporting up to Python 3.13), code updated accordingly
- Added option to render markdown _strings_ (via the `md` argument) in additions to markdown files

## [0.1.1] - 17-07-22

### Changed

- Bump `Dash` to version `>=2.5.0`, and `dash-extensions` to version `0.1.5`

## [0.1.0] - 21-04-22

Initial stable release
