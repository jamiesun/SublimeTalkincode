import urllib,urllib2
import logging
import traceback
import json
import sublime

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()

api_base_url = "http://127.0.0.1/api/"
langset = {"java":"java","c":"c","cpp":"c++",
           "pas":"pascal","rb":"ruby","php":"php",
           "pl":"perl","js":"javascript","sql":"sql",
           "lsp":"lisp","py":"python"}

def get_lang(ext):
    return  langset.get(ext,ext)

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
        else:
            raise Exception("error method")
        return json.loads(response.read())
    except:
        logger.error(" do_post error %s"%traceback.format_exc())
        raise

def register(username,password,email):
    params = dict(username=username,password=password,email=email)
    url = api_base_url + "register"
    return do_request(params,url,"post")

def add_code(params):
    url = api_base_url + "code/add"
    return do_request(params,url,"post")


if __name__ == "__main__":
    print do_request({"q":"python"},"http://www.google.com.hk","get")