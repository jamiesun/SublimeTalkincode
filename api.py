import urllib,urllib2
import json

api_base_url = "http://127.0.0.1/api/"
langset = {"java":"java","c":"c","cpp":"c++",
           "pas":"pascal","rb":"ruby","php":"php",
           "pl":"perl","js":"javascript","sql":"sql",
           "lsp":"lisp","py":"python",'css':'css','html':'html'}
langextset = {'c': 'c', 'java': 'java', 'lisp': 'lsp', 
              'javascript': 'js', 'c++': 'cpp', 'perl': 'pl',
               'python': 'py', 'pascal': 'pas', 'sql': 'sql',
                'php': 'php', 'ruby': 'rb','css':'css','html':'html'}


def get_lang(ext):
    return  langset.get(ext,ext)

def get_lang_ext(lang):
    return langextset.get(lang,lang)


def open_homepage():
    import webbrowser
    webbrowser.open("http://www.talkincode.org")
        


def do_request(params,url,method="get"):
    try:
        data = urllib.urlencode(params) 
        if method == "post":
            request = urllib2.Request(url, data)
            response = urllib2.urlopen(request)   
        elif method == "get":
            request = urllib2.Request("%s?%s"%(url,data))
            response = urllib2.urlopen(request)  
        else:
            raise Exception("Method not allowed")
        return json.loads(response.read())
    except:
        raise

def get_groups():
    url = api_base_url + "groups"
    return do_request({},url,"get")

def register(username,password,email):
    params = dict(username=username,password=password,email=email)
    url = api_base_url + "register"
    return do_request(params,url,"post")

def add_code(params):
    url = api_base_url + "code/add"
    return do_request(params,url,"post")

def get_code(uid):
    url = api_base_url + "code/get/%s"%uid
    return do_request({},url,"get")

def add_post(params):
    url = api_base_url + "post/add"
    return do_request(params,url,"post")

def add_post_comment(params):
    url = api_base_url + "comment/add"
    return do_request(params,url,"post")    

def get_post(uid):
    url = api_base_url + "post/get/%s"%uid
    return do_request({},url,"get")    

def list_codes(q,limit=100):
    params = dict(q=q,limit=limit)
    url = api_base_url + "code/index"
    return do_request(params,url,"get")

def list_posts(q,limit=100):
    params = dict(q=q,limit=limit)
    url = api_base_url + "post/index"
    return do_request(params,url,"get")

if __name__ == "__main__":
    print get_lang_ext("python")