import json


def read_json(path, default=None):
    if not path.exists():
        return default if default is not None else {}

    return json.loads(path.read_text(encoding="utf-8"))


def load_collection(folder):
    if not folder.exists():
        return []

    items = []

    for path in folder.glob("*.json"):
        data = read_json(path)
        data["_source"] = path.name
        items.append(data)

    return sorted(
        items,
        key=lambda item: (
            item.get("order", 9999),
            item.get("title", ""),
        ),
    )


def load_content(base):
    settings = base / "content" / "settings"

    general = read_json(settings / "general.json")
    homepage = read_json(settings / "homepage.json")
    about = read_json(settings / "about.json")
    process = read_json(settings / "process.json")
    contact = read_json(settings / "contact.json")
    legal = read_json(settings / "legal.json")

    services = load_collection(base / "content" / "services")
    projects = load_collection(base / "content" / "projects")

    services = [
        service
        for service in services
        if service.get("visible", True)
    ]

    return {
        "brand": general.get("brand", "Blickwert Studio"),
        "location": general.get("location", ""),
        "email": general.get("email", ""),
        "instagram": general.get("instagram", ""),

        "headline": homepage.get("headline", ""),
        "intro": homepage.get("intro", ""),
        "hero_image": homepage.get("hero_image", ""),
        "hero_image_alt": homepage.get("hero_image_alt", ""),

        "about_title": about.get("title", ""),
        "about_text": about.get("text", ""),
        "portrait": about.get("portrait", ""),

        "process": process.get("steps", []),

        "contact_title": contact.get("title", ""),
        "contact_text": contact.get("text", ""),

        "imprint": legal.get("imprint", ""),
        "privacy": legal.get("privacy", ""),

        "services": services,
        "projects": projects,
    }