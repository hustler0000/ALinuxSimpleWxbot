import sqlite3 as sl

while(1):
    sql = input(">>>")
    con = sl.connect('menbers.db')
    cursor = con.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    print(type(data))
    print(data)
    con.commit()
    con.close()
'''
sql="select id,roomname,last_post_time from POST"
con = sl.connect('menbers.db')
cursor = con.cursor()
cursor.execute(sql)
data = cursor.fetchall()
con.commit()
con.close()
for item in data:
    item=str(item)
    ii=item.split(",")
    i=ii[2]
    print(i[2:-1])

'''
