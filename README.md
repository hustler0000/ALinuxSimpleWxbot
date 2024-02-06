# SimpleWxbot
```
基于https://github.com/danni-cool/wechatbot-webhook
已fork
一个可以记录群员发言时间的简单微信机器人
```
# 安装
首先安装python以及一些必要组件：
```shell
sudo apt-get update
sudo apt-get install python-is-python3 curl python-pip git
```
pip安装需要的库：
```shell
python -m pip install fastapi uvicorn python-multipart apscheduler -i https://pypi.tuna.tsinghua.edu.cn/simple
feedparser，bs4和requests库可装可不装，项目中是为了实现定时推送
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
克隆库
```shell
git clone https://github.com/hustler0000/SimpleWxbot
```
# 初始化
在使用机器人之前，我们需要有一个微信账号来运行机器人，建议使用小号或者直接新注册一个微信账号，建议这个机器人账号添加常用微信号为好友，方便机器人通知反馈。运行机器人的账号必须实名，否则无法登录，也无法使用微信机器人，这是腾讯的限制，与项目无关
## 创建数据库
```
因为技术限制原因，机器人只能获取群成员的微信名称，而不能获取到群昵称，所以需要我们手动先创建一个数据库关联一下
提前现在windows下安装好python，并且pip安装以下库：

pip install ‎pywinauto psutil pandas numpy -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

安装好后在windows下打开微信，进入到你需要的群里，打开【微信=>目标群聊=>聊天成员=>查看更多】，尤其是【查看更多】，否则查找不全！
运行wxbotinit.py，等待程序运行完毕（40秒左右），会产生一个menbers.db文件，其结构和内容应该和给出的示例menbers.db文件类似，如果有出入，请重新生成。
数据库内的username段为微信名称，而roomname段为群昵称
如果有其他更好的办法，请提交issue
```
## 修改主程序
```
将项目克隆到服务器后，用vim或nano等文本编辑器打开simplewxbot.py进行修改：
在程序第64行处，将YourWXname修改为你的微信用户名
在程序第72行处，可以调整自动任务的执行时间，比如seconds=1，minutes=1，hours=1，day=1等
找到程序第159行左右，即"all"功能处，将群名修改为你要部署的群的群名称，将路径改为你存放all_menbers.txt的相应绝对路径
找到程序第176行左右，即"feedback"功能处，将微信名称改为你的微信名称
```
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
```
机器人会默默记下群成员的最后发言时间，@机器人发消息可以触发指令
改昵称必看（重要）：
\nroomname 群昵称 新老群成员可以使用这个修改在数据库里的群昵称，方便机器人称呼和统计最后发言时间，此功能只有在自己修改了群昵称后需要操作一次
\nusername 群昵称 此指令可以修改在数据库里的微信昵称，如果机器人没有提示请不要操作
以上两条指令，如无必要请不要操作，并且不要同时修改群昵称和微信昵称，不然机器人可能会坏掉

常规指令：
help 显示本帮助文档
last 显示本人最后发言时间
search 某人 输出某人的最后发言时间
all 输出一个文件，里面是所有人的最后发言时间
check 检查机器人存活状态
feedback 反馈内容 发送反馈

当有群成员使用发送反馈时，机器人会向你的主微信账号发送反馈内容，当有新群员加入时，机器人也会提醒你引导成员将自己的群昵称添加进数据库内，当然你也可以手动操作数据库来添加。
为了方便地手动操作数据库，还有一个SqliteOperate.py文件，这个python程序提供了简单管理sqlite数据库的条件，运行该程序，并输入相应数据库语句来对你的数据库进行操作。
用post请求访问服务器的3001端口下的/healthz?token=你的token 路径可以检查机器人docker程序是否掉线
用get请求访问服务器8080端口下的/check 路径可以检查机器人python程序是否掉线
```
# 原理
十分简单，因为是二次开发，就是docker收发微信信息，收到的信息通过api转发到python跑的api服务中并且处理
# 存在问题
```
1.程序可能存在sql注入漏洞，可能会导致机器人功能异常
2.目前机器人只能部署到一个群内，部署到多个群需要开启多个docker服务和python脚本，十分麻烦且浪费资源
3.微信定时两天掉线，详细解决方案以及讨论请查看https://github.com/danni-cool/wechatbot-webhook 内的issue。
4.只能用手机先登录机器人的微信账号，然后再扫码登录服务器docker中的微信，而且手机上的机器人微信还不能退出，否则机器人会掉线，即你需要有一台设备一直登录着机器人微信，并且这台设备能随时扫码登录服务器上的微信
```
