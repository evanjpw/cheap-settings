# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2025-10-18

### Added

- Support for datetime, date, time types (ISO format)
- Support for Decimal type (preserves precision for financial calculations)
- Support for UUID type (multiple formats accepted)

## [1.2.2] - 2025-10-17

### Added
- Both --flag and --no-flag for all boolean settings (fixes env var override issues)

## [1.2.1] - 2025-10-16

### Fixed
- Boolean command line flags can now override environment variables in both directions
- Optional types properly handle "none" from command line

## [1.2.0] - 2025-10-15

### Added

- Settings can now be added without initializers

## [1.1.0] - 2025-10-12

### Added

- Added the `from_env()` method to create static copies of the settings

## [1.0.0] - 2025-10-12

### Added

- Improved error handling

### Changed

- General cleanup for 1.0

## Previous Releases
For changes before v1.0.0, see the [commit history](https://github.com/evanjpw/cheap-settings/commits/main).
