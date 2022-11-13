import os
import json
rp=[["..","information_security"]]
exam_nb={
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

def _join_dirs(dirs:list):
    dir=''
    for i in dirs:
        dir=os.path.join(dir,i)
    if dir=='':dir=os.curdir
    return dir
def _md2nb(paths):
    cpath=_join_dirs(paths)
    for p in os.listdir(cpath):
        cp=os.path.join(cpath,p)
        if os.path.isfile(cp) and p.endswith('.md'):
            out_f=p.split('.',maxsplit=1)[0]+".ipynb"
            nb=exam_nb.copy()
            nb['cells'][0]['source']=open(cp,encoding='utf-8').readlines()
            json.dump(nb,open(os.path.join(cpath,out_f),"w",encoding='utf-8'),indent=4,ensure_ascii=False)
            os.remove(cp)
        elif os.path.isdir(cp):
            _md2nb(paths+[p])
if __name__=="__main__":
    for p in rp:
        _md2nb(p)