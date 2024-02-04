from fastapi import FastAPI, Form
import uvicorn
import json
import datetime
import sqlite3 as sl
import os

app = FastAPI()

@app.post("/receive_msg")
async def print_json(source: str=Form(), content: str = Form(), isMentioned: str=Form()):
    a={"success": True}
    source=json.loads(source)
    source=source.get("from")
    source=source.get("payload")
    name=source.get("name")
    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args = content.split("\u2005")
    if(len(args)>1):
        args = args[1]
        args = args.split(" ")
    sql="select * from POST where username='%s'" % (name)
    conn = sl.connect('menbers.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    if(data==""):
        sql="replace into POST(username,last_post_time) values('%s','%s')" % (name, time)
        cursor.execute(sql)
        a = {"success": True, "data": {"type": "text", "content": "我还不认识你，可能因为你是新成员，或者改了微信昵称，不过我已经把你加到我的小本本里了，如果你是新人，请使用：\nroomname 群昵称\n这条指令，在我的小本本上记下你的群昵称，欢迎你入群！\n\n如果你是修改了微信昵称，请使用：\nusername 你的群昵称\n在我的小本本上记下你的新微信昵称\n请不要同时修改微信昵称和群昵称，不然我真的记不过来呀[流泪]望见谅\n\n@我并输入help可以呼出我的帮助菜单哦！"}}
        cmd = 'curl --location "http://localhost:3001/webhook/msg" --header "Content-Type: application/json" --data \'{"to": "Doom.","type": "text","content":"群内有新成员或者有人改了微信昵称，新人或者昵称为' + name + '，请迅速检查处理!"}\''
        os.system(cmd)
    elif(isMentioned!="1"):
        sql="update POST set last_post_time='%s' where username='%s'" % (time,name)
        cursor.execute(sql)
    else:
        a={"success": True,"data": {"type": "text","content":"@"+name+"\u2005真闲！不过如果你真的无聊的话，可以试试sql注入我，帮助主人找漏洞哦！先在此谢过了！"}}
        if(args[0]=="roomname"):
            sql="update POST set roomname='%s' where username='%s'" % (args[1],name)
            cursor.execute(sql)
        if(args[0]=="username"):
            sql="update POST set username='%s' where roomname=%'s'" % (name,args[1])
            cursor.execute(sql)
            sql = "delete from POST where username='%s' and roomname is null"
            cursor.execute(sql)
        if(args[0]=="check"):
            a = {"success": True, "data": {"type": "text", "content":"alive!"}}
        if(args[0]=="help"):
            a={"success": True,"data": {"type": "text","content": "我是Scr1ptKidB0t，我会默默记下大家的最后发言时间\n@我发消息可以触发指令，大家@我的时候要我回复了才能继续@哦：\n\n改昵称必看（重要）：\nroomname 群昵称 新老群成员可以使用这个修改在小本本里的群昵称，方便我称呼和统计最后发言时间，此功能只有在自己修改了群昵称后需要操作一次哦\nusername 群昵称 此指令可以修改在小本本里的微信昵称，如果机器人没有提示请不要操作\n以上两条指令，如无必要请不要操作，并且不要同时修改群昵称和微信昵称，不然机器人可能会坏掉，谢谢\n\nhelp 显示本帮助文档\nlast 显示本人最后发言时间\nsearch 某人 输出某人的最后发言时间\nall 输出一个文件，里面是所有人的最后发言时间\ncheck 检查机器人存活状态\nfeedback 反馈内容 发送反馈\n\n项目地址：https://github.com/hustler0000/SimpleWxbot\n\n希望大家珍惜我，不要@我刷屏，不要连续@我，玩坏了掉线了及时告知我的主人，希望能和大家一起进步呀"}}
        if(args[0]=="last"):
            sql="select roomname,last_post_time from POST where username='%s'" % (name)
            cursor.execute(sql)
            data = cursor.fetchall()
            data=str(data)
            data=data.split(",")
            dname=data[0]
            dname=dname[3:-1]
            dtime=data[1]
            dtime=dtime[2:-3]
            a={"success": True,"data": {"type": "text","content": "你好"+dname+"\n你最后的发言时间是："+dtime+"\n记得要多发言，营造活跃的群内气氛哦！"}}
        if(args[0]=="search"):
            menb=args[1]
            sql="select roomname,last_post_time from POST where username='%s' or roomname='%s'" % (menb,menb)
            cursor.execute(sql)
            data = cursor.fetchall()
            data=str(data)
            data=data.split(",")
            dname=data[0]
            dname=dname[3:-1]
            dtime=data[1]
            dtime=dtime[2:-3]
            a={"success": True,"data": {"type": "text","content": "你好"+name+"\n"+dname+"最后的发言时间是："+dtime+"\n记得要多发言，营造活跃的群内气氛哦！"}}
        if(args[0]=="all"):
            os.system("rm -rf all_menbers.txt")
            sql="select id,roomname,last_post_time from POST"
            cursor.execute(sql)
            data = cursor.fetchall()
            with open("all_menbers.txt", "a") as f:
                for item in data:
                    item=str(item)
                    item=item.split(",")
                    roomname=item[1]
                    roomname=roomname[2:-1]
                    time=item[2]
                    time=time[2:-2]
                    f.write(roomname+" "+time+"\n")
                f.close()
            os.system("curl --location --request POST 'http://localhost:3001/webhook/msg' --form 'to=你的群名' --form content=@'你的部署路径/all_menbers.txt' --form 'isRoom=1'")
            a={"success": True,"data": {"type": "text","content":"以上是大家的发言时间记录，请大家踊跃发言，一起成长呀"}}
        if(args[0]=="feedback"):
            sql="select roomname from POST where username='%s'" % (name)
            cursor.execute(sql)
            data = cursor.fetchall()
            data=str(data)
            data=data.split(",")
            dname=data[0]
            dname=dname[3:-1]
            a={"success": True,"data": {"type": "text","content":"成员"+dname+"，你的反馈我已经告诉主人了，感谢你的支持呀！"}}
            fb=args[1]
            cmd='curl --location "http://localhost:3001/webhook/msg" --header "Content-Type: application/json" --data \'{"to": "你的微信名称","type": "text","content":"群内的'+dname+'发送了反馈，内容为'+fb+'，请迅速处理!"}\''
            os.system(cmd)
    conn.commit()
    conn.close()
    return a

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
