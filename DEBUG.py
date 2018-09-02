from selenium import webdriver
from bs4 import BeautifulSoup
import time
dong = '테스트'
printStr = \
    """
    1 .동    : {}
    2 .지번   : {}
    3 .도로명 : {}
    4 .랜드코드: {}
    5 .호수   : {} 
    6 .지붕   : {}
    7 .골조   : {}
    8 .용도(주): {}
    9 .용도(부): {}
    10.구분    : {}

    11.대지면적 : {}
    12.건축면적 : {}
    13.건폐율   : {}
    14.연면적   : {}
    15.지상연면적: {}
    16.용적률   : {} 

    17.높이    : {}
    18.지상층수 : {}
    19.지하층수 : {}
    20.세대수   : {} 
    21.주차장   : {}

    22.승인일   :{}
    23.지역지구 :{}

    24.전용면적 :{}
    25.공급면적 :{}
    26.대지권면적:{}

    27.어린이집(상위5개 m만): {}
    28.초등학교(상위3개 학교명,거리):{}
    29,중학교(상위3개 학교명,거리):{}
    30.고등학교(상위3개 학교명,거리):{}

    31.지하철 거리순5개(역명,거리):{}
    32.최근6개월매매 중위/상위30/하위30:{}
    33.현재 1㎡당 가격 : {}
    """
def get_bs_by_txt(_FILENAME):
    with open(_FILENAME,'r',encoding='utf8') as f:
        return BeautifulSoup(f.read(),'lxml')
def get_text_by_tag_attr(_tag,_attr,_value):
    if _attr == 'i':
        return bs4.find(_tag,id=_value).get_text().strip()
    elif _attr == 'c':
        return bs4.find(_tag, class_=_value).get_text().strip()
bs4 = get_bs_by_txt('26-11.txt')
#
gujuso = get_text_by_tag_attr('span', 'c', 'gujuso')  # 2열
dorojuso = get_text_by_tag_attr('span', 'c', 'dorojuso')  # 3열
landCode = ''  # 4열
honame = get_text_by_tag_attr('span', 'i', 'honame') + '(호)'  # 5열
roofName = get_text_by_tag_attr('span', 'i', 'roofName')  # 6열
gujoName = get_text_by_tag_attr('span', 'i', 'gujoName')  # 7열

# 8-9-10
rowD1Spans = bs4.find('div', class_='desc-row d1').find_all('span', class_='basicInfo')
usageMain = rowD1Spans[0].get_text().strip()  # 8열
usageSub = rowD1Spans[1].get_text().strip()  # 9열
tjttype = get_text_by_tag_attr('span', 'i', 'tjttype')  # 10열

# 11 ~ 16
rowD2Spans = bs4.find('div', class_='desc-row d2').find_all('span', class_='basicInfo')
daejiArea = rowD2Spans[0].get_text().strip() + '㎡'  # 11열
gunmulArea = rowD2Spans[1].get_text().strip() + '㎡'  # 12열
gunpaeArea = rowD2Spans[2].get_text().strip() + '%'  # 13열
yunArea = rowD2Spans[3].get_text().strip() + '㎡'  # 14열
jisangyunArea = rowD2Spans[4].get_text().strip() + '㎡'  # 15열
yongjukArea = rowD2Spans[5].get_text().strip() + '%'  # 16열

# 17 - 21
rowD3Spans = bs4.find('div', class_='desc-row d3').find_all('span', class_='basicInfo')
height = rowD3Spans[0].get_text().strip() + 'm'  # 17열
jihaHeight = rowD3Spans[1].get_text().strip() + '층'  # 18열
jisangHeight = rowD3Spans[2].get_text().strip() + '층'  # 19열
houseCnt = rowD3Spans[3].get_text().strip() + '세대'  # 20열
juchajang = ''  # 21열
# 22-23
rowD4Spans = bs4.find('div', class_='desc-row d4').find_all('span', class_='basicInfo')
agreeDate = rowD4Spans[0].get_text().strip()  # 22열
jiyuk = rowD4Spans[1].get_text().strip()  # 23열

# 24-26
jarea = get_text_by_tag_attr('span', 'i', 'jarea')  # 24
garea = get_text_by_tag_attr('span', 'i', 'garea')  # 25
daeji = get_text_by_tag_attr('span', 'i', 'daeji') + '㎡'  # 26

# 27~30
eduDivs = bs4.find('div', class_='edu-info').find_all('div', class_='view')
# 어린이집
eduKidsList = [0,0,0,0,0]
eduKidsListIdx = 0

eduKids = ""
trs = eduDivs[0].find_all('tr')[:5]
for tr in trs:
    try:
        eduKidsList[eduKidsListIdx] = tr.find('td', class_='dist').get_text().strip()
        eduKidsListIdx += 1
        eduKids += tr.find('td', class_='dist').get_text().strip() + ','
    except:
        pass
eduKids = eduKids[:-1]


# 초등학교
eduElement = ""
eduElementList = ['','','','','','']
eduElementListIdx = 0

trs = eduDivs[1].find_all('tr')[:3]
for tr in trs:
    try:
        eduElement += tr.find('td').get_text().strip() + tr.find('td',
                                                                 class_='dist').get_text().strip() + ','
        eduElementList[eduElementListIdx] = tr.find('td').get_text().strip()
        eduElementList[eduElementListIdx+1] = tr.find('td',class_='dist').get_text().strip()
        eduElementListIdx += 2
    except:
        pass
eduElement = eduElement[:-1]

# 중고등학교
eduMiddle = ""
middleCnt = 0
eduMiddleList = ['','','','','','']
eduMiddleListIdx = 0

eduHigh = ""
highCnt = 0
eduHighList = ['','','','','','']
eduHighListIdx = 0

trs = eduDivs[2].find_all('tr')
for tr in trs:
    tmp = tr.find('td').get_text().strip()
    if '중학교' in tmp:
        if '없습니다' in tmp:
            pass
        else:
            if middleCnt == 3:
                continue
            eduMiddle += tr.find('td').get_text().strip() + tr.find_all('td')[
                -1].get_text().strip() + ','
            eduMiddleList[eduMiddleListIdx] = tr.find('td').get_text().strip()
            eduMiddleList[eduMiddleListIdx+1] = tr.find_all('td')[-1].get_text().strip()
            eduMiddleListIdx +=2
            middleCnt += 1
    elif '고등학교' in tmp:
        if '없습니다' in tmp:
            pass
        else:
            if highCnt == 3:
                continue
            eduHigh += tr.find('td').get_text().strip() + tr.find_all('td')[
                -1].get_text().strip() + ','
            eduHighList[eduHighListIdx] = tr.find('td').get_text().strip()
            eduHighList[eduHighListIdx + 1] = tr.find_all('td')[-1].get_text().strip()
            eduHighListIdx += 2
            highCnt += 1
eduHigh = eduHigh[:-1]
eduMiddle = eduMiddle[:-1]


# 31
subwayDiv = bs4.find('div', class_='subway-info').find('div', class_='view')
subwayResult = ''
subwayList = ['','','','','','','','','','']
subwayListIdx = 0


trs = subwayDiv.find_all('tr')[:5]
for tr in trs:
    subwayResult += tr.find('td').get_text().strip() + tr.find_all('td')[
        -1].get_text().strip() + ','
    subwayList[subwayListIdx] = tr.find('td').get_text().strip()
    subwayList[subwayListIdx+1] = tr.find_all('td')[-1].get_text().strip()
    subwayListIdx+=2
subwayResult = subwayResult[:-1]
print(subwayList)
# 32
averPrice = get_text_by_tag_attr('span', 'i', 'sellText') + '만원'
highPrice = get_text_by_tag_attr('span', 'i', 'sellHLText-HIGH') + '만원'
lowPrice = get_text_by_tag_attr('span', 'i', 'sellHLText-LOW') + '만원'
price = averPrice + '/' + highPrice + '/' + lowPrice
# 33
perPrice = bs4.find('div', class_='sisedesc').find('span').get_text().strip() + '만원'
# TEST
print(printStr.format(dong,gujuso,dorojuso,landCode,honame,
                      roofName,gujoName,usageMain,usageSub,tjttype,
                      daejiArea,gunmulArea,gunpaeArea,yunArea,jisangyunArea,
                      yongjukArea,height,jisangHeight,jihaHeight,houseCnt,
                        juchajang,agreeDate,jiyuk,jarea,garea,
                      daeji,eduKids,eduElement,eduMiddle,eduHigh,
                      subwayResult,price,perPrice))
save_excel(FILENAME, [dong, gujuso, dorojuso, landCode, honame,
                                      roofName, gujoName, usageMain, usageSub, tjttype,
                                      daejiArea, gunmulArea, gunpaeArea, yunArea, jisangyunArea,
                                      yongjukArea, height, jisangHeight, jihaHeight, houseCnt,
                                      juchajang, agreeDate, jiyuk, jarea, garea,
                                      daeji, eduElementList[0],eduElementList[1],eduElementList[2],eduElementList[3],
                                    eduElementList[4],eduElementList[0],eduElementList[1],eduElementList[2],eduElementList[3],
                                eduElementList[4],eduElementList[5],eduMiddleList[0],eduMiddleList[1],eduMiddleList[2],
                            eduMiddleList[3],eduMiddleList[4],eduMiddleList[5],eduHighList[0],eduHighList[1],
                            eduHighList[2],eduHighList[3],eduHighList[4],eduHighList[5],subwayList[0],
                        subwayList[1],subwayList[2],subwayList[3],subwayList[4],subwayList[5],
                        subwayList[6],subwayList[7],subwayList[8],subwayList[9],averPrice,
                      highPrice,lowPrice,perPrice], None)


          '대지권면적', '어린이집1 m','어린이집2 m','어린이집3 m','어린이집4 m',
          '어린이집5 m','초등학교1 이름','초등학교1 거리','초등학교2 이름','초등학교3 거리',
          '초등학교3 이름','초등학교3 거리','중학교1 이름','중학교1 거리','중학교2 이름',
          '중학교2 거리','중학교3 이름','중학교3 거리','고등학교1 이름','고등학교1 거리',
          '고등학교2 이름','고등학교2 거리','고등학교3 이름','고등학교3 거리','지하철1 이름',
          '지하철1 거리','지하철2 이름','지하철2 거리','지하철3 이름','지하철3 거리',
          '지하철4 이름','지하철4 거리','지하철5 이름','지하철5 거리','최근6개월 중위',
          '최근6개월 상위30%','최근6개월 하위30%',' 현재 1㎡ 당 가격']