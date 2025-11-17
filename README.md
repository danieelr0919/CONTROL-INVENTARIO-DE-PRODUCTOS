PROYECTO: SISTEMA DE CONTROL DE INVENTARIO

DESCRIPCIÓN GENERAL:
Aplicación desarrollada en Python para la gestión completa de inventario 
de productos, con interfaz gráfica intuitiva y base de datos MySQL.

FUNCIONALIDADES IMPLEMENTADAS:

1. GESTIÓN DE PRODUCTOS (CRUD COMPLETO):
   - Crear nuevos productos
   - Leer y visualizar todos los productos
   - Actualizar productos existentes
   - Eliminar productos del inventario

2. BÚSQUEDA Y FILTROS AVANZADOS:
   - Búsqueda por nombre (búsqueda parcial)
   - Filtro por rango de precios
   - Filtro por stock máximo
   - Combinación múltiple de filtros

3. INTERFAZ GRÁFICA:
   - 2 pestañas organizadas (Gestión + Búsqueda)
   - Formularios con validación en tiempo real
   - Tablas con scroll para visualización de datos
   - Mensajes de confirmación y error
   - Botones con iconos intuitivos

TECNOLOGÍAS UTILIZADAS:
- Lenguaje: Python 3.x
- Interfaz Gráfica: Tkinter con ttk
- Base de Datos: MySQL
- Paradigma: Programación Orientada a Objetos (POO)

ESTRUCTURA DEL CÓDIGO:
- 1 clase principal (InventarioApp)
- 15+ métodos organizados por funcionalidad
- Separación de responsabilidades en métodos
- Manejo robusto de errores y validaciones

REQUISITOS DE EJECUCIÓN:
1. Python 3.6 o superior instalado
2. MySQL Server ejecutándose (XAMPP recomendado)
3. Base de datos 'inventario_productos' creada
4. Tabla 'productos' con estructura definida
5. Biblioteca: mysql-connector-python

INSTALACIÓN:
1. pip install mysql-connector-python
2. Ejecutar XAMPP y activar MySQL
3. Crear base de datos con script proporcionado
4. Ejecutar: python inventario.py

BASE DE DATOS:
Tabla: productos
- id INT AUTO_INCREMENT PRIMARY KEY
- nombre VARCHAR(100) NOT NULL
- descripcion TEXT
- precio DECIMAL(10,2) NOT NULL
- cantidad INT NOT NULL

- https://github.com/danieelr0919/MODELO-VISTA-CONTROLADOR-.git

