import json
import os

project_path = os.getcwd()
project_path = project_path.replace('/', "\\")
project_path += "\\"
reuters_path = project_path + "LanguageAnalysis\\Reuters"
print("projectpath:", project_path)
print("Reuters path", reuters_path)


def write2file(item, filename):
    # 将数据写入到文件中
    file = open(filename, 'w')
    str = json.JSONEncoder().encode(item)
    file.write(str)
    file.close()


# 获取文档名中的文档的id
def get_docID(filename):
    end = filename.find('.')
    docId = filename[0:end]
    return int(docId)


def get_whole_docList():
    files = os.listdir(reuters_path)
    file_list = []
    for file in files:
        file_list.append(get_docID(file))
    return sorted(file_list)


print("getting file list...")
wholeDocList = get_whole_docList()
