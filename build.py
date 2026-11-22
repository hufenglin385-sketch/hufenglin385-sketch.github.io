import json
import re
from datetime import date, datetime, timezone
from html import escape
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "content.json").read_text(encoding="utf-8-sig"))
site, posts = data["site"], data["posts"]
esc = lambda value: escape(str(value), quote=True)
seen = set()
for post in posts:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", post["slug"]) or post["slug"] in seen:
        raise ValueError("Each article needs a unique lowercase URL slug.")
    seen.add(post["slug"])
    date.fromisoformat(post["date"])
    section_ids = set()
    for section in post["sections"]:
        if not re.fullmatch(r"[a-z0-9-]+", section["id"]) or section["id"] in section_ids:
            raise ValueError("Section IDs must be unique URL-safe values.")
        section_ids.add(section["id"])
posts.sort(key=lambda post: post["date"], reverse=True)
generated = []

def write(path, text):
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    generated.append(path)

def pretty_date(value):
    year, month, day = map(int, value.split("-"))
    return f"{year} 年 {month} 月 {day} 日"

def read_minutes(post):
    text = "".join(paragraph for section in post["sections"] for paragraph in section["paragraphs"])
    return max(1, round(len(text) / 300))

def header():
    return f'''<a class="skip" href="#main">跳到正文</a>
<header class="site-header"><nav class="nav-inner" aria-label="主导航">
<a class="wordmark" href="/" aria-label="HF Notes 首页">HF Notes<span class="wordmark-dot" aria-hidden="true">.</span></a>
<div class="nav-links"><a href="/#notes">文章</a><a href="/#about">关于</a>
<a href="{esc(site['github'])}" target="_blank" rel="noopener noreferrer">GitHub<span class="sr-only">（新窗口）</span></a>
<button class="search-trigger" type="button" data-open-search aria-label="搜索文章" hidden><svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 4.5 4.5"/></svg></button></div>
</nav></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="footer-inner">
<div class="footer-top"><a class="wordmark" href="/">HF Notes.</a><span>保持好奇，持续记录。</span></div>
<div class="footer-bottom"><span>© {esc(site['since'])} HF Notes</span><div>
<a href="/feed.xml">RSS 订阅</a><a href="{esc(site['github'])}" target="_blank" rel="noopener noreferrer">GitHub</a>
<a href="https://images.unsplash.com/photo-1496181133206-80ce9b88a853" target="_blank" rel="noopener noreferrer">封面 · Unsplash</a>
</div></div></div></footer>'''

def layout(title, description, path, body, kind="website"):
    canonical = site["url"].rstrip("/") + path
    return f'''<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#f5f5f7"><meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="canonical" href="{esc(canonical)}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="HF Notes" href="/feed.xml">
<meta property="og:type" content="{kind}"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(site['url'])}/assets/workspace.webp"><meta property="og:locale" content="zh_CN">
<link rel="stylesheet" href="/assets/style.css"><script src="/assets/app.js" defer></script>
</head><body>{header()}{body}{footer()}</body></html>'''

def row(post):
    search = " ".join([post["title"], post["category"], post["excerpt"]] + [paragraph for section in post["sections"] for paragraph in section["paragraphs"]])
    return f'''<li class="note-item reveal" data-category="{esc(post['category'])}" data-search="{esc(search.casefold())}">
<a class="note-link" href="/notes/{esc(post['slug'])}/">
<div class="note-meta"><span>{esc(post['category'])}</span><time datetime="{post['date']}">{pretty_date(post['date'])}</time></div>
<div class="note-copy"><h3>{esc(post['title'])}</h3><p>{esc(post['excerpt'])}</p></div>
<span class="note-read">{read_minutes(post)} 分钟阅读<span class="read-mark" aria-hidden="true">＋</span></span>
</a></li>'''

categories = list(dict.fromkeys(post["category"] for post in posts))
filters = '<button type="button" class="filter is-active" data-filter="all" aria-pressed="true">全部</button>'
filters += "".join(f'<button type="button" class="filter" data-filter="{esc(category)}" aria-pressed="false">{esc(category)}</button>' for category in categories)
rows = "".join(row(post) for post in posts)
home = f'''<main id="main">
<section class="hero" aria-labelledby="hero-title">
<div class="hero-copy"><p class="eyebrow hero-enter">我的一小片互联网</p>
<h1 id="hero-title" class="hero-enter">HF Notes<span>.</span></h1>
<p class="hero-description hero-enter">保持好奇。让想法继续。</p>
<p class="hero-subtitle hero-enter">记录学习、尝试，和每一次新的开始。</p>
<div class="hero-actions hero-enter"><a class="button button-primary" href="#notes">开始阅读</a><a class="button button-outline" href="#about">关于我</a></div></div>
<div class="device-frame hero-enter" aria-label="一台笔记本电脑的产品摄影，屏幕上是 Hello 欢迎语">
<img class="device-photo" src="/assets/workspace.webp" width="1500" height="1000" fetchpriority="high" alt="">
<div class="device-screen" aria-hidden="true"><span class="screen-hello">Hello.</span><span class="screen-caption">A SPACE FOR WHAT'S NEXT.</span></div>
</div>
<div class="hero-footnote"><span>学习 · 记录 · 创造</span><span>始于 2026</span></div>
</section>
<section class="notes section" id="notes" aria-labelledby="notes-title"><div class="content-width">
<div class="section-heading reveal"><p class="eyebrow">一点记录，一点新发现。</p><h2 id="notes-title">最近写下的。</h2><p>从一个小小的开始，把探索的过程留住。</p></div>
<div class="notes-toolbar js-tools" hidden><div class="filters" role="group" aria-label="按分类筛选">{filters}</div>
<label class="search-field"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 4.5 4.5"/></svg><span class="sr-only">搜索文章</span><input id="note-search" type="search" placeholder="搜索文章" autocomplete="off"></label></div>
<p class="result-count" role="status" aria-live="polite" aria-atomic="true">{len(posts)} 篇文章</p>
<ul class="note-list">{rows}</ul>
<div class="empty-state" hidden><h3>还没有找到这篇笔记。</h3><p>换个关键词，或试试全部分类。</p><button class="button button-outline" type="button" data-reset-search>查看全部</button></div>
<noscript><p class="noscript">所有文章已列出。启用 JavaScript 后可使用搜索与分类。</p></noscript>
</div></section>
<section class="about section" id="about" aria-labelledby="about-title"><div class="content-width">
<div class="section-heading reveal"><p class="eyebrow">很高兴，在这里遇见你。</p><h2 id="about-title">关于我。<br><span class="muted">也关于正在发生的事。</span></h2>
<p class="about-intro">我正在搭建自己的博客，<br class="desktop-break">把学习中的问题、动手尝试的过程，慢慢写下来。</p></div>
<div class="about-details reveal"><div><h3>现在</h3><p>从一个自己的博客开始。</p><p class="muted">尝试把想法变成页面，也让零散的记录有一个长期停留的地方。</p></div>
<div><h3>在这里</h3><p>分享经历，也记录思考。</p><p class="muted">公开值得分享的过程，保留未公开项目的具体实现和业务细节。</p></div></div>
<div class="milestone reveal"><span>2026.11</span><p>第一次搭建个人博客，开始在自己的空间里记录。</p><span class="milestone-label">新的开始</span></div>
<a class="text-link reveal" href="{esc(site['github'])}" target="_blank" rel="noopener noreferrer">在 GitHub 找到我</a>
</div></section></main>'''
write("index.html", layout("HF Notes · 学习、记录与创造", site["description"], "/", home))

for index, post in enumerate(posts):
    sections = "".join(f'''<section id="{esc(section['id'])}" class="article-section"><h2>{esc(section['title'])}</h2>{''.join('<p>'+esc(paragraph)+'</p>' for paragraph in section['paragraphs'])}</section>''' for section in post["sections"])
    toc = "".join(f'<a href="#{esc(section["id"])}">{esc(section["title"])}</a>' for section in post["sections"])
    other = posts[(index + 1) % len(posts)] if len(posts) > 1 else None
    next_link = f'<a class="next-note" href="/notes/{esc(other["slug"])}/"><span>继续阅读</span><h2>{esc(other["title"])}</h2><p>{esc(other["excerpt"])}</p></a>' if other else ''
    article = f'''<div class="reading-progress" aria-hidden="true"><span></span></div>
<main id="main" class="article-main"><header class="article-header"><a class="text-link" href="/#notes">所有文章</a>
<p class="eyebrow">{esc(post['category'])}</p><h1>{esc(post['title'])}</h1>
<div class="article-meta"><time datetime="{post['date']}">{pretty_date(post['date'])}</time><span>{read_minutes(post)} 分钟阅读</span></div>
<p class="article-lead">{esc(post['lead'])}</p></header>
<details class="article-toc"><summary>本文目录</summary><nav aria-label="文章目录">{toc}</nav></details>
<article class="article-body">{sections}</article>
<div class="article-share"><span>感谢你读到这里。</span><button type="button" class="button button-outline" data-copy-link hidden>复制文章链接</button><span class="copy-status" role="status" aria-live="polite"></span></div>
{next_link}</main>'''
    write(f"notes/{post['slug']}/index.html", layout(post["title"]+" · HF Notes", post["excerpt"], f"/notes/{post['slug']}/", article, "article"))

not_found = '''<main id="main" class="not-found"><p class="eyebrow">404</p><h1>这一页，<br>还没有写下。</h1><p>地址可能有误，也可能这篇笔记已经搬家。</p><a class="button button-primary" href="/">回到首页</a></main>'''
write("404.html", layout("页面未找到 · HF Notes", "回到 HF Notes 继续阅读。", "/404.html", not_found))
base = site["url"].rstrip("/")
rss_items = []
for post in posts:
    link = base + f"/notes/{post['slug']}/"
    published = datetime.fromisoformat(post["date"]).replace(tzinfo=timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    rss_items.append(f'<item><title>{xml_escape(post["title"])}</title><link>{link}</link><guid>{link}</guid><description>{xml_escape(post["excerpt"])}</description><category>{xml_escape(post["category"])}</category><pubDate>{published}</pubDate></item>')
write("feed.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>HF Notes</title><link>'+base+'</link><description>'+xml_escape(site["description"])+'</description><language>zh-CN</language>'+''.join(rss_items)+'</channel></rss>\n')
urls = [base+"/"] + [base+f'/notes/{post["slug"]}/' for post in posts]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+url+'</loc></url>' for url in urls)+'</urlset>\n')
write("robots.txt", "User-agent: *\nAllow: /\nSitemap: "+base+"/sitemap.xml\n")
manifest = ROOT / "generated-files.json"
if manifest.exists():
    previous = json.loads(manifest.read_text(encoding="utf-8"))
    for old in previous:
        if old not in generated and re.fullmatch(r"notes/[a-z0-9-]+/index\.html", old):
            old_file = ROOT / old
            if old_file.exists():
                old_file.unlink()
                if not any(old_file.parent.iterdir()):
                    old_file.parent.rmdir()
manifest.write_text(json.dumps(generated, indent=2)+"\n",encoding="utf-8")
print(f"Built {len(posts)} articles and {len(generated)} public files.")
