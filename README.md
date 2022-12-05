# TongShuai's Blog generated based on jupyter

这是一个非常小的精简的博客生成器，基于jupyter，本文件夹也是博客生成器生成的博客，可以在这里访问`https://tsblog.pages.dev`

安装：`pip install -r requirements.txt`

~~配置文件：第一次运行只需要在配置文件`category_list`下面放好相对于`src_root`目录的相对路径，并设置好目标路径(blogs)，然后运行脚本`python tsblog.py`即可得到根据你的目录生成的列表~~

然后在`config.json`中填好各个列表的命名，再次生成即可得到可读性列表

文章标题在文章开头用一个`# `的标题表示

~~图片请放在`img`文件夹，资源请放在`assets`文件夹，会自动拷贝~~

推荐使用vscode插件`markdown paste`或jupyter-lab自带的图片粘贴功能

~~首先生成一次无误后，可以配置`auto_deploy=true`自动部署！~~

20221129更新：增加`-D`和`-G`选项，如果指定`-D`，则只部署，如果指定`-G`，则只生成，都不指定则先生成，并根据`auto_deploy`决定是否自动部署

20221204更新：

- 同时支持markdown和ipynb格式，markdown利用的是先转换为ipynb再转换，支持的格式列表位于`config.json`中`support_source`节点下
- 增加`-C`选项指定配置文件位置
- 友链位于`friends.json`，列表位于`category_list.json`单独文件中，便于管理
- 目录中文章标题采用细体字和目录区分
- 优化代码结构

20221205更新

- 删除之前存在后来不存在的文件/文件夹

## TODO

- [ ] 友链利用js根据`friends.json`生成，这样可以通过提交pr增加友链
- [ ] 目录利用js根据`category_list.json`生成
- [ ] 优化目录表示形式
- [ ] about改为json模式并利用js生成
- [ ] index改为json模式并利用js生成
- [ ] jupyter转html包含过多base64图片导致文件过大，转换成小markdown问题
- [ ] (可选)夜间模式
- [ ] (可选)文章搜索功能
