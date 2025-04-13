import mysql.connector
from mysql.connector import Error

try:
    # Veritabanı bağlantısını oluşturma
    VeriTabani1 = mysql.connector.connect(
        host="104.198.166.82",   # Default olarak 'localhost'
        user="root",        # MySQL kullanıcı adı
        password="2580"     # MySQL WorkBench kurarken belirlediğiniz şifre
    )

    if VeriTabani1.is_connected():
        # Cursor oluşturma ve veritabanı yaratma komutu
        secilenVT = VeriTabani1.cursor()

        # PROJE3 veritabanını oluşturma
        secilenVT.execute("CREATE DATABASE IF NOT EXISTS PROJE3")
        print("PROJE3 veritabanı başarıyla oluşturuldu veya zaten mevcut.")

        # PROJE3 veritabanını seçme
        secilenVT.execute("USE PROJE3")

        # rehber tablosunu oluşturma
        secilenVT.execute("""
            CREATE TABLE kayitli_ogrenciler2 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                class VARCHAR(50),
                phone VARCHAR(20),
                graduation VARCHAR(50),
                teacher VARCHAR(255)
            );
        """)
        print("Kayitli_ogrenciler1 tablosu başarıyla oluşturuldu veya zaten mevcut.")
    
except Error as e:
    # Hata durumunda hatayı yazdırma
    print("İşlem sırasında bir hata oluştu:", e)

finally:
    # Veritabanı bağlantısını kapatma
    if VeriTabani1.is_connected():
        secilenVT.close()
        VeriTabani1.close()
        print("Veritabanı bağlantısı kapatıldı.")

