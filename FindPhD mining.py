import os, requests ,csv ,time ,urllib.parse, urllib3
from bs4 import BeautifulSoup 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

date = datetime.today().strftime('%d-%m-%Y')
URLm = urllib3(os.getenv('WEB_SITE'))
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}

csv_name = os.getenv('CSV_OUTPUT_NAME')
csv_file = open(csv_name+'.csv', 'a', newline='', encoding='utf-8')
csv_writer=csv.writer(csv_file, delimiter=',')
csv_writer.writerow(['Page',' ','-','-','-'])

def subref(url):
	pageSub = requests.get(url, headers=headers)
	soupSub = BeautifulSoup(pageSub.content, 'lxml')
	mainDesc = soupSub.find("div",{"class":"phd-sections__content"}).text
	mainLink = soupSub.find("div",{"class":"col-xs-8 d-inline-block phd-sidebar__buttons--minor tight-left"})
	mainLink = mainLink.a.get('href')
	mainLink=mainLink.split('url=')
	mainLink=mainLink[1]
	mp = urllib.parse.unquote(mainLink)
	return([mainDesc,mp])

ulikns =[]
minn = 1# +3
maxx = 3
for i in range(minn, maxx):
	sURL = URLm + str(i)
	page = requests.get(sURL, headers=headers)
	soup = BeautifulSoup(page.content, 'lxml')
	match = soup.find("div",{"class":"search-results"})

	for m in match.findAll("div",class_="resultsRow phd-result-row-standard phd-result col-xs-24 tight"):
		title = m.findAll("a",{"class":"courseLink phd-result__title"})
		for t in title:
			t=t.get_text()
		desc = m.findAll("div",{"class":"descFrag"})
		for d in desc:
			d=d.text
		linkM = m.findAll("div",{"class":"descFrag"})
		for lM in linkM:
			time.sleep(2)

			lM= os.getenv('BASE_URL')+lM.a.get('href')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
			pageSub = requests.get(lM, headers=headers)
			soupSub = BeautifulSoup(pageSub.content, 'lxml')
			mainDesc = soupSub.find("div",{"class":"phd-sections__content"})
			if mainDesc is not None:
				mainDesc = soupSub.find("div",{"class":"phd-sections__content"}).text.strip()
			else:
				mainDesc ='Empty'

			mainLink = soupSub.find("div",{"class":"col-xs-8 d-inline-block phd-sidebar__buttons--minor tight-left"})
			if mainLink is not None:
				mainLink = soupSub.find("div",{"class":"col-xs-8 d-inline-block phd-sidebar__buttons--minor tight-left"})
				mainLink = mainLink.a.get('href')
				mainLink=mainLink.split('url=')
				mainLink=mainLink[1]
				mp = urllib.parse.unquote(mainLink)
			else:
				mp ='Empty'

		fund = m.findAll("a",{"class":"hoverTitle funding-type-option phd-result__key-info"})
		for f in fund:
			f=f.text
		csv_writer.writerow([date,t,d,lM,f,mainDesc,mp])
csv_file.close()
print()
print('---------------------------------------Scrapig completed---------------------------------------')
print('-Saved as: '+csv_name)
print('-CURRENT Min: '+str(minn)+' & Max: '+str(maxx))
print('-NEXT Min: '+str(maxx +1)+' & Max: '+str(maxx+3))
 