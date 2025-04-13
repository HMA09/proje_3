import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QTableWidget, 
    QTableWidgetItem
)

# Veritabanı bağlantısı
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="104.198.166.82",  
            user="root",      
            password="2580",  
            database="PROJE3"  
        )
        return connection
    except mysql.connector.Error as err:
        QMessageBox.critical(None, "Veritabanı Hatası", f"Bağlantı hatası: {err}")
        sys.exit(1)

# Giriş ekranı
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Giriş")
        self.setGeometry(100, 100, 300, 200)
        
        # Kullanıcı adı ve şifre alanları
        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()
        
        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Giriş butonu
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.check_login)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "1" and password == "1":
            QMessageBox.information(self, "Başarılı", "Giriş Başarılı!")
            # Giriş başarılı olduğunda rehber ekranını başlat
            self.open_rehber_window()
        else:
            QMessageBox.warning(self, "Hata", "Yanlış kullanıcı adı veya şifre")

    def open_rehber_window(self):
        self.rehber_window = RehberWindow()
        self.rehber_window.show()
        self.close()

class RehberWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Öğrenci Kayıt Programı")  # Pencere adı değiştirildi
        self.setGeometry(100, 100, 800, 600)
        self.connection = create_connection()
        self.init_ui()

    def init_ui(self):
        # Yeni giriş alanları
        self.first_name_label = QLabel("Öğrenci Adı:")
        self.first_name_input = QLineEdit()

        self.last_name_label = QLabel("Öğrenci Soyadı:")
        self.last_name_input = QLineEdit()

        self.class_label = QLabel("Sınıfı:")
        self.class_input = QLineEdit()

        self.phone_label = QLabel("Öğrenci Telefon Numarası:")
        self.phone_input = QLineEdit()

        self.graduation_label = QLabel("Mezuniyeti:")
        self.graduation_input = QLineEdit()

        self.teacher_label = QLabel("Öğretmeni:")
        self.teacher_input = QLineEdit()

        # Ekleme, silme ve güncelleme butonları
        self.add_button = QPushButton("Ekle")
        self.add_button.clicked.connect(self.add_person)

        self.delete_button = QPushButton("Sil")
        self.delete_button.clicked.connect(self.delete_person)

        self.update_button = QPushButton("Güncelle")
        self.update_button.clicked.connect(self.update_person)

        # Kişileri listeleme alanı
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Ad", "Soyad", "Sınıf", "Telefon", "Mezuniyet", "Öğretmen"])
        self.load_data()

        # Layout
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.first_name_label)
        form_layout.addWidget(self.first_name_input)
        form_layout.addWidget(self.last_name_label)
        form_layout.addWidget(self.last_name_input)
        form_layout.addWidget(self.class_label)
        form_layout.addWidget(self.class_input)
        form_layout.addWidget(self.phone_label)
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(self.graduation_label)
        form_layout.addWidget(self.graduation_input)
        form_layout.addWidget(self.teacher_label)
        form_layout.addWidget(self.teacher_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.update_button)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)

    # Veritabanından veri yükleme
    def load_data(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT first_name, last_name, class, phone, graduation, teacher FROM kayitli_ogrenciler2")
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            self.table.setItem(row_idx, 0, QTableWidgetItem(row_data[0]))  # Ad
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))  # Soyad
            self.table.setItem(row_idx, 2, QTableWidgetItem(row_data[2]))  # Sınıf
            self.table.setItem(row_idx, 3, QTableWidgetItem(row_data[3]))  # Telefon
            self.table.setItem(row_idx, 4, QTableWidgetItem(row_data[4]))  # Mezuniyet
            self.table.setItem(row_idx, 5, QTableWidgetItem(row_data[5]))  # Öğretmen

    # Kişi ekleme
    def add_person(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        class_name = self.class_input.text()
        phone = self.phone_input.text()
        graduation = self.graduation_input.text()
        teacher = self.teacher_input.text()

        if first_name and last_name and class_name and phone and graduation and teacher:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO kayitli_ogrenciler2 (first_name, last_name, class, phone, graduation, teacher) VALUES (%s, %s, %s, %s, %s, %s)",
                (first_name, last_name, class_name, phone, graduation, teacher)
            )
            self.connection.commit()
            QMessageBox.information(self, "Başarılı", "Kişi Eklendi!")
            self.load_data()
        else:
            QMessageBox.warning(self, "Hata", "Tüm alanlar doldurulmalıdır.")

    # Kişi silme
    def delete_person(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            first_name = self.table.item(selected_row, 0).text()
            last_name = self.table.item(selected_row, 1).text()

            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM kayitli_ogrenciler2 WHERE first_name=%s AND last_name=%s", (first_name, last_name))
            self.connection.commit()
            QMessageBox.information(self, "Başarılı", "Kişi Silindi!")
            self.load_data()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen silmek için bir kişi seçin.")

    # Kişi güncelleme
    def update_person(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            first_name = self.table.item(selected_row, 0).text()
            last_name = self.table.item(selected_row, 1).text()
            new_first_name = self.first_name_input.text()
            new_last_name = self.last_name_input.text()
            new_class = self.class_input.text()
            new_phone = self.phone_input.text()
            new_graduation = self.graduation_input.text()
            new_teacher = self.teacher_input.text()

            if new_first_name and new_last_name and new_class and new_phone and new_graduation and new_teacher:
                cursor = self.connection.cursor()
                cursor.execute(
                    "UPDATE kayitli_ogrenciler2 SET first_name=%s, last_name=%s, class=%s, phone=%s, graduation=%s, teacher=%s WHERE first_name=%s AND last_name=%s",
                    (new_first_name, new_last_name, new_class, new_phone, new_graduation, new_teacher, first_name, last_name)
                )
                self.connection.commit()
                QMessageBox.information(self, "Başarılı", "Kişi Güncellendi!")
                self.load_data()
            else:
                QMessageBox.warning(self, "Hata", "Tüm alanlar doldurulmalıdır.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen güncellemek için bir kişi seçin.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())