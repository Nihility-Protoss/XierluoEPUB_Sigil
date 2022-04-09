#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import base64
from confuseFont import obfuscate_plus, easy_font


def Convert(text, fonts_dict):
    def body_head(match):
        result = match.group()
        return result + '\n<div class="cry_font">\n'

    def body_last(match):
        result = match.group()
        return '\n</div>\n' + result

    def MAPPING(match):
        result = match.group()
        item_1 = fonts_dict.items()
        for i in item_1:
            if i[0] in result:
                result = re.sub(i[0], i[1] + ';', result)
        result = re.sub('<body.*?>', body_head, result, 0, re.S)
        result = re.sub('</body>', body_last, result, 0, re.S)
        result = re.sub('[\"/]' + fonts_dict['图'] + fonts_dict['片'] + '-*', '\"图片-', result)
        return result

    Result = re.sub(r'.+', MAPPING, text.group(), 0, re.S)
    return Result


def run(bk):
    a = os.urandom(32)
    b = base64.encodebytes(a).decode('utf8')
    c = re.findall('[a-zA-Z]*', b)
    ttf_name = ''.join(c)
    cry_fonts_list = obfuscate_plus(easy_font, ttf_name)
    cry_fonts_list = [i for i in cry_fonts_list]
    base_font_list = [i for i in easy_font]
    cry_fonts_dict = dict(zip(base_font_list, cry_fonts_list))

    f = open(ttf_name + '.ttf', 'rb')
    bk.addfile(ttf_name + ".ttf", ttf_name + ".ttf", f.read())
    f.close()
    os.remove(ttf_name + ".ttf")
    for css_id, href in bk.css_iter():
        css_content = ""
        css_content += '@font-face {font-family: "cry_font";\n' \
                       'src: url(../Fonts/' + ttf_name + ".ttf" + ');}\n'
        css_content += '.cry_font{font-family: cry_font;}\n'
        css_content += bk.readfile(css_id)
        bk.writefile(css_id, css_content)

    for Id, href in bk.text_iter():
        book = bk.readfile(Id)
        book = re.sub(r'<body.*?>.*</body>', lambda x: Convert(x, cry_fonts_dict),
                      book, 0, re.S)
        bk.writefile(Id, book)

    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
