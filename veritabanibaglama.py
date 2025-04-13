import mysql.connector
try:
    bağlantı = mysql.connector.connect(
    host = "104.198.166.82",
    user = "root",
    password = "2580"
    )
    print("Veri Tabanına Bağlandı")
except:
      print("Veri Tabanına Bağlanılamadı")