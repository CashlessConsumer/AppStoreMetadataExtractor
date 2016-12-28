import os
import codecs
import pycurl
import json
import configparser
import csv

def getAppListAndMetadata():
	with open('../input/UPIAppList.tsv','r') as f:
		for line in f.readlines():
			getMetadata(line.split('\t')[0].split('=')[1], line.split('\t')[1].split('\n'))

def main():
	#getAppListAndMetadata()
	#ParseUsableMetadata()
	RatingsSummary()
	#PermissionListExtractor()
	#UpdateGoogleSheets()

def PermissionListExtractor():
	return

def RatingsSummary():
	with codecs.open('../RatingSummary.csv', 'w','utf-8') as csvfile:
		fieldnames = ['name', 'title', 'average', 'count', 'star_count_1', 'star_count_2', 'star_count_3', 'star_count_4', 'star_count_5']
		ratingwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
		ratingwriter.writeheader()
		for filename in os.listdir('../output/'):
			#print filename
			with open('../output/'+filename) as f:
				data = json.loads(f.read())
				developer = data["content"]["developer"]["name"]
				app_name = data["content"]["store_info"]["title"]
				average =  data["content"]["ratings"]["average"]
				ratingcount = data["content"]["ratings"]["count"]
				rating1count = data["content"]["ratings"]["star_count"]["1"]
				rating2count = data["content"]["ratings"]["star_count"]["2"]
				rating3count = data["content"]["ratings"]["star_count"]["3"]
				rating4count = data["content"]["ratings"]["star_count"]["4"]
				rating5count = data["content"]["ratings"]["star_count"]["5"]
				print(app_name,developer,average,ratingcount,rating1count,rating2count,rating3count,rating4count,rating5count)
				ratingwriter.writerow({'title':app_name,'name':developer,'average':average,'count':ratingcount,'star_count_1':rating1count,'star_count_2':rating2count,'star_count_3':rating3count,'star_count_4':rating4count,'star_count_5':rating5count})

def getMetadata(application_id,application_name):
	print('Get metadata using AppTweak')
	apptweak_base_url = 'https://api.apptweak.com/android/applications/'
	request_suffix = '.json?country=in&language=en'

	request_url = apptweak_base_url + application_id + request_suffix
	config = configparser.ConfigParser()
	config.read('config.ini')
	APPTWEAK_API_KEY = config.get('DEFAULT','APPTWEAK_API_KEY')
	c = pycurl.Curl()

	with open('../output/' + application_name + '.json', 'w') as f:
		c.setopt(pycurl.URL, request_url)
		c.setopt(pycurl.HTTPHEADER, ['X-Apptweak-Key: ' + APPTWEAK_API_KEY,'Accept: application/json'])
		c.setopt(c.WRITEFUNCTION, f.write)
		c.perform()

if __name__ == "__main__":
	main()
