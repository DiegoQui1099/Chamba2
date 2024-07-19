import mysql.connector 

database = mysql.connector.connect(
    host='Diego10.mysql.pythonanywhere-services.com',
    user='Diego10',
    password='Samorgap123.',
    database='Diego10$default'
)

cursor = database.cursor()