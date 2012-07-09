import urllib,urllib2
import logging
import traceback
import json

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()


def do_request(params,url,method="get"):
    logger.info( "post request, please wait......")
    try:
        data = urllib.urlencode(params) 
        if method == "post":
            request = urllib2.Request(url, data)
            response = urllib2.urlopen(request)   
        elif method == "get":
            request = urllib2.Request("%s?%s"%(url,data))
            response = urllib2.urlopen(request)  
        return json.oads(response.read())
    except:
        logger.error(" do_post error %s"%traceback.format_exc())
        raise



if __name__ == "__main__":
    print do_request({"q":"python"},"http://www.google.com.hk","get")