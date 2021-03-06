# coding:utf-8
import os
import random
import traceback
import emoji
from pathlib import Path
from collections import OrderedDict

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

# 字体名
FAMILY_NAME = 'MyAwesomeFont'
STYLE_NAME = 'Regular'
use_TTF_name = 'KaiGenGothicCN-Regular'

# 一些meta信息，请修改
NAME_STRING = {
    'familyName': FAMILY_NAME,
    'styleName': STYLE_NAME,
    'psName': FAMILY_NAME + '-' + STYLE_NAME,
    'copyright': 'Created by solarhell',
    'version': 'Version 1.0',
}
easy_font = "：；（）@「」『』“‘’”。，、？！．…—_＊＋＝～$＠§·［］【】☆"
easy_font += "的书名公女殿下家庭教师暑假期间与冰火主拯救王国第一卷感言雪中悍刀行在六月二十九号偷提前上传到今天八已经更新三万字除去不七存稿多数看其实确也但却是这些年来最努力个了请断余日子里都保持那当只两千章节便知道我码吐血有几次大概肯定就属于搁以百分熬出憋啊游戏电影可终还坚过本才发段时很早跟球们说状态好候爆而想要即得老坐脑敲度做事况记没尽量证如此后完读者清楚废柴真着把满地操重捡起果观望等养肥之类再无所谓对成绩开始野心点击红票什么从求意庆幸比象首收藏总接近四应句付回报话瞎嚷思情慢涨直现种悲义哪会相信啥管否跳坑准备汉自然激敢掉链小奔人徐凤东西姑娘少怀诗怎忧郁伤爱轻狂资身边许疯玩他结婚生娃苏州浪白条哈顺恭喜金简介瞅貌似挺武侠根纯全玄幻嘛咋能楼指江羊皮裘头儿水珠破甲己高低反湖庙堂仙魔屠颠覆吃喝拉撒怪脾气市井寒酸欢离合和放弃胆叔祖扛兴担山为岁见骑鹤南逍遥呢狐脸练位美底男尚笨北修禅李愿佛烧舍利让慕拿买胭脂粉吗骁马踏龙虎角补觉趣故写快需走升级流田别忘凉铁弱纨绔标签面烟雾弹明捭阖变动线任务正初茅庐遇层历苦作乐借柱进京机将势朝廷风云酒每钟府盘踞门户极土木盛硕仅异姓毁誉参半功勋臣皇帝宝座外愧宰手遮翻雨难政私文绉骂声蛮居叵测诛丢顶帽热闹权亲摆辉煌仪仗迎骨听圣神痴傻爷闭关弟福缘解释打哭识窍通倒威派闻给取徒约至内处院落宗捻缕胡须眉紧皱背负柄常馗式桃剑配尘谁由衷赞世呐番显阻碍方议未犟蹲株梨树用屁股统论排宜傅咳该吧连劝循善诱透拐学你揍品官死怕爹撑腰捞太惜归尉五花披搭理盯瞧津味黄糖葫芦遍楂随摘啃赵硬挤抹笑容称份忒碜被超职郡鼎口干舌燥估计耐烦嫌呱噪翘噗响扭咧嘴抬僵罢陆猛刚绰憨斗肤病暗形较同龄瘦骇军杀锦匈奴部灭城镇压夷族样膂惊般铜筋拔河叹息若稍聪慧必陷阵双缓转辈士尴尬眼示免旦张甭帮孙喽束策嘿哥辰莫表呆板寻讷眸绽罕光彩刺住往冲廊曲径折则饱受夫诟潮亭握疼醒错路足炷香父箱仆带富敌素宠溺委屈街空荡先失继愤怒沉嘶吼沙哑暴躁场恐像久秋狩霉黑罴单枪匹撕瞪虚希亏篑奈微伸枯竹臂腕慈祥费赋禀立德哼续妙古挣脱淡缚悬步何谱霸安婢捏胳膊腿脚坏拍烂桌椅厚殷产愣冠袍咦悄加止狰狞兽闲咔嚓玉踩甩整掷眯睛丝毫惹命案斤摔平敬畏领又辖境虽规模例争够送炉珍丹药飘石狮凭搏按照嫡长脍炙法赏活技术银祸害青伶或骗阔钱纪录客菜摊畔鹞溢宣淫吵顾嫩魁窗叫掺非追究差牌鞭摞鹰犬陵寂寞漂亮抢欺俱奇葩嫁克丈蛋俏妆寡妇艳远播博精纬阴宫韩谷兵纵横司灿妹伙扯英勇战败脖架撵迫豪及礼晃载彻音墙含泪画幕雀宴宵入塞跑向乎瘾钧摇牵使晦涩搬巧膝钩深松猿猴媳咂星凡消兔崽群恶咬易邸娇滴夜冷暖贫俗偶尔悔畅聊洞昏晖布包裹囊衣衫褴褛夹杂草弄碗乞讨嶙跛茬麻逃荒民块肉稀馋梦邋遢呵露缺牙贼腾途魄沿摸鱼捉迷爬掏鸟窝荤熟盐巴顿饭村庄试图鸡鸭锄棍壮累膏粱鲜袭鞋蹭慌嗝伴郊岭挖挂杏疲抽鼻陶醉狠唯凳喊歇刻忙碌店原附嘞装卖劲货色算赶端招壶贵狗炎习惯敛喘账嗓鄙拇食奶吹哨趴陋鼾竟睡尖依闪隼飞禽箭矢掠征兆轰鸣翼捧绵延仿扬旗乖麾系驰骋辗锋它戟逆芒景降卒悉哀嚎雷锐浩虹充灵瞬静辙娴伍范畴肆跪末齐喃犯彪炳熊狼融洽贱忠既掳闺题尊扔决困体墨曾驯服交性蹄踢拳温碧讯急停啕裂肺劳推踉跄跌替唤浓蜀腔涕掌肩膀换春碎侧袋格输瘸吓恋且呼并驱辆车尤扮姐淑雅姿拎裙窜宅贝徕铺啦速振鸨龟泣妖娆穿冤煞呀尾黛狭妩媚瓜俊物左佩倨傲震慑混迹痞调良她嫉妒倾羞略犹豫拣选卦问护魂毕肿邻藩咱驳队隐语戮奢侈临紫檀雕螭饰斑尺待漏另设房杯具帖堆积砚价值笔海竖林密巨窑插晶菊独瑞貔貅耗炭冬晚赤毯妨室躺床盖蟒褥憔悴站旁洒燃涎恙厌伐唐舟胸贡恨毒拼材虑守匆探砸挨歪躲恬赔罪餐宿切斜绣扫帚怜冻督默契袖乏吁弯槛牛驴恼柔淌脏擦拭划环抱讶沾旅眶湿润撇嘲哦盒屋辛辣杆竿墩茶佳肴特豆蔻华揉伺惬拥扩建倍台榭耸雄伟垂钓孤承秘笈封率旨碾桀骜禁灰各届库典套缴劫复仇鲤饵料避啧榻抿弧夸拾掇猪退改洗舒泰汤浴褪丐刮颇界醋词勾围棋琴舞贴隆葱揩油投剁喂毗丰裤裆笼谴恩戴目掩憎距侍姜泥攻驻凰享妃眷嫔甚拦吊殉贞烈赠予绫猜幼湮揣化埃瞥挥嬉乡脯越峰峦伏昔沦登史匕符忍割强毅欲袁逢绝颅举妄耻描引致耳胖滚赖屑齿臃森严褚禄共患羽虫骏矛碑蜜腹逛兄裳隔怂恿妾偏耿苍鉴勒掐圈颤颊窃据衔散辱荣凑纳细专留驾视奸诈狈嘘馨戎颁遗症诽休侯代找斩众陛抗鬓驼鬼亡肝泛匍匐拜脊梁躬踹挑汗针毡缠召葡萄琉璃炖猎捕获叛购昵鸾雍跋扈煊赫疑碰陪抄妻占财顷霍黯纸氏君迭瞄迈仔徽携螺琅琊轩辕妞妓啄唉惨遭办诺厉筹支贲鼓谋擅戾奋遵诞灾右喏贪乱胜造浮郑吾孝剥颗橘糊凌逐渐欣慰嗯蜗移晓翁剩罩仍偎戈母姒懂胯因轮爽志爵崩析猢狲苟爪窟窿幅净眺卧趟砂滔秤迟盆抛栏跃慨腻缎磨砺俭渡溜阁孩添研侃厩搂甸佻呦串铃丽程贾暂仃枣唠嗑滑稽匣运凄编饿器璇玑歹匪丧忽悠某趁屎幽怨兮染薯烤焦额旬印峋咯浅痛痒忆寇念眨考侥璧件侵乌夔蚕呕阳诀籍腥枚片坦韵迥杰扑吞箓答栗逗违认米培搓艺僧侣济虱童愉训崭朴孔绕岔周陈旧乘唾耍悟恍缩滋质宁毋滥脉钻荐赎叨吉妥燎吸吩咐凝盈蚂蚁截瞠搞拒拖豢婆绑闯泼寸讪淳苇丛谈旖旎坛栈睹秀薇置摹嚼咽蓄短轨朵采琢剐班讲鼠蛇矩宦预壁牧谢罗柜谄奉抖惧肚兜验启弥漫蒙癖夺普阅捶软糯悦勉晴霹雳芥誓毛悚尸扣际键娶偌摩挲懒伦型拙审优窄鞘憾察询掀告诉注叮嘱导檐痕谑愕夏脆闷哩卓衬泄蛾喻忐忑射园危吴冢险睥睨批槁卫匿稻卸鞍赐甘鳞粗绍寐巍峨攒忌瞭厅责痨嗜寺残嘀咕孑栋僻灯达凿尝辄雁稚寄篱仰娱蹩睁扰溪池集昭彰翰谐剔剧畸唇亵诲渣滓朋友迁聚基工馊缜罐锅缝翩泫肠愁抵适联扶愈匠拓副轶述娓乍羡蛙挠莽豁讽殴党拌淮歌孽酩酊访席圆查销芳践讳演绚聋惑猖簪扇繁琐赘倜傥船缰绳蛆庖倌箫戳邪姨莲纤柳熨雏赊臀植芭蕉怔颜丫鬟猫增减璀璨诡抚赌幺棒锣喧轿剪岂莞滞波误萍腴庸撰著呻吟盏刹姬唱押怆评榜沮昂挟肃抑涉堪令弈饥祭墓眈冥泉铿锵茫惚刎蝉刃拈撞弓虾笃臭婊枕浊鲫兼智凛厮穴砍皙晕庞殒踪躯蛰渎狎襟辞斋绸捆酥滩婉撬扎畜俯挚纹绘帛惟肖袜浸泡粒趾攀绒逸淋漓朦胧渗藤揪摧刨坟胎哽丁辘厥鸽棉糕酱允捎逝塔瓣梅钵龛跏趺托筑寓匾御赚敦映帘袂广搜潜览梯屏奕烛歉稳索惭秽耽棠貂疏央艄鹿煦岸苗陌返检兢嬷彦梧嫣崔拱矫络窘潇柑戒突茧囫囵饶诚拧胁尿晨团鹅胃瀚帙穷孜倦缥缈递骄蹈薄瑟炼钝劈疾磅礴冽触凹槽苞刁削甜骤授课杜谲咒殊鸷沈艘篷煮酿绿醅诸渭丘壑饮弩氛赢洋敞膛豹唰迅懊馅狸乾元农拂芝列昆菩萨崇茕零暮巅叶熙姚逾萃儒帷幄觅纛岛涛蘑菇奥帆棺沧醇驸治篇蓊蔚洇敷业搅绎宋渔谙伯勤稔科巷俚殃骚谜湛蓝婀娜曳樊皆逼孱蹬污措粪龌龊莹郎恹兰唬朱漆妣贺讥源桥羔榔锤健嘟浆蹙坎坷巡萌限盎午泊澈淤耀昼卵锢锁浇酷监牢判嗖镜鳖浑蔽辟芽掂谯阀渊怠洁冒鲸蛟僚赛矜馆暇噤嚅蒜枝茂晾挡羹挪堤姹莺燕惠桐饲妍律熏拢臊坠施翅鲈笋沸宕执橹季蕴淹篮怖局跺固磐遁蜻蜓魏疙瘩杠焰膜抡猩啸宽骼控塌齑阎互犄穆拆睬宇悸岩缸嗡扁涟漪璞蒂劣育俩役沫矮叉撼簸乳烹饪腑涌嗤垫棵咀呸喷叼捂省咆哮衡弊犷婴哇喟崖碣晋罡矣邓阿铸蜚粘俺捅蜂吝啬鬃艰校叠绢蚯蚓呗靠掰诣撮镶桶泻搐厕苑栖柯麝鹦芬沁蝶焉逮枰肌详枢腋粹澡阶镳惦潭涧庵翠瓦玲珑戛梵创觑汹讹坊藐恢弘峭哄陡晒册弦恳篆页祟臻协澜祈霞恰惫洪赧谶腮凋敝旋宛衍卑壳羚剌胶哆嗦殄嗽凶疮浣垒惺蝎慵靴烫抓盲捣竭絮惋曰揖嘈钗懵瘫铮坨灌拨乙丙涂羸籁冶钉蠢昨糙赴悯溅挎吕埋裨益嗅衰撤择邀宾缁弁员绷陲栩吻砌垣制贯构梳劾奏奠坤涯谣项革曹葬殚吏网鸿寅旭迄戊庚壬癸栽桩丑洛毙序永枉漱魑魅糗区租窒碟谍蟊伎腆壤诌麂欠禾奖绪逊蟹窖恸咸渍琵琶撩蹒跚防捷簇疤霜辅嚣斥罚挞玺锻址糟媲戚贻营填旷怡馁蠹纰展骸赦韶麦沽贤黝揭坡篝烁姥晰舔獠吆缄愠帐扳秣婿顽效扼稷域核辩苛寥癯酣邃篓泞仲蔼憧憬瑕疵隅韪篡诩噼啪辨褶瀑刷暄笆亦睐髓液肢隙伪绞兀斧寝趋锥辽尼嘻嵌棘隋饽织遒楷蘸胚粥腌纲挈吭辜挫刑卯蔬圃警癫虻盾轴蹦雉岳谨蝇颔蔑犀助朽陀吱岿供胄犵肋炸喙衅汇膨胀袒惮梭猬罔煽勃雌颉颃荼障驭纠履桓肱韬殆瓶阑珊仑损窈窕筷淆腐汁均匀欧蚊隶醺锏粼迢桠渠戗宏潦繇朗俞蔓汪岗狱伞蓬瞒祷牡懑沟桂膺呃蛛寿喉魍魉裸撷罄豺祁萎靡羁绛晏譬恃茸蚍蜉筛楠箐仕熠萧咏呜葛帧纂溘券虔硫磺拘挽糅卜袅拮铛峥嵘缭筮噱乃诵哉哗纷霭眄粮萦呈攥颓疚筒瓷敏沛擒逞颐貘傧袈裟濡奄厢辫妮舵诳垢荷拗蜷剃秃商抉韧塘绯佑簌怯伥康砥企盟瑜伽译眠竺档邦溯谬驹骷髅屡忿谩旮旯肘漾谥帱疆夕扒忡獭娥惕维诘贬谏觊觎剿拽棱麟巢凸渴硝债嘎痹愚簧瞑杵嘉梢磬竽笙组甬佾蹑晌抔斛觳拴谆怄悼杖勺掖掬蒸螳睚眦髻笛箜篌钏黔铤嗔枭催瘪谅薪懈邛阙翦峙邢黎俐董幡恚诰觐祛秩卿炊抟侄掣骊恁恣瞌筏勿痪忤砰嵩屯驿煜沓谒跨吠撅孪窠臼诫聩昌仁夭愎缢眩刘泳慎桑椹裕栓偿医衙泽拄葺垆亩佥谪戍骧呛阡饬署鲁蛀嗟弛瓮骥遛腭叩献谛鞠茏鸦斟酌坪踮蓦锱铢川盗杨咫帜傀儡舆蛳翊盹抠炫旱遂屹缟犒款磕搀梗樱腼诧矟藉蹶巫蛊崆峒禹括瞻韦甫塾擂盔崛栅漠飙狡猾跻酆杳鳌霾淘笫忱颖椽县佐簿俸泾巾淅沥谦迂滂沱犊促弭纶褂蝼蛄倪皂籀霄烬鏖惶觥冀拟蟾蜍阱骛荫仓昧楹盼饼漉噩瘴焚贩粟钳悻忾歧蟑螂麈揽钦祀缮旺嗣麒蠕斯蹋阐兑馥亚洌孬综嫂泱姗笞峻鸠鹊耙嵋镫攘寨锈猥呲缉乔痰幌孟榨翱翔倔曦茗邹艾撂诨缀桢禳瘟疫妪援摄哧砣鸳鸯瓢葆频饕喀迸溃侮餮蚱蹊杞荜娑械矗瘠垮遣坍浏糜聘痊孕徘徊娩姻谚匡颂唏剖媾纽皓谎蜘雇佣湍峡礁靖睢敖社咎庶崂龚旌渺怦菅舱航窥玮颈嗥竞屿厘谊忪桨瓴绊孰淼箴馒瞩襄醮舸踱虺惩诤巩銮彬僭庇祠绺襦纱媛唧喳鼋佼蹴蚨沃烘窦潸抨版咄诋樯遐睫婪葵噙阂扪烙栾舰棚舅佬犁镖励楫濯袆紊洼倚颌枷桅渲藕菱虞珣堵傍妈睦釜霆吨虐诏黜痘濒荏牲掘砖壕耕痣柢掸憩嵬檄朕唆框轧廉髯奚枋藻塑砾樟跣敕佞梃丸丞箩筐萝俨蛔喇惆怅涸涵闸磋殳荆箍裴泯婶遏酬荧嘣鎏蒲储捐悖骈醍醐芙蓉甃脔裁彼酝攫砒垃圾氓茹泠纭慷颦缱绻咚饺垠稼砻舂闱抒偕茔肓厦寰玷姣淬咙曼匝褐廓瞳摒髫绅订痍缨懦槐彗筝侩潢秉揲拷偃膳菲齤恻绮晤擘墀攸釉茎莱瀛洲镂穹囚蘀涅舀孺啼帅衢驶捋槌铠骠谀斡卢庾柃薰枇杷钤濛琳裎疗痈恪褒屐氅贸徙厨鲛赅恤疽痂沆瀣亢虬馄饨骆锡瘿耄耋裱喵鲠售觞臆匮曝炒俑冕畿擎揶揄鹄堕睽删悭伛偻逻辑擢札鹭悌闳荟灶稗邂逅斓飏炝刽叙茄涣涡柿枥阉谕踌躇沐佚荀恕歙肇袤岑牯姊瞰杉阄芾柩吮鲵蝾螈纡搴舛蚀蜮胪蜿蜒聆萤邮荔襁褓盅姘钢秦炮娈铭砧驮讦翡芯杭彷徨狙骡魈凫黏铅袄澄篾颧宙鳅邵煎牍琼愫牒铲莅铄撸鹬蚌芋玛瑙肾霖渝哺蝗臾琥珀鲐熔饴汲淀桴灼漩缅宪隘诮苔钜辐辏骰髦嚏篙骝焖滤蟋蟀喑胰蛤蟆虢瑰鹘儆亘肮娼酗書蛧砭蜕嶂蓑煸膘矶叭湾艨艟飒斐喋税澎湃骢您叟骓秧噜槊筵懿囔蜃烽陇涮募垛坯稠裣孀赳椒沼媒颍赃炕叽搔耶臜咿楣摺跤埒榆唳噎哝冈蹂躏嗷蜡轱暧韭剂锭鹉诅仄仞燧垄堞夯谧捺础佯涤俘虏卉赝茱萸隍屉嫖棕耷穗狨柏啖膈蝣朔噬倩搡缪溉舐鳢彾港澹桔帏岌烩煅鹧鸪蛐驷啰濮珪瑾蕊腊婕妤弼枳薛熄贮摭霁啜炬甥歼馈申涝纣焕粝笠衲瘤惴貉衽羌绦岷胴伊胛孛酵酪鞣帕颚谭秒胞镞冉偈镀惰椿柘麋硠霎扉祚磊巳酉戌亥冯糨亨鳃瘀灸矿涓猱笳祝潺芜猸嶷蓟垦樵哎赁歃堡涪俎邯郸粽祗轫栉弑蝴浒咻埂旒牟雹钰媪蔗箸椴鹏锒咛踝靶钥匙蒐炽剽蹚爻怵浃摁蝠陨叱咤瘁钺汰搪侦稹曙杈堑卡蚤硌缔碱佃诂坳鹳腚牤癞麓蜈蚣谤箔诿岘樽龇璜绶祅毂譵鹜湟筠炯帔阮蔡怏飓籽呓茁缤跶煲鬻圭揎獐跷函勘鳝讧瞿蜇梓皎衮墁晷诙鸮烊膻粲聂彭筌獗笺棂蒿汛祉楸皑墟懋崧滨掎逶迤渥帼亿漕翎撄舢侏禧豸鲲泷蹉跎笏幞镴髭榴椟汽镯兕柙堰搽靥跗枸袼褙仈恒鸩蒋嵇牺坝伢贽悱锚殍脓莠坂讼崎岖佝辔瓯胥沌缛郭鲥贿赂斫稕箕闩桦熛厄蝻昙螃妁倘徇鲍掻圳抪湫谗潼蹿仨旄纺戡颀潘炀萼穉瘆浚黩黠隗圻馐镝沂榫桎梏哲瓘阕橡溶铐汝鸶饷幔缶袱榷豕縻辇倏猝乒隽篦艹汐笥荚畛狻猊蝮赈徭瑶鹂鹌鹑獾汾箬櫆绌馏鳜苹矍礅亟轳蕃毓趸檕栌潋滟乩秆褫狷睿驽汶皈瑛崴舷廛踵渟碛漭妯娌囤跐茯苓碉蒺藜髀溟惇辍冗鸢凯幢狄蠛蠓恫嗒檑剉曜鹇壅爇聱嘬椎榕贷铨攲磔闰藓阆珰辎塬墚槔楯橛嘹啻逑弋榧蘅刍倡撺垭夙蝙螟蛉噫嚱馕郐竦荃饯厂崦黍遑祐祯铗蔫芍诓菁噔椭阋钮憷缦诃锯蝈甪蟠郾哂灞桡酋鞅颢獬皿踊昀弗斌幂蓠彀壹婵芊疴伉俪啐巽娟筍竣逋荑恵踟蹰癣轵陉檠旆耘兹霓醯臬轸薜曱汴渤蕨粳肛殖痉挛腺翕哒爸铰阜刊菌泌瘙屄硅焊脐妊娠屌氧腱膣镣嘤胱唔殛遽嘚肪襞皋磁喔柚锉卞雯墅骺袢嗨哟莉咪婷蓓蕾噢後嗳侬麽咨鹫圧竜迪欸姆擤莎娅嚯汀翳玻玫咖啡隧沏币獺鼬噻诶绀嘭艉艏哐謀徳蹁跹谘伫橱蔺菖惘榈淖怱盂暍啤鳏噌祢罹飕鶫現実決創間話鷺楽見箇語疹疱瞟哔怼莓橙毎週芸組駅町煤咣甄設櫓戦時鉄砲場庫織長層営擞缆灬碴葉様昊槃俄浙汩忖尹邬圜楞嗬佰鱿獒赣洱茉殡鳄浦钞咝阚孵秭亍镭钛埠邱耒橄稂缏吽柒凼徼柽榄顼澳鲨吖詹磴俾鳗艇铂榉庋蜥裔穑靓啾乇槟洎潍栲毪殓舴衩嬴氢钇乓觋丅徂阗娲钠迕暾臧铟铩踽遨舣邳氮岚锑褡蠃涠昱癌龈痫蜴卤唼妲砗镌铀犸犼焱诠鳍圡嗮夻仒轲铬痔镰栊岐捱碳亾呤闫奂娄鹨蛹宸蒗囡魃亳唦嗗羟牀缇蹼睘蚴魇驓焐诬唛豌勐俅鑫赡豊仺钨丵胤聒茨尨玖峄戕嚐啵芶飚佤楔迩柞铡鯻戬汨闼堠鼍兠珐猧爞芈瓬鴀卐氘狃唲珈鄂旸捍虓钡巯玥摦楮颏垅鬯哞茵靺鞨犴嫦觇拚峪嶝耆砜锲砉岵奎喺滇岢牥霰隹晔錾鲶廿砝仝紥迦霈麴髹偦雒炆赭邕柊醲闇鞥犽舁魰閣論曇魜彤淙恺镊晩倥偬囱龅铆蔷腩镍锃氤氲琪怫廖泵讣嗲裾剜窸窣玦泓俦蚺镏殇栀柬呯侪鋭餍喁佶杼辋磷蛭嗵鬣逡洄遴邑靛熹皲祼骐黒崮诊埕泗趔趄镐枫焙圩逦翌嗞觍矅豚骘琮昳鼹啮蒹葭铎勠沅涑涔媵萱瑚孢纩踯躅叻黾姫芨祇忸怩蚋囧嗫蒌渏爰懞唁纾墉囿禇猗棣呔筚韫揆贰徜徉圬塄钊棝鲽榏舜锂誎瞋茜秾藠忏悒眬镕堇嘁徵胫痿噶珴舶珞楒蟥锷憇趐丕柠鸵腓酡俟旽氪愽璎梆坞汞嬛煨糠睑锴汊磙钲缙鲮牝莆铻嘅鲟椰茴濠樂狴尧斒卍痢蚩磳媽蝌蚪狍吒玎禆唎唵稜镗洊岣嵝璐蓍璋掼籼姤绡噓舫湘艮鸥雎玳瑁羿羲鲦仵臌獽谰桫椤颛菽嵯耨抻醴粕阇轺佟捌砼肼坻泔艽瀵癔炁給囹圄聿侨禺溥忻酾昕摈氐炾跆洺畑苒玟剡湎荇嗄弒錿邺暼濺啍镔萋珥琚墒菀愦陔铍釖歆檒靇偲霊砀缷鄷枊铉猕龀卋鍗椐镛叁彝"


def str_has_whitespace(s: str) -> bool:
    return ' ' in s


def str_has_emoji(s: str) -> bool:
    for character in s:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False


def deduplicate_str(s: str) -> str:
    return "".join(OrderedDict.fromkeys(s))


def ensure_cmap_has_all_text(cmap: dict, s: str) -> bool:
    for char in s:
        if ord(char) not in cmap:
            raise Exception(f'字库缺少{char}这个字')
    return True


# name混淆加强版
def obfuscate_plus(plain_text, filename: str):
    """
    :param plain_text: 用户看到的内容
    :param filename: 不含格式后缀的文件名
    """
    user_path = os.getenv('HOMEPATH')
    os.chdir('C:' + user_path + '\AppData\Local\sigil-ebook\sigil\plugins\CryFont')
    if str_has_whitespace(plain_text):
        raise Exception('明文不允许含有空格')
    if str_has_emoji(plain_text):
        raise Exception('明文不允许含有emoji')

    plain_text = deduplicate_str(plain_text)

    original_font = TTFont('KaiGenGothicCNRegular.ttf')
    original_cmap: dict = original_font.getBestCmap()

    try:
        ensure_cmap_has_all_text(original_cmap, plain_text)
    except Exception as e:
        raise e

    glyphs, metrics, cmap = {}, {}, {}

    private_codes = random.sample(range(0x4E00, 0x9FA5), len(plain_text))
    if 0x7684 not in private_codes:
        plain_text += '秫'
        private_codes += [0x7684]
    cjk_codes = random.sample(range(0x4E00, 0x9FA5), len(plain_text))

    glyph_set = original_font.getGlyphSet()

    pen = TTGlyphPen(glyph_set)

    glyph_order = original_font.getGlyphOrder()

    final_shadow_text: list = []

    if 'null' in glyph_order:
        glyph_set['null'].draw(pen)
        glyphs['null'] = pen.glyph()
        metrics['null'] = original_font['hmtx']['null']

        final_shadow_text += ['null']

    if '.notdef' in glyph_order:
        glyph_set['.notdef'].draw(pen)
        glyphs['.notdef'] = pen.glyph()
        metrics['.notdef'] = original_font['hmtx']['.notdef']

        final_shadow_text += ['.notdef']

    html_entities = []

    # 理论上这里还可以再打散一次顺序
    for index, plain in enumerate(plain_text):
        try:
            shadow_cmap_name = original_cmap[cjk_codes[index]]
        except KeyError:
            # 遇到基础字库不存在的字会出现这种错误
            traceback.print_exc()
            return obfuscate_plus(filename, plain_text)

        final_shadow_text += [shadow_cmap_name]

        glyph_set[original_cmap[ord(plain)]].draw(pen)
        glyphs[shadow_cmap_name] = pen.glyph()

        metrics[shadow_cmap_name] = original_font['hmtx'][original_cmap[ord(plain)]]

        cmap[private_codes[index]] = shadow_cmap_name
        html_entities += [hex(private_codes[index]).replace('0x', '&#x')]

    horizontal_header = {
        'ascent': original_font['hhea'].ascent,
        'descent': original_font['hhea'].descent,
    }

    fb = FontBuilder(original_font['head'].unitsPerEm, isTTF=True)
    fb.setupGlyphOrder(final_shadow_text)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(**horizontal_header)
    fb.setupNameTable(NAME_STRING)
    fb.setupOS2()
    fb.setupPost()
    fb.save(f'{filename}.ttf')

    return html_entities
