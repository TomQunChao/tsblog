# TongShuai's Blog generated based on jupyter

这是一个非常小的精简的博客生成器，基于jupyter，本文件夹也是博客生成器生成的博客，可以在这里访问`https://tsblog.pages.dev`

安装：`pip install -r requirements.txt`

配置文件：第一次运行只需要在配置文件`category_list`下面放好相对于`src_root`目录的相对路径，并设置好目标路径(blogs)，然后运行脚本`python tsblog.py`即可得到对于你的目录的列表

然后在`config.json`中填好各个列表的命名，再次生成即可得到可读性列表

文章标题在文章开头用一个`# `的标题表示

图片请放在`img`文件夹，资源请放在`assets`文件夹，会自动拷贝

推荐使用vscode插件`markdown paste`或jupyter-lab自带的图片粘贴功能

首先生成一次无误后，可以配置`auto_deploy=true`自动部署！

2022-11-29更新：增加`-D`和`-G`选项，如果指定`-D`，则只部署，如果指定`-G`，则只生成