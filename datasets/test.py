import pymysql  # 导入 pymysql



#连接数据库
db = pymysql.connect(host="127.0.0.1", user="root", password="yuanhua123456", db="testdb", port=3306,charset="utf8")


# 使用cursor()方法获取操作游标
cur = db.cursor()

# 1.查询操作
# 编写sql 查询语句  user 对应我的表名
sql = "select * from tableName"
try:
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    print("id", "name")
    # 遍历结果
    for row in results:
        id = row[0]
        name = row[1]
        print(id, name)
except Exception as e:
    raise e
finally:
    db.close()  # 关闭连接




