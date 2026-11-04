# Upstream integration plan

## Repository scope

This repository is an Arabic localization work area, not a complete FilmCraft source checkout. It currently contains an original Arabic catalog draft and project documentation; it cannot produce a FilmCraft application binary by itself.

The upstream project is [storytold/filmcraft](https://github.com/storytold/filmcraft). The user has confirmed that FilmCraft was updated today to **0.17.0**. Use the official upstream release tag [v0.17.0](https://github.com/storytold/filmcraft/releases/tag/v0.17.0), pinned to commit `eb59ec09daaea519c9c8fffa404a594ae50d00e0`, as the initial source baseline. Re-check the installed app's About/version screen before building or installing anything; do not assume the release tag still matches a later update.

## Localization work

The current draft catalog is `crates/ui-egui/src/i18n/ar.tsv`. It is an original translation draft; untranslated strings may continue to fall back to English.

On upstream tag `v0.17.0` (commit `eb59ec09daaea519c9c8fffa404a594ae50d00e0`), review and update these areas:

- `crates/ui-egui/src/i18n.rs`: add `Language::Ar`; include it in `Language::ALL`; implement its `code()`, `bcp47()`, `name()`, `parse()`, `from_locales()`, and catalog selection. Use `ar` for the language code and BCP-47 tag, and `العربية` as the display name. Ensure locale variants such as `ar-LY`, `ar-EG`, and `ar-SA` resolve to Arabic.
- Catalog loading: add the Arabic `OnceLock<Catalog>` and `include_str!("i18n/ar.tsv")` mapping in the same pattern as existing languages.
- `crates/ui-egui/src/menus.rs`: add the Arabic language command to the language menu, its command dispatch mapping, and the checked/current-language state. Persist the normal `general.interfaceLanguage` value as `ar`.
- `crates/ui-egui/src/i18n/tests.rs`: include the Arabic catalog and test parsing, code/name round trips, locale resolution, placeholder parity, catalog validity, and language switching.
- Settings and preference UI/schema: trace where `general.interfaceLanguage` is declared, validated, displayed, and loaded. Update any language option list or schema that constrains the supported values; do not confuse unrelated application/content language lists with the interface-language setting.
- RTL and fonts: inspect `crates/ui-egui/src/rtl.rs`, its call sites, egui layout direction, text editing, docking, menus, icons, and font setup. Add a font with Arabic glyph coverage and verify shaping/ligatures and mixed Arabic/Latin/numeric text.

## RTL acceptance criteria

A text direction setting such as `TextDirection::Auto`, or Unicode bidirectional handling for captions, does **not** establish full application RTL support. Test the actual interface end to end:

- Main menus, context menus, dialogs, panels, dock layout, and toolbars.
- Alignment and ordering of labels, buttons, icons, timeline controls, and property panels.
- Arabic text entry/editing, selection, caret movement, punctuation, and mixed Arabic/English/numbers.
- File paths, timecodes, numeric fields, shortcuts, and error messages remain readable and logically ordered.
- Fonts render Arabic shaping and connected letters correctly without missing glyphs.

Document any UI areas that remain intentionally left-to-right rather than claiming complete RTL support prematurely.

## Licensing and attribution

The upstream repository identifies its source license as **MIT OR Apache-2.0**. Preserve all applicable upstream copyright and license notices when porting upstream code. Include the Apache-2.0 license text/notice where required for copied or modified Apache-licensed material. Keep original Arabic translations clearly identified as project-authored. Review the license of every upstream file before copying it; do not copy source files wholesale into this repository as a shortcut.

## Build and test sequence

Run these from a full checkout of the compatible upstream source, not from this localization-only repository. First inspect the release README, workspace members, and any project-specific build/xtask instructions; adjust package names and commands to that revision.

Suggested initial checks, if supported by that checkout:

```powershell
cargo fmt --check
cargo test -p filmcraft-ui-egui i18n
cargo check --workspace
```

Then build the application using the release's documented build procedure and manually test language selection, persistence after restart, catalog fallback, Arabic shaping, and RTL acceptance criteria above.

## Safety and release gate

Do not modify the installed FilmCraft application or any existing user projects during development. Do not install or replace any application binary until the compatible source revision builds successfully, the localization and RTL checks pass, and the user explicitly approves installation.
