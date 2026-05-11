import threading   # Імпортуємо модуль для роботи з потоками
from socket import *   # Імпортуємо всі класи та функції з модуля socket
from customtkinter import *   # Імпортуємо бібліотеку CustomTkinter для створення UI

class MainWindow(CTk):   # Оголошуємо клас головного вікна, що наслідує CTk
   def __init__(self):   # Конструктор класу
       super().__init__()   # Викликаємо конструктор батьківського класу
       self.geometry('400x900')   # Встановлюємо розмір вікна
       self.label = None   # Ініціалізуємо змінну для Label

       # menu frame
       self.menu_frame = CTkFrame(self, width=30, height=300)   # Створюємо бокову панель
       self.menu_frame.pack_propagate(False)   # Забороняємо авто-зміну розміру
       self.menu_frame.place(x=0, y=0)   # Розташовуємо панель зліва
       self.is_show_menu = False   # Прапорець: чи показане меню
       self.speed_animate_menu = -5   # Швидкість анімації меню
       self.btn = CTkButton(self, text='▶️', command=self.toggle_show_menu, width=30)   # Кнопка для відкриття/закриття меню
       self.btn.place(x=0, y=0)   # Розташування кнопки

       # main
       self.chat_field = CTkTextbox(self, font=('Arial', 14, 'bold'), state='disable')   # Поле для чату (тільки для читання)
       self.chat_field.place(x=0, y=0)   # Розташування поля
       self.message_entry = CTkEntry(self, placeholder_text='Введіть повідомлення:', height=40)   # Поле для введення повідомлення
       self.message_entry.place(x=0, y=0)   # Розташування поля
       self.send_button = CTkButton(self, text='>', width=50, height=40, command=self.send_message)   # Кнопка відправки повідомлення
       self.send_button.place(x=0, y=0)   # Розташування кнопки

       self.username = 'Artem'   # Ім’я користувача
       try:
           self.sock = socket(AF_INET, SOCK_STREAM)   # Створюємо TCP-сокет
           self.sock.connect(('localhost', 8080))   # Підключаємося до сервера
           hello = f"TEXT@{self.username}@[SYSTEM] {self.username} приєднався(лась) до чату!\n"   # Формуємо повідомлення про підключення
           self.sock.send(hello.encode('utf-8'))   # Відправляємо повідомлення
           threading.Thread(target=self.recv_message, daemon=True).start()   # Запускаємо потік для прийому повідомлень
       except Exception as e:
           self.add_message(f"Не вдалося підключитися до сервера: {e}")   # Виводимо помилку

       self.adaptive_ui()   # Викликаємо функцію адаптивного інтерфейсу

   def toggle_show_menu(self):   # Метод для відкриття/закриття меню
       if self.is_show_menu:   # Якщо меню відкрите
           self.is_show_menu = False   # Закриваємо меню
           self.speed_animate_menu *= -1   # Міняємо напрям анімації
           self.btn.configure(text='▶️')   # Змінюємо текст кнопки
           self.show_menu()   # Викликаємо анімацію
       else:   # Якщо меню закрите
           self.is_show_menu = True   # Відкриваємо меню
           self.speed_animate_menu *= -1   # Міняємо напрям анімації
           self.btn.configure(text='◀️')   # Змінюємо текст кнопки
           self.show_menu()   # Викликаємо анімацію
           # setting menu widgets
           self.label = CTkLabel(self.menu_frame, text='Імʼя')   # Додаємо Label у меню
           self.label.pack(pady=30)   # Розташовуємо Label
           self.entry = CTkEntry(self.menu_frame)   # Додаємо поле вводу у меню
           self.entry.pack()   # Розташовуємо поле вводу

   def show_menu(self):   # Метод для анімації меню
       self.menu_frame.configure(width=self.menu_frame.winfo_width() + self.speed_animate_menu)   # Змінюємо ширину меню
       if not self.menu_frame.winfo_width() >= 200 and self.is_show_menu:   # Якщо меню ще не досягло потрібної ширини
           self.after(10, self.show_menu)   # Викликаємо метод знову через 10 мс
       elif self.menu_frame.winfo_width() >= 40 and not self.is_show_menu:   # Якщо меню закривається
           self.after(10, self.show_menu)   # Викликаємо метод знову через 10 мс
           if self.label and self.entry:   # Якщо є Label та Entry
               self.label.destroy()   # Видаляємо Label
               self.entry.destroy()   # Видаляємо Entry

   def adaptive_ui(self):   # Метод для адаптації інтерфейсу
       self.menu_frame.configure(height=self.winfo_height())   # Висота меню = висота вікна
       self.chat_field.place(x=self.menu_frame.winfo_width())   # Зміщуємо чат праворуч від меню
       self.chat_field.configure(width=self.winfo_width() - self.menu_frame.winfo_width(),
                                 height=self.winfo_height() - 40)   # Задаємо розміри чату
       self.send_button.place(x=self.winfo_width() - 50, y=self.winfo_height() - 40)   # Розташовуємо кнопку відправки
       self.message_entry.place(x=self.menu_frame.winfo_width(), y=self.send_button.winfo_y())   # Розташовуємо поле вводу
       self.message_entry.configure(
           width=self.winfo_width() - self.menu_frame.winfo_width() - self.send_button.winfo_width())   # Задаємо ширину поля вводу

       self.after(50, self.adaptive_ui)   # Викликаємо метод знову через 50 мс

   def add_message(self, text):   # Метод для додавання повідомлення у чат
       self.chat_field.configure(state='normal')   # Робимо поле доступним для редагування
       self.chat_field.insert(END, 'Я: ' + text + '\n')   # Додаємо текст у поле
       self.chat_field.configure(state='disable')   # Робимо поле недоступним для редагування

   def send_message(self):   # Метод для відправки повідомлення
       message = self.message_entry.get()   # Отримуємо текст з поля вводу
       if message:   # Якщо повідомлення не порожнє
           self.add_message(f"{self.username}: {message}")   # Додаємо повідомлення у чат
           data = f"TEXT@{self.username}@{message}\n"   # Формуємо рядок для відправки
           try:
               self.sock.sendall(data.encode())   # Відправляємо повідомлення на сервер
           except:
               pass   # Ігноруємо помилки
       self.message_entry.delete(0, END)   # Очищаємо поле вводу

   def recv_message(self):   # Метод для прийому повідомлень
       buffer = ""   # Буфер для накопичення даних
       while True:   # Нескінченний цикл
           try:
               chunk = self.sock.recv(4096)   # Отримуємо дані від сервера
               if not chunk:   # Якщо даних немає
                   break   # Виходимо з циклу
               buffer += chunk.decode()   # Додаємо отримані дані у буфер

               while "\n" in buffer:   # Якщо є завершене повідомлення
                   line, buffer = buffer.split("\n", 1)   # Відділяємо рядок
                   self.handle_line(line.strip())   # Обробляємо рядок
           except:
               break   # Виходимо при помилці
       self.sock.close()   # Закриваємо сокет

   def handle_line(self, line):   # Метод для обробки рядка повідомлення
       if not line:   # Якщо рядок порожній
           return   # Виходимо
       parts = line.split("@", 3)   # Розділяємо рядок на частини
       msg_type = parts[0]   # Тип повідомлення

       if msg_type == "TEXT":   # Якщо повідомлення текстове
           if len(parts) >= 3:   #
               if msg_type == "TEXT":  # Якщо тип повідомлення TEXT
                   if len(parts) >= 3:  # Перевіряємо, що є автор і текст
                       author = parts[1]  # Автор повідомлення
                       message = parts[2]  # Текст повідомлення
                       self.add_message(f"{author}: {message}")  # Додаємо повідомлення у чат
               elif msg_type == "IMAGE":  # Якщо тип повідомлення IMAGE
                   if len(parts) >= 4:  # Перевіряємо, що є автор і назва файлу
                       author = parts[1]  # Автор повідомлення
                       filename = parts[2]  # Назва файлу зображення

                       self.add_message(
                           f"{author} надіслав(ла) зображення: {filename}")  # Додаємо повідомлення про зображення
               else:  # Якщо тип повідомлення невідомий
                   self.add_message(line)  # Просто додаємо рядок у чат
win = MainWindow()   # Створюємо екземпляр головного вікна
win.mainloop()   # Запускаємо головний цикл програми (UI працює поки не закриють вікно)
