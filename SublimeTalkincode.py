#!/usr/bin/python2.7 
#coding:utf-8
import sublime,sublime_plugin
import re,os,sys,json
from utils import logger

reload(sys)
sys.setdefaultencoding('utf-8')



"""
@description:a sublime text plugin of a share code library 
@tags:python,sublime text 2
"""

settings = sublime.load_settings('ShareCodeLibrary.sublime-settings')      




class RegisterTic(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view

    def run(self, edit):
        pass


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
        pass

class AddTicPost(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view

    def run(self, edit):
        pass      

class AddTicComment(sublime_plugin.TextCommand):
    def __init__(self,view):
        self.view = view

    def run(self, edit):
        pass                