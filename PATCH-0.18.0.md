# FilmCraft 0.18.0 — Arabic localization integration

Pinned upstream source: `storytold/filmcraft` tag `v0.18.0`, commit `015d5b3ea37e1202a529e6245d3cc021c8c16ffd`.

## Scope

This project adds Arabic (`ar`) as an interface language to an isolated build of FilmCraft 0.18.0. It does not modify an installed application or user project.

## Source integration

`patches/apply-arabic-localization.py` checks each exact anchor before changing any source file. It updates:

- `crates/ui-egui/src/i18n.rs`: Arabic language registration, locale resolution and catalog loading.
- `crates/ui-egui/src/menus.rs`: language menu command and selection.
- `crates/engine/src/settings/schema.rs`: interface-language setting choice.
- `crates/ui-egui/src/i18n/tests.rs`: Arabic catalog and language-selection tests.

The script was applied successfully to a clean v0.18.0 checkout. The release adds the H.264 High10 profile to the dynamic UI strings; its label is included in the Arabic catalog.

## Arabic and RTL

The integration relies on the upstream Arabic/Hebrew font fallback and Unicode bidirectional shaping; it does not reverse Arabic strings manually. This does not imply that every UI panel is mirrored RTL. Menus, dialogs, panels, timeline labels, text editing, punctuation, mixed Arabic/English, numbers and timecodes still require manual Windows testing.

## Catalog status

`crates/ui-egui/src/i18n/ar.tsv` is an incremental translation draft. Missing source strings fall back to English. The workflow generates an untranslated-string report; do not describe the interface as fully translated until that report has been reviewed and the catalog expanded.

## Build checks

The workflow runs the upstream i18n report, Rust formatting check, UI library tests, workspace compile check, and Windows release build. A successful build is not a substitute for manual RTL/font verification.

## Install safety

The artifact is a portable, isolated preview. Do not copy it over an installed FilmCraft version. Installation or replacement requires separate explicit approval after the preview has been tested.
