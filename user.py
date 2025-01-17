
import tkinter as tk
from tkinter import messagebox

class UserApp:
    def __init__(self, root, db, username):
        self.root = root
        self.db = db
        self.username = username
        self.init_user_dashboard()

    def init_user_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Bienvenido, {self.username}", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Button(self.root, text="Buscar libros", command=self.search_books, bg="#007bff", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)
        tk.Button(self.root, text="Mis libros", command=self.view_my_books, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Cerrar sesión", command=self.logout, bg="#dc3545", fg="white", font=("Arial", 12), relief="flat").pack(pady=20)

    def search_books(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Buscar libros", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self.root, text="Título o autor:", font=("Arial", 12)).pack(pady=5)
        self.search_entry = tk.Entry(self.root, font=("Arial", 12))
        self.search_entry.pack(pady=5)

        tk.Button(self.root, text="Buscar", command=self.perform_search, bg="#007bff", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)

        self.results_listbox = tk.Listbox(self.root, width=50, font=("Arial", 12))
        self.results_listbox.pack(pady=10)

        self.load_all_books()

        tk.Button(self.root, text="Pedir libro", command=self.request_book, bg="#28a745", fg="white", font=("Arial", 12), relief="flat").pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.init_user_dashboard, font=("Arial", 12)).pack(pady=10)

    def load_all_books(self):
        self.results_listbox.delete(0, tk.END)
        books = self.db.get_books()
        for book in books:
            self.results_listbox.insert(tk.END, f"{book['title']} por {book['author']} (Stock: {book['stock']})")

    def perform_search(self):
        query = self.search_entry.get().lower()
        self.results_listbox.delete(0, tk.END)
        books = self.db.get_books()
        for book in books:
            if query in book["title"].lower() or query in book["author"].lower():
                self.results_listbox.insert(tk.END, f"{book['title']} por {book['author']} (Stock: {book['stock']})")

    def request_book(self):
        selected = self.results_listbox.curselection()
        if selected:
            book_title = self.results_listbox.get(selected[0]).split(" por ")[0]
            if self.db.request_book(self.username, book_title):
                messagebox.showinfo("Éxito", f"Has pedido el libro: {book_title}")
            else:
                messagebox.showerror("Error", f"El libro '{book_title}' no está disponible o ya lo tienes.")
        else:
            messagebox.showerror("Error", "Selecciona un libro de la lista.")

    def view_my_books(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Mis libros", font=("Arial", 16, "bold")).pack(pady=20)

        self.my_books_listbox = tk.Listbox(self.root, width=50, font=("Arial", 12))
        self.my_books_listbox.pack(pady=10)

        self.load_user_books()

        tk.Button(self.root, text="Devolver libro", command=self.return_book, bg="#28a745", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.init_user_dashboard, bg="#007bff", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)

    def load_user_books(self):
        self.my_books_listbox.delete(0, tk.END)
        my_books = self.db.get_user_books(self.username)
        if not my_books:
            self.my_books_listbox.insert(tk.END, "No tienes libros en este momento.")
        else:
            for book in my_books:
                self.my_books_listbox.insert(tk.END, book)

    def return_book(self):
        selected = self.my_books_listbox.curselection()
        if selected:
            book_title = self.my_books_listbox.get(selected[0])
            self.db.return_book(self.username, book_title)
            messagebox.showinfo("Éxito", f"Has devuelto el libro: {book_title}")
            self.load_user_books()
        else:
            messagebox.showerror("Error", "Selecciona un libro de la lista para devolver.")

    def logout(self):
        from main import LibraryApp
        LibraryApp(self.root)
