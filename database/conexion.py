import pymysql

def conectar():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="", 
        database="sigirec",
        cursorclass=pymysql.cursors.DictCursor
    )

sql = "SELECT * FROM usuarios"
print(sql)