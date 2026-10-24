from content_loader import load_content
from pathlib import Path
from cms_config import build_config
import json,html,shutil,os,re
BASE=Path(__file__).resolve().parent.parent
OUT=BASE/'dist'
if OUT.exists():shutil.rmtree(OUT)
shutil.copytree(BASE/'public',OUT)
s = load_content(BASE)
def e(v):return html.escape(str(v),quote=True)
def safe_url(v):
 return v if v.startswith(('https://','http://','/assets/','/uploads/')) else ''
def img(src,alt,cls=''):
 src=safe_url(src)
 return f'<img src="{e(src)}" alt="{e(alt)}" class="{cls}" loading="lazy" decoding="async">' if src else ''
projects=[p for p in s['projects'] if p.get('visible',True)]
project_html=''
for n,p in enumerate(projects):
 theme=p.get('theme','space') if p.get('theme') in ['space','detail','motion'] else 'space'
 media=img(p.get('image',''),p.get('image_alt',''))
 if not media:media='<div class="visual-type"><small>BLICKWERT / VISUAL DIRECTION</small>'+['SPACE<br>& STORY.','THE<br>DETAIL.','IN<br>MOTION.'][n%3]+'</div>'
 project_html+=f'''<article class="project" data-category="{e(p['category'])}"><button class="project-button" data-project="{n}" aria-label="Projekt ansehen: {e(p['title'])}"><div class="project-visual {theme}">{media}{'<span class="placeholder-note">GESTALTUNGSVORSCHAU</span>' if p.get('placeholder') else ''}</div><div class="project-meta"><div><h3>{e(p['title'])}</h3><p>{e(p['category'])} / BLICKWERT STUDIO</p></div><span class="arrow-circle" aria-hidden="true">↗</span></div></button></article>'''
services=''.join(f'<article class="service"><span class="service-number">0{i+1}</span><h3>{e(p["title"])}</h3><div><p>{e(p["text"])}</p><span class="tags">{e(p["tags"])}</span></div></article>' for i,p in enumerate(s['services']))
steps=''.join(f'<article class="step"><span>0{i+1} /</span><h3>{e(p["title"])}</h3><p>{e(p["text"])}</p></article>' for i,p in enumerate(s['process']))
hero_image=img(s.get('hero_image',''),s.get('hero_image_alt',''))
hero_art=hero_image or '<img src="/assets/mark.svg" class="hero-mark" alt=""><span class="art-label">A DIFFERENT POINT OF VIEW.</span>'
headline=s['headline'].split('\n');title=e(headline[0])+'<br><span>'+e(' '.join(headline[1:]))+'</span>' if len(headline)>1 else e(s['headline'])
portrait=img(s.get('portrait',''),'Sergen Franz, Fotograf und Videograf') or '<strong>Sergen.</strong><span>DER BLICK HINTER BLICKWERT.</span>'
instagram=safe_url(s.get('instagram',''))
navsocial=f'<a href="{e(instagram)}" target="_blank" rel="noopener noreferrer">Instagram ↗</a>' if instagram else ''
preview=os.getenv('SITE_LIVE')!='true'
if not preview:
 assert s.get('email') and '@' in s['email'],'Kontakt-E-Mail fehlt'
 assert s.get('imprint','').strip() and s.get('privacy','').strip(),'Impressum/Datenschutz fehlen'
 assert all(not p.get('placeholder') and p.get('image') for p in projects),'Gestaltungsvorschauen müssen vor Livegang ersetzt oder ausgeblendet werden'
html_page=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(s['brand'])} — Foto, Film & Social Content</title><meta name="description" content="{e(s['intro'])}"><meta name="robots" content="{'noindex,nofollow' if preview else 'index,follow'}"><meta name="theme-color" content="#121717"><meta property="og:title" content="{e(s['brand'])}"><meta property="og:description" content="{e(s['intro'])}"><meta property="og:type" content="website"><link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="stylesheet" href="/styles.css"><script src="/app.js" defer></script></head><body><a class="skip" href="#main">Zum Inhalt</a><header class="header"><div class="wrap nav"><a href="#" aria-label="Blickwert Studio Startseite"><img class="logo" src="/assets/logo.svg" alt="Blickwert Studio"></a><button class="menu" aria-expanded="false" aria-controls="navigation">Menü +</button><nav class="nav-links" id="navigation" aria-label="Hauptnavigation"><a href="#arbeiten">Arbeiten</a><a href="#leistungen">Leistungen</a><a href="#studio">Studio</a><a href="#kontakt" class="nav-contact">Projekt anfragen <span aria-hidden="true">↗</span></a></nav></div></header><main id="main"><section class="hero wrap"><div class="hero-top"><div class="eyebrow">Independent content studio</div><span>{e(s['location'])} / FOTO · FILM · SOCIAL</span></div><div class="hero-layout"><div><h1>{title}</h1><p class="hero-copy">{e(s['intro'])}</p><div class="hero-actions"><a class="button" href="#arbeiten">Arbeiten entdecken <span aria-hidden="true">↗</span></a><a class="text-link" href="#kontakt">Lass uns sprechen</a></div></div><div class="hero-art {'photo' if hero_image else ''}">{hero_art}</div></div><div class="hero-bottom"><span>KLARER BLICK. EIGENER CHARAKTER.</span><span>WEITER ENTDECKEN ↓</span></div></section><div class="ticker" aria-label="Fotografie, Film, Social Content"><span>Fotografie</span><i aria-hidden="true">✳</i><span>Film & Video</span><i aria-hidden="true">✳</i><span>Social Content</span><i aria-hidden="true">✳</i><span>Ein klarer Blick.</span></div><section id="arbeiten" class="section wrap"><div class="section-head"><div><div class="eyebrow">01 / Ausgewählte Arbeiten</div><h2>Ein Blick.<br>Viele Geschichten.</h2></div><p>Atmosphäre einfangen. Details sichtbar machen. Menschen zeigen. Hier bekommen Geschichten ihren eigenen Look.</p></div><div class="filters" role="group" aria-label="Projekte filtern"><button class="filter" aria-pressed="true" data-filter="Alle">Alle</button><button class="filter" aria-pressed="false" data-filter="Foto">Foto</button><button class="filter" aria-pressed="false" data-filter="Film">Film</button><button class="filter" aria-pressed="false" data-filter="Social">Social</button></div><div class="projects">{project_html}</div><p class="no-results" hidden>In dieser Kategorie sind noch keine Projekte veröffentlicht.</p>{'<p class="preview-note">ENTWURF — Die markierten Flächen sind visuelle Platzhalter. Eigene Arbeiten folgen.</p>' if any(p.get('placeholder') for p in projects) else ''}</section><section id="leistungen" class="section services"><div class="wrap"><div class="section-head"><div><div class="eyebrow">02 / Was ich für euch mache</div><h2>Starker Content.<br>Passend zu euch.</h2></div><p>Ein einzelnes Projekt oder eine regelmäßige Zusammenarbeit. Wir finden das Format, das zu eurem Unternehmen passt.</p></div>{services}</div></section><section id="studio" class="section wrap about"><div class="about-art">{portrait}</div><div><div class="eyebrow">03 / Das Studio</div><h2>{e(s['about_title'])}</h2><p>{e(s['about_text'])}</p><div class="signature">Sergen Franz<small>Foto & Video · {e(s['location'])}</small></div></div></section><section class="section wrap process"><div class="eyebrow">04 / Von der Idee zum Auftritt</div><h2>Unkompliziert.<br>Von Anfang an.</h2><div class="steps">{steps}</div></section><section id="kontakt" class="section contact"><div class="wrap contact-layout"><div><div class="eyebrow">05 / Dein nächstes Projekt</div><h2>{e(s['contact_title'])}</h2><p>{e(s['contact_text'])}</p></div><form class="contact-form"><div class="form-row"><label>Name<input name="name" autocomplete="name" required placeholder="Wie heißt du?" maxlength="120"></label><label>Unternehmen<input name="company" autocomplete="organization" placeholder="Dein Unternehmen" maxlength="160"></label></div><label>E-Mail<input name="email" type="email" autocomplete="email" required placeholder="du@unternehmen.de" maxlength="254"></label><label>Worum geht’s?<select name="service"><option>Foto & Video</option><option>Fotografie</option><option>Film & Video</option><option>Social Content</option><option>Erst mal kennenlernen</option></select></label><label>Deine Idee<textarea name="message" required placeholder="Was hast du vor?" maxlength="5000"></textarea></label><button class="button" type="submit">Anfrage als E-Mail öffnen <span aria-hidden="true">↗</span></button><p class="form-note">Öffnet dein E-Mail-Programm. Diese Website speichert die Eingaben nicht.</p><p class="form-status" role="status" aria-live="polite">{'Entwurfsmodus: Die Kontaktadresse wird vor dem Start ergänzt.' if not s['email'] else ''}</p></form></div></section></main><footer class="footer wrap"><div class="footer-top"><a href="#" aria-label="Zurück zum Anfang"><img class="logo" src="/assets/logo.svg" alt="Blickwert Studio"></a><div class="footer-links">{navsocial}<button class="text-link legal" data-legal="imprint" type="button" style="background:none;color:inherit;border:0">Impressum</button><button class="text-link legal" data-legal="privacy" type="button" style="background:none;color:inherit;border:0">Datenschutz</button><a href="/admin/">Studio-Login ↗</a></div></div><div class="footer-bottom"><span>© 2026 BLICKWERT STUDIO · SERGEN FRANZ</span><span>FOTO. FILM. EIN GUTER BLICK.</span></div></footer><dialog id="detail-dialog" aria-labelledby="dialog-title"><button class="close" aria-label="Dialog schließen">Schließen ×</button><div id="dialog-content"></div></dialog><noscript><p class="wrap">Für Projektfilter, Projektdetails und das Anfrageformular bitte JavaScript aktivieren.</p></noscript><script type="application/json" id="site-data">{json.dumps({'projects':projects,'email':s['email'],'imprint':s['imprint'],'privacy':s['privacy']},ensure_ascii=False).replace('<',chr(92)+'u003c')}</script></body></html>'''
(OUT/'index.html').write_text(html_page)
# Decap configuration is plain JSON (also valid YAML). Repo inferred only from explicit env.
repo=os.getenv('GITHUB_REPOSITORY','')
url=os.getenv('REPOSITORY_URL','')
if not repo and 'github.com' in url:repo=re.sub(r'^.*github.com[:/]','',url).removesuffix('.git')
if repo and not re.fullmatch(r'[\w.-]+/[\w.-]+',repo):raise ValueError('Ungültiges GITHUB_REPOSITORY')
def field(name,label,widget='string',**extra):return dict(name=name,label=label,widget=widget,**extra)

config = build_config(
    repo or "SergenF18/blickwert-studio",
    os.getenv("CMS_BRANCH", "main"),
)

(OUT / "admin/config.json").write_text(
    json.dumps(
        config,
        ensure_ascii=False,
        indent=2,
    )
)