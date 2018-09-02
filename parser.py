from bs4 import BeautifulSoup
from selenium import webdriver
from CONFIG import *
import time

def get_bs_by_txt(_FILENAME):
    with open(_FILENAME,'r',encoding='utf8') as f:
        return BeautifulSoup(f.read(),'lxml')

def get_text_by_tag_attr(_tag,_attr,_value):
    if _attr == 'i':
        return bs4.find(_tag,id=_value).get_text().strip()
    elif _attr == 'c':
        return bs4.find(_tag, class_=_value).get_text().strip()

if __name__ == "__main__":
    '''_______________ CONFIG _______________'''
    dong = input(">>> 동 이름을 입력하세요 : ")  # 1열 데이터
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    driver.get('https://www.lobig.co.kr/new/housing#')
    tt = input(">>> 로그인후 준비가돼면 말해주세요 : ")
    FILENAME = dong+".xlsx"
    f = open(dong+'.txt','r',encoding='utf8')
    lines = f.readlines()
    printStr =\
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
    '''______________________________________'''

    # === CODE START
    save_excel(FILENAME, None, HEADER)  # init

    # 10-14, 12-4, 11-16,
    # 초등많 26-11
    for line in lines:
        driver.find_element_by_xpath('//*[@id="bunji"]').clear()
        driver.find_element_by_xpath('//*[@id="bunji"]').send_keys(line.strip())
        time.sleep(1)
        while True:
            try:
                driver.find_element_by_xpath('//*[@id="btn-addrSearch"]').click()
                break
            except:
                time.sleep(0.5)
        while True:
            try:
                driver.find_element_by_xpath('/html/body/div[6]').click()
                if 'visibility: visible;' in driver.find_element_by_xpath('//*[@id="roadviewBox"]').get_attribute('style'):
                    whileidx = 1
                    while True:
                        whileidx += 1
                        if whileidx == 10:
                            break
                        try:
                            driver.find_element_by_xpath('//*[@id="roadviewBox"]/div[2]').click()
                            print("로드뷰끔")
                            print('반복1')
                            break
                        except:
                            time.sleep(1)
                break
            except:
                time.sleep(0.5)
        time.sleep(1)
        log('i', "현재 {} {} 진행중 ".format(dong, line.strip()))
        saveCnt = 0
        #
        while True:
            while True:
                try:
                    driver.find_element_by_xpath('/html/body/div[6]').click()
                    if 'visibility: visible;' in driver.find_element_by_xpath('//*[@id="roadviewBox"]').get_attribute(
                            'style'):
                        whileidx = 1
                        while True:
                            whileidx += 1
                            if whileidx == 10:
                                break
                            try:
                                driver.find_element_by_xpath('//*[@id="roadviewBox"]/div[2]').click()
                                print("로드뷰끔")
                                print('반복2')
                                break
                            except:
                                time.sleep(1)
                    break
                except:
                    time.sleep(0.5)
            bs4 = BeautifulSoup(driver.page_source, 'lxml')
            divs = bs4.find_all('div', class_='floor-number')
            floors = driver.find_elements_by_class_name('floor-number')

            for idx in range(len(divs)):
                foridx = 0
                while True:
                    try:
                        floors[idx].get_attribute('class') == 'floor-number' and floors[idx].get_attribute(
                            'style') != 'color: rgb(158, 158, 158);'
                    except:
                        print("페이지 안붙어서 쉰다.")
                        qwe = input(">>> 준비돼면 엔터눌러주세요 ::")
                        floors = driver.find_elements_by_class_name('floor-number')
                        if 'right: 0px' in driver.find_element_by_xpath('/html/body/div[6]').get_attribute('style'):
                            print('들어가있어서 클릭해준다')
                            time.sleep(2)
                            driver.find_element_by_xpath('/html/body/div[6]').click()
                        time.sleep(1)
                    try:
                        print("진입1")
                        foridx +=1
                        if foridx == 60:
                            break
                        if floors[idx].get_attribute('class') == 'floor-number' and floors[idx].get_attribute('style') != 'color: rgb(158, 158, 158);':
                            print("진입2")
                            floors[idx].click()
                            print("진입3")
                            time.sleep(0.5)
                            bs4 = BeautifulSoup(driver.page_source, 'lxml')
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
                            eduKidsList = [0, 0, 0, 0, 0]
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
                            eduElementList = ['', '', '', '', '', '']
                            eduElementListIdx = 0

                            trs = eduDivs[1].find_all('tr')[:3]
                            for tr in trs:
                                try:
                                    eduElement += tr.find('td').get_text().strip() + tr.find('td',
                                                                                             class_='dist').get_text().strip() + ','
                                    eduElementList[eduElementListIdx] = tr.find('td').get_text().strip()
                                    eduElementList[eduElementListIdx + 1] = tr.find('td',
                                                                                    class_='dist').get_text().strip()
                                    eduElementListIdx += 2
                                except:
                                    pass
                            eduElement = eduElement[:-1]

                            # 중고등학교
                            eduMiddle = ""
                            middleCnt = 0
                            eduMiddleList = ['', '', '', '', '', '']
                            eduMiddleListIdx = 0

                            eduHigh = ""
                            highCnt = 0
                            eduHighList = ['', '', '', '', '', '']
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
                                        eduMiddleList[eduMiddleListIdx + 1] = tr.find_all('td')[-1].get_text().strip()
                                        eduMiddleListIdx += 2
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
                            subwayList = ['', '', '', '', '', '', '', '', '', '']
                            subwayListIdx = 0

                            trs = subwayDiv.find_all('tr')[:5]
                            for tr in trs:
                                subwayResult += tr.find('td').get_text().strip() + tr.find_all('td')[
                                    -1].get_text().strip() + ','
                                subwayList[subwayListIdx] = tr.find('td').get_text().strip()
                                subwayList[subwayListIdx + 1] = tr.find_all('td')[-1].get_text().strip()
                                subwayListIdx += 2
                            subwayResult = subwayResult[:-1]
                            #print(subwayList)
                            # 32
                            averPrice = get_text_by_tag_attr('span', 'i', 'sellText') + '만원'
                            highPrice = get_text_by_tag_attr('span', 'i', 'sellHLText-HIGH') + '만원'
                            lowPrice = get_text_by_tag_attr('span', 'i', 'sellHLText-LOW') + '만원'
                            price = averPrice + '/' + highPrice + '/' + lowPrice
                            # 33
                            perPrice = bs4.find('div', class_='sisedesc').find('span').get_text().strip() + '만원'
                            # TEST
                            """
                            print(printStr.format(dong,gujuso,dorojuso,landCode,honame,
                                                  roofName,gujoName,usageMain,usageSub,tjttype,
                                                  daejiArea,gunmulArea,gunpaeArea,yunArea,jisangyunArea,
                                                  yongjukArea,height,jisangHeight,jihaHeight,houseCnt,
                                                    juchajang,agreeDate,jiyuk,jarea,garea,
                                                  daeji,eduKids,eduElement,eduMiddle,eduHigh,
                                                  subwayResult,price,perPrice))
                            print("_"*70)
                            """
                            save_excel(FILENAME, [dong, gujuso, dorojuso, landCode, honame,
                                                  roofName, gujoName, usageMain, usageSub, tjttype,
                                                  daejiArea, gunmulArea, gunpaeArea, yunArea, jisangyunArea,
                                                  yongjukArea, height, jisangHeight, jihaHeight, houseCnt,
                                                  juchajang, agreeDate, jiyuk, jarea, garea,
                                                  daeji, eduKidsList[0], eduKidsList[1], eduKidsList[2],
                                                  eduKidsList[3],
                                                  eduKidsList[4], eduElementList[0], eduElementList[1],
                                                  eduElementList[2],
                                                  eduElementList[3],
                                                  eduElementList[4], eduElementList[5], eduMiddleList[0],
                                                  eduMiddleList[1],
                                                  eduMiddleList[2],
                                                  eduMiddleList[3], eduMiddleList[4], eduMiddleList[5], eduHighList[0],
                                                  eduHighList[1],
                                                  eduHighList[2], eduHighList[3], eduHighList[4], eduHighList[5],
                                                  subwayList[0],
                                                  subwayList[1], subwayList[2], subwayList[3], subwayList[4],
                                                  subwayList[5],
                                                  subwayList[6], subwayList[7], subwayList[8], subwayList[9], averPrice,
                                                  highPrice, lowPrice, perPrice], None)
                            saveCnt+=1
                        break
                    except:
                        while True:
                            try:
                                driver.find_element_by_xpath('/html/body/div[6]').click()
                                print("반복3")
                                time.sleep(1)
                                break
                            except:
                                time.sleep(0.5)
            if saveCnt == 0:

                print("ㄱ")
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
                eduKidsList = [0, 0, 0, 0, 0]
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
                eduElementList = ['', '', '', '', '', '']
                eduElementListIdx = 0

                trs = eduDivs[1].find_all('tr')[:3]
                for tr in trs:
                    try:
                        eduElement += tr.find('td').get_text().strip() + tr.find('td',
                                                                                 class_='dist').get_text().strip() + ','
                        eduElementList[eduElementListIdx] = tr.find('td').get_text().strip()
                        eduElementList[eduElementListIdx + 1] = tr.find('td', class_='dist').get_text().strip()
                        eduElementListIdx += 2
                    except:
                        pass
                eduElement = eduElement[:-1]

                # 중고등학교
                eduMiddle = ""
                middleCnt = 0
                eduMiddleList = ['', '', '', '', '', '']
                eduMiddleListIdx = 0

                eduHigh = ""
                highCnt = 0
                eduHighList = ['', '', '', '', '', '']
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
                            eduMiddleList[eduMiddleListIdx + 1] = tr.find_all('td')[-1].get_text().strip()
                            eduMiddleListIdx += 2
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
                subwayList = ['', '', '', '', '', '', '', '', '', '']
                subwayListIdx = 0

                trs = subwayDiv.find_all('tr')[:5]
                for tr in trs:
                    subwayResult += tr.find('td').get_text().strip() + tr.find_all('td')[
                        -1].get_text().strip() + ','
                    subwayList[subwayListIdx] = tr.find('td').get_text().strip()
                    subwayList[subwayListIdx + 1] = tr.find_all('td')[-1].get_text().strip()
                    subwayListIdx += 2
                subwayResult = subwayResult[:-1]
                #print(subwayList)
                # 32
                averPrice = get_text_by_tag_attr('span', 'i', 'sellText') + '만원'
                highPrice = get_text_by_tag_attr('span', 'i', 'sellHLText-HIGH') + '만원'
                lowPrice = get_text_by_tag_attr('span', 'i', 'sellHLText-LOW') + '만원'
                price = averPrice + '/' + highPrice + '/' + lowPrice
                # 33
                perPrice = bs4.find('div', class_='sisedesc').find('span').get_text().strip() + '만원'
                # TEST
                """
                print(printStr.format(dong,gujuso,dorojuso,landCode,honame,
                                      roofName,gujoName,usageMain,usageSub,tjttype,
                                      daejiArea,gunmulArea,gunpaeArea,yunArea,jisangyunArea,
                                      yongjukArea,height,jisangHeight,jihaHeight,houseCnt,
                                        juchajang,agreeDate,jiyuk,jarea,garea,
                                      daeji,eduKids,eduElement,eduMiddle,eduHigh,
                                      subwayResult,price,perPrice))
                print("_"*70)
                """
                save_excel(FILENAME, [dong, gujuso, dorojuso, landCode, honame,
                                      roofName, gujoName, usageMain, usageSub, tjttype,
                                      daejiArea, gunmulArea, gunpaeArea, yunArea, jisangyunArea,
                                      yongjukArea, height, jisangHeight, jihaHeight, houseCnt,
                                      juchajang, agreeDate, jiyuk, jarea, garea,
                                      daeji, eduKidsList[0], eduKidsList[1], eduKidsList[2], eduKidsList[3],
                                      eduKidsList[4], eduElementList[0], eduElementList[1], eduElementList[2],
                                      eduElementList[3],
                                      eduElementList[4], eduElementList[5], eduMiddleList[0], eduMiddleList[1],
                                      eduMiddleList[2],
                                      eduMiddleList[3], eduMiddleList[4], eduMiddleList[5], eduHighList[0],
                                      eduHighList[1],
                                      eduHighList[2], eduHighList[3], eduHighList[4], eduHighList[5], subwayList[0],
                                      subwayList[1], subwayList[2], subwayList[3], subwayList[4], subwayList[5],
                                      subwayList[6], subwayList[7], subwayList[8], subwayList[9], averPrice,
                                      highPrice, lowPrice, perPrice], None)
                saveCnt += 1

            if bs4.find('div', class_='arrow right on') != None:
                while True:
                    try:
                        driver.find_element_by_xpath('//*[@id="nextHoBtn"]').click()
                        break
                    except:
                        while True:
                            try:
                                driver.find_element_by_xpath('/html/body/div[6]').click()
                                if 'visibility: visible;' in driver.find_element_by_xpath(
                                        '//*[@id="roadviewBox"]').get_attribute('style'):
                                    whileidx = 1
                                    while True:
                                        whileidx += 1
                                        if whileidx == 10:
                                            break
                                        try:
                                            driver.find_element_by_xpath('//*[@id="roadviewBox"]/div[2]').click()
                                            print("로드뷰끔")
                                            print('반복4')
                                            break
                                        except:
                                            time.sleep(1)
                                break
                            except:
                                time.sleep(0.5)
                while True:
                    try:
                        driver.find_element_by_xpath('/html/body/div[6]').click()
                        if 'visibility: visible;' in driver.find_element_by_xpath(
                                '//*[@id="roadviewBox"]').get_attribute('style'):
                            whileidx = 1
                            while True:
                                whileidx +=1
                                if whileidx == 10:
                                    break
                                try:
                                    driver.find_element_by_xpath('//*[@id="roadviewBox"]/div[2]').click()
                                    print("로드뷰끔")
                                    print('반복5')
                                    break
                                except:
                                    time.sleep(1)
                        break
                    except:
                        time.sleep(0.5)
            else:
                break


    driver.quit()
    f.close()