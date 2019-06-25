#--coding: utf-8
import os
import sys
import time, datetime
import pypandoc

def get_file_type(path):
    try:
        _list = path.split('.')
        if _list[1] == 'md':
            return 'md'
        if _list[1] == 'org':
            return 'org'
    except Exception as e:
        print('----get file type error --->' + e)
    return 'org'

def convert_org(file_path):
    _type = get_file_type(file_path)
    
    result = pypandoc.convert_file(file_path, 'html', format=_type)
    #https://stackoverflow.com/questions/9942594/unicodeencodeerror-ascii-codec-cant-encode-character-u-xa0-in-position-20
    # Python 这个编码问题需要好好研究一下了，遇到过好几次了。
    # result = u''.join((result)).encode('utf-8').strip()
    return result.encode('utf-8').strip()
    
def read_file(full_path):
    try:
        file = open(full_path,"r")
        return file.read().encode('utf-8').strip()
    except Exception as e:
        print("--read file error---" + e)
        return ""

def save_file(content, path):
    try:
        file = open(path,'w')
        file.write(content)
        print("---- save file success --->" + path)
    except Exception as e:
        print("----save file error ----" + path)
        print(e)

def walk_dir(dir):
    _list = []
    for root, dirs, files in os.walk(dir, True):
        for name in files:
            _list.append(os.path.join(root,name))
    return _list

def takeSecond(elem):
    return elem[1]

def takeFirst(elem):
    return elem[0]

def walk_dir_sort(dir):
    _list = []
    for root, dirs, files in os.walk(dir,True):
        for name in files:
            _path = os.path.join(root,name)
            _update_time = int(os.path.getmtime(_path))
            _list.append((_path,_update_time))
    _list.sort(key=takeSecond,reverse=True)
    final_list = list(map(takeFirst,_list))
    return final_list

def is_org_md(path):
    """
    判断文件是否是 org 或者 md
    """
    if (type(path) != str):
        return False
    
    _path_list = path.split('.')
    
    org_flag = False
    md_flag = False

    try: 
    	if _path_list.index('org'):
    	   org_flag = True
    except Exception as e:
    	org_flag = False
    
    try:
    	if _path_list.index('md'):
    	   md_flag = True
    except Exception as e:
    	md_flag = False
    		
    return org_flag or md_flag


def filter_org_md(file_list):
    """
    过滤非 .org .md 文件，只留下 .org .md 文件
    """
    return filter(is_org_md, file_list)    

def wrap_html_body(content_path):
    """
    根据 org 文件 path 拼接出一个完整的 html，添加 header 和 footer
    """
    try:
        header = read_file('/root/code/org-2-html/src/header.html')
        content = convert_org(content_path)
        footer = read_file('/root/code/org-2-html/src/footer.html')

        html = ''.join([header,content,footer])
        return html
    except Exception as e:
        print(e)
        return ''

def get_file_name_by_path(name):
    name_list = name.split('/')
    _len = len(name_list)
    name = '-'.join(name_list[3:_len])
    name_list = name.split('.')
    name = name_list[0] + '.html'
    return name

def test1():
    result = convert_org('/root/org/logbook/2019-06-24.org')
    print result 

def test2():
    result = walk_dir('/root/org/')
    result = filter_org_md(result)
    print(result)

def test3():
    """
    test read file 
    """
    content = read_file('/root/code/org-2-html/src/header.html')
    print(content)


def test4():
    """
    测试合并单个文件
    """
    html = wrap_html_body('/root/org/logbook/2019-06-24.org')
    print(html)

def test5():
    """
    测试合并多个问及那
    """
    file_list = walk_dir('/root/org/')
    for path in file_list:
        _html = wrap_html_body(path)
        print(_html)

def test6():
    """
    测试保存文件
    """
    html = wrap_html_body('/root/org/logbook/2019-06-24.org')
    save_file(html,'/root/code/org-2-html/public/test.html')

def test7():
    """
    test work dir sort 方法
    """
    list = walk_dir_sort('/root/org/')
    print(list)
    
def main():
    """
    测试生成指定 url (文件名称)
    """
    result = walk_dir('/root/org/')
    result = filter_org_md(result)
    for filePath in result:
        # print(filePath)
        html = wrap_html_body(filePath)
        save_path = '/root/code/org-2-html/public/' + get_file_name_by_path(filePath)
        save_file(html,save_path)


def build_index():
    org_list = walk_dir_sort('/root/org')
    org_list = filter_org_md(org_list)
    final_list = []
    for org in org_list:
        print(org)
        link = get_file_name_by_path(org)
        modify_time = datetime.datetime.strptime(time.ctime(os.path.getmtime(org)), "%a %b %d %H:%M:%S %Y")
        # org mode link style  [[http://www.gnu.org/software/emacs/][GNU Emacs]]
        link = str(modify_time) + ' [[' + 'http://org.andyiac.com/' + link + '][' + link[0:len(link)-5] + ']]' + '\n\n'
        final_list.append(link)
       # print(link)

    index_content = u''.join(final_list)
    index_path = '/root/org/index.org'
    save_file(index_content,index_path)
        
    
if __name__ == '__main__':
    build_index()
    main()

#   test7()
