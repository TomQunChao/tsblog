#!/bin/python
import os
import json
import jinja2
import time
# print("root path:",os.path.abspath(ROOT))
gen_cmd = "jupyter nbconvert --template classic --to html --theme {theme} --output {out_path} {src_path}"
mkdir_cmd = "mkdir {path}"
copy_dir_cmd = "cp {src} {dst} {args}"


class Generator:
    def __init__(self, config_path) -> None:
        c = json.load(open(config_path, encoding='utf-8'))
        self.troot = os.path.abspath(self._join_dir(c['dst_root']))
        self.sroot = self._join_dir(c['src_root'])
        self.config = c
        self.configf = config_path
        self.img_path = c['img_path_name']
        self.assets_path = c['assets_path_name']
        self.disallow_dir = []
        for d in c['disallow_dir']:
            self.disallow_dir.append(os.path.abspath(
                os.path.join(self.sroot, self._join_dir(d))))
        self.category_list: dict = c['category_list']
        self.auto_deploy = c['auto_deploy']
        self.theme = c['theme']
        self.blog_list = []
        self.ul_tag = c['ul_tag']
        self.li_tag = c['li_tag']
        self.ul_tag_t = c['ul_tag_t']
        self.li_tag_t = c['li_tag_t']
        self.nul_tag=c['nul_tag']
        self.nul_tag_t=c['nul_tag_t']
        self.force_update = c['force_update']
        self.theme = c['theme']
        

    def _str2time(self, t):
        return time.strftime("%Y-%m-%d", time.localtime(t))

    def _save(self):
        json.dump(self.config, open(self.configf, "w",
                  encoding='utf-8'), indent=4, ensure_ascii=False)

    def _join_dir(self, dirlist: list):
        dir = ''
        for i in dirlist:
            dir = os.path.join(dir, i)
        if dir == '':
            dir = os.curdir
        return dir

    def _get_title(self, f):
        t = '&lt unknown title article &gt'
        content = open(f, encoding='utf-8').read()
        if len(content) == 0:
            return t
        c = json.loads(content)
        cells = c['cells']
        if len(cells) > 0 and cells[0]['cell_type'] == 'markdown':
            source = cells[0]['source']
            if len(source) > 0 and len(source[0]) > 3:
                t = source[0][2:].strip()
        return t

    def _copy_dir(self, f, t):
        os.system(copy_dir_cmd.format(src=f, dst=t, args='-rf'))

    def _pages(self, paths: list, category_list: dict):
        # print("--")
        cpath = self._join_dir(paths)
        # print("compare:",os.path.abspath(cp),self.disallow_dir,os.path.abspath(cpath),category_list)
        if 'name' not in category_list.keys():
            category_list['name'] = ''
        if 'type' not in category_list.keys():
            category_list['type'] = 'directory'
        for p in os.listdir(cpath):
            cp = os.path.join(cpath, p)
            # print(cpath,p)
            tp = os.path.join(self.troot, cpath)
            if os.path.abspath(cp) in self.disallow_dir or p.startswith('.'):
                continue
            # print('continued...')
            if os.path.isfile(cp):
                if p.endswith('.ipynb'):
                    if 'mtime' in category_list.keys() and category_list['mtime'] == os.path.getmtime(cp) and not self.force_update and os.path.exists(os.path.join(tp, 'index.html')):
                        print("Already the newest! %s" % cp)
                        self.blog_list.append({
                            "title": category_list['name'],
                            "mtime": category_list['mtime'],
                            "link": "/".join(paths)
                        })
                        continue
                    c = gen_cmd.format(out_path=os.path.join(
                        tp, 'index.html'), src_path=os.path.abspath(cp), theme=self.theme)
                    # print(os.path.abspath(os.curdir))
                    os.system(c)
                    # print(c)
                    category_list['type'] = 'article'
                    category_list['name'] = self._get_title(cp)
                    category_list['mtime'] = os.path.getmtime(cp)
                    self.blog_list.append({
                        "title": category_list['name'],
                        "mtime": category_list['mtime'],
                        "link": "/".join(paths)
                    })
                else:
                    continue
            elif os.path.isdir(cp):
                if p == self.img_path or p == self.assets_path:
                    self._copy_dir(cp, tp)
                else:
                    to_mdir = os.path.join(tp, p)
                    if not os.path.exists(to_mdir):
                        os.makedirs(to_mdir)
                    if 'sub' not in category_list.keys():
                        category_list['sub'] = dict()
                    if not p in category_list['sub'].keys():
                        category_list['sub'][p] = dict()
                    paths.append(p)
                    self._pages(paths, category_list['sub'][p])
                    paths.pop()

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
                html+=f'{self.li_tag}{self.ul_tag}<a>{v["name"]}</a>'
                for f in v['link_list']:
                    html += f'{self.li_tag}<a href={f["link"]}><p>{f["name"]}\t{f["description"]}</p></a>{self.li_tag_t}'
                html+=f"{self.ul_tag_t}{self.li_tag_t}"
            else:
                print("unknown friend list type")

        html += f"{self.ul_tag_t}"
        return html

    def _render_friends(self):
        fri = self.config["friends"]
        open(os.path.join(self.troot, "friends.html"), "w",
             encoding="utf-8").write(self._render_html(self.render_friends_list(fri)))

    def _render_index(self):
        self.blog_list = sorted(self.blog_list, key=lambda x: -x['mtime'])
        html = f"{self.nul_tag}"
        for b in self.blog_list:
            html += f'{self.li_tag}<a href="{b["link"]}"><b>{b["title"]}</b>\t--<i>{self._str2time(b["mtime"])}</i></a>{self.li_tag_t}'
        html += f"{self.nul_tag_t}"
        open(os.path.join(self.troot, "index.html"), "w",
             encoding="utf-8").write(self._render_html(html))

    def _render_about(self):
        c = self.config
        open(os.path.join(self.troot, "about.html"), "w", encoding='utf-8').write(
            self._render_html(f'<img src={c["about_photo"]}><p>{c["about"]}</p>'))

    def _render_category_list(self, paths: list, category_list: dict):
        html = f'{self.ul_tag}'
        for k, v in category_list.items():
            if v['type'] == 'article':
                html += f'{self.li_tag}<a href="{"/".join(paths+[k])}"><p><b>{v["name"]}</b>\t--<i>{self._str2time(v["mtime"])}</i></p></a>{self.li_tag_t}'
            elif v['type'] == 'directory':
                disp_name=v['name']
                if disp_name=='':
                    disp_name=' &lt unknown category &gt'
                html+=f'{self.li_tag}<a><span class="ax-name">{disp_name}</span></a>'
                # if v['name'] == '':
                #     html += f'{self.li_tag}<a href="#"><span class="ax-name"> &lt unknown category &gt</span></a>'
                # else:
                #     html += f'{self.li_tag}<a href="#"><span class="ax-name">{v["name"]}</span></a>'
                if 'sub' in v.keys():
                    html += f'{self._render_category_list(paths+[k],v["sub"])}'
                html += f"{self.li_tag_t}"
            else:
                print("unknown category list type")
        html += f'{self.ul_tag_t}'
        return html

    def _render_category(self):
        rs = self._render_category_list([], self.category_list)
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

    def _deploy(self):
        os.system("git add *")
        os.system("git commit -m 'tsblog auto commit'")
        os.system("git push origin main")

    def run(self):
        self._gen_pages()
        self._render_category()
        self._render_about()
        self._render_friends()
        self._render_index()

        self._save()
        if self.auto_deploy:
            self._deploy()


if __name__ == '__main__':
    g = Generator("config.json")
    g.run()
