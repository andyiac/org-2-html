#--coding: utf-8
import os
import sys
import time, datetime
import pypandoc

def get_file_type(path):
    """
    只是支持 org 或 md 文件
    """
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
    # https://stackoverflow.com/questions/9942594/unicodeencodeerror-ascii-codec-cant-encode-character-u-xa0-in-position-20
    # Python 这个编码问题需要好好研究一下了，遇到过好几次了。
    # result = u''.join((result)).encode('utf-8').strip()
    return result.encode('utf-8').strip()
    
def read_file(full_path):
    try:
        file = open(full_path,"r")
        return file.read().encode('utf-8').strip()
    except Exception as e:
        print("** read file error:" + e)
        return ""

def save_file(content, path):
    try:
        file = open(path,'w')
        file.write(content)
        print("** save file success:" + path)
    except Exception as e:
        print("** save file error:" + path)
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

def generate_html_name_by_path(name):
    """
    根据文件路径生成 html 文件
    """
    name_list = name.split('/')
    _len = len(name_list)
    name = '-'.join(name_list[3:_len])
    name_list = name.split('.')
    name = name_list[0] + '.html'
    return name


def build_index():
    org_list = walk_dir_sort('/root/org')
    org_list = filter_org_md(org_list)
    final_list = []
    for org in org_list:
        print(org)
        link = generate_html_name_by_path(org)
        modify_time = datetime.datetime.strptime(time.ctime(os.path.getmtime(org)), "%a %b %d %H:%M:%S %Y")
        # org mode link style  [[http://www.gnu.org/software/emacs/][GNU Emacs]]
        link = str(modify_time) + ' [[' + 'http://org.andyiac.com/' + link + '][' + link[0:len(link)-5] + ']]' + '\n\n'
        final_list.append(link)
       # print(link)

    index_content = u''.join(final_list)
    index_path = '/root/org/index.org'
    save_file(index_content,index_path)


def build_index_html():
    org_list = walk_dir_sort('/root/org')
    org_list = filter_org_md(org_list)
    final_list = []
    for org in org_list:
        print(org)
        link = generate_html_name_by_path(org)
        modify_time = str(datetime.datetime.strptime(time.ctime(os.path.getmtime(org)), "%a %b %d %H:%M:%S %Y"))
        link = '<li> <a href="' + 'http://org.andyiac.com/' + link + '">'+ link[0:len(link)-5]+'</a> <span class="time">' + modify_time +'</span></li>'
        final_list.append(link)

    try:
        header = read_file('/root/code/org-2-html/src/header.html')
        content = '<ul class="link-list">' + u''.join(final_list) + '</ul>'
        footer = read_file('/root/code/org-2-html/src/footer.html')
        index_content = ''.join([header,content,footer])

        index_path = '/root/code/org-2-html/public/index.html'
        save_file(index_content,index_path)

    except Exception as e:
        print(e)

def build_org_md():
    result = walk_dir('/root/org/')
    result = filter_org_md(result)
    for filePath in result:
        html = wrap_html_body(filePath)
        save_path = '/root/code/org-2-html/public/' + generate_html_name_by_path(filePath)
        save_file(html,save_path)

def build_logbook():
    print("---build log book")
    """
    TODO 
    1. filter logbooks 
    2. merge logbooks (with title change and h1->h2 change) 
    3. save to html 
    4. add 2019 to menu
    """
    org_list = walk_dir_sort('/root/org')
    org_list = filter_org_md(org_list)
    logbook_list = filter(filter_logbook, org_list)
    concate_logbook_list(logbook_list,'/root/org/archive/2019.org')
    
    
def concate_file_list(file_path_list, save_path):
    filenames = file_path_list
    try:
        with open(save_path, 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)
    except Exception as e:
        print("Error: concate_file_list error , save path : " + save_path)
        print(e)

def concate_logbook_list(file_path_list, save_path):
    filenames = file_path_list
    try:
        with open(save_path, 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write('* ' + get_file_name_by_path(fname) + '\n')
                    for line in infile:
                        line = lower_heading(line)
                        outfile.write(line)
    except Exception as e:
        print("Error: concate_file_list error , save path : " + save_path)
        print(e)

def lower_heading(str_line):
	"""
	标题降级
	"""	
	try: 
	    if str_line.index('*') == 0 and str_line.index('* ') >= 0 and str_line.index('* ') <=6:
		str_line = '*' + str_line
		return str_line
	except Exception as e:
	    return str_line
	return str_line        
        
        
def is_date(_date):
    """
    params: _data demo 2019-08-09
    """
    try: 
        _time = time.strptime(_date, '%Y-%m-%d')
        return True 
    except Exception: 
        return False 

def get_file_name_by_path(_path):
    _list = _path.split('.')
    if _list[0]:
        _path = _list[0]
        _list = _path.split('/')
        if len(_list) > 0:
            return _list[len(_list)-1]
    return 'null'


def filter_logbook(_path):
    """
    返回 logbook list
    """
    name = get_file_name_by_path(_path)
    return is_date(name)

def main_build_flow():
    build_logbook()
    build_index_html()
    build_org_md()


if __name__ == '__main__':
    main_build_flow()
#    build_logbook()



################################################################################
#  TEST funcitons 
################################################################################


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
    test walk dir sort 方法
    """
    list = walk_dir_sort('/root/org/')
    print(list)
