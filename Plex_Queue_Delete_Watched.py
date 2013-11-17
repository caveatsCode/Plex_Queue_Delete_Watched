import cgi
import requests
from lxml import etree

def get_auth_token(page):
	tree = etree.HTML(page.text)
	auth_token = tree.find(".//meta[@name='csrf-token']").attrib['content']
	return auth_token

#request username and password via command line prompt
username = raw_input('Username: ')
password = raw_input('Password: ')
#define a session to preserve cookies
s = requests.session()
#open the login page and get the unique authenticity token
page = s.get("https://my.plexapp.com/users/sign_in")
auth_token = get_auth_token(page)
escaped_auth_token = cgi.escape(auth_token)
#login
login_details = "utf8=%E2%9C%93&authenticity_token=" + cgi.escape(auth_token) \
                + "&user%5Blogin%5D=" + cgi.escape(username) \
                + "&user%5Bpassword%5D=" + cgi.escape(password) \
                + "&user%5Bremember_me%5D=0&user%5Bremember_me%5D=1&commit=Sign+in"
login = s.post("https://my.plexapp.com/users/sign_in", data=login_details)
#goto the page of interest
page = s.get("https://my.plexapp.com/queue/watched")
#parse the page to find the id of each watched video
tree = etree.HTML(page.text)
for item in tree.findall(".//span[@class='delete']/a"):
	url = "https://my.plexapp.com"
	url += item.attrib['href']
	#include auth token with headers for the DELETE request
	auth_token = get_auth_token(page)
	headers = {'X-CSRF-Token': auth_token}
	print url
	r = s.delete(url, headers = headers)
	if r.status_code == requests.codes.ok:
		print 'Deleted'
	else:
		print 'Unable to delete (HTTP Status Code = ' + str(r.status_code) + ')'