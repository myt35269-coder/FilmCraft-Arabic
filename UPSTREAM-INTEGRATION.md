# Upstream integration

## Repository scope

This repository is an Arabic localization work area, not a complete FilmCraft source checkout. Its GitHub Actions workflow checks out the pinned upstream source, applies the integration script and Arabic catalog, then builds an isolated preview.

The upstream project is [storytold/filmcraft](https://github.com/storytold/filmcraft). The active target is official release [v0.20.1](https://github.com/storytold/filmcraft/releases/tag/v0.20.1), pinned to commit `cedf0c9bd060eb06a977d532402be2097c9ebe42` in `.github/workflows/arabic-build.yml`.

## Localization work

The catalog is `crates/ui-egui/src/i18n/ar.tsv`. It remains an incremental translation draft; untranslated strings may continue to fall back to English.

The integration script checks exact anchors before writing and updates these v0.20.1 files:

- `crates/ui-egui/src/i18n.rs`: Arabic language registration, locale resolution and catalog loading.
- `crates/ui-egui/src/menus.rs`: language menu command and selection.
- `crates/engine/src/settings/schema.rs`: interface-language setting choice.
- `crates/ui-egui/src/i18n/tests.rs`: Arabic catalog and language-selection tests.

The script's exact-anchor preflight was applied successfully to a clean v0.20.1 checkout. Run the checks below before treating the integration as build-verified.

## Translation and RTL status

A successful build or Unicode bidi shaping does not establish full application RTL support. Test menus, dialogs, panels, docking, text editing, punctuation, mixed Arabic/English, numbers and timecodes on Windows. The catalog is not yet fully translated; use the workflow's untranslated-string report and do not claim completeness while entries remain.

Document any UI areas that remain intentionally left-to-right rather than claiming complete RTL support.

## Licensing and attribution

The upstream repository identifies its source license as **MIT OR Apache-2.0**. Preserve all applicable upstream copyright and license notices when porting upstream code. Include the Apache-2.0 license text/notice where required for copied or modified Apache-licensed material. Keep original Arabic translations clearly identified as project-authored. Review the license of every upstream file before copying it; do not copy source files wholesale into this repository as a shortcut.

## Build and test sequence

The workflow runs the upstream i18n report, Rust formatting check, UI library tests, workspace compile check and Windows release build against the pinned source. All checks must pass before treating the preview as build-verified.

The `auto-translate.yml` workflow checks the latest stable upstream release daily. If its commit differs from the currently pinned release, it checks out that source, applies the current Arabic catalog and patch, runs the same checks, and uploads an isolated preview plus untranslated-string report. After a successful build, it opens a pull request to update the pinned commit and release notes; it never merges that update automatically. If upstream changes make the integration anchors incompatible, the workflow fails without proposing an unverified update. Enable **Settings → Actions → General → Allow GitHub Actions to create and approve pull requests** for the update PR to be created.

## Safety and release gate

Do not modify the installed FilmCraft application or any existing user projects during development. Do not install or replace any application binary until the compatible source revision builds successfully, the localization and RTL checks pass, and the user explicitly approves installation.
