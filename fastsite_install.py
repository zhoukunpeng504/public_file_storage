# coding:utf-8
# 运行环境： python2
# 安装 fastsite 到机器上
# 目录准备
from __future__ import print_function
import os
import subprocess
import urllib2
import re
import time
import json
import hashlib
from urllib2 import Request, build_opener
from urllib import urlencode, quote
import sys

panelPath = '/www/server/panel/'
#os.chdir(panelPath)
sys.path.append(panelPath + "class/")


def set_panel_pwd(username,password):
    import public, db
    sql = db.Sql()
    if len(username) < 3: return public.returnMsg(False, 'USER_USERNAME_LEN')
    if len(password) < 5: return public.returnMsg(False, 'USER_PASSWORD_LEN')
    # 修改用户名
    public.M('users').where('id=?',(1,)).setField('username', username)
    # 修改密码
    sql.table('users').where('id=?',(1,)).setField('password',public.password_salt(public.md5(password),uid=1))
    print("|-用户名: " + username)
    print("|-新密码: " + password)
    return public.returnMsg(True, '修改成功')


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
        data = urlencode(p_data).encode('utf-8')
        req = Request(url,data)
        opener = urllib2.build_opener()
        response = opener.open(req,timeout = timeout)
        result = response.read()
        if type(result) == bytes: result = result.decode('utf-8')
        return result


    def install_plugin(self, name, ver, type):
        url = self.__BT_PANEL + '/plugin?action=install_plugin'
        #准备POST数据
        p_data = self.__get_key_data()  #取签名
        p_data['sName'] = name
        p_data['version'] = ver
        p_data['type'] = type
        #请求面板接口
        #print(p_data)
        result = self.__http_post_cookie(url,p_data)
        #解析JSON数据
        return json.loads(result)


    def set_admin_path(self, admin_path):
        url = self.__BT_PANEL + '/config?action=set_admin_path'
        #准备POST数据
        p_data = self.__get_key_data()  #取签名
        p_data['admin_path'] = admin_path
        #请求面板接口
        result = self.__http_post_cookie(url,p_data)
        #解析JSON数据
        return json.loads(result)


    def get_task_speed(self):
        url = self.__BT_PANEL + '/files?action=GetTaskSpeed'
        #准备POST数据
        p_data = self.__get_key_data()  #取签名
        #请求面板接口
        result = self.__http_post_cookie(url,p_data)
        #解析JSON数据
        return json.loads(result)


    def add_ftp_user(self, user, passwd, path):
        url = self.__BT_PANEL + '/ftp?action=AddUser'
        #准备POST数据
        p_data = self.__get_key_data()  #取签名
        p_data['ftp_username'] = user
        p_data['ftp_password'] = passwd
        p_data['path'] = path
        p_data['ps'] = user
        #请求面板接口
        result = self.__http_post_cookie(url,p_data)
        #解析JSON数据
        return json.loads(result)


    def add_database(self, db_name, user, passwd):
        url_path = '/database?action=AddDatabase'
        url = self.__BT_PANEL + url_path
        #准备POST数据
        p_data = self.__get_key_data()  #取签名
        p_data['name'] = db_name
        p_data['codeing'] = 'utf8mb4'
        p_data['db_user'] = user
        p_data['password'] = passwd
        p_data['dtype'] = 'MySQL'
        p_data['dataAccess'] = '%'
        p_data['address'] = '%'
        p_data['ps'] = 'fastsite'
        #请求面板接口
        result = self.__http_post_cookie(url,p_data)
        #解析JSON数据
        return json.loads(result)


#bt_api = BTApi("http://172.19.0.16:8888",'B3g0qV1sECiJmHAK03OCWz3fHEavbwKo')
if __name__ == '__main__':

    def green_print(*msg):
        for _ in msg:
            print('\033[92m%s \033[0m' % _, end=' ')
        print('')


    def red_print(*msg):
        for _ in msg:
            print('\033[91m%s \033[0m' % _, end=' ')
        print('')


    def yellow_print(*msg):
        for _ in msg:
            print('\033[93m%s \033[0m' % _, end=' ')
        print('')

    assert len(sys.argv) == 3
    node_name, secret = sys.argv[1], sys.argv[2]
    node_name = node_name.strip()
    secret = secret.strip()
    assert len(secret) >= 6 ,Exception('secret长度不能小于6')
    if not node_name:
        raise Exception('node_name 参数必须设置')
    else:
        assert re.match("^([a-z,A-Z,0-9]+.){1,10}[a-z,A-Z,0-9]+$", node_name), \
            Exception("node_name 参数不合法")

    # 机器参数优化
    os.system('ulimit -n 10240')
    os.system('sysctl -w net.core.somaxconn=10241')
    with open("/etc/rc.local", "r") as f:
        _rc_local_content = f.read()
    _rc_local_content = _rc_local_content.replace("\nulimit -n 10240",'').rstrip("\n")
    _rc_local_content = _rc_local_content.replace("\nsysctl -w net.core.somaxconn=10241",'').rstrip("\n")
    with open("/etc/rc.local", "w") as f:
        _rc_local_content += "\nulimit -n 10240\n"
        _rc_local_content += '\nsysctl -w net.core.somaxconn=10241\n'
        f.write(_rc_local_content)

    current_dir = os.path.dirname(__file__)
    current_dir = os.path.abspath(current_dir)
    os.system("mkdir -p /root/.pip")
    # with open("/root/.pip/pip.conf", "w") as f:
    #     f.write('')
    os.system("mkdir -p /data")
    os.system("mkdir -p /data/www")
    if not os.path.exists("/www"):
      os.system("ln -s /data/www /www")
    os.system("yum install -y epel-release")
    os.system("yum install -y htop net-tools vim wget svn git gcc gcc-c++ initscripts bzip2 docker lrzsz")
    green_print("yum依赖包安装完成")
    os.system("wget -O install.sh http://download.bt.cn/install/install_6.0.sh && echo y |sh install.sh")
    os.system("service docker start")



    _p = subprocess.Popen('''ifconfig -a|grep inet|grep -v inet6|awk '{print $2}'|tr -d "addr:"''',
                          shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _p.wait()
    all_ip = _p.stdout.read().strip().split()
    all_ip = [i for i in all_ip if i]
    all_ip = list(set(["127.0.0.1"] + all_ip))
    config_json='{"open": true, "token": "abaaaf7c24c5fcc73fc394e208ebda03", "limit_addr": [%s], "binds": [{"time": 1597743896.5763838, "token": "mvRaBsOZumgBxeWkSv", "status": 0}], "apps": [], "key": "GVqlpFgeSSd9WQR6", "token_crypt": "B3g0qV1sECiJmHAK03OCWz3fHEavbwKo"}' % \
                (", ".join(['"%s"'% i for i in all_ip]))
    with open("/www/server/panel/config/api.json", "w") as f:
      f.write(config_json)

    local_ip = ''
    for i in all_ip:
      if i != '127.0.0.1':
        local_ip = i

    bt_url = "http://%s:8888" % local_ip
    bt_key = 'B3g0qV1sECiJmHAK03OCWz3fHEavbwKo'
    bt_api = BTApi(bt_url, bt_key)
    # bt入口 用户 密码修改
    print(bt_api.set_admin_path("/fastsite_bt"))
    #print(bt_api.reset_username('fastsite'))
    #print(bt_api.reset_passwd(secret))
    set_panel_pwd('fastsite', secret)
    green_print("宝塔登录入口已重置为：%s/fastsite_bt" % bt_url)
    green_print("宝塔登录用户已修改为：fastsite")
    green_print("宝塔登录密码已修改为：%s" % secret)
    green_print('宝塔基本参数初始化完成。')
    time.sleep(2)
    print("准备安装mysql nginx pureftpd...")
    time.sleep(2)
    # nginx mysql  ftp 安装
    for i in ['nginx-1.18:1', 'mysql-5.6:1', 'pureftpd-1.0:0']:
        name,ver,_type = re.match("([^-]+)-([\d]+\.[\d]+):(\d)",i).groups()
        for j in range(20):
            time.sleep(3)
            try:
                _ = bt_api.install_plugin(name, ver, _type)
                print(_)
                break
            except Exception as e:
                print("Exception:",str(e))

    # 等待安装完成
    while 1:
        result = bt_api.get_task_speed()
        if result.get('status', None) == False:
            green_print('\n宝塔插件( nginx mysql ftp )安装完成')
            break
        else:
            def wait_():
                msg = ''
                for i in range(20):
                    msg += msg.join('.')
                    a = "请耐心等待安装完成" + '{}'.format(msg)
                    if i % 10 == 0:  # 到第几次重头开始
                        msg = ''
                    print("\r", end='')
                    sys.stdout.flush()
                    sys.stdout.write(a)
                    sys.stdout.flush()
                    time.sleep(0.1)
            wait_()

    # ftp 开启  mysql设置
    try:
        os.mkdir("/data/site_template_dir")
    except:
        pass
    bt_api.add_ftp_user('fastsite', secret, '/data/site_template_dir')
    bt_api.add_database('fastsite', 'fastsite', secret)
    green_print("宝塔 mysql ftp设置完成")

    # 代码下载
    code_tar_name = 'fastsite-082601.tar.bz2'
    os.system("cd /data/ && wget https://raw.githubusercontent.com/zhoukunpeng504/public_file_storage/master/\
    fastsite_release/%s" % code_tar_name)
    # 解压代码
    os.system("cd /data/ && tar -jxvf %s" % code_tar_name)
    os.system("rm -rf /data/%s" % code_tar_name)
    with open("/data/fastsite/config.ini", "w") as f:
        _config_content = '''[fastsite]
# mysql 配置
mysql_host = 127.0.0.1
mysql_port = 3306
mysql_user = fastsite
mysql_passwd = {mysql_passwd}
mysql_db = fastsite
# 网站模板目录
site_template_dir = {template_dir}
# 节点secret，要求： 长度不小于6位， 用途： 调用api鉴权  网站管理  网站数据管理。
node_name = {node_name}
# 默认uwsgi 进程数量， 默认为4。 如果服务器内存大于2G，可以调大这个值
uwsgi_workers = 4
secret = {secret}

bt_url = {bt_url}
bt_key = {bt_key}
# 是否开启debug， 除非是为了调试，请勿开启debug， 否则可能会引起安全问题。
debug = false
\n'''.format(mysql_passwd=secret,
                                                            template_dir='/data/site_template_dir',
                                                            node_name=node_name,
                                                            secret=secret,
                                                            bt_url=bt_url,
                                                            bt_key=bt_key)
        f.write(_config_content)
    # 运行docker
    os.system("docker pull zhoukunpeng504/fastsite_base:0.5")
    green_print('docker 镜像拉取成功')
    os.system("mkdir -p /data/uwsgi/logs")
    os.system("docker run --name=fastsite_py -d -it "
              "-v /data/fastsite/:/data/fastsite -v /data/uwsgi/:/data/uwsgi "
              "-p 8081:8081 --privileged  "
              "--sysctl net.core.somaxconn=10240  "
              "zhoukunpeng504/fastsite_base:0.5  /usr/sbin/init")
    os.system("docker exec -it fastsite_py python3  /data/fastsite/fastsite.py start")
    green_print("运行成功")


