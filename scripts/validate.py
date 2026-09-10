from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
root = Path(__file__).resolve().parent.parent
class Validate(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = set(); self.anchors = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, 'Duplicate ID'
            self.ids.add(a['id'])
        for key in ('href', 'src'):
            value = a.get(key, '').split('?')[0]
            if value.startswith('/'):
                assert (root / value.lstrip('/')).is_file(), value
            if value.startswith('#') and len(value) > 1:
                self.anchors.append(value[1:])
        if tag == 'img' and a.get('class') == 'member-avatar':
            assert a.get('alt', '').endswith('GitHub 프로필 사진')
parser = Validate()
parser.feed((root / 'index.html').read_text())
assert set(parser.anchors) <= parser.ids
assert (root / 'index.html').read_text().count('class="member-avatar"') == 4
assert '갈매기 개발단' not in (root / 'index.html').read_text()
ET.parse(root / 'sitemap.xml')
ET.parse(root / 'assets/gull.svg')
print('Static assets, anchors, icon dimensions and XML validated.')
