import re
import os
import sys
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode


def has_glyph(font, glyph):
    for table in font['cmap'].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False


def run(bk):
    user_path = os.getenv('HOMEPATH')
    os.chdir('C:' + user_path + '\AppData\Local\sigil-ebook\sigil\plugins\\font')
    print('开始运行')
    count = 1
    htmltext = ''
    html_dic = []
    for html_id, href in bk.text_iter():
        temp = bk.readfile(html_id)
        html_dic.append({
            'id': html_id,
            'content': temp
        })
        htmltext += temp
        # bk.writefile(html_id, html)
    htmltext = re.sub(r'\s', '', htmltext)
    htmltext_set = set(htmltext)
    font = TTFont('reference.ttf')
    ls = []
    for ch in htmltext_set:
        if not has_glyph(font, ch):
            ls.append(ch)
    ls.sort()
    print('参考字体中没有的字符：\n', ls, '\n')

    action = {}
    fonts = []
    fonts_name = os.listdir('fonts')
    fonts_name.sort()
    for f in fonts_name:
        fonts.append([f, TTFont('fonts/' + f)])

    for ch in ls:
        for font in fonts:
            if has_glyph(font[1], ch):
                action[font[0]] = action.get(font[0], '')+ch
                break

    for name, text in action.items():
        ftname = os.path.splitext(name)[0]
        ftfullname = ftname + '.ttf'
        options = subset.Options()
        font = subset.load_font('fonts/' + name, options)
        subsetter = subset.Subsetter(options)
        subsetter.populate(text='的' + text)
        subsetter.subset(font)
        subset.save_font(font, 'font_temp.ttf', options)
        f = open('font_temp.ttf', 'rb')
        bk.addfile(ftfullname, ftfullname, f.read())
        f.close()
        os.remove('font_temp.ttf')
        for css_id, href in bk.css_iter():
            css_content = bk.readfile(css_id)
            css_content += '\n@font-face {font-family: "' + \
                ftname + '";src: url(../Fonts/'+ftfullname+');}'
            bk.writefile(css_id, css_content)
        print('使用{}处理了以下字符：\n{}\n'.format(name, text))

    for html in html_dic:
        text = html['content']
        for name, subtext in action.items():
            family = os.path.splitext(name)[0]
            for ch in subtext:
                text = text.replace(
                    ch, '<span style="font-family: {};">'.format(family) + ch + '</span>')
        bk.writefile(html['id'], text)

    print('\n处理完毕')
    return 0


def main():
    print('请将本插件导入至sigil后运行\n')
    return -1


if __name__ == "__main__":
    import sys
    sys.exit(main())

