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

    is_name_section = False

    name_string = ''

    for linenum, line in enumerate(file.readlines()):

        if len(str(line).strip('\n')) == 0:
            continue

        if '### 一、方案名称' in line:
            is_name_section = True

            continue

        if '### 二、关键字' in line:
            is_name_section = False
            break

        if is_name_section == True and len(str(line).strip('\n')) != 0:
            name_string = name_string + str(line).strip('\n')
            break

    abbrlink = filename.split(".")[0]

    if abbrlink != "Note_00000_20150625":
        list.append((name_string,abbrlink))

# 按第一个元素排序
def takeFirst(element):
    return element[0]

def writeCatalogue(contents,filename):

    with open(filename, "w") as f:
        f.write(contents)

# 主函数
def main():
    # 整理自定义笔记

    dir = current_file_dir()

    introduce = dir + "/Note_00000_Introduce.md"

    print("开始读取介绍信息...")

    with open(introduce, "r+") as f:
      contents = f.read() 

    contents = contents + "\n"

    dir = dir.replace("Notes_Draft","iosnotebook")

    print("开始读取目录信息...")
    for root, dirs, files in os.walk(dir):

        for item in files:
            parse_file(root,item)
    
    print("开始生成目录...")
    list.sort(key=takeFirst)

    index = 0
    for item in list:
        index = index + 1
        contents = contents + str(index) + ". ["+ item[0] +"]("+ item[1] +".html)\n"

    path = dir + "/Note_00000_20150625.md"

    print("开始写入目录...")
    writeCatalogue(contents,path)

    print("目录更新完成！")

if __name__ == '__main__':
    main()
