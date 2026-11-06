# FilmCraft 0.17.1 — Arabic localization integration

Pinned upstream source: `storytold/filmcraft` tag `v0.17.1`, commit `2fe0d0460da86621fd8b193dcc0a61f790106200`.

## Scope

This project adds Arabic (`ar`) as an interface language. It does not modify an installed FilmCraft application or any user project. The GitHub Actions workflow builds an isolated Windows x64 preview artifact.

## Source integration

The patch script updates five v0.17.1 source files after checking every exact anchor before writing:

- `crates/ui-egui/src/i18n.rs`: language enum, stable code, BCP 47 tag, self-name, locale selection and catalog registration.
- `crates/ui-egui/src/menus.rs`: Edit → Language command, dispatch allowlist and language selection.
- `crates/engine/src/settings/schema.rs`: General → Interface Language choice.
- `crates/ui-egui/src/i18n/tests.rs`: catalog loading, locale selection, round-trip and language-name tests.
- `apps/filmcraft/src/native_menu.rs`: native menu language state on supported native platforms.

The menu and settings choice lists are kept in the same order and checked by the upstream UI test.

## Arabic and RTL

The v0.17.1 upstream source already contains `crates/ui-egui/src/rtl.rs`, which adds Arabic/Hebrew fallback-font discovery and uses the egui fork's Unicode bidi shaping for document text. The integration relies on that implementation; it does not reverse Arabic strings manually. This does not imply that every UI panel is mirrored RTL. The preview still requires manual Windows testing of menus, dialogs, panels, timeline labels, text editing, punctuation, mixed Arabic/English, numbers and timecodes.

## Catalog status

`crates/ui-egui/src/i18n/ar.tsv` is an incremental translation draft. Missing source strings fall back to English. The workflow generates an untranslated-string report; do not describe the interface as fully translated until that report has been reviewed and the catalog expanded.

## Build checks

The workflow runs the upstream i18n report, Rust formatting check, UI library tests, workspace compile check, and Windows release build. A successful build is not a substitute for manual RTL/font verification.

## Install safety

The artifact is portable and isolated. Do not copy it over the user's installed FilmCraft 0.17.1. Installation or replacement requires separate explicit approval after the preview has been tested.
