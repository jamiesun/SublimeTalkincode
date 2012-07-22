#!/usr/bin/python2.7 
#coding:utf-8
import sublime,sublime_plugin
import re,os,sys
import api

reload(sys)
sys.setdefaultencoding('utf-8')

"""
@description:talkincode.org  sublime text 2 plugin 
@tags:python,sublime text 2
@author:jamiesun.net@gmail.com
"""
settings = sublime.load_settings("SublimeTalkincode.sublime-settings")

# register_flag = "Talkincode.org Register:"
# codeid_flag = "Talkincode.org @codeid:"
# postid_flag = "Talkincode.org @postid:"
# newpost_flag = "Talkincode.org new Topic:"

########################################################################################
####   Talkincode.org Register                  
########################################################################################

class RegisterTic(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view   
        self.window = view.window() 

    def run(self, edit):
        def on_username(username):
            def on_password(password):
                def on_email(email):
                    try:
                        result = api.register(username,password,email)
                        if result and result.has_key("error"):
                            sublime.error_message("fail %s"%result["error"])
                        else:
                            settings.set("authkey",result["authkey"])
                            settings.set("author",result["username"])
                            settings.set("email",result["email"])
                            sublime.save_settings('SublimeTalkincode.sublime-settings')
                            sublime.message_dialog("success")
                    except Exception, e:
                        sublime.error_message("register user error  error %s "%e)
                self.window.show_input_panel("Type Email::","",on_email,None,None)
            self.window.show_input_panel("Type Password::","",on_password,None,None)
        self.window.show_input_panel("Type Username::","",on_username,None,None)



########################################################################################
####   Talkincode.org search                
########################################################################################

def get_code_content(result,idx):
    uid = result[idx]["id"]
    lang = api.get_lang_ext(result[idx]["lang"])
    code_file_path = "%s/%s.%s"%(os.environ["TMP"],uid,lang)

    codeobj = api.get_code(uid)
    if type(codeobj) ==dict and codeobj.has_key("error"):
        raise Exception(codeobj.get("error"))

    code_file = open(code_file_path,"wb")
    code_file.write(codeobj['content'])
    code_file.close()
    return code_file_path

class QueryTicMyCodes(sublime_plugin.WindowCommand):
    def run(self):      
        sublime.status_message("search my code, please wait......")
        try:
            result = api.list_mycodes(settings.get("authkey"))
            if type(result) ==dict and result.has_key("error"):
                raise Exception(result.get("error"))

            def format_it(row):
                return  ["%s - %s"%(row["lang"],row["title"]),
                         "by @%s <%s> hits : %s"%(row["author"],row["email"],row["hits"] )]
            items = [format_it(row) for row in result]

            def on_code_click(idx):
                if idx == -1:
                    return
                code_view = self.window.open_file(get_code_content(result,idx))
                self.window.focus_view(code_view)
                code_view.settings().set("codeid",result[idx]["id"])

            self.window.show_quick_panel(items,on_code_click)            
        except Exception, e:
            sublime.error_message("error:%s"%e)            



class QueryTicCodes(sublime_plugin.WindowCommand):
    def run(self):      
        sublime.status_message("search code, please wait......")
        def on_input(keywd):
            try:
                result = api.list_codes(keywd)
                if type(result) ==dict and result.has_key("error"):
                    raise Exception(result.get("error"))

                def format_it(row):
                    return  ["%s - %s"%(row["lang"],row["title"]),
                             "by @%s <%s> hits : %s"%(row["author"],row["email"],row["hits"] )]
                items = [format_it(row) for row in result]

                def on_code_click(idx):
                    if idx == -1:
                        return
                    code_view = self.window.open_file(get_code_content(result,idx))
                    self.window.focus_view(code_view)
                    code_view.settings().set("codeid",result[idx]["id"])

                self.window.show_quick_panel(items,on_code_click)            
            except Exception, e:
                sublime.error_message("error:%s"%e)            

        self.window.show_input_panel("search keyword::","",on_input,None,None)


def get_post_content(result,idx):
    uid = result[idx]["id"]
    post_file_path = "%s/%s.md"%(os.environ["TMP"],uid)
    post_result = api.get_post(uid)
    if not post_result:
        raise Exception(post_result.get("content not exists"))
    if type(post_result) ==dict and post_result.has_key("error"):
        raise Exception(post_result.get("error"))

    postobj = post_result['post']
    comments = post_result['comments']
    code_file = open(post_file_path,"wb")
    code_file.write("### @title:%s\n"%postobj['title'])
    code_file.write("### @tags:%s\n"%postobj['tags'])
    code_file.write("### @author:%s\n"%postobj['username'])
    code_file.write("### @content:\n\n")
    code_file.write(postobj['content'])
    code_file.write("\n\n")
    code_file.write("### @comments:\n\n")
    if comments:
        for cm in comments:
            code_file.write("\n")
            code_file.write("* "*40)
            code_file.write("\n\n")
            code_file.write(cm['content'])
            code_file.write("\n\n")
            code_file.write("%s %s via:%s\n"%(cm['author'],cm["created"],cm.get("via")))
    code_file.close()   
    return post_file_path

class QueryTicMyPosts(sublime_plugin.WindowCommand):
    def run(self):      
        sublime.status_message("search my topic, please wait......")
        try:
            result = api.list_myposts(settings.get("authkey"))
            if not result:
                return

            if type(result) ==dict and result.has_key("error"):
                raise Exception(result.get("error"))

            def format_it(row):
                return  ["%s - %s"%(row["title"],row["tags"]),
                         "by @%s  hits : %s %s"%(row["username"],row["hits"],row["created"]  )]
            items = [format_it(row) for row in result]

            def on_post_click(idx):
                if idx == -1:
                    return
                code_view = self.window.open_file(get_post_content(result,idx))
                self.window.focus_view(code_view)
                code_view.settings().set("postid",result[idx]["id"])

            self.window.show_quick_panel(items,on_post_click)            
        except Exception, e:
            sublime.error_message("error:%s"%e)            
 
        
class QueryTicPosts(sublime_plugin.WindowCommand):
    def run(self):      
        sublime.status_message("search topic, please wait......")
        def on_input(keywd):
            try:
                result = api.list_posts(keywd)
                if not result:
                    return

                if type(result) ==dict and result.has_key("error"):
                    raise Exception(result.get("error"))

                def format_it(row):
                    return  ["%s - %s"%(row["title"],row["tags"]),
                             "by @%s  hits : %s %s"%(row["username"],row["hits"],row["created"]  )]
                items = [format_it(row) for row in result]

                def on_post_click(idx):
                    if idx == -1:
                        return
                    code_view = self.window.open_file(get_post_content(result,idx))
                    self.window.focus_view(code_view)
                    code_view.settings().set("postid",result[idx]["id"])

                self.window.show_quick_panel(items,on_post_click)            
            except Exception, e:
                sublime.error_message("error:%s"%e)            

        self.window.show_input_panel("search keyword::","",on_input,None,None)

class RefreshTicPost(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
    def is_visible(self):
        return self.view.settings().get("postid")     

    def run(self, edit):    
        uid = self.settings().get("postid")
        try:
            post_file_path = "%s/%s.md"%(os.environ["TMP"],uid)
            post_result = api.get_post(uid)
            if not post_result:
                raise Exception(post_result.get("content not exists"))
            if type(post_result) ==dict and post_result.has_key("error"):
                raise Exception(post_result.get("error"))

            postobj = post_result['post']
            comments = post_result['comments']
            code_file = open(post_file_path,"wb")
            code_file.write("## @title:%s\n"%postobj['title'])
            code_file.write("## @tags:%s\n"%postobj['tags'])
            code_file.write("## @author:%s\n"%postobj['username'])
            code_file.write("### @content:\n\n")
            code_file.write(postobj['content'])
            code_file.write("\n\n")
            code_file.write("### @comments:\n\n")
            if comments:
                for cm in comments:
                    code_file.write("\n")
                    code_file.write("* "*40)
                    code_file.write("\n\n")
                    code_file.write(cm['content'])
                    code_file.write("\n\n")
                    code_file.write("%s %s via %s\n"%(cm['author'],cm["created"],cm.get("via")))
            code_file.close()
            # sublime.active_window().run_command('close')
            # code_view = sublime.active_window().open_file(post_file_path)
            # sublime.active_window().focus_view(code_view)
            sublime.message_dialog("Refresh ok")
        except Exception,e:
            sublime.error_message("error:%s"%e)  

########################################################################################
####   Talkincode.org add code                  
########################################################################################

class AddTicCode(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view

    def run(self, edit):
        def on_title(title):
            def on_tags(tags):
                try:
                    view = self.view
                    region = sublime.Region(0L, view.size())
                    filename = os.path.basename(view.file_name())
                    content = view.substr(region)
                    idgrp = re.search("@id:(.*)\n",content)
                    pid = idgrp and idgrp.group(1)

                    if sublime.ok_cancel_dialog("submit code to talkincode.org,continue?"):
                        filename = view.file_name()
                        fext = os.path.splitext(filename)[1]
                        if len(fext) >1:
                            fext = fext[1:]
                        lang = api.get_lang(fext)
                        tags = tags and "%s,%s"%(lang,tags) or lang
                        params = dict(pid=pid,
                            title=title,
                            author=settings.get("author"),
                            email=settings.get("email"),
                            tags=tags,
                            content=content,
                            lang=lang,
                            filename=os.path.basename(view.file_name()),
                            authkey=settings.get("authkey"))
                        
                        result = api.add_code(params)
                        if result and result.has_key("error"):
                            sublime.error_message("fail %s"%result["error"])
                        else:
                            sublime.message_dialog("success")
                except Exception,e:
                    sublime.error_message("submit code error %s "%e)
            if title:
                sublime.active_window().show_input_panel("Type tags (Optional)::","",on_tags,None,None)

        sublime.active_window().show_input_panel("Type title (required)::","",on_title,None,None)


########################################################################################
####   Talkincode.org add topic                  
########################################################################################        

class AddTicPostForm(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view           

    def run(self, edit):
        rview = sublime.active_window().new_file()
        sublime.active_window().focus_view(rview)
        rview.insert(edit,0,"@title:\n@tags:\n@content:")
        rview.settings().set("AddTicPostForm",True) 
        
    def is_visible(self):
        return self.view.settings().get("AddTicPostForm")  is None         

class AddTicPost(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
    def is_visible(self):
        return self.view.settings().get("AddTicPostForm")        

    def run(self, edit):
        try:
            view = self.view
            region = sublime.Region(0L, view.size())
            content_src = view.substr(region)
            titlegrp = re.search("@title:(.*)\n",content_src)
            tagsgrp = re.search("@tags:(.*)\n",content_src)

            region2 = sublime.Region(content_src.index("@content:")+9, view.size())
            content = view.substr(region2)
            
            title = titlegrp and titlegrp.group(1)
            #content = contentgrp and contentgrp.group(1)
            tags = tagsgrp and tagsgrp.group(1)

            if not title or not content:
                sublime.error_message("title,content can not be empty")
            else:
                if not sublime.ok_cancel_dialog("submit topic to talkincode.org,continue?"):
                    return
                
                params = dict(
                    title=title,
                    tags=tags,
                    content=content,
                    authkey=settings.get("authkey"))
                
                result = api.add_post(params)
                if result and result.has_key("error"):
                    raise Exception(result["error"])
                else:
                    sublime.message_dialog("success")
        except Exception,e:
            sublime.error_message("submit topic error %s "%e)


class UpdateTicPost(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
    def is_visible(self):
        return self.view.settings().get("postid")        
    def run(self, edit):
        try:
            view = self.view
            region = sublime.Region(0L, view.size())
            content_src = view.substr(region)
            titlegrp = re.search("@title:(.*)\n",content_src)
            tagsgrp = re.search("@tags:(.*)\n",content_src)
            postid =self.view.settings().get("postid")       
            title = titlegrp and titlegrp.group(1)
            tags = tagsgrp and tagsgrp.group(1)

            region2 = sublime.Region(content_src.index("@content:")+9, content_src.index("### @comments:"))
            content = view.substr(region2)

            if not postid or not content:
                sublime.error_message("postid,content can not be empty")
            else:
                if not sublime.ok_cancel_dialog("submit topic to talkincode.org,continue?"):
                    return
                
                params = dict(
                    postid=postid,
                    title=title,
                    tags=tags,
                    content=content,
                    authkey=settings.get("authkey"))
                
                result = api.update_post(params)
                if result and result.has_key("error"):
                    raise Exception(result["error"])
                else:
                    sublime.message_dialog("success")
        except Exception,e:
            sublime.error_message("submit topic error %s "%e)


class AddTicPostComment(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
    def is_visible(self):
        return self.view.settings().get("postid")    

    def run(self, edit):    
        view = self.view
        def on_input(cmtxt):
            postid = self.view.settings().get("postid")       
            try:
                params = dict(postid=postid,content=cmtxt,authkey=settings.get("authkey"))
                result = api.add_post_comment(params)
                if result and result.has_key("error"):
                    raise Exception(result["error"])
                else:
                    view.run_command("refresh_tic_post")
                    #sublime.message_dialog("comment success")                
            except Exception, e:
                 sublime.error_message(str(e))

        sublime.active_window().show_input_panel("Comment content::","",on_input,None,None)


########################################################################################
####   Talkincode.org  project              
########################################################################################     
def get_project_content(result,idx):
    uid = result[idx]["id"]
    proj_file_path = "%s/%s.md"%(os.environ["TMP"],uid)

    projobj = api.get_project(uid)

    if not projobj:
        raise Exception(projobj.get("content not exists"))
    if type(projobj) ==dict and projobj.has_key("error"):
        raise Exception(projobj.get("error"))

    proj_file = open(proj_file_path,"wb")
    proj_file.write("### @title:%s\n"%projobj['name'])
    proj_file.write("### @tags:%s\n"%projobj['tags'])
    proj_file.write("### @owner:%s\n"%projobj['owner'])
    proj_file.write("### @image:%s\n"%projobj['image'])
    proj_file.write("### @license:%s\n"%projobj['license'])
    proj_file.write("### @homepage:%s\n"%projobj['homepage'])
    proj_file.write("### @lang:%s\n"%projobj['lang'])
    proj_file.write("### @content:\n\n")
    proj_file.write(projobj['description'])
    proj_file.close()   
    return proj_file_path

class QueryTicProjects(sublime_plugin.WindowCommand):
    def run(self):      
        sublime.status_message("search project, please wait......")
        def on_input(keywd):
            try:
                result = api.list_projects(keywd)
                if not result:
                    return

                if type(result) ==dict and result.has_key("error"):
                    raise Exception(result.get("error"))

                def format_it(row):
                    return  ["%s - %s"%(row["name"],row["tags"]),
                             "owner:%s  hits : %s %s"%(row["owner"],row["hits"],row["created"]  )]
                items = [format_it(row) for row in result]

                def on_post_click(idx):
                    if idx == -1:
                        return
                    try:
                        proj_view = self.window.open_file(get_project_content(result,idx))
                        sublime.active_window().focus_view(proj_view)
                        proj_view.settings().set("project_id", result[idx]["id"])
                    except Exception,e:
                        sublime.error_message("get project error:%s"%e)    

                self.window.show_quick_panel(items,on_post_click)            
            except Exception, e:
                sublime.error_message("error:%s"%e)            
        self.window.show_input_panel("search keyword::","",on_input,None,None)   

class AddTicProjectForm(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view           

    def run(self, edit):
        rview = sublime.active_window().new_file()
        sublime.active_window().focus_view(rview)
        form = "@title:\n@image:\n@owner:\n@license:\n@homepage:\n@lang:\n@tags:\n@content:\n"
        rview.insert(edit,0,form)
        rview.settings().set("AddTicProjectForm",True)
        
    def is_visible(self):
        return self.view.settings().get("AddTicProjectForm") is None

class AddTicProject(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
    def is_visible(self):
        return self.view.settings().get("AddTicProjectForm")       
    def run(self, edit):
        try:
            view = self.view
            region = sublime.Region(0L, view.size())
            content_src = view.substr(region)
            titlegrp = re.search("@title:(.*)\n",content_src)
            tagsgrp = re.search("@tags:(.*)\n",content_src)
            ownergrp = re.search("@owner:(.*)\n",content_src)
            licensegrp = re.search("@license:(.*)\n",content_src)
            imagegrp = re.search("@image:(.*)\n",content_src)
            homepagegrp = re.search("@homepage:(.*)\n",content_src)
            langgrp = re.search("@lang:(.*)\n",content_src)

            region2 = sublime.Region(content_src.index("@content:")+9, view.size())
            content = view.substr(region2)

            if not titlegrp or not content:
                sublime.error_message("title,content can not be empty")
            else:
                if not sublime.ok_cancel_dialog("submit project to talkincode.org,continue?"):
                    return
                params = dict(
                    title=titlegrp and titlegrp.group(1),
                    image=imagegrp and imagegrp.group(1),
                    tags=tagsgrp and tagsgrp.group(1),
                    owner=ownergrp and ownergrp.group(1),
                    license=licensegrp and licensegrp.group(1),
                    homepage=homepagegrp and homepagegrp.group(1),
                    lang=langgrp and langgrp.group(1),
                    content=content,
                    authkey=settings.get("authkey"))
                result = api.add_project(params)
                if result and result.has_key("error"):
                    raise Exception(result["error"])
                else:
                    sublime.message_dialog("success")
        except Exception,e:
            sublime.error_message("submit Project error %s "%e)

class UpdateTicProject(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view

    def is_visible(self):
         return self.view.settings().get("project_id")    

    def run(self, edit):
        try:
            view = self.view
            region = sublime.Region(0L, view.size())
            content_src = view.substr(region)
            titlegrp = re.search("@title:(.*)\n",content_src)
            tagsgrp = re.search("@tags:(.*)\n",content_src)
            ownergrp = re.search("@owner:(.*)\n",content_src)
            licensegrp = re.search("@license:(.*)\n",content_src)
            imagegrp = re.search("@image:(.*)\n",content_src)
            homepagegrp = re.search("@homepage:(.*)\n",content_src)
            langgrp = re.search("@lang:(.*)\n",content_src)

            region2 = sublime.Region(content_src.index("@content:")+9, view.size())
            content = view.substr(region2)

            if  not content:
                sublime.error_message("content can not be empty")
            else:
                if not sublime.ok_cancel_dialog("submit topic to talkincode.org,continue?"):
                    return
                
                params = dict(
                    id=self.view.settings().get("project_id"),
                    title=titlegrp and titlegrp.group(1),
                    image=imagegrp and imagegrp.group(1),
                    tags=tagsgrp and tagsgrp.group(1),
                    owner=ownergrp and ownergrp.group(1),
                    license=licensegrp and licensegrp.group(1),
                    homepage=homepagegrp and homepagegrp.group(1),
                    lang=langgrp and langgrp.group(1),
                    content=content,
                    authkey=settings.get("authkey"))
                
                result = api.update_project(params)
                if result and result.has_key("error"):
                    raise Exception(result["error"])
                else:
                    sublime.message_dialog("success")
        except Exception,e:
            sublime.error_message("submit Project error %s "%e)

class BrowserTicSite(sublime_plugin.WindowCommand):
    def run(self):
        api.open_homepage()

