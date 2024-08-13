#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import base64
import tkinter as tk
from tkinter import messagebox

from confuseFont import obfuscate_plus, easy_font


def RandomName():
    a = os.urandom(32)
    b = base64.encodebytes(a).decode('utf8')
    c = re.findall('[a-zA-Z]*', b)
    d = ''.join(c)
    # e = re.sub("[a-z]", '_', d)
    # f = re.sub("[A-Z]", '*', e)
    return d

def Init(bk, _ttf_name):
    ttf_name = _ttf_name
    cry_fonts_list = obfuscate_plus(easy_font, ttf_name)
    cry_fonts_list = [i for i in cry_fonts_list]
    base_font_list = [i for i in easy_font]
    cry_fonts_dict = dict(zip(base_font_list, cry_fonts_list))

    f = open(ttf_name + '.ttf', 'rb')
    bk.addfile(ttf_name + ".ttf", ttf_name + ".ttf", f.read())
    f.close()
    os.remove(ttf_name + ".ttf")
    return cry_fonts_dict

def Convert(text, fonts_dict, file_name):
    def body_head(match):
        result = match.group()
        return result + '\n<div class="cry_font_##">\n'.replace("##", file_name)

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

def make_new_css(bk, html_file_name_list, ttf_name):
    base_name = RandomName()
    css_fmt = '@font-face {font-family: "cry_font_##";\n' \
                   'src: url(../Fonts/' + ttf_name + ".ttf" + ');}\n'
    css_fmt += '.cry_font_##{font-family: cry_font_##;}\n'
    css_content = ""
    for html_file_name in html_file_name_list:
        css_content += css_fmt.replace("##", html_file_name)

    bk.addfile(
        uniqueid=base_name, basename=f"{base_name}.css",
        data=css_content, mime="text/css"
    )
    return f"style/{base_name}.css"

def run(bk):
    ttf_name = RandomName()
    cry_fonts_dict = Init(bk, ttf_name)
    text_iter = [(_i,_j) for _i,_j in bk.text_iter()]

    # 创建主窗口
    root = tk.Tk()
    root.title("List Selection")
    # 创建列表框
    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=len(text_iter))
    listbox.pack(padx=20, pady=50)
    # 将数据添加到列表框
    for item in text_iter:
        listbox.insert(tk.END, item)
    def run_selected_items():
        selected_indices = listbox.curselection()
        selected_items = [listbox.get(i) for i in selected_indices]
        file_name_list = []
        for Id, href in selected_items:
            file_name_list.append(href.split(".")[0])
        css_href = make_new_css(bk, file_name_list, ttf_name)
        for Id, href in selected_items:
            book = bk.readfile(Id)
            book = re.sub(
                "</head>",
                f'<link href="{css_href}" rel="stylesheet" type="text/css"/>\n</head>',
                book, 0, re.S
            )
            book = re.sub(
                r'<body.*?>.*</body>',
                lambda x: Convert(x, cry_fonts_dict, href.split(".")[0]),
                book, 0, re.S
            )
            bk.writefile(Id, book)
        root.quit()

    # 创建按钮
    button = tk.Button(root, text="Run Crypto Font", command=run_selected_items)
    button.pack(pady=10)

    root.mainloop()
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
