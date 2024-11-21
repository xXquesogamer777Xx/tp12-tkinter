import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Configuración de conexión a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="tu_usuario",       # Reemplaza con tu usuario de MySQL
            password="tu_contraseña", # Reemplaza con tu contraseña de MySQL
            database="Biblioteca"    # Reemplaza con el nombre de tu base de datos
        )
        return conexion
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None

# Ventana principal
def main():
    ventana = tk.Tk()
    ventana.title("Gestión de Biblioteca")
    ventana.geometry("500x400")

    # Botones principales
    tk.Label(ventana, text="Gestión de Biblioteca", font=("Arial", 18)).pack(pady=10)
    tk.Button(ventana, text="Crear Libro", width=20, command=ventana_crear).pack(pady=5)
    tk.Button(ventana, text="Consultar Libros", width=20, command=ventana_consultar).pack(pady=5)
    tk.Button(ventana, text="Actualizar Libro", width=20, command=ventana_actualizar).pack(pady=5)
    tk.Button(ventana, text="Eliminar Libro", width=20, command=ventana_eliminar).pack(pady=5)

    ventana.mainloop()

# Crear un nuevo libro
def ventana_crear():
    crear = tk.Toplevel()
    crear.title("Crear Libro")
    crear.geometry("400x300")

    tk.Label(crear, text="Título:").pack(pady=5)
    titulo_entry = tk.Entry(crear)
    titulo_entry.pack()

    tk.Label(crear, text="ID Autor:").pack(pady=5)
    autor_entry = tk.Entry(crear)
    autor_entry.pack()

    tk.Label(crear, text="ID Género:").pack(pady=5)
    genero_entry = tk.Entry(crear)
    genero_entry.pack()

    tk.Label(crear, text="Fecha de Publicación (YYYY-MM-DD):").pack(pady=5)
    fecha_entry = tk.Entry(crear)
    fecha_entry.pack()

    def guardar():
        titulo = titulo_entry.get()
        id_autor = autor_entry.get()
        id_genero = genero_entry.get()
        fecha = fecha_entry.get()

        if not titulo or not id_autor or not id_genero or not fecha:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            query = "INSERT INTO Libros (titulo, id_autor, id_genero, fecha_publicacion) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (titulo, id_autor, id_genero, fecha))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Libro creado exitosamente.")
            crear.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    tk.Button(crear, text="Guardar", command=guardar).pack(pady=10)

# Consultar libros
def ventana_consultar():
    consultar = tk.Toplevel()
    consultar.title("Consultar Libros")
    consultar.geometry("600x400")

    text_area = tk.Text(consultar, wrap="word")
    text_area.pack(expand=True, fill="both")

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = "SELECT id_libro, titulo, id_autor, id_genero, fecha_publicacion FROM Libros"
        cursor.execute(query)
        libros = cursor.fetchall()
        conexion.close()

        text_area.insert("1.0", "ID\tTítulo\tAutor\tGénero\tFecha\n")
        text_area.insert("2.0", "-" * 50 + "\n")
        for libro in libros:
            text_area.insert("end", f"{libro[0]}\t{libro[1]}\t{libro[2]}\t{libro[3]}\t{libro[4]}\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo consultar la base de datos: {e}")

# Actualizar un libro
def ventana_actualizar():
    actualizar = tk.Toplevel()
    actualizar.title("Actualizar Libro")
    actualizar.geometry("400x300")

    tk.Label(actualizar, text="ID del Libro a Actualizar:").pack(pady=5)
    id_entry = tk.Entry(actualizar)
    id_entry.pack()

    tk.Label(actualizar, text="Nuevo Título:").pack(pady=5)
    titulo_entry = tk.Entry(actualizar)
    titulo_entry.pack()

    def actualizar_libro():
        id_libro = id_entry.get()
        nuevo_titulo = titulo_entry.get()

        if not id_libro or not nuevo_titulo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            query = "UPDATE Libros SET titulo = %s WHERE id_libro = %s"
            cursor.execute(query, (nuevo_titulo, id_libro))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Libro actualizado correctamente.")
            actualizar.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el libro: {e}")

    tk.Button(actualizar, text="Actualizar", command=actualizar_libro).pack(pady=10)

# Eliminar un libro
def ventana_eliminar():
    eliminar = tk.Toplevel()
    eliminar.title("Eliminar Libro")
    eliminar.geometry("400x300")

    tk.Label(eliminar, text="ID del Libro a Eliminar:").pack(pady=5)
    id_entry = tk.Entry(eliminar)
    id_entry.pack()

    def eliminar_libro():
        id_libro = id_entry.get()

        if not id_libro:
            messagebox.showerror("Error", "El ID es obligatorio.")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            query = "DELETE FROM Libros WHERE id_libro = %s"
            cursor.execute(query, (id_libro,))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
            eliminar.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el libro: {e}")

    tk.Button(eliminar, text="Eliminar", command=eliminar_libro).pack(pady=10)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()


