"""Generate a dependency-free GitHub Pages site from content.json."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
e = escape

def header(prefix=''):
    home = prefix or './'
    return f'''<a class="skip" href="#main">Skip to content</a><div class="wrap">
<header class="header"><a class="wordmark" href="{home}">Personal Homepage</a>
<nav aria-label="Main navigation"><a href="{home}#work">Work</a><a href="{home}#publications">Publications</a><a href="{home}#practice">Practice</a><a href="{home}#about">Education</a><a class="nav-cv" href="{prefix}assets/zhixiang-fan-cv.pdf">CV</a></nav></header>'''

def footer():
    return '''<footer class="footer"><span>Zhixiang Fan · Tsinghua University</span><a href="mailto:fzx24@mails.tsinghua.edu.cn">fzx24@mails.tsinghua.edu.cn ↗</a></footer></div>'''

def document(title, description, body, prefix='', path=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}">
<meta name="theme-color" content="#ffffff"><meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<link rel="canonical" href="https://char1ss.github.io/{path}"><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}styles.css"><script src="{prefix}gallery.js" defer></script></head>
<body>{header(prefix)}{body}{footer()}</body></html>'''

def visual(p, prefix=''):
    if p['cover']:
        return f'<img class="project-cover" src="{prefix}{e(p["cover"])}" alt="{e(p["mediaNote"])}" width="640" height="400" loading="lazy">'
    return f'''<div class="placeholder {e(p['id'])}"><div class="placeholder-top"><span>Project {p['number']}</span><span>Media forthcoming</span></div><div class="placeholder-no" aria-hidden="true">{p['number']}</div><div class="placeholder-bottom">{e(p['mediaLabel'])}<span>Images and video will be added here.</span></div></div>'''

def tags(p):
    return '<ul class="tags" aria-label="Topics">'+''.join(f'<li>{e(t)}</li>' for t in p['tags'])+'</ul>'

def project_card(p):
    href=f'projects/{p["id"]}/'
    intro_link=f' <a href="{e(p["introLink"]["url"])}">{e(p["introLink"]["label"])}</a>' if p.get('introLink') else ''
    return f'''<article class="project"><a class="project-visual" href="{href}" tabindex="-1" aria-hidden="true">{visual(p)}</a><div><p class="project-category">{e(p['category'])} · {p['year']}</p><h3><a href="{href}">{e(p['title'])}</a></h3><p class="project-summary">{e(p['summary'])}{intro_link}</p>{tags(p)}<a class="project-link" href="{href}">Explore project <span aria-hidden="true">→</span><span class="sr-only"></span></a></div></article>'''

def carousel(items, label, prefix='', compact=False):
    if not items:return ''
    slides=[]
    for i,m in enumerate(items):
        src=prefix+e(m['src']);caption=e(m['caption'])
        if m['type']=='video':
            poster=f' poster="{prefix}{e(m["poster"])}"' if m.get('poster') else ''
            media=f'<video controls playsinline preload="none"{poster} aria-label="{caption}"><source src="{src}" type="video/mp4">Your browser does not support this video. <a href="{src}">Download video</a>.</video>'
        else:
            media=f'<a class="image-expand" href="{src}" aria-haspopup="dialog" aria-label="Open full image: {caption}"><img src="{src}" alt="{e(m.get("alt",m["caption"]))}" loading="lazy" decoding="async"></a>'
        slides.append(f'<figure class="slide" role="group" aria-label="{i+1} of {len(items)}">{media}<figcaption>{caption}</figcaption></figure>')
    return f'''<section class="carousel {'compact' if compact else 'project-gallery'}" aria-label="{e(label)}"><div class="carousel-track" tabindex="0" aria-label="{e(label)}; use left and right arrow keys">{''.join(slides)}</div><div class="carousel-bar"><span class="gallery-hint">{'Paper figures' if compact else 'Images and video'} <span class="gallery-count" aria-live="polite">1 / {len(items)}</span></span><div class="carousel-buttons"><button type="button" class="prev" aria-label="Previous slide" disabled>←</button><button type="button" class="next" aria-label="Next slide">→</button></div></div></section>'''

def publication(p):
    title=e(p['title'])
    if p['url']:title=f'<a href="{e(p["url"])}">{title}</a>'
    authors=e(p['authors']).replace('Zhixiang Fan','<strong>Zhixiang Fan</strong>')
    link=f'<a class="pub-link" href="{e(p["url"])}" aria-label="DOI for {e(p["title"])}">DOI ↗</a>' if p['url'] else ''
    pdf=f'<a class="pub-link" href="{e(p["pdf"])}" aria-label="Read PDF: {e(p["title"])}">PDF ↗</a>' if p.get('pdf') else ''
    return f'''<li class="publication"><span class="pub-year">{p['year']}</span><div><h3 class="pub-title">{title}</h3><p class="pub-authors">{authors}</p><p class="pub-venue">{e(p['venue'])}<span class="pub-status">{e(p['status'])}</span>{pdf}{link}</p>{carousel(p.get('gallery',[]),p['title']+' figures',compact=True)}</div></li>'''

def experience(p):
    tasks=''.join(f'<li>{e(t)}</li>' for t in p['tasks'])
    return f'<article class="experience"><span>{e(p["dates"])}</span><div class="experience-body"><div class="experience-heading"><span class="practice-logo"><img src="{e(p["logo"])}" alt="" width="56" height="56" loading="lazy" decoding="async"></span><div><h3>{e(p["organization"])}</h3><p class="role">{e(p["role"])}</p></div></div><ul class="practice-tasks">{tasks}</ul></div></article>'

def interests():
    images=''.join(f'<a class="sketch" href="{e(m["src"])}" aria-haspopup="dialog" aria-label="View drawing: {e(m["alt"])}"><img src="{e(m["thumb"])}" alt="{e(m["alt"])}" width="{m["width"]}" height="{m["height"]}" loading="lazy" decoding="async"></a>' for m in data['interests'])
    return f'<section class="section interests" id="interests" aria-labelledby="interests-title"><div class="section-title"><h2 id="interests-title">Beyond research</h2><span>Hand drawing & personal interests</span></div><p class="interests-intro">A sketchbook of architecture, gardens and landscapes.</p><div class="sketch-wall">{images}</div></section>'

home=f'''<main id="main"><section class="hero profile-hero" aria-labelledby="name"><img class="profile-photo" src="assets/profile/zhixiang-fan-original.jpg" alt="Portrait of Zhixiang Fan" width="1733" height="2428" fetchpriority="high"><div class="profile-text"><h1 id="name">Zhixiang Fan</h1><p class="eyebrow">Spatial intelligence · Design · Interaction</p><p class="intro">{e(data['intro'])}</p><p class="research-intro">{e(data['research'])}</p><div class="contact-links"><a href="mailto:{e(data['email'])}">Email ↗</a><a href="{e(data['github'])}">GitHub ↗</a><a href="assets/zhixiang-fan-cv.pdf">Curriculum vitae ↗</a></div></div></section>
<section class="section" id="work" aria-labelledby="work-title"><div class="section-title"><h2 id="work-title">Selected work</h2><span>Research & creative systems</span></div>{''.join(project_card(p) for p in data['projects'])}</section>
<section class="section" id="publications" aria-labelledby="pub-title"><div class="section-title"><h2 id="pub-title">Publications</h2><span>Journal articles, challenge & interactive art</span></div><ol class="pub-list">{''.join(publication(p) for p in data['publications'])}</ol></section>
<section class="section" id="practice" aria-labelledby="practice-title"><div class="section-title"><h2 id="practice-title">Practice</h2></div>{''.join(experience(p) for p in data['practice'])}</section>
<section class="section" id="about" aria-labelledby="about-title"><div class="section-title"><h2 id="about-title">Education</h2></div><div class="about-grid"><div class="education-entry"><img class="school-emblem" src="assets/education/tsinghua.png" alt="Tsinghua University emblem" width="72" height="72" loading="lazy"><p class="education-item"><strong>Tsinghua University</strong><span>Beijing, China</span><span>PhD student in Design · Academy of Arts & Design<br>2024–present</span></p></div><div class="education-entry"><img class="school-emblem" src="assets/education/nanjing-forestry.jpeg" alt="Nanjing Forestry University emblem" width="72" height="72" loading="lazy"><p class="education-item"><strong>Nanjing Forestry University</strong><span>Nanjing, China</span><span>Master’s in Landscape Architecture<br>2021–2024</span></p></div></div></section>{interests()}</main>'''
(ROOT/'index.html').write_text(document('Zhixiang Fan · Spatial Intelligence & Design',data['intro'],home),encoding='utf-8')

for i,p in enumerate(data['projects']):
    prefix='../../'
    links=''.join(f'<a href="{e(x["url"])}">{e(x["label"])} ↗</a>' for x in p['links'])
    gallery=carousel(p['gallery'],p['title']+' gallery',prefix)
    nxt=data['projects'][(i+1)%len(data['projects'])]
    content=f'''<main id="main"><a class="back" href="../../#work">← All projects</a><section class="project-hero"><p class="eyebrow">{e(p['category'])} · {p['year']}</p><h1>{e(p['title'])}</h1><p class="project-subtitle">{e(p['subtitle'])}</p>{tags(p)}</section><div class="detail-visual">{visual(p,prefix)}</div><div class="detail-body"><aside class="project-meta"><div><h2>My contribution</h2><p>{e(p['role'])}</p></div><div><h2>Project focus</h2><p>{e(p['mediaNote'])}</p>{links}</div></aside><div class="project-copy"><section><h2>Research question</h2><p>{e(p['question'])}</p></section><section><h2>Approach</h2><p>{e(p['approach'])}</p></section><section><h2>Current work</h2><p>{e(p['outcome'])}</p></section><p class="scope">{e(p['scope'])}</p></div></div><div class="gallery">{gallery}</div><div class="project-pager"><a href="../../#work"><small>Selected work</small>← Back to overview</a><a href="../{nxt['id']}/"><small>Next project</small>{e(nxt['title'])} →</a></div></main>'''
    path=f'projects/{p["id"]}/'
    dest=ROOT/path;dest.mkdir(parents=True,exist_ok=True)
    (dest/'index.html').write_text(document(p['title']+' · Zhixiang Fan',p['summary'],content,prefix,path),encoding='utf-8')
print('Built index.html and 4 project pages.')
