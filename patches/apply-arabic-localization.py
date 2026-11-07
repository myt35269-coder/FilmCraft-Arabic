#!/usr/bin/env python3
"""Apply Arabic interface localization to a FilmCraft v0.18.0 source checkout.

Run from the FilmCraft repository root:
    python patches/apply-arabic-localization.py

All edits are staged in memory and exact anchors are checked before any file is written.
This script never modifies an installed FilmCraft application.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "crates/ui-egui/src/i18n.rs",
    "crates/ui-egui/src/menus.rs",
    "crates/engine/src/settings/schema.rs",
    "crates/ui-egui/src/i18n/tests.rs",
    "crates/ui-egui/src/i18n/ar.tsv",
]
missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
if missing:
    raise SystemExit("v0.18.0 source checkout is incomplete: " + ", ".join(missing))

staged = {}

def edit(path, old, new):
    source = staged.get(path)
    if source is None:
        source = (ROOT / path).read_text(encoding="utf-8")
    count = source.count(old)
    if count != 1:
        raise SystemExit(
            f"Preflight failed for {path}: expected exactly one anchor, found {count}. "
            "No source files were changed."
        )
    staged[path] = source.replace(old, new, 1)

p = "crates/ui-egui/src/i18n.rs"
edit(p, "    Tr,\n}\n\nstatic JAPANESE", "    Tr,\n    /// Arabic (RTL), persisted as ar.\n    Ar,\n}\n\nstatic ARABIC: OnceLock<Catalog> = OnceLock::new();\nstatic JAPANESE")
edit(p, "pub const ALL: [Self; 17] = [", "pub const ALL: [Self; 18] = [")
edit(p, "        Self::Bs,\n    ];", "        Self::Bs,\n        Self::Ar,\n    ];")
edit(p, "            Self::Tr => \"tr\",\n        }\n    }\n\n    /// The language's catalog", "            Self::Tr => \"tr\",\n            Self::Ar => \"ar\",\n        }\n    }\n\n    /// The language's catalog")
edit(p, '            Self::Tr => "Türkçe",\n        }\n    }\n\n    pub fn parse', '            Self::Tr => "Türkçe",\n            Self::Ar => "العربية",\n        }\n    }\n\n    pub fn parse')
edit(p, '            "tr" => Some(Self::Tr),\n            _ => None,', '            "tr" => Some(Self::Tr),\n            "ar" => Some(Self::Ar),\n            _ => None,')
edit(p, '            ("tr", Language::Tr),\n        ];', '            ("tr", Language::Tr),\n            ("ar", Language::Ar),\n        ];')
edit(p, "const PRIMARY: [(&str, Language); 17] = [", "const PRIMARY: [(&str, Language); 18] = [")
edit(p, """            Self::Tr => "tr",
        }
    }

    pub fn name""", """            Self::Tr => "tr",
            Self::Ar => "ar",
        }
    }

    pub fn name""")
edit(p, '            Self::En => None,\n            Self::Ja => Some(JAPANESE', '            Self::En => None,\n            Self::Ar => Some(ARABIC.get_or_init(|| Catalog::parse(include_str!("i18n/ar.tsv")))),\n            Self::Ja => Some(JAPANESE')

p = "crates/ui-egui/src/menus.rs"
edit(p, """    uic!("app.language.english", "English", ["Edit", "Language"], None),
    // Alphabetical by the language's own name after English; Cyrillic, then CJK names follow
    // the Latin ones. Settings ▸ General ▸ Interface Language lists them the same way.""",
         """    uic!("app.language.english", "English", ["Edit", "Language"], None),
    uic!("app.language.arabic", "العربية", ["Edit", "Language"], None),
    // Arabic is listed after English; remaining names follow the existing Latin, Cyrillic and CJK order.
    // Settings ▸ General ▸ Interface Language lists them the same way.""")
edit(p, '            | "app.language.turkish"\n    ) {', '            | "app.language.turkish"\n            | "app.language.arabic"\n    ) {')
edit(p, '            "app.language.turkish" => crate::i18n::Language::Tr,\n            _ => crate::i18n::Language::En,', '            "app.language.turkish" => crate::i18n::Language::Tr,\n            "app.language.arabic" => crate::i18n::Language::Ar,\n            _ => crate::i18n::Language::En,')
edit(p, '            "app.language.turkish" => it.checked = Some(app.ui.language == crate::i18n::Language::Tr),\n            _ => {}', '            "app.language.turkish" => it.checked = Some(app.ui.language == crate::i18n::Language::Tr),\n            "app.language.arabic" => it.checked = Some(app.ui.language == crate::i18n::Language::Ar),\n            _ => {}')

p = "crates/engine/src/settings/schema.rs"
edit(p, """                    ("en", "English"),
                    // Alphabetical by the language's own name after English; Cyrillic, then""",
         """                    ("en", "English"),
                    ("ar", "العربية"),
                    // Arabic is listed after English; remaining names follow the existing Latin, Cyrillic and CJK order.""")

p = "crates/ui-egui/src/i18n/tests.rs"
edit(p, '        Language::En => None,\n        Language::Ja => Some(include_str!("ja.tsv")),',
         '        Language::En => None,\n        Language::Ar => Some(include_str!("ar.tsv")),\n        Language::Ja => Some(include_str!("ja.tsv")),')
edit(p, '    assert_eq!(Language::En.tr("File"), "File");\n    assert_eq!(Language::parse("xx"), None);',
         '    assert_eq!(Language::En.tr("File"), "File");\n    assert_eq!(Language::Ar.bcp47(), "ar");\n    assert_eq!(Language::from_locales(&["ar-LY".to_string()]), Language::Ar);\n    assert_eq!(Language::from_locales(&["ar_EG.UTF-8".to_string()]), Language::Ar);\n    assert_eq!(Language::parse("xx"), None);')
edit(p, '        (Language::PtBr, "Português (Brasil)"),',
         '        (Language::Ar, "العربية"),\n        (Language::PtBr, "Português (Brasil)"),')

for relative, content in staged.items():
    (ROOT / relative).write_text(content, encoding="utf-8", newline="\n")

print(f"Applied Arabic integration to {len(staged)} FilmCraft v0.18.0 source files.")
print("The upstream source includes Arabic/Hebrew bidi shaping and script fallback fonts in rtl.rs.")
print("Run cargo fmt, i18n tests, workspace check, and the Windows release build next.")
print("The installed FilmCraft application was not modified.")
