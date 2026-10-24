from pathlib import Path
import json
import re
import shutil

BASE = Path(__file__).resolve().parent.parent
OLD = BASE / "content" / "site.json"


def slugify(value):
    value = (
        value.lower()
        .replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if not OLD.exists():
    raise FileNotFoundError("content/site.json wurde nicht gefunden.")

site = json.loads(OLD.read_text(encoding="utf-8"))

# Backup
backup = BASE / "content" / "site.legacy.json"
if not backup.exists():
    shutil.copy2(OLD, backup)

# Website-Einstellungen
write_json(
    BASE / "content/settings/general.json",
    {
        "brand": site.get("brand", "Blickwert Studio"),
        "location": site.get("location", ""),
        "email": site.get("email", ""),
        "instagram": site.get("instagram", ""),
    },
)

write_json(
    BASE / "content/settings/homepage.json",
    {
        "headline": site.get("headline", ""),
        "intro": site.get("intro", ""),
        "hero_image": site.get("hero_image", ""),
        "hero_image_alt": site.get("hero_image_alt", ""),
    },
)

write_json(
    BASE / "content/settings/about.json",
    {
        "title": site.get("about_title", ""),
        "text": site.get("about_text", ""),
        "portrait": site.get("portrait", ""),
    },
)

write_json(
    BASE / "content/settings/process.json",
    {
        "steps": site.get("process", []),
    },
)

write_json(
    BASE / "content/settings/contact.json",
    {
        "title": site.get("contact_title", ""),
        "text": site.get("contact_text", ""),
    },
)

write_json(
    BASE / "content/settings/legal.json",
    {
        "imprint": site.get("imprint", ""),
        "privacy": site.get("privacy", ""),
    },
)

# Leistungen
services_dir = BASE / "content/services"
services_dir.mkdir(parents=True, exist_ok=True)

for index, service in enumerate(site.get("services", []), start=1):
    service = {
        **service,
        "order": index,
        "visible": True,
    }
    filename = slugify(service.get("title", f"leistung-{index}")) + ".json"
    write_json(services_dir / filename, service)

# Projekte
projects_dir = BASE / "content/projects"
projects_dir.mkdir(parents=True, exist_ok=True)

for index, project in enumerate(site.get("projects", []), start=1):
    project = {
        **project,
        "order": index,
        "featured": index == 1,
        "gallery": [],
    }

    filename = slugify(project.get("title", f"projekt-{index}")) + ".json"
    write_json(projects_dir / filename, project)

print("Migration abgeschlossen.")
print("Backup:", backup)