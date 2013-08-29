import random, urllib2
from time import sleep

URL_list = ["facebook", "google", "youtube", "yahoo", "baidu", "wikipedia", "live", "amazon", "qq", "twitter", "taobao", "blogspot", "linkedin", "msn", "ebay", "wordpress", "bing", "vk", "babylon", "163", "weibo", "microsoft", "tumblr", "pinterest", "apple", "soso", "paypal", "tmall", "fc2", "blogger", "imdb", "ask", "sohu", "hao123", "conduit", "go", "youku", "adobe", "flickr", "avg", "ifeng"]


def main():
        while True:
		random.shuffle(URL_list)

		for URL in URL_list:
			try:
				page = urllib2.urlopen("http://" + URL + ".com")
			except (urllib2.URLError, urllib2.HTTPError), e:
				pass
			
			sleep(5)



if __name__ == '__main__':
   main()
