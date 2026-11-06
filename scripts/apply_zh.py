# -*- coding: utf-8 -*-
"""把 zh_dict.py 的中文映射应用到 FModel 源码。
只改显示文本：XAML 属性 / XAML 元素文本 / [Description] / 少量弹窗字符串。
不触碰绑定表达式、命令参数、配置键、技术标识符。
"""
import os, re, glob, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zh_dict import ATTR_MAP, DESC_MAP, ELEMENT_MAP, CS_MAP

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'FModel'))
ATTRS = r'(?:Header|Text|Content|ToolTip|Title|Watermark|Placeholder|InputGestureText|HeaderStringFormat|StringFormat|ContentStringFormat)'
attr_re = re.compile(r'\b(' + ATTRS + r')="([^"]*)"')
desc_re = re.compile(r'(\[Description\(")([^\"]*)("\)\])')
elem_re = re.compile(r'(>\s*)([A-Za-z][A-Za-z0-9 ,.&;:()/\'\-]{2,90})(\s*<)')

hits = collections.Counter()
files_changed = 0

# ---- XAML ----
for p in sorted(glob.glob(ROOT + '/**/*.xaml', recursive=True)):
    with open(p, encoding='utf-8-sig') as f:
        s = f.read()
    orig = s

    def sub_attr(m):
        k = m.group(2)
        if k in ATTR_MAP:
            hits['attr'] += 1
            return m.group(1) + '="' + ATTR_MAP[k] + '"'
        return m.group(0)

    s = attr_re.sub(sub_attr, s)

    def sub_elem(m):
        k = m.group(2).strip()
        if k in ELEMENT_MAP:
            hits['element'] += 1
            return m.group(1) + ELEMENT_MAP[k] + m.group(3)
        return m.group(0)

    s = elem_re.sub(sub_elem, s)

    if s != orig:
        with open(p, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(s)
        files_changed += 1

# ---- C# ----
for p in sorted(glob.glob(ROOT + '/**/*.cs', recursive=True)):
    with open(p, encoding='utf-8-sig') as f:
        s = f.read()
    orig = s

    def sub_desc(m):
        if m.group(2) in DESC_MAP:
            hits['description'] += 1
            return m.group(1) + DESC_MAP[m.group(2)] + m.group(3)
        return m.group(0)

    s = desc_re.sub(sub_desc, s)

    for en, zh in CS_MAP.items():
        needle = '"' + en + '"'
        if needle in s:
            n = s.count(needle)
            s = s.replace(needle, '"' + zh + '"')
            hits['cs_message'] += n

    if s != orig:
        with open(p, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(s)
        files_changed += 1

print('files changed:', files_changed)
print('replacements:', dict(hits), 'total', sum(hits.values()))
print('dict sizes: attr', len(ATTR_MAP), 'desc', len(DESC_MAP), 'element', len(ELEMENT_MAP), 'cs', len(CS_MAP))

# 校验：XAML 里不应残留未翻译的英文 UI 属性值（排除绑定/技术值）
leftover = collections.Counter()
for p in sorted(glob.glob(ROOT + '/**/*.xaml', recursive=True)):
    s = open(p, encoding='utf-8-sig').read()
    for m in attr_re.finditer(s):
        v = m.group(2)
        if '{' in v or '}' in v or not re.search(r'[A-Za-z]', v):
            continue
        if re.search(r'[\u4e00-\u9fff]', v):
            continue
        leftover[v] += 1
print('\nremaining untranslated attribute values:', len(leftover))
for k, c in sorted(leftover.items())[:45]:
    print('  %3d | %s' % (c, k[:100]))
