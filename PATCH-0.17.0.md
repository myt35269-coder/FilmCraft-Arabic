# FilmCraft 0.17.0 — Arabic integration work sheet

Pinned upstream baseline: `storytold/filmcraft` tag `v0.17.0`, commit `eb59ec09daaea519c9c8fffa404a594ae50d00e0`.

This file is an implementation worksheet for applying the Arabic localization to a full upstream checkout. It is **not** a claim that the upstream Rust files have already been patched or that a binary has been built.

## Verified upstream structure

The 0.17.0 source currently has 17 interface languages in `crates/ui-egui/src/i18n.rs`. Add Arabic as the 18th language.

The source already has `crates/ui-egui/src/rtl.rs` with Arabic script fallback-font discovery (including Windows Segoe UI/Tahoma/Arial candidates), bidi-aware document text, and font installation through the UI theme. This is useful existing infrastructure, but it does not by itself prove that every panel, menu, dock, toolbar, and editor control is laid out RTL.

The source's language menu is in `crates/ui-egui/src/menus.rs`. The settings choices for `general.interfaceLanguage` are separately defined in the engine settings tree and must be kept in the same order as the menu (there is an existing test enforcing this).

## Source files to change

### 1. `crates/ui-egui/src/i18n.rs`

- Add `Ar` to `Language` (serde's lowercase representation is `ar`).
- Add `ARABIC: OnceLock<Catalog>`.
- Increase `Language::ALL` from 17 to 18 and include `Ar`.
- Add `Ar => "ar"` to `bcp47()` and `code()`.
- Add `Ar => "العربية"` to `name()`.
- Accept `"ar"` in `parse()`.
- Add `("ar", Language::Ar)` to `from_locales()` and increase its `PRIMARY` array length from 17 to 18. The existing primary-subtag parsing should then cover `ar-LY`, `ar-EG`, `ar-SA`, `ar_XX.UTF-8`, etc.
- Add the catalog arm:
  `Language::Ar => Some(ARABIC.get_or_init(|| Catalog::parse(include_str!("i18n/ar.tsv"))))`.

### 2. `crates/ui-egui/src/menus.rs`

Add `app.language.arabic` with the self-name `العربية` to the language menu. Add the ID to the language-command whitelist, map it to `Language::Ar`, and add its checked-state arm. Keep the menu ordering consistent with the settings choice list; the existing test compares both lists.

### 3. Engine settings choices

Trace the actual `general.interfaceLanguage` field in the 0.17.0 engine settings source. Add the `ar` option with label `العربية` in the same relative position as the menu. Do not add Arabic to unrelated content-language or transcription-language lists. Confirm that preference validation accepts `ar` and that `system` remains the default.

### 4. `crates/ui-egui/src/i18n/tests.rs`

- Add `Language::Ar => Some(include_str!("ar.tsv"))` to the test catalog selector.
- Test `Language::parse("ar")`, `code()`, `bcp47()`, `name()`, serde round-trip, and `Language::ALL` membership.
- Test locale selection for `ar`, `ar-LY`, `ar-EG`, `ar-SA`, and POSIX-style `ar_LY.UTF-8`.
- Test menu switching, persistence of `general.interfaceLanguage = "ar"`, and exactly one checked menu item.
- Test that menu and settings language choices remain in identical order.
- Add a bundled-font coverage test for the Arabic alphabet and every Arabic letter/mark used in `ar.tsv`, following the existing `assert_bundled_fonts_cover` tests. If the build does not bundle an Arabic face, test the supported system fallback path on Windows rather than claiming a bundled font exists.

## RTL verification

The existing `rtl.rs` handles script font fallbacks and bidi layout for its document-text helper. Verify the real UI call paths and test at least:

- Menus, dialogs, settings rows, dock tabs, panels, and toolbars.
- Timeline track labels, property panels, text fields, numeric inputs, and file pickers.
- Arabic typing, selection, caret movement, punctuation, parentheses, and mixed Arabic/English/numbers.
- Timecodes, file paths, keyboard shortcuts, and numeric values remain logically ordered.
- Icons and directional affordances are mirrored only where semantically appropriate.

Do not globally reverse strings or reverse individual words. Keep stored strings and editor text in logical Unicode order; let the bidi/text system render visual order.

## Current catalog status

The project-authored `crates/ui-egui/src/i18n/ar.tsv` is an initial partial translation. Unknown or untranslated source strings fall back to English by design. Before release, run the upstream i18n report and expand the catalog based on actual missing strings. Preserve placeholders exactly and keep context keys aligned with the source catalog.

## Checks on a full upstream checkout

First read that checkout's README and xtask instructions. Then, if the commands are supported by this revision:

```powershell
cargo fmt --check
cargo test -p filmcraft-ui-egui i18n
cargo check --workspace
cargo xtask i18n-report
```

Also build using the documented v0.17.0 procedure and perform manual RTL/font checks on Windows.

## Licensing and release safety

The upstream project is licensed MIT OR Apache-2.0. Preserve upstream notices for every upstream file copied or modified and include required license texts/notices. The Arabic catalog is an original project translation.

Do not modify the installed FilmCraft application or user projects during development. Do not install or replace any binary until the compatible source builds, tests pass, and the user explicitly approves installation.
