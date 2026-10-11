# Biblioteca Virtual (Python + Tkinter)

Aplicación de escritorio para gestionar una biblioteca: los usuarios piden y devuelven libros, y el administrador gestiona el catálogo y las cuentas. Proyecto académico de programación orientada a objetos en Python.

![Biblioteca Virtual](https://github.com/user-attachments/assets/f09604d0-79a0-437d-ad2a-e7677eb0210b)

## Funcionalidades

**Usuario**
- Registro e inicio de sesión.
- Buscar libros del catálogo.
- Pedir y devolver libros; ver "Mis libros".

**Administrador**
- Agregar y eliminar libros.
- Agregar y eliminar usuarios.

**Seguridad**
- Contraseñas almacenadas con PBKDF2-SHA256 y salt aleatorio.
- Acceso de administrador por rol (`role: "admin"`), sin credenciales en el código.

## Requisitos

- Python 3.10 o superior con Tkinter (incluido en los instaladores oficiales de python.org; en Linux: `sudo apt install python3-tk`).
- Sin dependencias externas.

## Uso

```bash
git clone https://github.com/Benjyyy16/biblioteca-python.git
cd biblioteca-python
python main.py
```

Cuentas de demostración:

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `adm` | `12` |
| Usuario | `user` | `user` |

> Son credenciales de ejemplo. Cámbialas antes de cualquier uso real.

## Estructura

```
├── main.py          # Ventana principal, login y registro
├── user.py          # Vista de usuario (buscar, pedir, devolver)
├── admin.py         # Panel de administración de usuarios
├── book_admin.py    # Gestión de libros
├── database.py      # Persistencia en JSON, hashing y roles
├── books.json       # Catálogo
├── users.json       # Usuarios (contraseñas hasheadas)
├── user_books.json  # Préstamos por usuario
└── tests/           # Tests unitarios
```

## Tests

```bash
python -m unittest discover -s tests -t . -v
```

Se ejecutan automáticamente en cada Pull Request con GitHub Actions (Python 3.10 y 3.12).

## Autor

[Benjamin Aguilar](https://github.com/Benjyyy16) · [aguilarb.tech](https://aguilarb.tech)
