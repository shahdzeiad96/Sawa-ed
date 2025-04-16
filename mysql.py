import mysql.connector
dataBase= mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='3171996',

)
cursorObject=dataBase.cursor()
cursorObject.execute("CREATE DATABASE sawaed-db") # here you can change the name based on the database the we will create 

print("data base created")