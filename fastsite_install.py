# coding:utf-8
# 运行环境： python2
# 安装 fastsite 到机器上
# 目录准备
import os
import subprocess
import urllib


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
all_ip = list(set(["127.0.0.1"] + [i for i in all_ip if i == docker0_ip]))
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

# nginx mysql  ftp 安装


# ftp 开启

# docker pull 镜像


# fastsite django项目  启动

# 打印节点相关信息


