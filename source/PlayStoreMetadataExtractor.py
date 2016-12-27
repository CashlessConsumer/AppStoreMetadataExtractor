import os
import pycurl
import json
import configparser
import pprint

def getAppListAndMetadata():
	with open('../input/UPIAppList.tsv','r') as f:
		for line in f.readlines():
			getMetadata(line.split('\t')[0].split('=')[1], line.split('\t')[1])

def main():
	#getAppListAndMetadata()
	#ParseUsableMetadata()
	PermissionListExtractor()
	#UpdateGoogleSheets()

def PermissionListExtractor():
	for filename in os.listdir('../output/'):
		print filename
		with open('../output/'+filename) as f:
			data = json.loads(f.read())
			#print data['content']
			pprint(data['content']["developer"]["name"])
			pprint(data['content']["ratings"]["average"])

def getMetadata(application_id,application_name):
	print 'Get metadata using AppTweak'
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
