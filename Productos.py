import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error


class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario Productos")
        self.root.geometry("1000x800")
        self.root.configure(background="#d9d9d9")
        self.crear_notebook()
        self.crear_pestañas()
        
        # CONEXION A LA BASE DE DATOS
        
        self.conn = self.crear_conexion_mysql()
    
    def crear_conexion_mysql(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="inventario_productos"
            )
            return conn
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
    
    # CREAR EL NOTEBOOK DE LAS PESTAÑAS 
    
    def crear_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

    # CREACION DE LAS PESTAÑAS 
    # PESTAÑA 1: GESTION DE PRODUCTOS
    def crear_pestañas(self):
        self.tab_gestion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_gestion, text="Gestion de productos")
        self.crear_inventario_productos()

        # PESTAÑA 2 : busqueda y filtros
        self.tab_busqueda = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_busqueda, text="Busqueda y Filtros")
        self.crear_inventario_busquedas()
        
        # FUNCIONES PARA CARGAR DATOS DE LAS TABLAS 
        
    def cargar_productos(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion, precio, cantidad FROM productos")
            
            # OBTENER TODOS LOS PRODUCTOS
            productos = cursor.fetchall()
            
            for item in self.tabla_productos.get_children():
                self.tabla_productos.delete(item)
                
            # INSERTAR LOS PRODUCTOS EN LA TABLA
            for producto in productos:
                self.tabla_productos.insert("", "end", values=producto)
            
            print(f"{len(productos)} productos cargados correctamente")
            
            cursor.close()
            
        except Exception as e:
            print(f"Error al cargar los productos: {e}")

    # ------------------ CRUD Y VALIDACIONES ------------------
    def guardar_producto(self):
        nombre = self.nombre_producto.get().strip()
        descripcion = self.descripcion_producto.get().strip()
        precio_text = self.precio_producto.get().strip()
        cantidad_text = self.cantidad_stock.get().strip()

        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "El nombre del producto es obligatorio.")
            return
        try:
            precio = float(precio_text)
            if precio < 0:
                raise ValueError()
        except Exception:
            messagebox.showerror("Error", "El precio debe ser un número mayor o igual a 0.")
            return
        try:
            cantidad = int(cantidad_text)
            if cantidad < 0:
                raise ValueError()
        except Exception:
            messagebox.showerror("Error", "La cantidad debe ser un entero mayor o igual a 0.")
            return

        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, descripcion, precio, cantidad) VALUES (%s, %s, %s, %s)",
                (nombre, descripcion, precio, cantidad)
            )
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
            self.limpiar_producto()
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto: {e}")

    def actualizar_producto(self):
        id_text = self.producto_id.get().strip()
        if not id_text.isdigit():
            messagebox.showerror("Error", "Debe indicar un ID válido para actualizar.")
            return
        producto_id = int(id_text)

        nombre = self.nombre_producto.get().strip()
        descripcion = self.descripcion_producto.get().strip()
        precio_text = self.precio_producto.get().strip()
        cantidad_text = self.cantidad_stock.get().strip()

        if not nombre:
            messagebox.showerror("Error", "El nombre del producto es obligatorio.")
            return
        try:
            precio = float(precio_text)
            if precio < 0:
                raise ValueError()
        except Exception:
            messagebox.showerror("Error", "El precio debe ser un número mayor o igual a 0.")
            return
        try:
            cantidad = int(cantidad_text)
            if cantidad < 0:
                raise ValueError()
        except Exception:
            messagebox.showerror("Error", "La cantidad debe ser un entero mayor o igual a 0.")
            return

        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, cantidad=%s WHERE id=%s",
                (nombre, descripcion, precio, cantidad, producto_id)
            )
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            self.limpiar_producto()
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")

    def eliminar_producto(self):
        id_text = self.producto_id.get().strip()
        if not id_text.isdigit():
            messagebox.showerror("Error", "Debe indicar un ID válido para eliminar.")
            return
        producto_id = int(id_text)

        if not messagebox.askyesno("Confirmar", "¿Desea eliminar el producto seleccionado?"):
            return

        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id=%s", (producto_id,))
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            self.limpiar_producto()
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")

    def limpiar_producto(self):
        self.producto_id.delete(0, tk.END)
        self.nombre_producto.delete(0, tk.END)
        self.descripcion_producto.delete(0, tk.END)
        self.precio_producto.delete(0, tk.END)
        self.cantidad_stock.delete(0, tk.END)

    def on_producto_select(self, event):
        selected = self.tabla_productos.selection()
        if not selected:
            return
        values = self.tabla_productos.item(selected[0])['values']
        if not values:
            return

        try:
            self.producto_id.delete(0, tk.END)
            self.producto_id.insert(0, values[0])
            self.nombre_producto.delete(0, tk.END)
            self.nombre_producto.insert(0, values[1])
            self.descripcion_producto.delete(0, tk.END)
            self.descripcion_producto.insert(0, values[2])
            self.precio_producto.delete(0, tk.END)
            self.precio_producto.insert(0, values[3])
            self.cantidad_stock.delete(0, tk.END)
            self.cantidad_stock.insert(0, values[4])
        except Exception:
            pass
    

        # MODULO 1: GESTION DE PRODUCTOS

    def crear_inventario_productos(self):
        titulo = tk.Label(self.tab_gestion, text="Gestion de Productos", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        titulo.pack(padx=20, pady=20)

        # Frame del Formulario
        form_frame = tk.Frame(self.tab_gestion, bg="#d9d9d9", padx=20, pady=20, relief="groove", bd=1)
        form_frame.pack(padx=20, pady=20, fill="x")

        # CAMPOS DEL INVENTARIO DE PRODUCTOS
        tk.Label(form_frame, text="ID :" , bg="#d9d9d9", font=("Arial", 12)).grid(column=0, row=0,sticky="w", pady=5)

        self.producto_id = tk.Entry(form_frame, width=30)
        self.producto_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Nombre del Producto  :", bg="#d9d9d9", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.nombre_producto = tk.Entry(form_frame, width=30)
        self.nombre_producto.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Descripcion del Producto  :", bg="#d9d9d9", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
        self.descripcion_producto = tk.Entry(form_frame, width=30)
        self.descripcion_producto.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Precio :", bg="#d9d9d9", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
        self.precio_producto = tk.Entry(form_frame, width=30)
        self.precio_producto.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Cantidad en stock :", bg="#d9d9d9", font=( "Arial", 12)).grid(row=4, column=0, padx=5, pady=5)
        self.cantidad_stock = tk.Entry(form_frame, width=30)
        self.cantidad_stock.grid(row=4, column=1, padx=5, pady=5)

        # BOTONES DE GESTION DE PRODUCTOS

        btn_frame = tk.Frame(self.tab_gestion, bg="#d9d9d9")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="✅ Guardar", bg="#28a745", fg="white", width=12, command=self.guardar_producto).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Actualizar", bg="#17a2b8", fg="white", width=12, command=self.actualizar_producto).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", bg="#dc3545", fg="white", width=12, command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#6c757d", fg="white", width=12, command=self.limpiar_producto).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Cargar Datos", bg="#ffc107", fg="black", width=12, command=self.cargar_productos).pack(side=tk.LEFT, padx=5)
        
        # TABLA DE PRODUCTOS
        tabla_frame = tk.Frame(self.tab_gestion, bg="#d9d9d9")
        tabla_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # TITULO DE LA TABLA 
        tk.Label(tabla_frame, text=" Lista De Productos", font=("Arial", 16, "bold"), bg="#d9d9d9", fg="#2c3e50").pack(pady=10)
        
        # CREAMOS EL TREEVIEW PARA LAS TABLAS
        columnas = ("ID", "Nombre", "Descripcion", "Precio", "Cantidad")
        self.tabla_productos = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)
        
        # CONFIGURAR LAS COLUMNAS 
        self.tabla_productos.heading("ID", text="ID")
        self.tabla_productos.heading("Nombre", text="Nombre")
        self.tabla_productos.heading("Descripcion", text="Descripcion")
        self.tabla_productos.heading("Precio", text="Precio")
        self.tabla_productos.heading("Cantidad", text="Cantidad")
        
        # AJUSTAR EL TAMAÑO DE LAS COLUMNAS PARA LA INFORMACION 
        self.tabla_productos.column("ID", width=50)
        self.tabla_productos.column("Nombre", width=200)
        self.tabla_productos.column("Descripcion", width=200)
        self.tabla_productos.column("Precio", width=100)
        self.tabla_productos.column("Cantidad", width=100)
        
        # CREAMOS UN SCROLLBAR PARA LA TABLA
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        
        self.tabla_productos.pack( side="left",fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # LLENAR LA TABLA CON LOS DATOS DE LA BASE DE DATOS
        self.tabla_productos.bind("<<TreeviewSelect>>", self.on_producto_select)
        
        

    def crear_inventario_busquedas(self):

        # MODULO 2 : BUSQUEDA Y FILTROS
        titulo = tk.Label(self.tab_busqueda, text="🔍 Busqueda y Filtros", font=( "Arial", 16, "bold"), fg="white", bg="#2c3e50")
        titulo.pack(padx=20, pady=20)

        # Frame del Formulario
        form_frame = tk.Frame(self.tab_busqueda, bg="#d9d9d9", padx=20, relief="groove", bd=1)
        form_frame.pack(padx=20, pady=20)

        # CAMPOS DE LA BUSQUEDA Y FILTROS
        tk.Label(form_frame, text="Buscar Por Nombre :", bg="#f8f0e3", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)

        self.buscar_producto_entry = tk.Entry(form_frame, width=30)
        self.buscar_producto_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Filtro por Rangos de Precio :", bg="#f8f0e3", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)

        self.filtrar_producto_entry = tk.Entry(form_frame, width=30)
        self.filtrar_producto_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Filtro por Stock :", bg="#f8f0e3",font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)

        self.filtro_stock_entry = tk.Entry(form_frame, width=30)
        self.filtro_stock_entry.grid(row=2, column=1, padx=5, pady=5)

        # BOTONES DE BUSQUEDA Y FILTROS
        btn_frame = tk.Frame(self.tab_busqueda, bg="#d9d9d9")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="🔍 Buscar", bg="#ffc107", fg="black", width=12, command=self.ejecutar_busqueda).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🧹 Limpiar Filtros", bg="#6c757d", fg="white", width=12, command=self.limpiar_filtros).pack(side=tk.LEFT, padx=5)
        
        # TABLA DE BUSQUEDAS Y FILTROS 
        tabla_frame = tk.Frame(self.tab_busqueda, bg="#d9d9d9")
        tabla_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # TITULO DE LA TABLA
        tk.Label(tabla_frame, text="Busqueda y Filtros", font=("Arial", 16, "bold"), bg="#d9d9d9", fg="#2c3e50").pack(pady=10)
        
        # CREAMOS EL TREEVIEW PARA LAS TABLAS
        columnas = ("ID", "Nombre", "Descripcion", "Precio", "Cantidad")
        self.tabla_busqueda = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)
        
        # CONFIGURAR LAS COLUMNAS 
        self.tabla_busqueda.heading("ID", text="ID")
        self.tabla_busqueda.heading("Nombre", text="Nombre")
        self.tabla_busqueda.heading("Descripcion", text="Descripcion")
        self.tabla_busqueda.heading("Precio", text="Precio")
        self.tabla_busqueda.heading("Cantidad", text="Cantidad")
        
        # AJUSTAR EL TAMAÑO DE LAS COLUMNAS PARA LA INFORMACION 
        self.tabla_busqueda.column("ID", width=50)
        self.tabla_busqueda.column("Nombre", width=200)
        self.tabla_busqueda.column("Descripcion", width=200)
        self.tabla_busqueda.column("Precio", width=100)
        self.tabla_busqueda.column("Cantidad", width=100)
        
        # CREAMOS UN SCROLLBAR PARA LA TABLA
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_busqueda.yview)
        self.tabla_busqueda.configure(yscrollcommand=scrollbar.set)
        
        self.tabla_busqueda.pack( side="left",fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Métodos de búsqueda y filtros
        
    def ejecutar_busqueda(self):
        nombre = self.buscar_producto_entry.get().strip()
        rango_precio = self.filtrar_producto_entry.get().strip()
        filtro_stock = self.filtro_stock_entry.get().strip()

        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos.")
            return

        query = "SELECT id, nombre, descripcion, precio, cantidad FROM productos WHERE 1=1"
        params = []

        if nombre:
            query += " AND nombre LIKE %s"
            params.append(f"%{nombre}%")

        # rango_precio esperado como "min-max"
        if rango_precio:
            try:
                if "-" in rango_precio:
                    min_p, max_p = rango_precio.split("-", 1)
                    min_p = float(min_p.strip())
                    max_p = float(max_p.strip())
                    query += " AND precio BETWEEN %s AND %s"
                    params.extend([min_p, max_p])
                else:
                    # si sólo un número, buscar precio exacto
                    p = float(rango_precio)
                    query += " AND precio = %s"
                    params.append(p)
            except Exception:
                messagebox.showerror("Error", "El rango de precio debe tener el formato min-max o un número.")
                return

        if filtro_stock:
            try:
                s = int(filtro_stock)
                query += " AND cantidad <= %s"
                params.append(s)
            except Exception:
                messagebox.showerror("Error", "El filtro de stock debe ser un entero.")
                return

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, tuple(params))
            resultados = cursor.fetchall()
            cursor.close()

            # Limpiar tabla de busqueda
            for item in self.tabla_busqueda.get_children():
                self.tabla_busqueda.delete(item)

            for fila in resultados:
                self.tabla_busqueda.insert("", "end", values=fila)

            messagebox.showinfo("Resultados", f"{len(resultados)} productos encontrados.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar la búsqueda: {e}")

    def limpiar_filtros(self):
        try:
            self.buscar_producto_entry.delete(0, tk.END)
            self.filtrar_producto_entry.delete(0, tk.END)
            self.filtro_stock_entry.delete(0, tk.END)
            for item in self.tabla_busqueda.get_children():
                self.tabla_busqueda.delete(item)
        except Exception:
            pass
        

        
if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()


