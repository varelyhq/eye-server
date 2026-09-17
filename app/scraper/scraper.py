import re
import json
import codecs
# import unicodedata
from lxml import html
import httpx2 as httpx
from urllib.parse import urlparse
from html_to_markdown import convert as convert_to_md

EXCLUDE = ['premium', 'kuznica']

# def slugify(text: str) -> str:
#     text = unicodedata.normalize("NFKD", text)
#     text = text.encode("ascii", "ignore").decode("ascii")
#     text = text.lower()
#     text = re.sub(r"[^a-z0-9]+", "-", text)
#     return text.strip("-")

def get_slug(href: str):
    parsed = urlparse(href)
    splitted = parsed.hostname.split('.')
    if len(splitted) > 2 and splitted[0] != 'www':
        return splitted[0]
    if parsed.path:
        return parsed.path.split('/')[-1] or parsed.path.split('/')[-2]

def scrape_sea_cams(url: str):
    res = httpx.get(url)
    tree = html.fromstring(res.content)
    cams = tree.cssselect('.listing .cam')
    output = []
    for cam in cams:
        href = cam.get('href')

        flag = False
        for word in EXCLUDE:
            if word in href:
                flag = True
                break
        if flag: continue

        data = {
            'name': cam.cssselect('h3')[0].text_content(),
            'title': cam.get('title'),
            'image': cam.cssselect('img')[0].get('src'),
            'slug': get_slug(href),
            'original_url': href,
            'is_online': 'cam--disabled' not in cam.get('class')
        }
        output.append(data)

    return output

def scrape_single_cam(url: str):
    res = httpx.get(url)
    tree = html.fromstring(res.content)
    description_el = tree.cssselect('.cam-description')[0]
    description_html = html.tostring(description_el[0], encoding='unicode')
    description = convert_to_md(description_html).content
    match = re.search(
        r'window\.STREAM_PLAYER_CONFIG\s*=\s*(\{.*?\})\s*;',
        res.text,
        re.DOTALL
    )
    stream_config = json.loads(match.group(1)) if match else None
    stream_config['video_src'] = codecs.decode(stream_config['video_src'], 'rot13')

    return {
        # 'config': stream_config,
        'stream_url': stream_config.get('video_src'),
        'description': description,
    }
