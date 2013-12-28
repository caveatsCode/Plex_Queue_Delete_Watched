#utilizes plex api with basic authentication to delete all watched videos in plex queue

import requests
from requests.auth import HTTPBasicAuth
from lxml import etree

#request username and password via command line prompt
username = raw_input('Username: ')
password = raw_input('Password: ')
#goto the page of interest
page = requests.get("https://plex.tv/pms/playlists/queue/watched", auth=HTTPBasicAuth(username, password))
#parse the page to find the id of each watched video
tree = etree.XML(page.content)
for item in tree.findall(".//Video"):
	url = "https://plex.tv/pms/playlists/queue/items/"
	url += item.attrib['id']
	print url
	r = requests.delete(url, auth=HTTPBasicAuth(username, password))
	if r.status_code == requests.codes.ok:
		print 'Deleted'
	else:
		print 'Unable to delete (HTTP Status Code = ' + str(r.status_code) + ')'