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

register_flag = "Talkincode.org Register:"
codeid_flag = "Talkincode.org @codeid:"
postid_flag = "Talkincode.org @postid:"
newpost_flag = "Talkincode.org new Topic:"

########################################################################################
####   Talkincode.org Register                  
########################################################################################

class RegisterTicForm(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view    

    def run(self, edit):
        rview = sublime.active_window().new_file()
        sublime.active_window().focus_view(rview)
        rview.insert(edit,0,"%s\n@username:\n@password:\n@email:\n"%register_flag)
        self._visible = False

    def is_visible(self):
        return self.view.find(register_flag,0,sublime.IGNORECASE) is None


class RegisterTic(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
    def is_visible(self):
        return self.view.find(register_flag,0) is not None      

    def run(self, edit):
        region = sublime.Region(0L, self.view.size())
        content = self.view.substr(region)
        username_grp = re.search("@username:(.*)\n",content)
        passwd_grp = re.search("@password:(.*)\n",content)
        email_grp = re.search("@email:(.*)\n",content)

        username = username_grp and username_grp.group(1)
        passwd = passwd_grp and passwd_grp.group(1)
        email = email_grp and email_grp.group(1)

        if not username or not passwd or not email:
            sublime.error_message("username,password,email can not be empty")
            return

        if re.search("\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*",email) == None:
            sublime.error_message("email is not valid")
            return            

        if sublime.ok_cancel_dialog("To be registered talkincode.org,continue?"):
            try:
                result = api.register(username,passwd,email)
                if result and result.has_key("error"):
                    sublime.error_message("fail %s"%result["error"])
                else:
                    settings.set("authkey",result["authkey"])
                    settings.set("author",result["username"])
                    settings.set("email",result["email"])
                    sublime.save_settings('SublimeTalkincode.sublime-settings')
                    sublime.message_dialog("success")
                    region = sublime.Region(0L, self.view.size())
                    self.view.replace(edit,region,"")
                    sublime.active_window().run_command('close')                
            except Exception, e:
                sublime.error_message("register user error  error %s "%e)
            
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
    code_file.write("%s%s\n"%(codeid_flag,uid))
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
    code_file.write("%s%s\n\n"%(postid_flag,uid))
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

                self.window.show_quick_panel(items,on_post_click)            
            except Exception, e:
                sublime.error_message("error:%s"%e)            

        self.window.show_input_panel("search keyword::","",on_input,None,None)

class RefreshTicPost(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
    def is_visible(self):
        return self.view.find(postid_flag,0) is not None      

    def run(self, edit):    
        region = sublime.Region(0L, self.view.size())
        content = self.view.substr(region)
        postid_grp = re.search("%s(.*)\n"%postid_flag,content)
        uid = postid_grp and postid_grp.group(1)
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
            code_file.write("%s%s\n\n"%(postid_flag,uid))
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
        def on_input(title):
            try:
                view = self.view
                region = sublime.Region(0L, view.size())
                filename = os.path.basename(view.file_name())
                content = view.substr(region)
                tagsgrp = re.search("@tags:(.*)\n",content)
                idgrp = re.search("@id:(.*)\n",content)

                tags = tagsgrp and tagsgrp.group(1)
                pid = idgrp and idgrp.group(1)
                if not title:
                    sublime.error_message("title can not be empty ")
                    return
                else:
                    if not sublime.ok_cancel_dialog("submit code to talkincode.org,continue?"):
                        return
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

        sublime.active_window().show_input_panel("input title::","",on_input,None,None)


########################################################################################
####   Talkincode.org add topic                  
########################################################################################        

class AddTicPostForm(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view           

    def run(self, edit):
        rview = sublime.active_window().new_file()
        sublime.active_window().focus_view(rview)
        rview.insert(edit,0,"%s\n@title:\n@tags:\n@content:"%newpost_flag)
        
    def is_visible(self):
        return self.view.find(newpost_flag,0,sublime.IGNORECASE) is None         

class AddTicPost(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
    def is_visible(self):
        return self.view.find(newpost_flag,0,sublime.IGNORECASE) is not None           
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
        return self.view.find(postid_flag,0,sublime.IGNORECASE) is not None           
    def run(self, edit):
        try:
            view = self.view
            region = sublime.Region(0L, view.size())
            content_src = view.substr(region)
            postidgrp = re.search("@postid:(.*)\n",content_src)
            titlegrp = re.search("@title:(.*)\n",content_src)
            tagsgrp = re.search("@tags:(.*)\n",content_src)
            postid = postidgrp and postidgrp.group(1)
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
        return self.view.find(postid_flag,0) is not None 

    def run(self, edit):    
        view = self.view
        def on_input(cmtxt):
            region = sublime.Region(0L, view.size())
            content = view.substr(region)
            postid_grp = re.search("%s(.*)\n"%postid_flag,content)
            postid = postid_grp and postid_grp.group(1)  
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



class BrowserTicSite(sublime_plugin.WindowCommand):
    def run(self):
        api.open_homepage()

