
import tkinter as tk
from tkinter import messagebox
from admin import AdminApp
from user import UserApp
from database import Database

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca Virtual")
        self.root.geometry("600x400")
        self.root.configure(bg="#121212")
        self.db = Database()
        self.init_login_screen()

    def init_login_screen(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título principal
        tk.Label(self.root, text="Bienvenido a la Biblioteca Virtual", font=("Arial", 20, "bold"), fg="white", bg="#121212").pack(pady=20)

        # Usuario
        tk.Label(self.root, text="Usuario:", font=("Arial", 14), fg="white", bg="#121212").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 14), bg="#1e1e1e", fg="white", insertbackground="white", relief="flat")
        self.username_entry.pack(pady=5)

        # Contraseña
        tk.Label(self.root, text="Contraseña:", font=("Arial", 14), fg="white", bg="#121212").pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 14), show="*", bg="#1e1e1e", fg="white", insertbackground="white", relief="flat")
        self.password_entry.pack(pady=5)

        # Botones
        tk.Button(self.root, text="Iniciar Sesión", command=self.login, font=("Arial", 14), bg="#007bff", fg="white", relief="flat").pack(pady=10)
        tk.Button(self.root, text="Registrarse", command=self.create_account_screen, font=("Arial", 14), bg="#28a745", fg="white", relief="flat").pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "adm" and password == "12":
            AdminApp(self.root, self.db)
        elif self.db.verify_user(username, password):
            UserApp(self.root, self.db, username)
        else:
            messagebox.showerror("Error de inicio de sesión", "Credenciales inválidas")

    def create_account_screen(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Crear nueva cuenta", font=("Arial", 20, "bold"), fg="white", bg="#121212").pack(pady=20)

        tk.Label(self.root, text="Usuario:", font=("Arial", 14), fg="white", bg="#121212").pack(pady=5)
        self.new_username_entry = tk.Entry(self.root, font=("Arial", 14), bg="#1e1e1e", fg="white", insertbackground="white", relief="flat")
        self.new_username_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=("Arial", 14), fg="white", bg="#121212").pack(pady=5)
        self.new_password_entry = tk.Entry(self.root, font=("Arial", 14), show="*", bg="#1e1e1e", fg="white", insertbackground="white", relief="flat")
        self.new_password_entry.pack(pady=5)

        tk.Button(self.root, text="Crear cuenta", command=self.create_account, font=("Arial", 14), bg="#28a745", fg="white", relief="flat").pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.init_login_screen, font=("Arial", 14), bg="#dc3545", fg="white", relief="flat").pack(pady=10)

    def create_account(self):
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()

        if username and password:
            if self.db.add_user({"username": username, "password": password}):
                messagebox.showinfo("Éxito", "Cuenta creada con éxito. Ahora puedes iniciar sesión.")
                self.init_login_screen()
            else:
                messagebox.showerror("Error", "El nombre de usuario ya existe.")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
