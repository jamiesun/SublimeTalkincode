SublimeTalkincode
=================

[Sublime Text 2](http://www.sublimetext.com/2) plugin for share source code and publish topic to [Talkincode](http://www.talkincode.org) 

Install
=======

Through [Package Control](http://wbond.net/sublime_packages/package_control)

`Command Palette` > `Package Control: Install Package` > `SublimeTalkincode`

or clone this repository in

* Windows: `%APPDATA%/Roaming/Sublime Text 2/Packages/`
* OSX: `~/Library/Application Support/Sublime Text 2/Packages/`
* Linux: `~/.Sublime Text 2/Packages/`
* Portable Installation: `Sublime Text 2/Data/`

Usage
=====

`Command Palette` > `Talkincode.org: ...`

`Context menu` > `Talkincode.org`

Features
========

`Register new user`: join talkincode.org,You will receive a authkey

`Post current code`: share current source code to talkincode.org

`Post new topic`: Publish a topic and post to talkincode.org

`Comment current topic`:Comment on the topic you open

`Search code`:Search talkincode.org code

`Search topic`:Search talkincode.org topic

*************************************************************************
[submineTalkincode](http://www.talkincode.org) 是一个[Sublime Text 2](http://www.sublimetext.com/2) 的插件，通过这个插件可以直接在sublime text 2 中分享代码和讨论话题 

安装
=======

通过 [Package Control](http://wbond.net/sublime_packages/package_control)

`Command Palette` > `Package Control: Install Package` > `SublimeTalkincode`

或者直接在插件目录克隆这个[仓库](https://github.com/jamiesun/SublimeTalkincode)

* Windows: `%APPDATA%/Roaming/Sublime Text 2/Packages/`
* OSX: `~/Library/Application Support/Sublime Text 2/Packages/`
* Linux: `~/.Sublime Text 2/Packages/`
* Portable Installation: `Sublime Text 2/Data/`

如何使用
========

* `Tools` > `Command Palette` > `Talkincode.org: ...`

* 在编辑器上下文（鼠标右键）菜单中通过Talkincode.org项

* 大部分功能都有快捷键，在菜单 `preferences` > `Package Settings` > `Sublime Talkincode` 你可以找到,   你也可以设置自己习惯的快捷键。

功能特性
========

`Register new user`: 注册成为talkincode.org的成员，你将获得一个authkey，在发布内容时它用来认证身份

`Search code`:搜索talkincode.org的代码，输入关键字，查询请求会发送到talkincode.org，然后返回一个结果列表，你可以查看你感兴趣的代码。

`Search topic`:和搜索代码一样，你可以搜索你感兴趣的话题，打开一个话题，你还可以对他进行评论。

`Post current code`: 将你当前视图中的代码分享到talkincode.org，在代码中必须包含(单独一行)“@description:{some txt}”,这会成为这段代码的标题，同时你也可以加入标签，通过包含(单独一行)“@tags:...”，你可以把这些内容放在注释你而不影响代码的运行。比如：

    # @description: 一段python代码
    # @tags:python,helloword

    print 'hello world'

`Post new topic`: 发布一个讨论话题到talkincode.org，在talkincode.org中你可以讨论各种关于编程的话题，直接在很酷的sublime text 2编辑器中讨论，这看起来更酷了。

`Comment current topic`:对当前打开的话题进行评论