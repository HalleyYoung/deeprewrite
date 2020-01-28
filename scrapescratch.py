import urllib.parse as urlparse
from bs4 import BeautifulSoup
import urllib
import re

def getDomain(url):
	splits = url.split("/")
	if len(splits) < 3:
		return False
	return url.split("/")[2]

start_urls = ["https://www.vgmusic.com/music/console/", "http://midkar.com/", "http://hindimidipalace.tripod.com/index.html", "https://www.cse.iitk.ac.in/users/tvp/music/", "http://www.iskandar.com/joseph/arabicmusiclist.html", "http://arabicmidipalace.tripod.com/index.html", "https://freemidi.org/"]
allowed_domains = list(map(getDomain, start_urls))#["http://www.legco.gov.hk/general/chinese/counmtg/yr04-08/mtg_0708.htm#hansard"]


files = {}

domains = []
urls_parsed = []
url_queue = set(start_urls)
fnames = set([])



while len(url_queue) > 0:
	html_domain = url_queue.pop()
	urls_parsed.append(html_domain)
	try:
		html_page = urllib.request.urlopen(html_domain)
	except:
		continue
	soup = BeautifulSoup(html_page)
	for link in soup.findAll('a'):
		current_link = urlparse.urljoin(html_domain,link.get('href')).replace(" ", "_")		
		if current_link.endswith(".midi") or current_link.endswith(".mid") or current_link.endswith(".zip"):
			print("I have link: " + current_link)
			fname = current_link.split("/")[2] + "-" + current_link.split("/")[-1]
			if fname not in fnames:
				try:
					res = urllib.request.urlopen(current_link)
					pdf = open("/Users/halley/Documents/midi/" + fname, 'wb')
					pdf.write(res.read())
					pdf.close()
					fnames.add(fname)
				except:
					pass
		else:
			new_page = urlparse.urljoin(html_domain,link.get('href'))
			if getDomain(new_page) in allowed_domains and new_page not in urls_parsed and new_page not in url_queue:
				url_queue.add(new_page)
	print(len(fnames))



"""


start_urls = ["https://freemidi.org/"]#["https://www.vgmusic.com/music/console/", "http://midkar.com/", "http://hindimidipalace.tripod.com/index.html", "https://www.cse.iitk.ac.in/users/tvp/music/", "http://www.iskandar.com/joseph/arabicmusiclist.html", "http://arabicmidipalace.tripod.com/index.html", "https://freemidi.org/"]
allowed_domains = list(map(getDomain, start_urls))#["http://www.legco.gov.hk/general/chinese/counmtg/yr04-08/mtg_0708.htm#hansard"]

urls_parsed = []
"""