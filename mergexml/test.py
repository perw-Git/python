#!/usr/bin/python
# encoding: utf-8
import re

s1 = '{d}Blue Berries {aa} alksdjfa {bbbb}asdf'
pattern = '{*}'
for m in re.finditer(r"\{[a-zA-Z.]*\}", s1):
#     print ('String match "%s" at %d:%d') % (s1[s:e], s, e)
    print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))
#     print(match.start())
#     s = match.start()
#     e = match.end()
#     print ('String match "%s" at %d:%d' % (s1[s:e], s, e)