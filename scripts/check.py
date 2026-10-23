from pathlib import Path
import json,subprocess,os,re,tempfile,shutil
from html.parser import HTMLParser
B=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.assets=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t=='a':self.links.append(a.get('href',''))
  if t in ('img','script','link'):
   u=a.get('src',a.get('href',''))
   if u.startswith('/'):self.assets.append(u)
page=(B/'dist/index.html').read_text();p=Page();p.feed(page)
assert len(p.ids)==len(set(p.ids)),'Doppelte IDs'
for a in p.links:
 if a.startswith('#') and len(a)>1:assert a[1:] in p.ids,a
for asset in p.assets:assert (B/'dist'/asset.lstrip('/')).is_file(),asset
assert 'noindex,nofollow' in page
j=json.loads(re.search(r'<script type="application/json" id="site-data">(.*?)</script>',page,re.S)[1]);assert len(j['projects'])==3
c=json.loads((B/'dist/admin/config.json').read_text());assert c['backend']['name']=='github'
source=json.loads((B/'content/site.json').read_text())
fields=c['collections'][0]['files'][0]['fields'];assert {f['name'] for f in fields}==set(source),'CMS deckt Inhalt nicht vollständig ab'
# Isolated build verifies that release guards reject placeholders and escaping is safe.
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp)/'site';shutil.copytree(B,t,ignore=shutil.ignore_patterns('dist','.git'))
 d=json.loads((t/'content/site.json').read_text());d['headline']='Test <script>alert(1)</script>\nZweite Zeile';d['projects'][0]['description']='</script><script>alert(1)</script>';d['projects'][1]['visible']=False
 (t/'content/site.json').write_text(json.dumps(d))
 r=subprocess.run(['python3',str(t/'scripts/build.py')],capture_output=True,text=True,env={**os.environ,'GITHUB_REPOSITORY':'test/studio'})
 assert r.returncode==0,r.stderr
 h=(t/'dist/index.html').read_text();assert '<script>alert(1)</script>' not in h
 j=json.loads(re.search(r'<script type="application/json" id="site-data">(.*?)</script>',h,re.S)[1]);assert len(j['projects'])==2;assert j['projects'][0]['description']==d['projects'][0]['description']
 r=subprocess.run(['python3',str(t/'scripts/build.py')],capture_output=True,text=True,env={**os.environ,'SITE_LIVE':'true'});assert r.returncode!=0,'Unvollständiger Livegang muss stoppen'
print('OK: Links, Assets, CMS-Felder, HTML-Escaping, Projektsichtbarkeit und Livegang-Sperre.')
