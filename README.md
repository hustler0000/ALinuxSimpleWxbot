# SimpleWxbot
基于https://github.com/danni-cool/wechatbot-webhook，已fork
一个可以记录群员发言时间的简单微信机器人
# 安装
首先安装python以及一些必要组件：
```shell
sudo apt-get update
sudo apt-get install python-is-python3 curl python-pip
```
pip安装需要的库：
```shell
python -m pip install sqlite3
```
安装docker，各发行版安装方法大同小异，这里以Ubuntu为例：
```shell
sudo apt update
sudo apt-get install ca-certificates curl gnupg lsb-release
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
拉取docker镜像
```shell
sudo docker pull dannicool/docker-wechatbot-webhook
```
