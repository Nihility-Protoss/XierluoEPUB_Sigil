#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import base64
import tkinter as tk
from tkinter import ttk

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

    # 创建Treeview
    tree = ttk.Treeview(
        root, columns=("Data1", "Data2"),
        # columns=("Checkbox", "Data1", "Data2"),
        show="headings", height=len(text_iter), style="Treeview"
    )
    tree.column("#0", width=0, stretch=tk.NO)
    # tree.column("Checkbox", anchor=tk.CENTER, width=50)
    tree.column("Data1", anchor=tk.W, width=150)
    tree.column("Data2", anchor=tk.W, width=150)
    # tree.heading("Checkbox", text="")
    tree.heading("Data1", text="guid")
    tree.heading("Data2", text="pref")

    # # 添加垂直滚动条控件
    # scroll_bar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    # scroll_bar.grid(row=0, column=1, sticky='ns')
    # # 滚动条与 Treeview 控件进行关联
    # tree.configure(yscrollcommand=scroll_bar.set)

    # 填充数据
    for index, (data1, data2) in enumerate(text_iter):
        tree.insert(parent="", index=tk.END, iid=index, values=(data1, data2))
        tree.tag_configure(f"{index}", background="#f0f0f0")  # 设置背景色
        # tree.tag_bind(f"{index}", "<Button-1>", lambda event, _=index: toggle_checkbox(event, _))

    # # 创建复选框
    # checkboxes = {}
    # for index in range(len(text_iter)):
    #     checkboxes[index] = tk.BooleanVar()
    #     tree.set(index, "Checkbox", "×")
    # def toggle_checkbox(event, _):
    #     checkboxes[_].set(not checkboxes[_].get())
    #     tree.set(_, "Checkbox", "✓" if checkboxes[_].get() else "×")

    def run_selected_items():
        selected_items = []
        for i in tree.selection():
            selected_items.append(tree.item(i)['values'])
        print(selected_items)
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

    tree.pack()

    introduction_text = "请在上述列表中，Ctrl选取 或 Shift选取"
    label = tk.Label(root, text=introduction_text, justify=tk.LEFT)
    label.pack(padx=10, pady=10)

    button = tk.Button(root, text="Run Crypto Font", command=run_selected_items)
    button.pack(pady=10)

    root.mainloop()
    return 0


def main():
    print("I reached main when I should not have\n")
    return -1


if __name__ == "__main__":
    sys.exit(main())
