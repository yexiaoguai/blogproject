#!/usr/bin/env python
#coding:utf-8

import sqlite3

conn = sqlite3.connect("db.sqlite3")
conn.text_factory = str
cur = conn.cursor()

movies = [
(81,'谍影重重','https://movie.douban.com/subject/1304102/','8.5',149379,
'http://www.thebourneidentity.com','NULL','NULL','NULL','NULL','NULL',' 美国 / 德国 / 捷克','2002-11-21(中国大陆)',
'马特·达蒙 弗兰卡·波坦特 克里斯·库珀 克里夫·欧文 朱丽娅·斯蒂尔斯 布莱恩·考克斯 阿德沃尔·阿吉纽依-艾格拜吉 加布里埃尔·曼 沃尔顿·戈金斯 约什·汉密尔顿 Orso Maria Guerrini','道格·里曼','动作 悬疑 冒险',
'http://www.hunantv.com/v/3/46084/f/1746082.html',
'NULL','NULL','4',1,'','NULL','NULL','NULL','NULL','/static/movie/img/p1597183981.jpg'),
# (82,'燕尾蝶','https://movie.douban.com/subject/1307793/','8.7',92982,'http://www.imdb.com/title/tt0117797','NULL','NULL','NULL','NULL','NULL','','1996-09-14(日本)','三上博史 恰拉 伊藤步 江口洋介 许志安 渡部笃郎 山口智子 大塚宁宁 桃井薰 浅野忠信','岩井俊二','剧情 犯罪','http://v.youku.com/v_show/id_XMzkxMzY0NzI0.html','NULL','NULL','4',1,'p532195562.jpg','NULL','NULL','NULL','NULL','NULL'),
# (83,'7号房的礼物','https://movie.douban.com/subject/10777687/','8.7',122859,'http://www.7gift.kr','NULL','NULL','NULL','NULL','NULL','','2013-01-23(韩国)','柳承龙 朴信惠 郑镇荣 金正泰 吴达洙 朴元尚 郑满植 葛素媛','李焕庆','剧情 喜剧 家庭','http://www.letv.com/ptv/vplay/21654375.html','NULL','NULL','4',1,'p1816276065.jpg','NULL','NULL','NULL','NULL','NULL'),
# (84,'绿里奇迹','https://movie.douban.com/subject/1300374/','8.7',85710,'http://www.imdb.com/title/tt0120689','NULL','NULL','NULL','NULL','NULL','','1999-12-10(美国)','汤姆·汉克斯 大卫·摩斯 迈克·克拉克·邓肯 邦尼·亨特 詹姆斯·克伦威尔 迈克尔·杰特 格雷厄姆·格林 道格·休切逊 山姆·洛克威尔 巴里·佩珀 杰弗里·德曼 派翠西娅·克拉克森 哈利·戴恩·斯坦通 戴布思·格里尔 Eve Brent','弗兰克·德拉邦特','剧情 悬疑 犯罪 奇幻','http://www.iqiyi.com/v_19rrhwqjjc.html?fc=87451bff3f7d2f4a#vfrm=2-3-0-1','NULL','NULL','4',1,'p767586451.jpg','NULL','NULL','NULL','NULL','NULL'),
# (85,'哈利·波特与死亡圣器(下)','https://movie.douban.com/subject/3011235/','8.6',224194,'http://www.imdb.com/title/tt1201607','NULL','NULL','NULL','NULL','NULL','','2011-08-04(中国大陆)','丹尼尔·雷德克里夫 艾玛·沃森 鲁伯特·格林特 海伦娜·伯翰·卡特 拉尔夫·费因斯 艾伦·瑞克曼 玛吉·史密斯 汤姆·费尔顿 邦妮·怀特 朱丽·沃特斯 迈克尔·刚本 伊文娜·林奇 多姆纳尔·格里森 克蕾曼丝·波西 詹森·艾萨克 海伦·麦克洛瑞 马修·刘易斯 梁佩诗','大卫·叶茨','剧情 悬疑 奇幻 冒险','http://so.iqiyi.com/outsitevip?url=http%3A%2F%2Ffilm.qq.com%2Fcover%2Fe%2Feshodxofa7omesm.html%3Fptag%3Diqiyi&site=%E8%85%BE%E8%AE%AF&name=%E5%93%88%E5%88%A9%C2%B7%E6%B3%A2%E7%89%B9%E4%B8%8E%E6%AD%BB%E4%BA%A1%E5%9C%A3%E5%99%A8+%E4%B8%8B&sign=2f784ca7f69ef6','NULL','NULL','4',1,'p917846733.jpg','NULL','NULL','NULL','NULL','NULL'),
# (86,'罗生门','https://movie.douban.com/subject/1291879/','8.7',94778,'http://www.imdb.com/title/tt0042876','NULL','NULL','NULL','NULL','NULL','','1950-08-25(日本)','三船敏郎 千秋实 京町子 森雅之 志村乔','黑泽明','剧情 悬疑 犯罪','http://www.iqiyi.com/w_19rr6p0j8x.html#vfrm=2-3-0-1','NULL','NULL','4',1,'p1864872647.jpg','NULL','NULL','NULL','NULL','NULL'),
# (87,'梦之安魂曲','https://movie.douban.com/subject/1292270/','8.7',86175,'http://www.imdb.com/title/tt0180093','NULL','NULL','NULL','NULL','NULL','','2000-10-27','艾伦·伯斯汀 杰瑞德·莱托 詹妮弗·康纳利 马龙·韦恩斯 克里斯托弗·麦克唐纳 露易丝·拉塞尔 玛西娅·让·库尔茨 夏洛特·阿罗诺夫斯基 马克·马戈利斯 Janet Sarno Suzanne Shepherd','达伦·阿伦诺夫斯基','剧情','http://www.iqiyi.com/dianying/20120131/1b4ba4f7fe43040b.html#vfrm=2-3-0-1','NULL','NULL','4',1,'p884936202.jpg','NULL','NULL','NULL','NULL','NULL'),
# (88,'迁徙的鸟','https://movie.douban.com/subject/1292281/','9.1',45757,'http://www.imdb.com/title/tt0301727','NULL','NULL','NULL','NULL','NULL','','2001-12-12(法国)','Philippe Labro 雅克·贝汉','雅克·贝汉 雅克·克鲁奥德米歇尔·德巴','纪录片','http://v.pptv.com/show/zdbLSbEXh8Uopiao.html','NULL','NULL','4',1,'p2238274168.jpg','NULL','NULL','NULL','NULL','NULL'),
# (89,'消失的爱人','https://movie.douban.com/subject/21318488/','8.7',259853,'http://www.imdb.com/title/tt2267998','NULL','NULL','NULL','NULL','NULL','','2014-09-26(纽约电影节)','本·阿弗莱克 裴淳华 尼尔·帕特里克·哈里斯 凯莉·库恩 泰勒·派瑞 金·迪肯斯 米西·派勒 波伊德·霍布鲁克 艾米丽·拉塔科斯基 雪拉·渥德 派屈克·福吉特 斯科特·麦克纳里 凯西·威尔逊 李·诺里斯','大卫·芬奇','剧情 悬疑 惊悚 犯罪','http://www.iqiyi.com/v_19rro18qig.html?fc=87451bff3f7d2f4a#vfrm=2-3-0-1','NULL','NULL','4',1,'p2221768894.jpg','NULL','NULL','NULL','NULL','NULL'),
# (90,'战争之王','https://movie.douban.com/subject/1419936/','8.5',145192,'http://www.imdb.com/title/tt0399295','NULL','NULL','NULL','NULL','NULL','','2005-09-16(美国)','尼古拉斯·凯奇 伊桑·霍克 杰瑞德·莱托 Shake Tukhmanyan 布丽姬·穆娜','安德鲁·尼科尔','剧情 犯罪','http://www.letv.com/ptv/vplay/1374489.html','NULL','NULL','4',1,'p453719066.jpg','NULL','NULL','NULL','NULL','NULL'),
# (91,'恐怖直播','https://movie.douban.com/subject/21360417/','8.7',140534,'http://www.imdb.com/title/tt2990738','NULL','NULL','NULL','NULL','NULL','','2013-07-31(韩国)','河正宇 李璟荣 全慧珍 李大为','金秉祐','剧情 悬疑 犯罪','http://www.tudou.com/albumplay/y7_-8VE07kQ/48LynvKRnwE.html','NULL','NULL','4',1,'p2016930906.jpg','NULL','NULL','NULL','NULL','NULL'),
# (92,'朗读者','https://movie.douban.com/subject/2213597/','8.4',238846,'http://www.imdb.com/title/tt0976051','NULL','NULL','NULL','NULL','NULL','','2008-12-10(纽约首映)','凯特·温丝莱特 拉尔夫·费因斯 大卫·克劳斯 詹妮特·海因 苏珊娜·罗莎 Alissa Wilms 弗罗里安·巴西奥罗麦 Friederike Becht 马赛斯·哈贝奇 Frieder Venus Marie-Anne Fliegel Hendrik Arnst Rainer Sellien Torsten Michaelis Moritz Grove','史蒂芬·戴德利','剧情 爱情','http://www.iqiyi.com/v_19rrhk107w.html#vfrm=2-3-0-1','NULL','NULL','4',1,'p1140984198.jpg','NULL','NULL','NULL','NULL','NULL'),
# (93,'追随','https://movie.douban.com/subject/1397546/','9.0',59393,'http://www.imdb.com/title/tt0154506','NULL','NULL','NULL','NULL','NULL','','1998-09-12(多伦多电影节)','杰里米·西奥伯德 亚历克斯·霍 露西·拉塞尔 约翰·诺兰','克里斯托弗·诺兰','悬疑 惊悚 犯罪','http://www.tudou.com/programs/view/aH_fuK6Dfqk/?tpa=dW5pb25faWQ9MTAyMjEzXzEwMDAwMV8wMV8wMQ','NULL','NULL','4',1,'p2074443514.jpg','NULL','NULL','NULL','NULL','NULL'),
# (94,'可可西里','https://movie.douban.com/subject/1308857/','8.6',107055,'http://www.imdb.com/title/tt0386651','NULL','NULL','NULL','NULL','NULL','','2004-10-01(中国大陆)','多布杰 张磊 亓亮 赵雪莹 马占林 赵一穗','陆川','剧情','http://www.hunantv.com/v/3/54311/f/709752.html','NULL','NULL','4',1,'p1159398311.jpg','NULL','NULL','NULL','NULL','NULL'),
# (44160,'喜宴','https://movie.douban.com/subject/1303037/','8.7',101248,'http://www.imdb.com/title/tt0107156',NULL,NULL,NULL,NULL,NULL,'','1993-02(柏林电影节)','赵文瑄 归亚蕾 金素梅 郎雄 米切尔·利希藤斯坦','李安','剧情 喜剧 爱情 同性 家庭','http://v.qq.com/page/w/n/I/w0010TsWrnI.html?ptag=iqiyi',NULL,NULL,'4',1,'p2173713676.jpg',NULL,NULL,NULL,NULL,NULL),
# (44161,'海盗电台','https://movie.douban.com/subject/3007773/','8.7',147588,'http://www.imdb.com/title/tt1131729',NULL,NULL,NULL,NULL,NULL,'','2009-04-01(英国)','比尔·奈伊 肯尼思·布拉纳 菲利普·塞默·霍夫曼 尼克·弗罗斯特 汤姆·斯图里奇 瑞斯·伊凡斯 瑞斯·达比 克里斯·奥多德 妲露拉·莱莉 凯瑟琳·帕金森 杰克·达文波特','理查德·柯蒂斯','剧情 喜剧 音乐','http://so.iqiyi.com/outsitevip?url=http%3A%2F%2Fwww.hunantv.com%2Fv%2F3%2F12083%2Ff%2F1746106.html&site=%E8%8A%92%E6%9E%9Ctv&name=%E6%B5%B7%E7%9B%97%E7%94%B5%E5%8F%B0&sign=8a2596b9a3f65444324824d486c0af80',NULL,NULL,'4',1,'p769608791.jpg',NULL,NULL,NULL,NULL,NULL),
# (44162,'红辣椒','https://movie.douban.com/subject/1865703/','8.8',88288,'http://www.imdb.com/title/tt0851578',NULL,NULL,NULL,NULL,NULL,'','2006-09-02(威尼斯电影节)','林原惠美 古谷彻 江守彻 山寺宏一 堀胜之祐 大塚明夫 岩田光央 田中秀幸','今敏','科幻 动画 悬疑 惊悚','http://www.iqiyi.com/v_19rrjczkbc.html#vfrm=2-3-0-1',NULL,NULL,'4',1,'p672363704.jpg',NULL,NULL,NULL,NULL,NULL),
# (44163,'萤火之森','https://movie.douban.com/subject/5989818/','8.8',115258,'http://www.hotarubi.info',NULL,NULL,NULL,NULL,NULL,'','2011-09-17(日本)','佐仓绫音 内山昂辉','大森贵弘','剧情 爱情 动画 奇幻','http://www.iqiyi.com/dongman/20120626/ece98897b70d6a00.html#vfrm=2-3-0-1',NULL,NULL,'4',1,'p1272904657.jpg',NULL,NULL,NULL,NULL,NULL),
# (44164,'浪潮','https://movie.douban.com/subject/2297265/','8.7',100688,'http://www.imdb.com/title/tt1063669',NULL,NULL,NULL,NULL,NULL,'','2008-03-13(德国)','约根·沃格尔 詹妮弗·乌尔里希 马克思·雷迈特 克里斯蒂安妮·保罗 弗雷德里克·劳','丹尼斯·甘塞尔','剧情','http://www.iqiyi.com/w_19rqt4f3zd.html#vfrm=2-3-0-1',NULL,NULL,'4',1,'p1344888983.jpg',NULL,NULL,NULL,NULL,NULL),
# (44165,'纵横四海','https://movie.douban.com/subject/1295409/','8.7',109587,'http://www.imdb.com/title/tt0101020',NULL,NULL,NULL,NULL,NULL,'','1991-02-02(香港)','周润发 张国荣 钟楚红 朱江 曾江 胡枫 唐宁 邓一君','吴宇森','剧情 喜剧 动作 犯罪','http://www.iqiyi.com/v_19rrmy7e98.html#vfrm=2-3-0-1',NULL,NULL,'4',1,'p933122297.jpg',NULL,NULL,NULL,NULL,NULL),
# (44166,'撞车','https://movie.douban.com/subject/1388216/','8.6',147272,'http://www.crashfilm.com/',NULL,NULL,NULL,NULL,NULL,'','2004-09-10(多伦多电影节)','桑德拉·布洛克 唐·钱德尔 马特·狄龙 布兰登·费舍 泰伦斯·霍华德 坦迪·牛顿 卢达克里斯 迈克尔·佩纳 珍妮弗·艾斯波西多','保罗·哈吉斯','剧情 犯罪','http://www.iqiyi.com/v_19rrh5aifc.html#vfrm=2-3-0-1',NULL,NULL,'4',1,'p2075132390.jpg',NULL,NULL,NULL,NULL,NULL),
# (44167,'碧海蓝天','https://movie.douban.com/subject/1300960/','8.7',95455,'http://www.imdb.com/title/tt0095250',NULL,NULL,NULL,NULL,NULL,'','1988-05-11(法国)','让-马克·巴尔 让·雷诺 罗姗娜·阿奎特','吕克·贝松','剧情 爱情','http://vod.kankan.com/v/33/33347.shtml?id=731100',NULL,NULL,'4',1,'p455724599.jpg',NULL,NULL,NULL,NULL,NULL),
# (44168,'冰川时代','https://movie.douban.com/subject/1291578/','8.4',227632,'http://www.imdb.com/title/tt0268380',NULL,NULL,NULL,NULL,NULL,'','2002-03-15(美国)','雷·罗马诺 约翰·雷吉扎莫 丹尼斯·利瑞 杰克·布莱克','卡洛斯·沙尔丹哈克里斯·韦奇','喜剧 动画 冒险','http://www.iqiyi.com/v_19rrn4rmcc.html?fc=87451bff3f7d2f4a#vfrm=2-3-0-1',NULL,NULL,'4',1,'p1910895719.jpg',NULL,NULL,NULL,NULL,NULL),
# (44169,'香水','https://movie.douban.com/subject/1760622/','8.4',228743,'http://www.parfum.film.de/',NULL,NULL,NULL,NULL,NULL,'','2006-09-07(德国)','本·卫肖 艾伦·瑞克曼 蕾切儿·哈伍德 达斯汀·霍夫曼 大卫·卡尔德 波奇特·密尼梅雅 Carlos Gramaje 西恩·托马斯 佩里·米尔沃德 山姆·道格拉斯 卡洛琳·赫弗斯 Carolina Vera Squella 莎拉·弗里斯蒂 科琳娜·哈弗奇 洁西卡·史瓦兹 杰罗姆·威利斯','汤姆·提克威','剧情 犯罪 奇幻','http://www.iqiyi.com/dianying/20130703/1556a8144b2cc82b.html?fc=87451bff3f7d2f4a#vfrm=2-3-0-1',NULL,NULL,'4',1,'p470006658.jpg',NULL,NULL,NULL,NULL,NULL),
# (44170,'雨中曲','https://movie.douban.com/subject/1293460/','8.9',74520,'http://www.imdb.com/title/tt0045152',NULL,NULL,NULL,NULL,NULL,'','1952-04-11(美国)','吉恩·凯利 唐纳德·奥康纳 黛比·雷诺斯 赛德·查里斯 简·哈根','斯坦利·多南吉恩·凯利','喜剧 爱情 歌舞','http://v.pptv.com/show/4YR7ibWHHN3XYVpo.html',NULL,NULL,'4',1,'p1612355875.jpg',NULL,NULL,NULL,NULL,NULL),
# (44171,'英雄本色','https://movie.douban.com/subject/1297574/','8.7',113404,'http://www.imdb.com/title/tt0092263',NULL,NULL,NULL,NULL,NULL,'','1986-08-02(香港)','周润发 狄龙 张国荣 朱宝意 李子雄 田丰 吴宇森 曾江 成奎安 徐克','吴宇森','动作 犯罪','http://www.iqiyi.com/dianying/20120803/923648c1b05a019b.html#vfrm=2-3-0-1',NULL,NULL,'4',1,'p2157672975.jpg',NULL,NULL,NULL,NULL,NULL),
# ]

cur.executemany("insert into movie_movie values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", movies)
conn.commit()