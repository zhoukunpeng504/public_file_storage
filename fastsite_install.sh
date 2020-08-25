# 安装 fastsite 到机器上

# 安装bt
# 目录准备
CRTDIR=$(pwd)
mkdir -p /data
mkdir -p /data/www
dirname='/www'
# echo "the dir name is $dirname"
if [ ! -d $dirname  ];then
  ln -s /data/www /www
else
  echo ''
fi
yum install -y epel-release
yum install -y htop net-tools vim wget svn git gcc gcc-c++ initscripts
wget -O install.sh http://download.bt.cn/install/install_6.0.sh && echo y |sh install.sh

# 对api配置文件进行修改 ,打开bt api
config_json='{"open": true, "token": "abaaaf7c24c5fcc73fc394e208ebda03", "limit_addr": ["127.0.0.1"], "binds": [{"time": 1597743896.5763838, "token": "mvRaBsOZumgBxeWkSv", "status": 0}], "apps": [], "key": "GVqlpFgeSSd9WQR6", "token_crypt": "B3g0qV1sECiJmHAK03OCWz3fHEavbwKo"}'
echo $config_json > /www/server/panel/config/api.json
# 等待安装完成， 然后打印 bt 相关信息 ， mysql 相关信息
/etc/init.d/bt default
# nginx mysql  ftp 安装


# docker pull 镜像


# fastsite django项目  启动

# 打印节点相关信息


