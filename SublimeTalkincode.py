#!/usr/bin/python2.7 
#coding:utf-8
import sublime,sublime_plugin
import re,os,sys
import api

reload(sys)
sys.setdefaultencoding('utf-8')

"""
@description:talkincode.org  sublime text plugin 
@tags:python,sublime text 2
"""
logger = api.logger 
settings = sublime.load_settings("SublimeTalkincode.sublime-settings")

class RegisterTicForm(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view    

    def run(self, edit):
        rview = sublime.active_window().new_file()
        sublime.active_window().focus_view(rview)
        rview.insert(edit,0,"Talkincode Register:\n@username:\n@password:\n@email:")
        self._visible = False

    def is_visible(self):
        return self.view.find(r"Talkincode Register:",0,sublime.IGNORECASE) is None


class RegisterTic(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view
    def is_visible(self):
        return self.view.find("Talkincode Register:",0) is not None      

    def run(self, edit):
        region = sublime.Region(0L, self.view.size())
        content = self.view.substr(region)
        username_grp = re.search("@username:(.*)\n",content)
        passwd_grp = re.search("@password:(.*)\n",content)
        email_grp = re.search("@email:(.*)",content)

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
            


class QueryTicCodes(sublime_plugin.WindowCommand):
    def run(self):      
        pass

        
class QueryTicPosts(sublime_plugin.WindowCommand):
    def run(self):      
        pass

class AddTicCode(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view

    def run(self, edit):
        try:
            view = self.view
            region = sublime.Region(0L, view.size())
            filename = os.path.basename(view.file_name())

            content = view.substr(region)
            titlegrp = re.search("@description:(.*)\n",content)
            tagsgrp = re.search("@tags:(.*)\n",content)
            idgrp = re.search("@id:(.*)\n",content)
            if not titlegrp:
                sublime.error_message(r"your source code must contains @description:{some text of title} ")
            else:
                if not sublime.ok_cancel_dialog("post code to talkincode.org,continue?"):
                    return
                title = titlegrp.group(1)
                tags = None
                if tagsgrp:
                    tags=tagsgrp.group(1)

                filename = view.file_name()
                fext = os.path.splitext(filename)[1]
                if len(fext) >1:
                    fext = fext[1:]

                params = dict(pid=(idgrp and idgrp.group(1) or 0),
                    title=title,
                    author=settings.get("author"),
                    email=settings.get("email"),
                    tags=tags,
                    content=content,
                    lang=api.get_lang(fext),
                    filename=os.path.basename(view.file_name()),
                    authkey=settings.get("authkey"))
                
                result = api.add_code(params)
                if result and result.has_key("error"):
                    sublime.error_message("fail %s"%result["error"])
                else:
                    sublime.message_dialog("success")
        except Exception,e:
            sublime.error_message("add code error %s "%e)

class AddTicPost(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view

    def run(self, edit):
        pass      

class AddTicCodeComment(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view

    def run(self, edit):
        pass     

class AddTicPostComment(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view

    def run(self, edit):
        pass         