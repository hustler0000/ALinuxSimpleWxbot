# SimpleWxbot
基于https://github.com/danni-cool/wechatbot-webhook
已fork
一个可以记录群员发言时间的简单微信机器人
# 安装
首先安装python以及一些必要组件：
```shell
sudo apt-get update
sudo apt-get install python-is-python3 curl python-pip
```
pip安装需要的库：
```shell
python -m pip install fastapi uvicorn python-multipart -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```
然后安装docker，各发行版安装方法大同小异，这里以Ubuntu为例：
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
# 初始化
因为技术限制原因，机器人只能获取群成员的微信名称，而不能获取到群昵称，所以需要我们手动先创建一个数据库关联一下
提前现在windows下安装好python，并且pip安装以下库：
```shell
pip install ‎pywinauto psutil pandas numpy -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```
安装好后在windows下打开微信，进入到你需要的群里，打开【微信=>目标群聊=>聊天成员=>查看更多】，尤其是【查看更多】，否则查找不全！
运行wxbotinit.py，等待程序运行完毕（40秒左右），会产生一个menbers.db文件，其结构和内容应该和给出的示例menbers.db文件类似，如果有出入，请重新生成。
数据库内的username段为微信名称，而roomname段为群昵称
如果有其他更好的办法，请提交issue
# 主程序
该机器人适用于linux服务器环境，这里只做linux服务器的说明
## 启动
使用命令
```shell
service docker start #启动docker后使用ifconfig查看docker0网卡的ip地址
docker run -d --name wxBotWebhook -p 3001:3001 -e LOGIN_API_TOKEN="YourToken" -e RECVD_MSG_API="http://YourDockerIP:8080/receive_msg" dannicool/docker-wechatbot-webhook # 在YourToken处填入一个你喜欢的字符串做token，在YourDockerIP处填入docker0网卡的ip地址
docker logs -f wxBotWebhook # 启动日志，可以在这里扫码登录微信机器人，会输出机器人的一些状态
nohup python simplewxbot.py & # 后台持续运行wxbot
```
## 帮助/功能菜单

为了方便，还有一个SqliteOperate.py文件，这个python程序提供了简单管理sqlite数据库的条件，运行该程序，并输入相应数据库语句来对你的数据库惊醒
