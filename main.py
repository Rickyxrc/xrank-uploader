import sys,csv,requests,json

__ignore_rows = ['编号','总分'] # 忽略的列
__instant_baseurl = 'http://localhost' # xrank 示例地址
__SECRET_API_KEY = 'apikeyy' # 环境变量API_KEY

__post_headers = {"content-type":"application/json"}

def init():
    global __csv_file_path
    try:
        __csv_file_path = sys.argv[1]
    except IndexError:
        print('arg exceped:path of the csv file.')
        exit(1)

def initcsv():
    global __csv_file,__csv_reader
    global table_header,table_body
    try:
        table_body=[]
        __csv_file = open(__csv_file_path,'r',encoding='utf-8')
        __csv_reader = csv.reader(__csv_file)
        # print(__csv_reader.)
        count=0
        for row in __csv_reader:
            if count==0 :
                table_header = row
            else:
                table_body.append(row)
            count+=1
            # print(row)
            # for e in row:
                # print(e,end=',')
    except Exception as e:
        print(e)

def processcsv():
    global __ignore_rows
    global table_header,table_body
    for __ignore_rows_index in __ignore_rows:
        # 获取忽略的列所在位置
        __tp_index = table_header.index(__ignore_rows_index)
        # 全删
        del table_header[__tp_index]
        for table_body_sub in table_body:
            del table_body_sub[__tp_index]

def get_namelist():
    global __instant_baseurl,__post_headers,__SECRET_API_KEY
    global id_list,name_list
    id_list = []
    name_list = []
    res = requests.post(__instant_baseurl+'/queryuid/?API_KEY='+__SECRET_API_KEY)
    assert res.status_code == 200
    for name in json.loads(res.text):
        id_list.append(name['id'])
        name_list.append(name['name'])

def get_unappeared_names():
    global table_header,table_body,__insert_name_sql
    __tp_notin = []
    for user in table_body:
        user[0] = user[0].strip()
        if user[0] not in name_list and user[0]!="":
            __tp_notin.append(user[0])
            # print(user[0],end='|\n')
    __insert_name_sql = '(\"'+'\"),(\"'.join(__tp_notin)+'\")'

def insert_names():
    global __insert_name_sql
    if __insert_name_sql != '(\"\")':
        assert requests.post(__instant_baseurl+'/adduser/?API_KEY='+__SECRET_API_KEY+'&&data='+__insert_name_sql).status_code == 200

def convert_commandlist():
    global table_header,table_body
    global id_list,name_list
    global api_dat
    api_dat=''
    for user in table_body:
        for i in range(1,len(user)):
            if user[i]!='0': #??????????
                api_dat+='('+str(user[i])+',\"'+str(table_header[i])+'\",'+str(id_list[name_list.index(user[0])])+')'+',' # 语句 values 拼串
    api_dat = api_dat[:-1] # 去除末尾逗号

def upload_data():
    global api_dat
    requests.post(__instant_baseurl+'/upload/?API_KEY='+__SECRET_API_KEY+'&&data='+api_dat).text

init()
initcsv()
processcsv()
get_namelist()
get_unappeared_names()
insert_names()
get_namelist()
convert_commandlist()
upload_data()