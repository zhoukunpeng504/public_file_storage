# coding:utf-8
# 运行环境： python2
# 安装 fastsite 到机器上
# 目录准备
import os
import subprocess
import urllib2
import re
import time
import json
import hashlib
from urllib2 import Request, build_opener
from urllib import urlencode, quote


class BTApi:

    def __init__(self, bt_panel , bt_key):
        self.__BT_PANEL = bt_panel
        self.__BT_KEY = bt_key


    #取面板日志
    def get_logs(self):
        #拼接URL地址
        url = self.__BT_PANEL + '/data?action=getData'
        #准备POST数据
        p_data = self.__get_key_data()  #取签名
        p_data['table'] = 'logs'
        p_data['limit'] = 10
        p_data['tojs'] = 'test'
        #请求面板接口
        result = self.__http_post_cookie(url,p_data)
        #解析JSON数据
        return json.loads(result)


    def __get_md5(self,s):
        m = hashlib.md5()
        m.update(s.encode('utf-8'))
        return m.hexdigest()


    #构造带有签名的关联数组
    def __get_key_data(self):
        now_time = int(time.time())
        p_data = {
                    'request_token':self.__get_md5(str(now_time) + '' + self.__get_md5(self.__BT_KEY)),
                    'request_time':now_time
                 }
        return p_data


    #发送POST请求并保存Cookie
    #@url 被请求的URL地址(必需)
    #@data POST参数，可以是字符串或字典(必需)
    #return string
    def __http_post_cookie(self,url,p_data,timeout=20):
        import ssl,http.cookiejar
        data = urlencode(p_data).encode('utf-8')
        req = Request(url,data)
        opener = urllib2.build_opener()
        response = opener.open(req,timeout = timeout)
        result = response.read()
        if type(result) == bytes: result = result.decode('utf-8')
        return result

    def get_logs(self):
        #拼接URL地址
        url = self.__BT_PANEL + '/data?action=getData'
        #准备POST数据
        p_data = self.__get_key_data()  #取签名
        p_data['table'] = 'logs'
        p_data['limit'] = 10
        p_data['tojs'] = 'test'
        #请求面板接口
        result = self.__http_post_cookie(url,p_data)
        #解析JSON数据
        return json.loads(result)


    def install_plugin(self, name, ver, type):
        url = self.__BT_PANEL + '/plugin?action=install_plugin'
        #准备POST数据
        p_data = self.__get_key_data()  #取签名
        p_data['sName'] = 'name'
        p_data['version'] = ver
        p_data['type'] = type
        #请求面板接口
        result = self.__http_post_cookie(url,p_data)
        #解析JSON数据
        return json.loads(result)



#bt_api = BTApi("http://172.19.0.16:8888",'B3g0qV1sECiJmHAK03OCWz3fHEavbwKo')


current_dir = os.path.dirname(__file__)
current_dir = os.path.abspath(current_dir)
os.system("mkdir -p /data")
os.system("mkdir -p /data/www")
if not os.path.exists("/www"):
  os.system("ln -s /data/www /www")
os.system("yum install -y epel-release")
os.system("yum install -y htop net-tools vim wget svn git gcc gcc-c++ initscripts bzip2 docker")
os.system("wget -O install.sh http://download.bt.cn/install/install_6.0.sh && echo y |sh install.sh")
os.system("service docker start")

_p = subprocess.Popen('''ifconfig docker0|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"''',
                      shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
_p.wait()
docker0_ip = _p.stdout.read()

_p = subprocess.Popen('''ifconfig -a|grep inet|grep -v inet6|awk '{print $2}'|tr -d "addr:"''',
                      shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
_p.wait()
all_ip = _p.stdout.read()
all_ip = [i for i in all_ip.strip() if i]
all_ip = list(set(["127.0.0.1"] + [i for i in all_ip if i != docker0_ip]))
config_json='{"open": true, "token": "abaaaf7c24c5fcc73fc394e208ebda03", "limit_addr": [%s], "binds": [{"time": 1597743896.5763838, "token": "mvRaBsOZumgBxeWkSv", "status": 0}], "apps": [], "key": "GVqlpFgeSSd9WQR6", "token_crypt": "B3g0qV1sECiJmHAK03OCWz3fHEavbwKo"}' % \
            (",".join(['"%s"'% i for i in all_ip]))
with open("/www/server/panel/config/api.json", "w") as f:
  f.write(config_json)

local_ip = ''
for i in all_ip:
  if i != '127.0.0.1':
    local_ip = i

bt_url = "http://%s:8888" % local_ip
os.system("/etc/init.d/bt default")

bt_api = BTApi(bt_url,'B3g0qV1sECiJmHAK03OCWz3fHEavbwKo')
# nginx mysql  ftp 安装
for i in ['nginx-1.18:1', 'mysql-5.6:1', 'pureftpd-1.0:0']:
    name,ver,type = re.match("([^-]+)-([\d]+\.[\d]+):(\d)",i).groups()
    _ = bt_api.install_plugin(name, ver, type)
    print _
# ftp 开启

# docker pull 镜像


# fastsite django项目  启动

# 打印节点相关信息


