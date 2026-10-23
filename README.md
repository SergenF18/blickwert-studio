# Blickwert Studio

Neue Studio-Website im Anthrazit-Türkis-Look. Responsive statische Website mit
serverseitig beim Build erzeugtem HTML, Projektfiltern, Projekt-Dialogen,
Videoplayern, Kontakt per E-Mail-Programm und Decap CMS.

## Lokal ansehen

Python 3.9 oder neuer genügt. Keine npm-Installation nötig.

```sh
python3 scripts/build.py
python3 -m http.server 4321 --directory dist
```

Dann http://localhost:4321 öffnen. Nach Dateiänderungen Build erneut ausführen.
In VS Code den gesamten Ordner öffnen.

## Inhalte

`content/site.json` ist die Inhaltsquelle. Im CMS unter `/admin/` sind
Überschrift, Einleitung, Titelbild, Porträt, Über-mich-Text, Leistungen,
Ablauf, Kontakt und Projekte (auch Reihenfolge/Sichtbarkeit) bearbeitbar.
Layoutänderungen bleiben Codeänderungen.
Bilder werden unter `public/uploads` im Repository gespeichert.
Große Videodateien extern hosten und die direkte HTTPS-MP4/WebM-URL im
Projektfeld hinterlegen. YouTube-Seitenlinks sind keine direkten Videodateien.
Die Website lädt keine fremden Schriftarten oder Analyse-Skripte.
Der Adminbereich lädt Decap vom jsDelivr-CDN.

## GitHub und Netlify

1. Auf GitHub ein leeres privates Repository `blickwert-studio` anlegen.
2. In VS Code „Ordner öffnen“, diesen Projektordner wählen. Unter
   Quellcodeverwaltung Repository initialisieren und auf GitHub veröffentlichen
   (oder mit dem leeren Repository verbinden). Hauptbranch: `main`.
3. In Netlify das GitHub-Repository importieren. `netlify.toml` enthält bereits
   Build-Befehl und Veröffentlichungsordner.
4. Netlify-Umgebungsvariable `GITHUB_REPOSITORY` auf `BENUTZER/blickwert-studio`
   setzen. Der Build kann alternativ die von Netlify gesetzte
   `REPOSITORY_URL` auswerten. Für einen anderen Branch `CMS_BRANCH` setzen.
5. GitHub-OAuth einrichten: GitHub OAuth App mit der Website als Homepage
   und `https://api.netlify.com/auth/done` als Callback-URL anlegen.
   Client-ID und Client-Secret bei Netlify unter den OAuth-Providern für
   GitHub hinterlegen. Secrets niemals ins Repository schreiben.
   Aktuelle Schritte: https://docs.netlify.com/manage/security/secure-access-to-sites/oauth-provider-tokens/
   Decap: https://decapcms.org/docs/github-backend/
6. Neu deployen, `/admin/` öffnen, mit GitHub anmelden. Der GitHub-Nutzer
   benötigt Schreibzugriff auf dieses Repository. Speichern erzeugt einen
   Commit; Netlify veröffentlicht den neuen Build automatisch.
7. Login, Upload und Veröffentlichung mit einem Testprojekt prüfen.
   Diese externe Integration wurde in diesem Entwurf noch nicht eingerichtet.
8. Die richtige Strato-Domain in Netlify hinzufügen und ausschließlich die
   dort angezeigten DNS-Werte übernehmen. Vorhandene E-Mail-DNS-Einträge
   nicht überschreiben. HTTPS anschließend prüfen.

## Vor öffentlichem Start

Der Build läuft standardmäßig im Vorschau-Modus mit noindex und robots-Sperre.
Das verhindert keine Zugriffe: eine Netlify-Vorschau ist ohne weiteren
Zugriffsschutz öffentlich erreichbar. Noch keine privaten Inhalte hochladen.

Kontakt-E-Mail, vollständiges Impressum und zum Hosting/Verarbeitungsumfang
passende Datenschutzerklärung eintragen. Gestaltungsvorschauen durch eigene
Arbeiten ersetzen oder ausblenden. Nutzungsfreigaben für Kundenmedien prüfen.
Dann Netlify-Variable `SITE_LIVE=true` setzen. Der Build stoppt bei fehlenden
Kontakt-/Rechtsangaben oder sichtbaren Projektplatzhaltern.
Die Prüfung kontrolliert das Vorhandensein, keine rechtliche Vollständigkeit.

Das Formular versendet selbst keine Nachricht und speichert keine Eingaben.
Es öffnet eine vorbereitete E-Mail im Mailprogramm des Besuchers.
Ein serverseitiger Versand kann später ergänzt werden.

## Design und Medien

Die Marken-SVGs stammen aus dem erstellten Blickwert-Logo-Set.
Abstrakte Projektflächen sind lokale CSS-Grafiken und ausdrücklich als
Gestaltungsvorschau gekennzeichnet; sie behaupten keine Kundenreferenzen.
Die Originalmedien von Sergen sind noch einzusetzen.
