#!/usr/bin/env python3
"""Apply Arabic interface-language integration to a FilmCraft v0.17.0 source checkout.
Run from the FilmCraft repository root: python patches/apply-arabic-localization.py
The script verifies exact upstream anchors and refuses mismatched source files.
It never builds, installs, or modifies an installed FilmCraft application.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FILES = ["crates/ui-egui/src/i18n.rs", "crates/ui-egui/src/menus.rs",
         "crates/engine/src/settings/schema.rs", "crates/ui-egui/src/i18n/tests.rs"]
if any(not (ROOT / p).is_file() for p in FILES):
    raise SystemExit("Run from the FilmCraft v0.17.0 source checkout; required files are missing.")

def sub(rel, old, new):
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"Refusing to patch {rel}: expected one exact anchor, found {n}.")
    p.write_text(s.replace(old, new, 1), encoding="utf-8", newline="\n")

p = "crates/ui-egui/src/i18n.rs"
sub(p, "    Tr,\n}\n\nstatic JAPANESE", "    Tr,\n    /// Arabic interface, persisted as ar.\n    Ar,\n}\n\nstatic ARABIC: OnceLock<Catalog> = OnceLock::new();\nstatic JAPANESE")
sub(p, "pub const ALL: [Self; 17] = [", "pub const ALL: [Self; 18] = [")
sub(p, "        Self::Bs,\n    ];\n\n    /// BCP 47", "        Self::Bs,\n        Self::Ar,\n    ];\n\n    /// BCP 47")
sub(p, '            Self::Tr => "tr",\n        }\n    }\n\n    pub fn name', '            Self::Tr => "tr",\n            Self::Ar => "ar",\n        }\n    }\n\n    pub fn name')
sub(p, '            Self::Tr => "Türkçe",\n        }\n    }\n\n    pub fn parse', '            Self::Tr => "Türkçe",\n            Self::Ar => "العربية",\n        }\n    }\n\n    pub fn parse')
sub(p, '            "tr" => Some(Self::Tr),\n            _ => None,', '            "tr" => Some(Self::Tr),\n            "ar" => Some(Self::Ar),\n            _ => None,')
sub(p, "const PRIMARY: [(&str, Language); 17] = [", "const PRIMARY: [(&str, Language); 18] = [")
sub(p, '            ("tr", Language::Tr),\n        ];', '            ("tr", Language::Tr),\n            ("ar", Language::Ar),\n        ];')
sub(p, '            Self::Tr => "tr",\n        }\n    }\n\n    /// The language\\'s catalog', '            Self::Tr => "tr",\n            Self::Ar => "ar",\n        }\n    }\n\n    /// The language\\'s catalog')
sub(p, '            Self::En => None,\n            Self::Ja => Some(JAPANESE', '            Self::En => None,\n            Self::Ar => Some(ARABIC.get_or_init(|| Catalog::parse(include_str!("i18n/ar.tsv")))),\n            Self::Ja => Some(JAPANESE')

p = "crates/ui-egui/src/menus.rs"
sub(p, '    uic!("app.language.english", "English", ["Edit", "Language"], None),\n    // Alphabetical', '    uic!("app.language.english", "English", ["Edit", "Language"], None),\n    uic!("app.language.arabic", "العربية", ["Edit", "Language"], None),\n    // Alphabetical')
sub(p, '            | "app.language.turkish"\n    ) {', '            | "app.language.turkish"\n            | "app.language.arabic"\n    ) {')
sub(p, '            "app.language.turkish" => crate::i18n::Language::Tr,\n            _ => crate::i18n::Language::En,', '            "app.language.turkish" => crate::i18n::Language::Tr,\n            "app.language.arabic" => crate::i18n::Language::Ar,\n            _ => crate::i18n::Language::En,')
sub(p, '            "app.language.turkish" => it.checked = Some(app.ui.language == crate::i18n::Language::Tr),\n            _ => {}', '            "app.language.turkish" => it.checked = Some(app.ui.language == crate::i18n::Language::Tr),\n            "app.language.arabic" => it.checked = Some(app.ui.language == crate::i18n::Language::Ar),\n            _ => {}')

p = "crates/engine/src/settings/schema.rs"
sub(p, '                    ("en", "English"),\n                    // Alphabetical', '                    ("en", "English"),\n                    ("ar", "العربية"),\n                    // Alphabetical')

p = "crates/ui-egui/src/i18n/tests.rs"
sub(p, '        Language::En => None,\n        Language::Ja => Some(include_str!("ja.tsv")),', '        Language::En => None,\n        Language::Ar => Some(include_str!("ar.tsv")),\n        Language::Ja => Some(include_str!("ja.tsv")),')
sub(p, '        (Language::PtBr, "Português (Brasil)"),', '        (Language::Ar, "العربية"),\n        (Language::PtBr, "Português (Brasil)"),')
sub(p, '    assert_eq!(Language::En.tr("File"), "File");', '    assert_eq!(Language::En.tr("File"), "File");\n    assert_eq!(Language::Ar.bcp47(), "ar");\n    assert_eq!(Language::from_locales(&["ar-LY".to_string()]), Language::Ar);')

print("Arabic integration patch applied. Run cargo fmt and focused i18n tests next.")
print("No build or installation was performed.")
