# coding=utf-8

# Created by Alfred Jiang 20150514


import json
import os
import sys

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding( "utf-8" )


iosnotebook_project_url = "https://github.com/viktyz/iosnotebook/blob/master/"

list = []


# 获取脚本文件的当前路径
def current_file_dir():
    path = sys.path[0]

    if os.path.isdir(path):

        return path

    elif os.path.isfile(path):
        return os.path.dirname(path)


def parse_file(filepath, filename):
    url_string = iosnotebook_project_url

    if str(filename).startswith('Note_'):

        url_string = url_string + 'Notes/' + filename

    elif str(filename).startswith('JavaScript_'):

        url_string = url_string + 'JavaScript/' + filename

    elif str(filename).startswith('Python_'):

        url_string = url_string + 'Python/' + filename

    else:

        return

    fullpath = filepath + '/' + filename

    file = open(fullpath, 'r')

    is_need_revise = False
    is_update_searched = False
    is_title_searched = False

    revise_string = ''

    for linenum, line in enumerate(file.readlines()):

        if len(str(line).strip('\n')) == 0:
            continue
            
        if is_update_searched == True and is_title_searched == False:
            if line != '\n' and line != '### 一、方案名称\n':
                revise_string = revise_string + line

        if '### 八、变更记录' in line:
            is_update_searched = True
            
            if is_title_searched == False:
                revise_string = revise_string + line + '\n'
                continue
            else:
                break


        if '### 一、方案名称' in line:
            is_title_searched = True
            
            if is_update_searched == True:
                # 替换
                break
            else:
                break

    file.close()

    if len(revise_string) > 0:
    
        replace_string = "\n" + revise_string
        file_new = open(fullpath, "r")
        file_content = file_new.read()
        result = file_content.replace(revise_string,"")
        result = result + "\n" + replace_string
        
        with open(fullpath,"w") as f1:
            f1.write(result)
        
    else:
        print("Need not replace : " + filename)



def get_file_from_dir(dir, callback):
    for root, dirs, files in os.walk(dir):

        for item in files:
            callback(root, item)


def load(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data


def get_file_from_json(jpath):
    itemlist = load(jpath)

    for t1item in itemlist:

        t1name = t1item['name']

        if 'list' in t1item.keys():

            t1list = t1item['list']

            for t2item in t1list:
                t2name = t2item['name']

                if 'list' in t2item.keys():

                    t2list = t2item['list']

                    for t3item in t2list:
                        add_item_to_list(t3item, t2name + ' - ' + t1name)

                else:
                    add_item_to_list(t2item, t1name)
        else:
            add_item_to_list(t1item, '')


def add_item_to_list(item, pname):
    tname = item['name']
    towner = item['owner']

    info = dict()

    if 'desc' in item.keys():
        tdesc = item['desc']
        info['title'] = towner + '/' + tname + ' - ' + tdesc + ' - ' + pname
        info['tags'] = towner + '\\' + tname + '\\' + tdesc
    else:
        info['title'] = towner + '/' + tname + ' - ' + pname
        info['tags'] = towner + '\\' + tname

    info['category'] = pname
    info['url'] = get_url(item)
    info['date'] = ''

    list.append(info)


def get_url(repo):
    url = ''
    if not repo or not repo['name']:
        return url

    if 'url' in repo.keys() and len(repo['url']) > 0:
        url = repo['url']
    elif 'owner' in repo.keys() and len(repo['owner']) > 0:
        url = 'https://github.com/' + repo['owner'] + '/' + repo['name']
    else:
        url = 'https://github.com/search?q=' + repo['name']

    return url


def cp_files_to_gitbook():
    current = current_file_dir()
    list = current.split('/')
    del list[(len(list) - 1)]
    npath = '/'.join(list) + '/iOSNotebook-Gitbook'

    if os.path.exists(npath):
        notes = current + '/Notes'
        pnotes = npath + '/'
        cnotes = 'cp -R ' + notes + ' ' + pnotes
        os.system(cnotes)
        print(cnotes)

        pythons = current + '/Python'
        ppythons = npath + '/'
        cpythons = 'cp -R ' + pythons + ' ' + ppythons
        os.system(cpythons)
        print(cpythons)

        readme = current + '/README.md'
        preadme = npath + '/README.md'
        creadme = 'cp ' + readme + ' ' + preadme
        os.system(creadme)
        print(creadme)

        summary = current + '/SUMMARY.md'
        psummary = npath + '/SUMMARY.md'
        csummary = 'cp ' + summary + ' ' + psummary
        os.system(csummary)
        print(csummary)
    else:
        print('Not Exist iOSNotebook-Gitbook in folder : ' + npath)


# 主函数
def main():
    # 整理自定义笔记
    get_file_from_dir(current_file_dir(), parse_file)
    print("finished")

if __name__ == '__main__':
    main()
