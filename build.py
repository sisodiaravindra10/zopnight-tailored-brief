"""Build the two deliverables from one template.

  artifact  -> zopnight-brief.html      images inlined as data URIs, rep strip on
  hosted    -> <repo>/index.html        images as cached files, rep strip off (?rep=1 shows it)
"""
import base64
import os
import re
import struct
import sys

SRC = 'zopnight-deck.template.html'
REPO = '/Users/zop.dev/ZopNight Marketing problem/zopnight-tailored-brief'
IMG = os.path.join(REPO, 'img')


def jpeg_size(path):
    """Read intrinsic pixel dimensions straight from the JPEG markers."""
    with open(path, 'rb') as f:
        f.read(2)
        while True:
            b = f.read(1)
            while b and b != b'\xff':
                b = f.read(1)
            marker = f.read(1)
            while marker == b'\xff':
                marker = f.read(1)
            if marker[0] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                             0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                f.read(3)
                h, w = struct.unpack('>HH', f.read(4))
                return w, h
            seg = struct.unpack('>H', f.read(2))[0]
            f.read(seg - 2)


def file_for(token):
    name = token[2:-2]                       # strip {{ }}
    if name.startswith('SHOT_'):
        return 'shot-%s.jpg' % name[5:]
    return '%s.jpg' % name[2:]               # S_foo -> foo.jpg


def build(mode):
    t = open(SRC, encoding='utf-8').read()
    inline = mode == 'artifact'

    def src_for(token):
        fn = file_for(token)
        p = os.path.join(IMG, fn)
        if inline:
            return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
        return 'img/' + fn

    # feature screenshots: resolve the path and pin the aspect ratio beside it
    def feature(m):
        token = m.group(1)
        w, h = jpeg_size(os.path.join(IMG, file_for(token)))
        return "shot:'%s',ar:'%d/%d'" % (src_for(token), w, h)

    t = re.sub(r"shot:'(\{\{[A-Za-z0-9_-]+\}\})'", feature, t)

    # the one static <img> on the pitch slide
    w, h = jpeg_size(os.path.join(IMG, 'shot-011.jpg'))
    t = t.replace('{{DIM_011}}', 'width="%d" height="%d"' % (w, h))

    t = t.replace('{{REP_DEFAULT}}', 'true' if inline else 'false')
    t = re.sub(r'\{\{([A-Za-z0-9_-]+)\}\}', lambda m: src_for(m.group(0)), t)

    left = re.findall(r'\{\{[^}]*\}\}', t)
    assert not left, 'unresolved placeholders: %s' % left[:5]
    return t


if __name__ == '__main__':
    a = build('artifact')
    open('zopnight-brief.html', 'w', encoding='utf-8').write(a)
    print('artifact  %6d KB  zopnight-brief.html' % (len(a.encode()) // 1024))

    h = build('hosted')
    open(os.path.join(REPO, 'index.html'), 'w', encoding='utf-8').write(h)
    print('hosted    %6d KB  %s/index.html' % (len(h.encode()) // 1024, REPO))
