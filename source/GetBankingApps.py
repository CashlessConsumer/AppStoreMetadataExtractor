import urllib2
from bs4 import BeautifulSoup

def GetAppsByDeveloper(developer):
	global applist
	applist = []
	dev_id_url = 'https://play.google.com/store/apps/developer?id='
	#url = dev_id_url + 'State+Bank+of+India';
	#url = dev_id_url + 'ICICI+Bank+Ltd.';

	url = dev_id_url + developer

	doc = urllib2.urlopen(url)
	soup = BeautifulSoup(doc, 'html.parser')
	apps = soup.find_all("a","card-click-target")


	for app in apps:
		if app.get('href').split('id=')[1] not in applist:
			applist.append(app.get('href').split('id=')[1])
	print '\n'.join(applist)

def GetDeveloper(appname):
	print appname
	doc = urllib2.urlopen('https://play.google.com/store/apps/details?id='+appname)
	soup = BeautifulSoup(doc, 'html.parser')
	return soup.find_all("a","document-subtitle primary")[0].find('span').contents[0].replace(' ','+')

def GetUPIDevelopers():
	#GetListofUniqueDevelopers
	#GetListofEachApp
	with open('../input/UPIAppList.tsv','r') as f:
		for line in f.readlines():
			developer = GetDeveloper(line.split('\t')[0].split('=')[1])
			GetAppsByDeveloper(developer)
	return

if __name__ == "__main__":
	GetUPIDevelopers()
