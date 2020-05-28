import json
from nCovNews import db
from nCovNews import datatype , data_predict
from datetime import date , timedelta

namemap = {"Canada":"加拿大",
"Turkmenistan":"土库曼斯坦",
"Saint Helena":"圣赫勒拿",
"Lao PDR":"老挝",
"Lithuania":"立陶宛",
"Cambodia":"柬埔寨",
"Ethiopia":"埃塞俄比亚",
"Faeroe Is.":"法罗群岛",
"Swaziland":"斯威士兰",
"Palestine":"巴勒斯坦",
"Belize":"伯利兹",
"Argentina":"阿根廷",
"Bolivia":"玻利维亚",
"Cameroon":"喀麦隆",
"Burkina Faso":"布基纳法索",
"Aland":"奥兰群岛",
"Bahrain":"巴林",
"Saudi Arabia":"沙特阿拉伯",
"Fr. Polynesia":"法属波利尼西亚",
"Cape Verde":"佛得角",
"W. Sahara":"西撒哈拉",
"Slovenia":"斯洛文尼亚",
"Guatemala":"危地马拉",
"Guinea":"几内亚",
"Dem. Rep. Congo":"刚果（金）",
"Germany":"德国",
"Spain":"西班牙",
"Liberia":"利比里亚",
"Netherlands":"荷兰",
"Jamaica":"牙买加",
"Solomon Is.":"所罗门群岛",
"Oman":"阿曼",
"Tanzania":"坦桑尼亚",
"Costa Rica":"哥斯达黎加",
"Isle of Man":"曼岛",
"Gabon":"加蓬",
"Niue":"纽埃",
"Bahamas":"巴哈马",
"New Zealand":"新西兰",
"Yemen":"也门",
"Jersey":"泽西岛",
"Pakistan":"巴基斯坦",
"Albania":"阿尔巴尼亚",
"Samoa":"萨摩亚",
"CzechRep.":"捷克",
"United Arab Emirates":"阿拉伯联合酋长国",
"Guam":"关岛",
"India":"印度",
"Azerbaijan":"阿塞拜疆",
"N. Mariana Is.":"北马里亚纳群岛",
"Lesotho":"莱索托",
"Kenya":"肯尼亚",
"Belarus":"白俄罗斯",
"Tajikistan":"塔吉克斯坦",
"Turkey":"土耳其",
"Afghanistan":"阿富汗",
"Bangladesh":"孟加拉国",
"Mauritania":"毛里塔尼亚",
"Dem. Rep. Korea":"朝鲜",
"Saint Lucia":"圣卢西亚",
"Br. Indian Ocean Ter.":"英属印度洋领地",
"Mongolia":"蒙古",
"France":"法国",
"Culaçao":"库拉索岛",
"S. Sudan":"南苏丹",
"Rwanda":"卢旺达",
"Slovakia":"斯洛伐克",
"Somalia":"索马里",
"Peru":"秘鲁",
"Vanuatu":"瓦努阿图",
"Norway":"挪威",
"Malawi":"马拉维",
"Benin":"贝宁",
"St. Vin. and Gren.":"圣文森特和格林纳丁斯",
"Korea":"韩国",
"Singapore":"新加坡",
"Montenegro":"黑山共和国",
"Cayman Is.":"开曼群岛",
"Togo":"多哥",
"China":"中国",
"Heard I. and McDonald Is.":"赫德岛和麦克唐纳群岛",
"Armenia":"亚美尼亚",
"Falkland Is.":"马尔维纳斯群岛（福克兰）",
"Ukraine":"乌克兰",
"Ghana":"加纳",
"Tonga":"汤加",
"Finland":"芬兰",
"Libya":"利比亚",
"Dominican Rep.":"多米尼加",
"Indonesia":"印度尼西亚",
"Mauritius":"毛里求斯",
"Eq. Guinea":"赤道几内亚",
"Sweden":"瑞典",
"Vietnam":"越南",
"Mali":"马里",
"Russia":"俄罗斯",
"Bulgaria":"保加利亚",
"United States":"美国",
"Romania":"罗马尼亚",
"Angola":"安哥拉",
"Chad":"乍得",
"South Africa":"南非",
"Fiji":"斐济",
"Liechtenstein":"列支敦士登",
"Malaysia":"马来西亚",
"Austria":"奥地利",
"Mozambique":"莫桑比克",
"Uganda":"乌干达",
"Japan":"日本",
"Niger":"尼日尔",
"Brazil":"巴西",
"Kuwait":"科威特",
"Panama":"巴拿马",
"Guyana":"圭亚那",
"Madagascar":"马达加斯加",
"Luxembourg":"卢森堡",
"American Samoa":"美属萨摩亚",
"Andorra":"安道尔",
"Ireland":"爱尔兰",
"Italy":"意大利",
"Nigeria":"尼日利亚",
"Turks and Caicos Is.":"特克斯和凯科斯群岛",
"Ecuador":"厄瓜多尔",
"U.S. Virgin Is.":"美属维尔京群岛",
"Brunei":"文莱",
"Australia":"澳大利亚",
"Iran":"伊朗",
"Algeria":"阿尔及利亚",
"El Salvador":"萨尔瓦多",
"Côte d'Ivoire":"科特迪瓦",
"Chile":"智利",
"Puerto Rico":"波多黎各",
"Belgium":"比利时",
"Thailand":"泰国",
"Haiti":"海地",
"Iraq":"伊拉克",
"São Tomé and Principe":"圣多美和普林西比",
"SierraLeone":"塞拉利昂",
"Georgia":"格鲁吉亚",
"Denmark":"丹麦",
"Philippines":"菲律宾",
"S. Geo. and S. Sandw. Is.":"南乔治亚岛和南桑威奇群岛",
"Moldova":"摩尔多瓦",
"Morocco":"摩洛哥",
"Namibia":"纳米比亚",
"Malta":"马耳他",
"Guinea-Bissau":"几内亚比绍",
"Kiribati":"基里巴斯",
"Switzerland":"瑞士",
"Grenada":"格林纳达",
"Seychelles":"塞舌尔",
"Portugal":"葡萄牙",
"Estonia":"爱沙尼亚",
"Uruguay":"乌拉圭",
"Antigua and Barb.":"安提瓜和巴布达",
"Lebanon":"黎巴嫩",
"Uzbekistan":"乌兹别克斯坦",
"Tunisia":"突尼斯",
"Djibouti":"吉布提",
"Greenland":"格陵兰",
"Timor-Leste":"东帝汶",
"Dominica":"多米尼克",
"Colombia":"哥伦比亚",
"Burundi":"布隆迪",
"Bosnia and Herz.":"波斯尼亚和黑塞哥维那",
"Cyprus":"塞浦路斯",
"Barbados":"巴巴多斯",
"Qatar":"卡塔尔",
"Palau":"帕劳",
"Bhutan":"不丹",
"Sudan":"苏丹",
"Nepal":"尼泊尔",
"Micronesia":"密克罗尼西亚",
"Bermuda":"百慕大",
"Suriname":"苏里南",
"Venezuela":"委内瑞拉",
"Israel":"以色列",
"St. Pierre and Miquelon":"圣皮埃尔和密克隆群岛",
"Central African Rep.":"中非",
"Iceland":"冰岛",
"Zambia":"赞比亚",
"Senegal":"塞内加尔",
"Papua New Guinea":"巴布亚新几内亚",
"Trinidad and Tobago":"特立尼达和多巴哥",
"Zimbabwe":"津巴布韦",
"Jordan":"约旦",
"Gambia":"冈比亚",
"Kazakhstan":"哈萨克斯坦",
"Poland":"波兰",
"Eritrea":"厄立特里亚",
"Kyrgyzstan":"吉尔吉斯斯坦",
"Montserrat":"蒙特塞拉特",
"New Caledonia":"新喀里多尼亚",
"Macedonia":"马其顿",
"Paraguay":"巴拉圭",
"Latvia":"拉脱维亚",
"Hungary":"匈牙利",
"Syria":"叙利亚",
"Honduras":"洪都拉斯",
"Myanmar":"缅甸",
"Mexico":"墨西哥",
"Egypt":"埃及",
"Nicaragua":"尼加拉瓜",
"Cuba":"古巴",
"Serbia":"塞尔维亚",
"Comoros":"科摩罗",
"United Kingdom":"英国",
"Fr. S. Antarctic Lands":"南极洲",
"Congo":"刚果（布）",
"Greece":"希腊",
"Sri Lanka":"斯里兰卡",
"Croatia":"克罗地亚",
"Botswana":"博茨瓦纳",
"Siachen Glacier":"锡亚琴冰川地区"

}

def data():
    # 中国数据
    chinatotal = datatype.CHINATOTAL.query.all()
    chinatotal.sort(key=lambda x:x.date)
    timeseries = []
    china = {'confirmedtotal':[],'confirmedexist':[],'suspected':[],'cures':[],'deaths':[],'asymptomatic':[]}
    chinaInc = {'confirmedtotal':[],'confirmedexist':[],'suspected':[],'cures':[],'deaths':[],'asymptomatic':[]}
    for item in chinatotal:
        timeseries.append(str(item.date))
        china['confirmedtotal'].append([str(item.date),item.confirmed])
        china['confirmedexist'].append([str(item.date),item.confirmed-item.cures-item.deaths])
        china['cures'].append([str(item.date),item.cures])
        china['suspected'].append([str(item.date),item.suspected])
        chinaInc['suspected'].append([str(item.date),item.suspectedInc])# 新增疑似
        china['deaths'].append([str(item.date),item.deaths])
        china['asymptomatic'].append([str(item.date),item.asymptomatic])  
    # 计算变化量(不含疑似)
    for i in range(len(chinatotal)-1):
        chinaInc['confirmedtotal'].append([timeseries[i+1],china['confirmedtotal'][i+1][1]-china['confirmedtotal'][i][1]])
        chinaInc['confirmedexist'].append([timeseries[i+1],china['confirmedexist'][i+1][1]-china['confirmedexist'][i][1]])
        chinaInc['cures'].append([timeseries[i+1],china['cures'][i+1][1]-china['cures'][i][1]])
        chinaInc['deaths'].append([timeseries[i+1],china['deaths'][i+1][1]-china['deaths'][i][1]])
        chinaInc['asymptomatic'].append([timeseries[i+1],china['asymptomatic'][i+1][1]-china['asymptomatic'][i][1]])
    # 计算百分比
    chinaPercent = {'cures':[],'deaths':[]}
    for item in chinatotal:
        num=int(item.cures/item.confirmed*10000)
        chinaPercent['cures'].append([str(item.date),num/100])
        num=int(item.deaths/item.confirmed*10000)
        chinaPercent['deaths'].append([str(item.date),num/100])
    # 构造预测序列
    predictseries = []
    dt = 100 # 预测天数
    for i in range(0,len(chinatotal)+dt):
        if i<len(chinatotal):
            predictseries.append(chinatotal[i].date)
        else:
            predictseries.append(predictseries[i-1]+timedelta(days = 1))
    for i in range(0,len(chinatotal)+dt):
        predictseries[i] = str(predictseries[i])
    # 趋势预测
    chinaPredict = {'confirmedtotal':[],'confirmedexist':[],'suspected':[],'cures':[],'deaths':[],'asymptomatic':[]}
    chinaPredict['confirmedtotal']=data_predict.result2(predictseries,china['confirmedtotal'],0.55)
    chinaPredict['confirmedexist']=data_predict.result2(predictseries,china['confirmedexist'],0.4)
    # 地图数据
    provinces = datatype.PROVINCE.query.filter_by(date=date.today()).all()
    map = {'confirmedtotal':[],'confirmedexist':[],'cures':[],'deaths':[],'asymptomatic':[]}
    for item in provinces:
        map['confirmedtotal'].append({'name':item.name,'value':item.confirmed})
        map['confirmedexist'].append({'name':item.name,'value':item.confirmed-item.cures-item.deaths})
        map['cures'].append({'name':item.name,'value':item.cures})
        map['deaths'].append({'name':item.name,'value':item.deaths})
        map['asymptomatic'].append({'name':item.name,'value':item.asymptomatic})
    # 中国Top数据
    chinaTop = {'confirmedtotal':{},'confirmedexist':{},'cures':{},'deaths':{},'asymptomatic':{}}
    for item in map:
        map[item].sort(key=lambda x:x['value'],reverse=True)
        name , value = [] , []
        for i in range(0,10):
            name.append(map[item][i]['name'])
            value.append(map[item][i]['value'])
        chinaTop[item]['name']=name
        chinaTop[item]['value']=value
    # 世界地图数据
    mymap = {}
    for item in namemap:
        mymap[namemap[item]] = item
    countries = datatype.COUNTRY.query.filter_by(date=date.today()).all()
    worldmap = {'confirmedtotal':[],'confirmedexist':[],'cures':[],'deaths':[]}
    for item in countries:
        if (item.name in mymap):
            name = mymap[item.name]
        else:
            name = item.name
        worldmap['confirmedtotal'].append({'name':name,'value':item.confirmed})
        worldmap['confirmedexist'].append({'name':name,'value':item.confirmed-item.cures-item.deaths})
        worldmap['cures'].append({'name':name,'value':item.cures})
        worldmap['deaths'].append({'name':name,'value':item.deaths})
    # 补充中国数据
    worldmap['confirmedtotal'].append({'name':'China','value':china['confirmedtotal'][len(china)][1]})
    worldmap['confirmedexist'].append({'name':'China','value':china['confirmedexist'][len(china)][1]})
    worldmap['cures'].append({'name':'China','value':china['cures'][len(china)][1]})
    worldmap['deaths'].append({'name':'China','value':china['deaths'][len(china)][1]})
    # 世界Top数据
    worldTop = {'confirmedtotal':{},'confirmedexist':{},'cures':{},'deaths':{}}
    for item in worldmap:
        worldmap[item].sort(key=lambda x:x['value'],reverse=True)
        name , value = [] , []
        for i in range(0,10):
            t = worldmap[item][i]['name']
            if t in namemap:
               t=namemap[t]
            name.append(t)
            value.append(worldmap[item][i]['value'])
        worldTop[item]['name']=name
        worldTop[item]['value']=value
    return json.dumps({'timeseries':timeseries,
                       'predictseries':predictseries,
                       'china':china,
                       'chinaInc':chinaInc,
                       'chinaPercent':chinaPercent,
                       'chinaPredict':chinaPredict,
                       'map':map,
                       'chinaTop':chinaTop,
                       'worldmap':worldmap,
                       'worldTop':worldTop,
                       },ensure_ascii=False)