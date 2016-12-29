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
	ParseUsableMetadata()
	#RatingsSummary()
	#PermissionListExtractor()
	#UpdateGoogleSheets()

def ParseUsableMetadata():
	with codecs.open('../MetadataSummary.csv', 'w','utf-8') as csvfile:
		fieldnames = ['Title','Name','Developer Email','Developer Website','App Size', 'App version', 'Last Release date']
		metadatawriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
		metadatawriter.writeheader()
		for filename in os.listdir('../output/'):
			with open('../output/'+filename) as f:
				data = json.loads(f.read())
				title = data["content"]["store_info"]["title"]
				dev_name = data["content"]["developer"]["name"]
				dev_email = data["content"]["developer"]["email"]
				dev_site = data["content"]["developer"]["website"]
				app_size = data["content"]["store_info"]["size"]["current"]["data"] / (1024 * 1024)
				app_version = data["content"]["store_info"]["versions"][0]["version"]
				app_release_date = data["content"]["store_info"]["versions"][0]["release_date"]

				metadatawriter.writerow({'Title':title,'Name':dev_name,'Developer Email':dev_email, 'Developer Website':dev_site, 'App Size':app_size, 'App version' : app_version, 'Last Release date':app_release_date})
	return

def PermissionListExtractor():
	with codecs.open('../PermissionSummary.csv', 'w','utf-8') as csvfile:
		fieldnames = ['title','count','permission']
		permissionwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
		permissionwriter.writeheader()
		for filename in os.listdir('../output/'):
			with open('../output/'+filename) as f:
				data = json.loads(f.read())
				title = data["content"]["store_info"]["title"]
				permissions = data["content"]["store_info"]['permissions']
				permissionwriter.writerow({'title':title,'count':len(permissions),'permission':','.join(permissions)})
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
