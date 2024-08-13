# XierluoEPUB_Sigil

个人制作、更新的Sigil插件合集，制作部分均为自制，更新部分为对部分开源插件的更新

## CryFont

**自制**

主要作用为对EPUB中的主文本部分进行文本混淆加密，小幅度提高破解难度

##### *使用方案：*

下载Release中对应的压缩包即可使用，github代码仅包含插件主体，未包含所有支持项

Release中的ttf文件为模板字体文件，可以自行替换为其他字体文件。

##### *代码解析：*

代码段由三个部分组成：

1、简单文件名混淆

```python
a = os.urandom(32)
b = base64.encodebytes(a).decode('utf8')
c = re.findall('[a-zA-Z]*', b)
ttf_name = ''.join(c)
```

2、混淆ttf文件生成与使用

```python
# 生成ttf文件并导入
cry_fonts_list = obfuscate_plus(easy_font, ttf_name)
bk.addfile(ttf_name + ".ttf", ttf_name + ".ttf", f.read())

# 生成新的css文件调用字体
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
```

3、混淆文字替换

```python
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
```

##### *实现效果：*

原始情况

```html
<head>
    <title></title>
    <link href="style/base_css.css" rel="stylesheet" type="text/css"/>
</head>
<body>
    <p>啊—......好累。</p>
    <p>在这如蒸炉般炎热的七月天中，大概没人愿意动弹吧。</p>
    <p>『爱丽丝舞台』的活动结束已经过去两天，但我的兴奋还未结束。</p>
    <p>一闭上眼，那天的欢呼，压倒性的演出什么的，现在还历历在目。</p>
    <p>还有，SD由奈酱的可爱姿态。</p>
    <p>于是，第二节课的体育课，就改成旁观学习了。（译：見学，旁观学习，就是上课的时候在旁边请假摸鱼的意思）</p>
    <p>“诶......游一。你果然也在那天活动上耗尽了全力吗”</p>
</body>
```

混淆情况

```html
<head>
  <title></title>
    <link href="style/base_css.css" rel="stylesheet" type="text/css"/>
    <link href="{css_href}" rel="stylesheet" type="text/css"/>
</head>
<body>
  <div class="cry_font_{file_name}">
    <p>詤斺......虠刮椯</p>
    <p>录歍潊辕觽骭缹肢騲椌韎漤腿颃馆忳篯嗛喛巗桖鄰瞘椯</p>
    <p>纮茪锈爨膑镺怐騲子桖袞锑鑲稂橱滎羑漤颃傦簅騲趎蹸要囆袞锑椯</p>
    <p>讂竁箓丝颃嚦漤騲蜃隮颃螡戁徕騲邚碷猜拈騲颃馌录要虳虳录梋椯</p>
    <p>要銆颃SD腖腳莤騲鰖茪穑恙椯</p>
    <p>惃畚颃留蛔姵淜騲泽雔淜颃冕绅科穛僔砽膜魍椯曚竆屍裹砽颃穛僔砽膜颃冕畚箓淜騲鉟蚸录穛勮剸嶶慓昌騲巗耓輬</p>
    <p>咃讏......錈讂椯李楲飏蟕录嚦漤子桖箓缸靎魍學耽椶揗</p>
  </div>
</body>
```

效果图(v1版本)
![Image text](https://github.com/Nihility-Protoss/XierluoEPUB_Sigil/blob/main/img_README/CryFont.png)


## font

更新，原代码发布在：[天使动漫（无语大佬）](https://www.tsdm39.net/forum.php?mod=viewthread&tid=971897&mobile=yes)

针对原本需要自己手动修改用户名地址的问题，进行了一点点优化，现在能够不修改直接使用了

##### *核心更新代码：*

```python
# 更新前
# HOMEPATH需要使用者手动更换
os.chdir('C:\\home\$HOMEPATH\AppData\Local\sigil-ebook\sigil\plugins\\font')

# 更新后
user_path = os.getenv('HOMEPATH')
os.chdir('C:' + user_path + '\AppData\Local\sigil-ebook\sigil\plugins\\font')
```
