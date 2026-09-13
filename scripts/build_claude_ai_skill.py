"""Package skills/inlane-data-guide/ into a claude.ai-compatible custom Skill zip.

claude.ai custom Skills don't understand the ${CLAUDE_PLUGIN_ROOT} variable that
the Claude Code plugin uses, and each zip upload is a full snapshot (no delta,
no auto-sync) -- see semantics_memory.md. Re-run this after any change to
SKILL.md, conventions.md, schema_map.md, open_questions.md, future_work.md,
tables/, or metrics/, then re-upload the resulting zip to claude.ai.

Usage: python scripts/build_claude_ai_skill.py
"""

import shutil
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "inlane-data-guide"
STAGING_DIR = REPO_ROOT / "build" / SKILL_NAME
OUTPUT_ZIP = REPO_ROOT / f"{SKILL_NAME}.zip"

# Same exclusion policy as PROJECT_KNOWLEDGE_UPLOAD_LIST.md: no credentials,
# no raw introspection output, no unfixed-bug SQL, no spreadsheet.
FILES_TO_COPY = [
    "conventions.md",
    "schema_map.md",
    "open_questions.md",
    "future_work.md",
]
DIRS_TO_COPY = [
    "tables",
    "metrics",
]


def build():
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True)

    skill_md_src = REPO_ROOT / "skills" / SKILL_NAME / "SKILL.md"
    skill_md_text = skill_md_src.read_text(encoding="utf-8")
    skill_md_text = skill_md_text.replace("${CLAUDE_PLUGIN_ROOT}/", "")
    skill_md_text = skill_md_text.replace(
        "This plugin bundles verified documentation",
        "This Skill bundles verified documentation",
    )
    (STAGING_DIR / "SKILL.md").write_text(skill_md_text, encoding="utf-8")

    for name in FILES_TO_COPY:
        shutil.copy2(REPO_ROOT / name, STAGING_DIR / name)
    for name in DIRS_TO_COPY:
        shutil.copytree(REPO_ROOT / name, STAGING_DIR / name)

    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in STAGING_DIR.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(STAGING_DIR.parent))

    shutil.rmtree(STAGING_DIR.parent)
    print(f"Built {OUTPUT_ZIP.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    build()
