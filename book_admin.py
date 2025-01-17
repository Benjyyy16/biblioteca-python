
import tkinter as tk
from tkinter import messagebox

class BookAdmin:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.init_manage_books()

    def init_manage_books(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Gestión de libros", font=("Arial", 16, "bold")).pack(pady=20)

        self.books_listbox = tk.Listbox(self.root, width=50, font=("Arial", 12))
        self.books_listbox.pack(pady=10)

        self.load_books_into_listbox()

        tk.Button(self.root, text="Agregar libro", command=self.add_book_screen, bg="#007bff", fg="white", font=("Arial", 12), relief="flat").pack(pady=5)
        tk.Button(self.root, text="Eliminar libro", command=self.delete_selected_book, bg="#dc3545", fg="white", font=("Arial", 12), relief="flat").pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.return_to_dashboard, font=("Arial", 12)).pack(pady=10)

    def load_books_into_listbox(self):
        self.books_listbox.delete(0, tk.END)
        books = self.db.get_books()
        for idx, book in enumerate(books):
            self.books_listbox.insert(tk.END, f"{idx+1}. {book['title']} - {book['author']} (Stock: {book['stock']})")

    def add_book_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Agregar nuevo libro", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self.root, text="Título", font=("Arial", 12)).pack(pady=5)
        self.title_entry = tk.Entry(self.root, font=("Arial", 12))
        self.title_entry.pack(pady=5)

        tk.Label(self.root, text="Autor", font=("Arial", 12)).pack(pady=5)
        self.author_entry = tk.Entry(self.root, font=("Arial", 12))
        self.author_entry.pack(pady=5)

        tk.Label(self.root, text="Stock", font=("Arial", 12)).pack(pady=5)
        self.stock_entry = tk.Entry(self.root, font=("Arial", 12))
        self.stock_entry.pack(pady=5)

        tk.Button(self.root, text="Agregar libro", command=self.add_book, bg="#28a745", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.init_manage_books, font=("Arial", 12)).pack(pady=10)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        stock = self.stock_entry.get().strip()

        if title and author and stock.isdigit():
            self.db.add_book({"title": title, "author": author, "stock": int(stock)})
            messagebox.showinfo("Éxito", "Libro agregado con éxito")
            self.init_manage_books()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios y el stock debe ser un número.")

    def delete_selected_book(self):
        selected_idx = self.books_listbox.curselection()
        if selected_idx:
            self.db.delete_book(selected_idx[0])
            messagebox.showinfo("Éxito", "Libro eliminado con éxito")
            self.load_books_into_listbox()
        else:
            messagebox.showerror("Error", "Selecciona un libro para eliminar.")

    def return_to_dashboard(self):
        from admin import AdminApp
        AdminApp(self.root, self.db)
