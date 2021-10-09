import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import date, timedelta,datetime

def main_crawler(query,s_date, e_date, news_office, maxpage, sort, printed):
    print(s_date, e_date)
    y,m,d = s_date.split(".")
    ey,em,ed = e_date.split(".")
    today = datetime(int(y),int(m),int(d))
    endday = datetime(int(ey),int(em),int(ed))
    file_path = "./" + query.replace(" ","_")  + '.csv'
    # f = open(file_path, 'a', encoding='utf-8', newline='')
    # wr=csv.writer(f)
    # wr.writerow(["날짜","기자","신문사","제목","내용","댓글갯수","댓글내용","기사_주소"])
    #print(s_date, endday)

    while today <endday:
        #print(s_date)
        y,m,d = s_date.split(".")
        first_date = "%s%s%s000000"%(y,m,d)
        crawler(query, first_date, first_date, news_office, maxpage, sort, printed, wr)
        today = datetime(int(y),int(m),int(d))
        next_day = today + timedelta(days=1)
        ny, nm, nd = next_day.year,next_day.month,next_day.day
        s_date = "%s.%02d.%02d"%(ny,int(nm),int(nd))    
        #print(s_date)
    #f.close()

def crawler(query, s_date, e_date, pcompany, maxpage, sort, printed, wr):
    pre_article = ""
    article = ""
    page =1
    while page < maxpage:
        url = "https://search.daum.net/search?w=news&DA=STC&enc=utf8&cluster=y&cluster_page=1&q=" + \
        query + "&cp=1643iWOgL7_L3uY84L,16GnI7O0bgWGPu8g3q,166uA3-wXI9pkYJd1q,16NFZtGOil_tXN93-m&cpname=" + \
        pcompany + "&p="+str(page)+"&period=u&sd="+sdate+ "&ed="+edate+"&sort=old"
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            }
        req = requests.get(url,headers=header)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')
        if soup.select("#noResult > div > strong"):
            break
        news_tit  =soup.select("a.tit_main.fn_tit_u")
        for news_number, urls in enumerate(news_tit):
            article=urls['href']
            print(article,pre_article,news_number)
            if (news_number == 0 and pre_article == article):
                break
            elif news_number == 0 and pre_article != article:
                pre_article = article
            pcompany = soup.select("span.f_nb")[news_number*2].text
            pdate = soup.select("span.f_nb")[news_number*2+1].text
            
            news_detail = newscompany_crwal(article,pcompany, pdate)
            wr.writerow(news_detail)
        page+=1

def newscompany_crwal(article, pcompany, pdate):
  if pcompany == "기독교한국신문":
    return cpbc_news(article, pcompany, pdate)
  elif pcompany == "기독신문":
    return kidok(article, pcompany, pdate)
  elif pcompany == "기독연합신문":
    return igoodnews(article, pcompany, pdate)    
  elif pcompany == "기독인뉴스":
    return kidokin(article, pcompany, pdate)    
  elif pcompany == "크리스천투데이":
    return christiantoday(article, pcompany, pdate)         

def igoodnews(article, pcompany, pdate): 
    news_detail = [] 
    #print(article) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    news_detail.append(pdate) 

    # 기자 파싱
    journalist = bsoup.select("#user-container > div.float-center.max-width-1080 > header > section > div > ul > li:nth-of-type(1)")[0].text.strip()
    news_detail.append(journalist) 

    # 신문사 크롤링
    news_detail.append(pcompany) 

    # 제목 파싱 
    title = bsoup.select("div.article-head-title")[0].text
    news_detail.append(title) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select("#article-view-content-div")[0].text.strip().replace('\n', "") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip()) 
    news_detail.append(article)  

    return news_detail


def kidokin(article, pcompany, pdate): 
    news_detail = [] 
    #print(article) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    news_detail.append(pdate) 

    # 기자 파싱(신문사에서 기자이름을 기독인기자로 제공중...)
    journalist = "기독인기자"
    news_detail.append(journalist) 

    # 신문사 크롤링
    news_detail.append(pcompany) 

    # 제목 파싱 
    title = bsoup.select("#menuPos > table:nth-of-type(8) > tbody > tr > td:nth-of-type(2) > table > tbody > tr > td > div.sub_top_article_24px")[0].text
    subtitle = bsoup.select("#menuPos > table:nth-child(8) > tbody > tr > td:nth-child(2) > table > tbody > tr > td > div.normal_15px_bold")[0].text
    news_detail.append(title+" "+subtitle) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select("#menuPos > table:nth-of-type(8) > tbody > tr > td:nth-of-type(2) > table > tbody > tr > td > div:nth-of-type(5) > table")[0].text.strip().replace('\n', "") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip()) 
    news_detail.append(article)  

    return news_detail


def cknews(article, pcompany, pdate): 
    news_detail = [] 
    #print(article) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    news_detail.append(pdate) 

    # 기자 파싱
    journalist = bsoup.select("#article-view > header > div > div > ul > li.press > em.name")[0].text.strip()
    news_detail.append(journalist) 

    # 신문사 크롤링
    news_detail.append(pcompany) 

    # 제목 파싱 
    title = bsoup.select("#article-view > header > div > h3")[0].text
    news_detail.append(title) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select("#article-view-content-div")[0].text.strip().replace('\n', "") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip()) 
    news_detail.append(article)  

    return news_detail


def kidok(article, pcompany, pdate): 
    news_detail = [] 
    #print(article) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    news_detail.append(pdate) 

    # 기자 파싱
    journalist = bsoup.select("#user-container > div.view-default3.float-center.max-width-1200 > header > section > div.info-text > ul > li:nth-of-child(1)")[0].text.strip()
    news_detail.append(journalist) 

    # 신문사 크롤링
    news_detail.append(pcompany) 

    # 제목 파싱 
    title = bsoup.select("div.article-head-title")[0].text
    news_detail.append(title) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select("#article-view-content-div")[0].text.strip().replace('\n', "") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip()) 
    news_detail.append(article)  

    return news_detail

def christiantoday(article, pcompany, pdate): 
    news_detail = [] 
    #print(article) 
    headers = {'User-Agent':'Chrome/66.0.3359.181'}
    req = urllib.request.Request(article, headers=headers)
    source_code_from_URL = urllib.request.urlopen(req)
    bsoup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

    # 날짜 파싱
    news_detail.append(pdate) 

    # 기자 파싱
    journalist = bsoup.select("body > div.container-fluid > main > header > div > div.col-sm-8 > div > a:nth-of-type(1)")[0].text.strip()
    news_detail.append(journalist) 

    # 신문사 크롤링
    news_detail.append(pcompany) 

    # 제목 파싱 
    title = bsoup.select("body > div.container-fluid > main > header > div > div.col-sm-8 > h1")[0].text
    news_detail.append(title) 
    
    # 기사 본문 크롤링 
    _text = bsoup.select("body > div.container-fluid > main > div > div.col-l.col-sm-7.col-md-8 > div > article > div.article-body.clearfix")[0].text.strip().replace('\n', "") 
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "") 
    btext = btext.replace('\r', " ")
    btext = btext.replace('\t', " ")
    btext = re.sub('[a-zA-Z]', '', btext)
    btext = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', btext)
    btext = btext.replace('본문 내용    플레이어     플레이어     오류를 우회하기 위한 함수 추가', '')
    btext = btext.replace('정보공유 라이선스 20영리금지', '')
    news_detail.append(btext.strip())
    news_detail.append(article)  

    return news_detail
