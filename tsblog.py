#!/bin/python
import os
import json
import jinja2
import time
import argparse
import string
import random
import hashlib
# from multiprocessing import Pool as ThPool TODO 多线程支持
# print("root path:",os.path.abspath(ROOT))
mkdir_cmd = "mkdir {path}"
copy_dir_cmd = "cp {src} {dst} {args}"

class Util:
    def gen_unique_fname(d, suffix='.ipynb', l=10):
        r = ''.join(random.choice(string.ascii_letters+string.digits)
                    for _ in range(l))+suffix
        while os.path.exists(os.path.join(d, r)):
            r = ''.join(random.choice(string.ascii_letters+string.digits)
                        for _ in range(l))+suffix
        return r
    def str2time(t):
        return time.strftime("%Y-%m-%d", time.localtime(t))
    def join_dir(dirlist: list):
        dir = ''
        for i in dirlist:
            dir = os.path.join(dir, i)
        if dir == '':
            dir = os.curdir
        return dir
    def get_file_md5(src):
        return hashlib.md5(open(src,'rb').read()).hexdigest()
    def get_file_mtime(src):
        return os.path.getmtime(src)
    def copy_dir(f, t):
        os.system(copy_dir_cmd.format(src=f, dst=t, args='-rf'))
class FormatTranslator:
    _cmd_prefix = "jupyter nbconvert --template {template} --to {to_fmt} --theme {theme} {embed_img}"
    _cmd_suffix=" --output {out_path} {src_path}"
    _exam_nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# This is Title"
                ]
            }
        ],
        "metadata": {
            "language_info": {
                "name": "python"
            },
            "orig_nbformat": 4
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    def __init__(self,theme='light',template="classic",embed_images=False,to_fmt="html") -> None:
        self._cmd_pre=self._cmd_prefix.format(template=template,theme=theme,embed_img='--embed_images'if embed_images else '',to_fmt=to_fmt)
    def ipynb2html(self,src,dst,):
        '''
        @param: theme dark,jupyterlab_miami_nights
        @param: template classic,basic
        @param: embed_images: 如果为True则
        '''
        cmd=self._cmd_pre+self._cmd_suffix.format(out_path=dst, src_path=src)
        os.system(cmd)
    def md2ipynb(self,src,dst):
        nb=self._exam_nb
        nb['cells'][0]['source']=open(src,encoding='utf-8').readlines()
        json.dump(nb,open(os.path.join(dst),"w",encoding='utf-8'),indent=4,ensure_ascii=False)
    def md2html(self,src,dst):
        src_dir=os.path.dirname(src)
        tmp=os.path.join(src_dir,Util.gen_unique_fname(src_dir))
        self.md2ipynb(src,tmp)
        self.ipynb2html(tmp,dst)
        os.remove(tmp)
    def ipynb2md(self):
        raise NotImplementedError()

class Generator:
    def __init__(self, config_path) -> None:
        c = json.load(open(config_path, encoding='utf-8'))
        self.troot = os.path.abspath(Util.join_dir(c['dst_root']))
        self.sroot = Util.join_dir(c['src_root'])
        self.config = c
        self.configf = config_path
        self.disallow_dir = []
        for d in c['disallow_dir']:
            self.disallow_dir.append(os.path.abspath(
                os.path.join(self.sroot, Util.join_dir(d))))
        self.auto_deploy = c['auto_deploy']
        self.blog_list = []
        self.ul_tag = c['ul_tag']
        self.li_tag = c['li_tag']
        self.ul_tag_t = c['ul_tag_t']
        self.li_tag_t = c['li_tag_t']
        self.nul_tag = c['nul_tag']
        self.nul_tag_t = c['nul_tag_t']
        self.force_update = c['force_update']
        self.fmt_trans = FormatTranslator(c['theme'],c['template'],c['embed_img'])
        self.file_cmp_mode=c['file_cmp_mode']
        self.support_source=c['support_source']
        self.assets_folder=c['assets_folder']
        self.friends_path=c['friends_path']
        self.category_list_path=c['category_list_path']
        self._load()

    def _load(self):
        p=os.path.join(self.troot,self.category_list_path)
        self.category_list=dict()
        if os.path.exists(p):
            self.category_list=json.load( open(p,encoding='utf-8'))
    def _save(self):
        json.dump(self.category_list, open(os.path.join(self.troot,self.category_list_path), "w",
                  encoding='utf-8'), indent=4, ensure_ascii=False)

    def _get_ipynb_title(self, f):
        t = '&lt unknown title article &gt'
        content = open(f, encoding='utf-8').read()
        if len(content) == 0:
            return t
        c = json.loads(content)
        cells = c['cells']
        if len(cells) > 0 and cells[0]['cell_type'] == 'markdown':
            source = cells[0]['source']
            if len(source) > 0 and source[0].startswith('# '):
                t = source[0][2:].strip()
        return t

    def _get_md_title(self, f):
        t = '&lt unknown title article &gt'
        content = open(f, encoding='utf-8').readlines()
        if len(content) > 0 and content[0].startswith('# '):
            t = content[0][2:].strip()
        return t

    def _is_file_motified(self,src,art_info,dst):
        mtime=Util.get_file_mtime(src)
        link,linkest=None,False
        if 'link' in art_info:
            link=art_info['link'].split('/')[-1]
            linkest=True
            if not os.path.exists(os.path.join(dst,link)):
                linkest=False
        if self.file_cmp_mode=='md5':
            if 'md5' not in art_info or art_info['md5'] is None or link is None or not linkest:
                return True,Util.get_file_md5(src),mtime,link
            ha=Util.get_file_md5(src)
            if ha!=art_info['md5']:
                return True,ha,mtime,link
            return False,ha,mtime,link
        elif self.file_cmp_mode=='mtime':
            if 'mtime' not in art_info or link is None or not linkest:
                return True,None,mtime,link
            if mtime>art_info['mtime']:
                return True,None,mtime,link
            return False,None,mtime,link
        else:
            raise NotImplementedError("Unsupported file cmp mode")
    def _process_page(self,typ,cp,tpath,art_info,p):
        title_func={
            ".ipynb":self._get_ipynb_title,
            ".md":self._get_md_title
        }
        trans_func={
            ".ipynb":self.fmt_trans.ipynb2html,
            ".md":self.fmt_trans.md2html
        }
        is_modi,ha,mtime,link=self._is_file_motified(cp,art_info,tpath)
        if not is_modi:
            if 'name' in art_info:
                title=art_info['name']
            return title,mtime,ha,link
        title=title_func[typ](cp)
        if link is None:
            link=p+'.html'
        trans_func[typ](cp,os.path.join(tpath,link))
        return title,mtime,ha,link
    def _pages(self, paths: list, category_list: dict):
        cpath = Util.join_dir(paths)
        if 'name' not in category_list.keys():
            category_list['name'] = ''
        if 'type' not in category_list.keys():
            category_list['type'] = 'directory'
        dirps=os.listdir(cpath)
        if 'sub' in category_list:
            ks=set(category_list['sub'].keys())
            for s in ks:
                if s not in dirps:
                    category_list['sub'].pop(s)
        for p in dirps:
            cp = os.path.join(cpath, p)
            tpath = os.path.join(self.troot, cpath)
            if os.path.abspath(cp) in self.disallow_dir or p.startswith('.'):
                continue
            if os.path.isfile(cp):
                _,ext=os.path.splitext(cp)
                if ext in self.support_source:
                    art_info=dict()
                    if 'sub' in category_list and p in category_list['sub']:
                        art_info=category_list['sub'][p]
                    title,mtime,ha,link=self._process_page(ext,cp,tpath,art_info,p)
                    linkp='/'.join(paths+[link])
                    self.blog_list.append({
                        'title':title,
                        'mtime':mtime,
                        'link':linkp
                    })
                    art_info=dict()
                    art_info['type']='article'
                    art_info['mtime']=mtime
                    art_info['name']=title
                    art_info['hash']=ha
                    art_info['link']=linkp
                    if 'sub' not in category_list:
                        category_list['sub'] = dict()
                    category_list['sub'][p] = art_info
            elif os.path.isdir(cp):
                if p in self.assets_folder:
                    Util.copy_dir(cp, tpath)
                else:
                    to_mdir = os.path.join(tpath, p)
                    if not os.path.exists(to_mdir):
                        os.makedirs(to_mdir)
                    if 'sub' not in category_list:
                        category_list['sub'] = dict()
                    if p not in category_list['sub']:
                        category_list['sub'][p] = dict()
                    paths.append(p)
                    self._pages(paths, category_list['sub'][p])
                    paths.pop()
            else:
                raise NotImplementedError("Unknown file type")

    def _gen_pages(self):
        cdir = os.path.abspath(os.curdir)
        os.chdir(self.sroot)
        for k, v in self.category_list.items():
            self._pages([k], v)
        os.chdir(cdir)

    def render_friends_list(self, fri_list: dict):
        html = f"{self.ul_tag}"
        for v in fri_list.values():
            if v['type'] == 'directory':
                html += f'{self.li_tag}<a>{v["name"]}</a>'
                html += f'{self.render_friends_list(v["sub"])}'
                html += f"{self.li_tag_t}"
            elif v['type'] == 'leaf':
                html += f'{self.li_tag}<a>{v["name"]}</a>{self.ul_tag}'
                for f in v['link_list']:
                    html += f'{self.li_tag}<a href={f["link"]}><p><b>{f["name"]}</b>\t"<i>{f["description"]}</i>"</p></a>{self.li_tag_t}'
                html += f"{self.ul_tag_t}{self.li_tag_t}"
            else:
                print("unknown friend list type")

        html += f"{self.ul_tag_t}"
        return html

    def _render_friends(self):
        fri = json.load(open(os.path.join(self.troot,self.friends_path),encoding='utf-8'))
        open(os.path.join(self.troot, "friends.html"), "w",
             encoding="utf-8").write(self._render_html(self.render_friends_list(fri)))

    def _render_index(self):
        self.blog_list = sorted(self.blog_list, key=lambda x: -x['mtime'])
        html = f"{self.nul_tag}"
        for b in self.blog_list:
            html += f'{self.li_tag}<a href="{b["link"]}"><b>{b["title"]}</b>\t--<i>{Util.str2time(b["mtime"])}</i></a>{self.li_tag_t}'
        html += f"{self.nul_tag_t}"
        open(os.path.join(self.troot, "index.html"), "w",
             encoding="utf-8").write(self._render_html(html))

    def _render_about(self):
        c = self.config
        open(os.path.join(self.troot, "about.html"), "w", encoding='utf-8').write(
            self._render_html(f'<img src={c["about_photo"]}><p>{c["about"]}</p>'))

    def _render_category_list(self,category_list: dict):
        html = f'{self.ul_tag}'
        for k, v in category_list.items():
            if v['type'] == 'article':
                html += f'{self.li_tag}<a href="{v["link"]}"><p>{v["name"]}\t--<i>{Util.str2time(v["mtime"])}</i></p></a>{self.li_tag_t}'
            elif v['type']=='directory' and 'sub' in v and len(v['sub'])==1 and list(v['sub'].values())[0]['type']=='article':
                # 历史遗留问题
                art=list(v['sub'].values())[0]
                html += f'{self.li_tag}<a href="{art["link"]}"><p>{art["name"]}\t--<i>{Util.str2time(art["mtime"])}</i></p></a>{self.li_tag_t}'
            elif v['type'] == 'directory':
                disp_name = v['name']
                if disp_name == '':
                    disp_name = ' &lt unknown category &gt'
                html += f'{self.li_tag}<a><span class="ax-name">{disp_name}</span></a>'
                if 'sub' in v:html += f'{self._render_category_list(v["sub"])}'
                html += f"{self.li_tag_t}"
            else:
                print("unknown category list type")
        html += f'{self.ul_tag_t}'
        return html

    def _render_category(self):
        rs = self._render_category_list(self.category_list)
        open(os.path.join(self.troot, "category.html"), "w",
             encoding='utf-8').write(self._render_html(rs))

    def _render_html(self, s: str):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'))
        template = env.get_template('template.html')
        html_content = template.render(content=s)
        return html_content

    def _gen_href(self):
        open("index.html", "w").write(
            f'<!DOCTYPE html><html><head></head><body><script>document.location.href="{"/".join(self.config["dst_root"])}"</script></body></html>')

    def deploy(self):
        os.system("git add *")
        os.system("git commit -m 'tsblog auto commit'")
        os.system("git push origin +main")

    def generate(self):
        self._gen_pages()
        self._render_category()
        self._render_about()
        self._render_friends()
        self._render_index()
        self._save()

    def run(self):
        self.generate()
        if self.auto_deploy:
            self.deploy()


parser = argparse.ArgumentParser(prog="tsblog")
parser.add_argument('-D', '--deploy', action='store_true', default=False)
parser.add_argument('-G', '--generate', action='store_true', default=False)
parser.add_argument('-C','--config',default='./config.json',help="config file path")
if __name__ == '__main__':
    args = parser.parse_args()
    g = Generator(args.config)
    if args.deploy and args.generate:
        g.generate()
        g.deploy()
    elif args.deploy:
        g.deploy()
    elif args.generate:
        g.generate()
    else:
        g.run()
