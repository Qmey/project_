import tkinter as tk
from tkinter import ttk, Tk, Entry, Frame, Label, PhotoImage, LabelFrame
from tkinter import messagebox
import psycopg2
from PIL import Image, ImageTk
import subprocess

conn = psycopg2.connect(database="Pharmacy",
                        user="postgres",
                        password="12345678",
                        host='localhost',
                        port=5432)
cur = conn.cursor()

def exit_button():
    window.destroy()


def check_enter(event):
    if event.keysym == "Return":
        authenticate()


def authenticate():
    username = entry_username.get()
    password = entry_password.get()

    if not username.isdigit():
        messagebox.showerror("Қателік/Ошибка/Error", "Username should be ID. Example: 404")
    else:
        try:
            cur.execute("SELECT * FROM login WHERE login = %s;", (username,))
            result = cur.fetchone()

            print(f"Query Result: {result}")  # Debugging

            if result and password == str(result[1]):  # Ensure type compatibility
                window.destroy()
                subprocess.run(['python', 'GUI_APP_script.py'])
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")


def on_enter_username(event):
    entry_username.delete(0, 'end')


def on_leave_username(event):
    name = entry_username.get()
    if name == '':
        entry_username.insert(0, 'Username')


def on_enter_password(event):
    entry_password.delete(0, 'end')


def on_leave_password(event):
    enter = entry_password.get()
    if enter == '':
        entry_password.insert(0, 'Password')


# create a main window
window = tk.Tk()
window.title('Forate')
window.geometry("1500x800")
window.attributes('-fullscreen', True)

# create a frame
frame1 = LabelFrame(window, width=600, height=600, border=0)
frame1.pack(side="left")
frame2 = LabelFrame(window, width=900, height=600, border=0)
frame2.pack(side="right")

# create style for entry
style = ttk.Style()
style.configure("Custom.TButton", font=("Arial", 12, "bold"))
style.map("Custom.TButton", foreground=[('focus', 'red')], background=[('focus', 'red')])

# import images
# logo_image = Image.open("C:/Users/Yerlan/OneDrive/Рабочий стол/Education/2_cource/Python+SQL/pictures/LOGO_289x90.png")
# logo_photo = ImageTk.PhotoImage(logo_image)
main_image = Image.open(
    "C:/Users/Yerlan/PycharmProjects/Project/login.jpg")
main_photo = ImageTk.PhotoImage(main_image)

# create button, entry and so on
button_exit = ttk.Button(frame1, text='Exit', style="Custom.TButton", command=exit_button)
label_username = tk.Label(frame1, text='User ID', font=('Arial', 15))
label_password = tk.Label(frame1, text='Password', font=('Arial', 15))
entry_username = ttk.Entry(frame1, font=('Arial', 15))
entry_password = ttk.Entry(frame1, show="*", font=('Arial', 15))
# label_logo = tk.Label(frame1, image=logo_photo)
label_main = tk.Label(frame2, image=main_photo)

# Places for elements(button, entry, images)
label_main.pack()
# label_logo.pack(pady=20, padx=60)
label_username.pack(pady=20, padx=60)
entry_username.pack(pady=20, padx=60)
label_password.pack(pady=20, padx=60)
entry_password.pack(pady=20, padx=60)
button_exit.pack(pady=20, padx=60)

# button checker on laptop
entry_username.insert(0, 'Username')
entry_password.insert(0, 'Password')
entry_username.bind('<FocusIn>', on_enter_username)
entry_username.bind('<FocusOut>', on_leave_username)
entry_password.bind('<FocusIn>', on_enter_password)
entry_password.bind('<FocusOut>', on_leave_password)
entry_password.bind('<KeyPress>', check_enter)

window.mainloop()
