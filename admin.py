
import tkinter as tk
from book_admin import BookAdmin

class AdminApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.init_admin_dashboard()

    def init_admin_dashboard(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Panel de Administrador", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self.root, text="Gestionar Libros", command=self.manage_books, bg="#007bff", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)
        tk.Button(self.root, text="Gestionar Usuarios", command=self.manage_users, bg="#007bff", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)
        tk.Button(self.root, text="Cerrar Sesión", command=self.logout, bg="#dc3545", fg="white", font=("Arial", 12), relief="flat").pack(pady=20)

    def manage_books(self):
        BookAdmin(self.root, self.db)

    def manage_users(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Gestión de Usuarios", font=("Arial", 16, "bold")).pack(pady=20)

        self.users_listbox = tk.Listbox(self.root, width=30, font=("Arial", 12))
        self.users_listbox.pack(pady=10)

        self.load_users_into_listbox()

        tk.Button(self.root, text="Agregar Usuario", command=self.add_user_screen, bg="#007bff", fg="white", font=("Arial", 12), relief="flat").pack(pady=5)
        tk.Button(self.root, text="Eliminar Usuario", command=self.delete_selected_user, bg="#dc3545", fg="white", font=("Arial", 12), relief="flat").pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.init_admin_dashboard, font=("Arial", 12)).pack(pady=10)

    def load_users_into_listbox(self):
        self.users_listbox.delete(0, tk.END)
        users = self.db.get_users()
        for user in users:
            self.users_listbox.insert(tk.END, f"{user['username']}")

    def add_user_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Agregar Nuevo Usuario", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self.root, text="Usuario", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Agregar Usuario", command=self.add_user, bg="#28a745", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.manage_users, font=("Arial", 12)).pack(pady=10)

    def add_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username and password:
            if self.db.add_user({"username": username, "password": password}):
                messagebox.showinfo("Éxito", "Usuario agregado con éxito")
                self.manage_users()
            else:
                messagebox.showerror("Error", "El usuario ya existe")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def delete_selected_user(self):
        selected_idx = self.users_listbox.curselection()
        if selected_idx:
            username = self.users_listbox.get(selected_idx[0])
            self.db.delete_user(username)
            messagebox.showinfo("Éxito", "Usuario eliminado con éxito")
            self.load_users_into_listbox()
        else:
            messagebox.showerror("Error", "Selecciona un usuario para eliminar.")

    def logout(self):
        from main import LibraryApp
        LibraryApp(self.root)
