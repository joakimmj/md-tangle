# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

## [2.0.0] - 2026-02-14

> [!WARNING]
> **BREAKING CHANGE**: dropping support for Python 2

### Added

- `feature`: add tags for filtering
  - This will allow code blocks to be omitted if not included by using the `-i`/`--include` flag.
- `feature`: add `-p`/`--block-padding` flag
  - This flag allows for adding padding between code blocks when tangled.

### Changed

- `refactor!`: `src-layout` and `pyproject.toml`
  - Update the project structure to `src-latout`
  - Switch from `setup.py` to `pyproject.toml`
  - Added `Makefile` to handle different operations
  - Added linting and typecheck

## [1.4.4] - 2025-02-12
### Changed
- Fix: allow for creating nested folders

## [1.4.3] - 2025-02-12
### Changed
- Fix: fix cases where only filename or one path

## [1.4.2] - 2025-02-12
### Changed
- Fix: use correct dictionary for getting common path

## [1.4.1] - 2025-02-12
### Changed
- Fix: use original block dictionary when looping

## [1.4.0] - 2025-02-12
### Changed
- Make sure `-d`/`--destination` flag only replaces common path

## [1.3.1] - 2020-08-24
### Added
- Set encoding to `UTF-8`

## [1.3.0] - 2019-05-03
### Added
- Support for overwriting output destination

## [1.2.0] - 2019-03-11
### Added
- Support for Python 2

### Changed
- Merged the two tools into one

## [1.1.0] - 2019-03-09
### Added
- Support for tangling to multiple files.

### Updated
- Documentation

## [1.0.1] - 2019-03-09
### Changed
- Updated link to DOCS in README to use full GitHub URL. This is for better support on [PyPI].
- Renamed project from `md_tangle` to `md-tangle`.

## [1.0.0] - 2019-03-07
### Added
- First version pushed to [PyPI].


[Unreleased]: https://github.com/joakimmj/md-tangle/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/joakimmj/md-tangle/compare/v1.4.4...v2.0.0
[1.4.4]: https://github.com/joakimmj/md-tangle/compare/v1.4.3...v1.4.4
[1.4.3]: https://github.com/joakimmj/md-tangle/compare/v1.4.2...v1.4.3
[1.4.2]: https://github.com/joakimmj/md-tangle/compare/v1.4.1...v1.4.2
[1.4.1]: https://github.com/joakimmj/md-tangle/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/joakimmj/md-tangle/compare/v1.3.1...v1.4.0
[1.3.1]: https://github.com/joakimmj/md-tangle/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/joakimmj/md-tangle/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/joakimmj/md-tangle/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/joakimmj/md-tangle/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/joakimmj/md-tangle/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/joakimmj/md-tangle/releases/tag/v1.0.0
[PyPI]: https://pypi.org/project/md-tangle
