from bs4 import BeautifulSoup
from CONFIG import *

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
    FILENAME = "테스트.xlsx"

    dong = '논현동' # 1열 데이터
    ['동', '지번', '부번', '17자리 LAND코드', '호수',
     '지붕', '골조', '용도(주)', '용도(부)', '용도(구분)',
     '면적(대지)', '면적(건축)', '면적(건폐율)', '면적(연면적)', '면적(지상연면적)',
     '면적(용적률)', '구성(높이)', '구성(지상층수)', '구성(지하층수)', '구성(세대수)',
     '구성(주차장)', '승인(사용승인일)', '승인(지역지구)', '전용면적', '공급면적',
     '대지권면적', '교육정보(어린이집)상위5개 m만',
     '교육정보(초등학교)상위3개 학교명 및 거리', '교육정보(중학교)상위3개 학교명 및 거리',
     '교육정보(고등학교)상위3개 학교명 및 거리', '지하철 거리순 5개 역명 및 거리',
     '최근6개월 매매 시세평가액 중위/상위30%/하위30%', ' 현재 1㎡ 당 가격']
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
    
    """
    '''______________________________________'''

    # === CODE START
    # save_excel(FILENAME, None, HEADER)  # init

    # 10-14, 12-4, 11-16
    bs4 = get_bs_by_txt('10-14.txt') # init

    gujuso = get_text_by_tag_attr('span','c','gujuso')          # 2열
    dorojuso = get_text_by_tag_attr('span','c','dorojuso')      # 3열
    landCode = '' # 4열
    honame = get_text_by_tag_attr('span','i','honame') + '(호)'    # 5열
    roofName = get_text_by_tag_attr('span','i','roofName')      # 6열
    gujoName = get_text_by_tag_attr('span','i','gujoName')      # 7열

    # 8-9-10
    rowD1Spans = bs4.find('div',class_='desc-row d1').find_all('span',class_='basicInfo')
    usageMain = rowD1Spans[0].get_text().strip() # 8열
    usageSub = rowD1Spans[1].get_text().strip()  # 9열
    tjttype = get_text_by_tag_attr('span','i','tjttype') # 10열

    # 11 ~ 16
    rowD2Spans = bs4.find('div',class_='desc-row d2').find_all('span',class_='basicInfo')
    daejiArea = rowD2Spans[0].get_text().strip()+'㎡' # 11열
    gunmulArea = rowD2Spans[1].get_text().strip()+'㎡' # 12열
    gunpaeArea = rowD2Spans[2].get_text().strip()+'%' # 13열
    yunArea = rowD2Spans[3].get_text().strip()+'㎡'  # 14열
    jisangyunArea = rowD2Spans[4].get_text().strip()+'㎡' # 15열
    yongjukArea = rowD2Spans[5].get_text().strip()+'%' # 16열

    # 17 - 21






    # TEST
    print(printStr.format(dong,gujuso,dorojuso,landCode,honame,
                          roofName,gujoName,usageMain,usageSub,tjttype,
                          daejiArea,gunmulArea,gunpaeArea,yunArea,jisangyunArea,
                          yongjukArea))
