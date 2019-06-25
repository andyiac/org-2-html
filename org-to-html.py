#--coding: utf-8
import os
import sys
import pypandoc;


#import sys 
#reload(sys)
#sys.setdefaultencoding('utf-8')

def convert_org(file_path):
    result = pypandoc.convert_file(file_path, 'html', format='org')
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
        print("----save file error ----")
        print(e)

def walk_dir(dir):
    _list = []
    for root, dirs, files in os.walk(dir, True):
        for name in files:
            _list.append(os.path.join(root,name))
    return _list

def is_org_md(path):
    """
    判断文件是否是 org 或者 md
    """
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
    name = '-'.join(name_list[_len-3:_len])
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
    测试生成指定 url (文件名称)
    """
    result = walk_dir('/root/org/')
    result = filter_org_md(result)
    for filePath in result:
        print(filePath)
        html = wrap_html_body(filePath)
        save_path = '/root/code/org-2-html/public/' + get_file_name_by_path(filePath)
        save_file(html,save_path)


    
if __name__ == '__main__':
    test7()
