def field(name, label, widget="string", **extra):
    return {
        "name": name,
        "label": label,
        "widget": widget,
        **extra,
    }


def build_config(repo, branch="main"):

    website = {
        "name": "website",
        "label": "Website",
        "files": [

            {
                "name": "general",
                "label": "Allgemein",
                "file": "content/settings/general.json",
                "format": "json",
                "fields": [
                    field("brand", "Markenname"),
                    field("location", "Standort"),
                    field(
                        "email",
                        "Kontakt-E-Mail",
                        required=False,
                    ),
                    field(
                        "instagram",
                        "Instagram-URL",
                        required=False,
                    ),
                ],
            },

            {
                "name": "homepage",
                "label": "Startseite",
                "file": "content/settings/homepage.json",
                "format": "json",
                "fields": [
                    field(
                        "headline",
                        "Hauptüberschrift",
                        "text",
                        hint="Zeilenumbrüche sind möglich.",
                    ),
                    field(
                        "intro",
                        "Einleitung",
                        "text",
                    ),
                    field(
                        "hero_image",
                        "Titelbild",
                        "image",
                        required=False,
                    ),
                    field(
                        "hero_image_alt",
                        "Bildbeschreibung",
                        required=False,
                    ),
                ],
            },

            {
                "name": "about",
                "label": "Über Blickwert",
                "file": "content/settings/about.json",
                "format": "json",
                "fields": [
                    field("title", "Überschrift"),
                    field("text", "Text", "text"),
                    field(
                        "portrait",
                        "Porträt",
                        "image",
                        required=False,
                    ),
                ],
            },

            {
                "name": "process",
                "label": "Ablauf",
                "file": "content/settings/process.json",
                "format": "json",
                "fields": [
                    field(
                        "steps",
                        "Ablauf",
                        "list",
                        summary="{{fields.title}}",
                        fields=[
                            field("title", "Titel"),
                            field(
                                "text",
                                "Beschreibung",
                                "text",
                            ),
                        ],
                    ),
                ],
            },

            {
                "name": "contact",
                "label": "Kontakt",
                "file": "content/settings/contact.json",
                "format": "json",
                "fields": [
                    field("title", "Überschrift"),
                    field(
                        "text",
                        "Kontakttext",
                        "text",
                    ),
                ],
            },

            {
                "name": "legal",
                "label": "Rechtliches",
                "file": "content/settings/legal.json",
                "format": "json",
                "fields": [
                    field(
                        "imprint",
                        "Impressum",
                        "text",
                        required=False,
                    ),
                    field(
                        "privacy",
                        "Datenschutz",
                        "text",
                        required=False,
                    ),
                ],
            },
        ],
    }

    services = {
        "name": "services",
        "label": "Leistungen",
        "label_singular": "Leistung",
        "folder": "content/services",
        "create": True,
        "delete": True,
        "extension": "json",
        "format": "json",
        "slug": "{{slug}}",
        "identifier_field": "title",
        "summary": "{{order}} · {{title}}",
        "fields": [
            field("title", "Titel"),

            field(
                "text",
                "Beschreibung",
                "text",
            ),

            field(
                "tags",
                "Stichworte",
                hint="z. B. Business · Gastronomie · Produkte",
            ),

            field(
                "order",
                "Reihenfolge",
                "number",
                default=10,
                value_type="int",
                min=1,
            ),

            field(
                "visible",
                "Auf Website anzeigen",
                "boolean",
                default=True,
            ),
        ],
    }

    projects = {
        "name": "projects",
        "label": "Projekte",
        "label_singular": "Projekt",
        "folder": "content/projects",
        "create": True,
        "delete": True,
        "extension": "json",
        "format": "json",
        "slug": "{{slug}}",
        "identifier_field": "title",
        "summary": "{{order}} · {{title}} — {{category}}",

        "fields": [

            field(
                "title",
                "Projektname",
            ),

            field(
                "category",
                "Kategorie",
                "select",
                options=[
                    "Foto",
                    "Film",
                    "Social",
                ],
            ),

            field(
                "description",
                "Projektbeschreibung",
                "text",
            ),

            field(
                "image",
                "Vorschaubild",
                "image",
                required=False,
            ),

            field(
                "image_alt",
                "Bildbeschreibung Vorschaubild",
                required=False,
            ),

            field(
                "gallery",
                "Projektgalerie",
                "list",
                required=False,
                summary="{{fields.alt}}",
                fields=[
                    field(
                        "image",
                        "Bild",
                        "image",
                    ),
                    field(
                        "alt",
                        "Bildbeschreibung",
                        required=False,
                    ),
                ],
            ),

            field(
                "video",
                "Video",
                required=False,
                hint="Direkte HTTPS MP4/WebM-URL.",
            ),

            field(
                "featured",
                "Hervorgehobenes Projekt",
                "boolean",
                default=False,
            ),

            field(
                "visible",
                "Auf Website anzeigen",
                "boolean",
                default=True,
            ),

            field(
                "order",
                "Reihenfolge",
                "number",
                default=10,
                value_type="int",
                min=1,
            ),

            field(
                "placeholder",
                "Gestaltungsvorschau",
                "boolean",
                default=False,
            ),

            field(
                "theme",
                "Fallback-Design",
                "select",
                options=[
                    {
                        "label": "Space",
                        "value": "space",
                    },
                    {
                        "label": "Detail",
                        "value": "detail",
                    },
                    {
                        "label": "Motion",
                        "value": "motion",
                    },
                ],
                default="space",
            ),
        ],
    }

    return {
        "backend": {
            "name": "github",
            "repo": repo,
            "branch": branch,
        },

        "media_folder": "public/uploads",
        "public_folder": "/uploads",

        "locale": "de",

        "logo_url": "/assets/logo.svg",

        "collections": [
            website,
            services,
            projects,
        ],
    }