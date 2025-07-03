from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_mysqldb import MySQL
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['CARPETAU'] = 'uploads'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbtrastearte'  

mysql = MySQL(app)
principal = app  # Alias

# ----------- RUTAS -----------

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from flask_mysqldb import MySQL
import hashlib
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['CARPETAU'] = 'uploads'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbtrastearte'  

mysql = MySQL(app)
principal = app  # Alias

# ----------- RUTAS DE AUTENTICACIÓN -----------

@principal.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        id_usuario = request.form['id']
        nombre = request.form['nombre']
        contra = request.form['contra']
        cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_usuario FROM usuarios WHERE id_usuario=%s", (id_usuario,))
        existe = cur.fetchone()
        if existe:
            cur.close()
            return render_template("registro.html", msg="El usuario ya existe.")
        sql = "INSERT INTO usuarios (id_usuario, nombre, contrasena) VALUES (%s, %s, %s)"
        cur.execute(sql, (id_usuario, nombre, cifrada))
        mysql.connection.commit()
        cur.close()
        return redirect("/")
    return render_template("registro.html")

@principal.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@principal.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id = request.form['username']
        contra = request.form['password']
        cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
        cur = mysql.connection.cursor()
        sql = f"SELECT nombre FROM usuarios WHERE id={id} and contrasena='{contra}'"
        print(sql)
        cur.execute(sql)
        resultado = cur.fetchall()
        cur.close()
        if len(resultado) > 0:
            session["login"] = True
            session["id"] = id
            session["nombre"] = resultado[0][0]
            return redirect("/opciones")
        else:
            return render_template("index.html", msg="Credenciales incorrectas")
    return render_template("login.html")

@principal.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        id_usuario = request.form['id']
        nombre = request.form['nombre']
        contra = request.form['contra']
        cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_usuario FROM usuarios WHERE id_usuario=%s", (id_usuario,))
        existe = cur.fetchone()
        if existe:
            cur.close()
            return render_template("registrar.html", msg="El usuario ya existe.")
        sql = "INSERT INTO usuarios (id_usuario, nombre, contrasena) VALUES (%s, %s, %s)"
        cur.execute(sql, (id_usuario, nombre, cifrada))
        mysql.connection.commit()
        cur.close()
        return redirect("/")
    return render_template("registrar.html")

@principal.route("/usuario", methods=["GET"])
def usuario():
    if session.get('login'):
        id = session.get('id')
        cur = mysql.connection.cursor()
        sql = "SELECT * FROM usuarios WHERE id_usuario=%s"
        cur.execute(sql, (id,))
        resultado = cur.fetchall()
        cur.close()
        return render_template("usuario.html", usu=resultado[0])
    else:
        return redirect("/")

@principal.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@principal.route("/opciones")
def opciones():
    if session.get('login'):
        return render_template("opciones.html")
    else:
        return redirect("/")

# ----------- RUTAS DE GESTIÓN -----------






@principal.route("/clientes", methods=["GET", "POST"])
def clientes():
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        sql = "INSERT INTO clientes (nombre, direccion, telefono, email, borrado) VALUES (%s, %s, %s, %s, 0)"
        cur.execute(sql, (nombre, direccion, telefono, email))
        mysql.connection.commit()
    sql = "SELECT * FROM clientes WHERE borrado=0"
    cur.execute(sql)
    clientes = cur.fetchall()
    cur.close()
    return render_template("clientes.html", clientes=clientes)

@principal.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        sql = "UPDATE clientes SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE id_cliente=%s"
        cur.execute(sql, (nombre, direccion, telefono, email, id))
        mysql.connection.commit()
        cur.close()
        return redirect("/clientes")
    sql = "SELECT * FROM clientes WHERE id_cliente=%s"
    cur.execute(sql, (id,))
    cliente = cur.fetchone()
    cur.close()
    return render_template("editar_cliente.html", cliente=cliente)

@principal.route("/clientes/eliminar/<int:id>", methods=["POST"])
def eliminar_cliente(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql = "UPDATE clientes SET borrado=1 WHERE id_cliente=%s"
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/clientes")

# ----------- RUTAS DE PROVEEDORES -----------

@principal.route("/provedores", methods=["GET", "POST"])
def provedores():
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        sql = "INSERT INTO proveedores (nombre, direccion, telefono, email, borrado) VALUES (%s, %s, %s, %s, 0)"
        cur.execute(sql, (nombre, direccion, telefono, email))
        mysql.connection.commit()
    sql = "SELECT * FROM proveedores WHERE borrado=0"
    cur.execute(sql)
    proveedores = cur.fetchall()
    cur.close()
    return render_template("proveedores.html", proveedores=proveedores)

@principal.route("/provedores/editar/<int:id>", methods=["GET", "POST"])
def editar_proveedor(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        sql = "UPDATE proveedores SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE id_proveedor=%s"
        cur.execute(sql, (nombre, direccion, telefono, email, id))
        mysql.connection.commit()
        cur.close()
        return redirect("/provedores")
    sql = "SELECT * FROM proveedores WHERE id_proveedor=%s"
    cur.execute(sql, (id,))
    proveedor = cur.fetchone()
    cur.close()
    return render_template("editar_proveedor.html", proveedor=proveedor)

@principal.route("/provedores/eliminar/<int:id>", methods=["POST"])
def eliminar_proveedor(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql = "UPDATE proveedores SET borrado=1 WHERE id_proveedor=%s"
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/provedores")

# ----------- RUTAS DE INVENTARIO -----------

@principal.route("/inventario", methods=["GET", "POST"])
def inventario():
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre")
        cantidad = request.form.get("cantidad")
        precio = request.form.get("precio")
        sql = "INSERT INTO inventario (nombre, cantidad, precio, borrado) VALUES (%s, %s, %s, 0)"
        cur.execute(sql, (nombre, cantidad, precio))
        mysql.connection.commit()
    sql = "SELECT * FROM inventario WHERE borrado=0"
    cur.execute(sql)
    inventario = cur.fetchall()
    cur.close()
    return render_template("inventario.html", inventario=inventario)

@principal.route("/inventario/editar/<int:id>", methods=["GET", "POST"])
def editar_inventario(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre")
        cantidad = request.form.get("cantidad")
        precio = request.form.get("precio")
        sql = "UPDATE inventario SET nombre=%s, cantidad=%s, precio=%s WHERE id_producto=%s"
        cur.execute(sql, (nombre, cantidad, precio, id))
        mysql.connection.commit()
        cur.close()
        return redirect("/inventario")
    sql = "SELECT * FROM inventario WHERE id_producto=%s"
    cur.execute(sql, (id,))
    producto = cur.fetchone()
    cur.close()
    return render_template("editar_inventario.html", producto=producto)

@principal.route("/inventario/eliminar/<int:id>", methods=["POST"])
def eliminar_inventario(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql = "UPDATE inventario SET borrado=1 WHERE id_producto=%s"
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/inventario")

# ----------- RUTAS DE LOTES DE PRODUCTOS -----------

@principal.route("/lote_productos", methods=["GET", "POST"])
def lote_productos():
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre")
        cantidad = request.form.get("cantidad")
        precio = request.form.get("precio")
        sql = "INSERT INTO lote_productos (nombre, cantidad, precio, borrado) VALUES (%s, %s, %s, 0)"
        cur.execute(sql, (nombre, cantidad, precio))
        mysql.connection.commit()
    sql = "SELECT * FROM lote_productos WHERE borrado=0"
    cur.execute(sql)
    lotes = cur.fetchall()
    cur.close()
    return render_template("lote_producto.html", lotes=lotes)

@principal.route("/lote_productos/editar/<int:id>", methods=["GET", "POST"])
def editar_lote(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre")
        cantidad = request.form.get("cantidad")
        precio = request.form.get("precio")
        sql = "UPDATE lote_productos SET nombre=%s, cantidad=%s, precio=%s WHERE id_lote=%s"
        cur.execute(sql, (nombre, cantidad, precio, id))
        mysql.connection.commit()
        cur.close()
        return redirect("/lote_productos")
    sql = "SELECT * FROM lote_productos WHERE id_lote=%s"
    cur.execute(sql, (id,))
    lote = cur.fetchone()
    cur.close()
    return render_template("editar_lote.html", lote=lote)

@principal.route("/lote_productos/eliminar/<int:id>", methods=["POST"])
def eliminar_lote(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql = "UPDATE lote_productos SET borrado=1 WHERE id_lote=%s"
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/lote_productos")

# ----------- RUTAS DE ABONOS -----------

@principal.route("/abonos", methods=["GET", "POST"])
def abonos():
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        id_cliente = request.form.get("id_cliente")
        monto = request.form.get("monto")
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO abonos (id_cliente, monto, fecha, borrado) VALUES (%s, %s, %s, 0)"
        cur.execute(sql, (id_cliente, monto, fecha))
        mysql.connection.commit()
    sql = "SELECT * FROM abonos WHERE borrado=0"
    cur.execute(sql)
    abonos = cur.fetchall()
    cur.close()
    return render_template("abonos.html", abonos=abonos)

@principal.route("/abonos/editar/<int:id>", methods=["GET", "POST"])
def editar_abono(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        id_cliente = request.form.get("id_cliente")
        monto = request.form.get("monto")
        sql = "UPDATE abonos SET id_cliente=%s, monto=%s WHERE id_abono=%s"
        cur.execute(sql, (id_cliente, monto, id))
        mysql.connection.commit()
        cur.close()
        return redirect("/abonos")
    sql = "SELECT * FROM abonos WHERE id_abono=%s"
    cur.execute(sql, (id,))
    abono = cur.fetchone()
    cur.close()
    return render_template("editar_abono.html", abono=abono)

@principal.route("/borra_abono/<id>")
def borra_abono(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql = "UPDATE abonos SET borrado=1 WHERE id_abono=%s"
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/abonos")

# ----------- RUTAS DE FACTURAS -----------

@principal.route("/factura", methods=["GET", "POST"])
def factura():
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        id_cliente = request.form.get("id_cliente")
        fecha = request.form.get("fecha")
        total = request.form.get("total")
        metodo_pago = request.form.get("metodo_pago")
        sql = "INSERT INTO factura (id_cliente, fecha, total, metodo_pago, borrado) VALUES (%s, %s, %s, %s, 0)"
        cur.execute(sql, (id_cliente, fecha, total, metodo_pago))
        mysql.connection.commit()
    sql = "SELECT * FROM factura WHERE borrado=0"
    cur.execute(sql)
    facturas = cur.fetchall()
    cur.close()
    return render_template("factura.html", facturas=facturas)

@principal.route("/factura/editar/<int:id>", methods=["GET", "POST"])
def editar_factura(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        id_cliente = request.form.get("id_cliente")
        fecha = request.form.get("fecha")
        total = request.form.get("total")
        metodo_pago = request.form.get("metodo_pago")
        sql = "UPDATE factura SET id_cliente=%s, fecha=%s, total=%s, metodo_pago=%s WHERE id_factura=%s"
        cur.execute(sql, (id_cliente, fecha, total, metodo_pago, id))
        mysql.connection.commit()
        cur.close()
        return redirect("/factura")
    sql = "SELECT * FROM factura WHERE id_factura=%s"
    cur.execute(sql, (id,))
    factura = cur.fetchone()
    cur.close()
    return render_template("editar_factura.html", factura=factura)

@principal.route("/borrafactura/<id>")
def borrafactura(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql = "UPDATE facturas SET borrado=1 WHERE id_factura=%s"
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/factura")

# ----------- RUTAS DE COMPRAS -----------

@principal.route("/compras", methods=["GET", "POST"])
def compras():
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        id_proveedor = request.form.get("proveedor_id")
        fecha_compra = request.form.get("fecha_compra")
        total = request.form.get("total")
        metodo_pago = request.form.get("metodo_pago")
        sql = "INSERT INTO compras (id_proovedor, fecha_pedido, total, metodo_pago, borrado) VALUES (%s, %s, %s, %s, 0)"
        cur.execute(sql, (id_proveedor, fecha_compra, total, metodo_pago))
        mysql.connection.commit()
    sql = "SELECT * FROM compras WHERE borrado=0"
    cur.execute(sql)
    compras = cur.fetchall()
    cur.close()
    return render_template("compras.html", compras=compras)

@principal.route("/compras/editar/<int:id>", methods=["GET", "POST"])
def editar_compra(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        id_proveedor = request.form.get("proveedor_id")
        fecha_compra = request.form.get("fecha_compra")
        total = request.form.get("total")
        metodo_pago = request.form.get("metodo_pago")
        sql = "UPDATE compras SET id_proovedor=%s, fecha_pedido=%s, total=%s, metodo_pago=%s WHERE id_pedido=%s"
        cur.execute(sql, (id_proveedor, fecha_compra, total, metodo_pago, id))
        mysql.connection.commit()
        cur.close()
        return redirect("/compras")
    sql = "SELECT * FROM compras WHERE id_pedido=%s"
    cur.execute(sql, (id,))
    compra = cur.fetchone()
    cur.close()
    return render_template("editar_compra.html", compra=compra)

@principal.route("/compras/eliminar/<int:id>", methods=["POST"])
def eliminar_compra(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql = "UPDATE compras SET borrado=1 WHERE id_pedido=%s"
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/compras")

# ----------- RUTAS DE CATEGORÍAS -----------

@principal.route("/categorias")
def categorias():
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM categorias WHERE borrado=0"
    cur.execute(sql)
    categorias = cur.fetchall()
    cur.close()
    return render_template("categorias.html", categorias=categorias)

@principal.route("/categorias/agregar", methods=["POST"])
def agregar_categoria():
    id = request.form.get("id")
    desc = request.form.get("descripcion")
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql=f"SELECT * FROM categorias WHERE id_categoria={id}"
    cur.execute(sql)
    resultado = cur.fetchone()
    if len(resultado) == 0: 
        sql = f"INSERT INTO categorias (id_categoria, descripcion) VALUES ({id},'{desc}')"
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()
        return redirect("/categorias")  
    else:
        sql = "SELECT * FROM categorias WHERE borrado=0"
        cur.execute(sql)
        categorias = cur.fetchall()
        cur.close()
        return render_template("categorias.html", categorias=categorias, msg="La categoría ya existe.")

@principal.route("/categorias/editar/<int:id>", methods=["GET", "POST"])    
def editar_categoria(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        descripcion = request.form.get("descripcion")
        sql = "UPDATE categorias SET descripcion=%s WHERE id_categoria=%s"
        cur.execute(sql, (descripcion, id))
        mysql.connection.commit()
        cur.close()
        return redirect("/categorias")
    sql = f"SELECT * FROM categorias WHERE id_categoria={id}"
    cur.execute(sql)
    categoria = cur.fetchone()
    cur.close()
    return render_template("editar_categoria.html", categoria=categoria)

@principal.route("/categorias/modificar", methods=["POST"])
def modificar_categoria():
    id = request.form.get("id")
    desc = request.form.get("descripcion")
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql = f"UPDATE categorias SET descripcion='{desc}' WHERE id_categoria={id}"
    cur.execute(sql)
    mysql.connection.commit()
    cur.close()
    return redirect("/categorias")  

@principal.route("/categorias/eliminar/<int:id>")
def eliminar_categoria(id):
    cur = mysql.connection.cursor()
    sql = f"UPDATE categorias SET borrado=1 WHERE id_categoria={id}"
    cur.execute(sql)
    mysql.connection.commit()
    cur.close()
    flash("Categoría registrada correctamente.", "success")
    return redirect("/categorias")



# ----------- RUTAS DE PRODUCTOS -----------

@principal.route("/productos", methods=["GET", "POST"])
def productos():
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        id_categoria = request.form.get("id_categoria")
        descripcion = request.form.get("descripcion")
        precio_compra = request.form.get("precio_compra")
        iva = request.form.get("iva")
        stock = request.form.get("stock")
        sql = "INSERT INTO productos (id_categoria, descripcion, precio_compra_producto, iva, stock, borrado) VALUES (%s, %s, %s, %s, %s, 0)"
        cur.execute(sql, (id_categoria, descripcion, precio_compra, iva, stock))
        mysql.connection.commit()
    sql = "SELECT * FROM productos WHERE borrado=0"
    cur.execute(sql)
    productos = cur.fetchall()
    cur.close()
    return render_template("productos.html", productos=productos)

@principal.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        id_categoria = request.form.get("id_categoria")
        descripcion = request.form.get("descripcion")
        precio_compra = request.form.get("precio_compra")
        iva = request.form.get("iva")
        stock = request.form.get("stock")
        sql = "UPDATE productos SET id_categoria=%s, descripcion=%s, precio_compra_producto=%s, iva=%s, stock=%s WHERE id_producto=%s"
        cur.execute(sql, (id_categoria, descripcion, precio_compra, iva, stock, id))
        mysql.connection.commit()
        cur.close()
        return redirect("/productos")
    sql = "SELECT * FROM productos WHERE id_producto=%s"
    cur.execute(sql, (id,))
    producto = cur.fetchone()
    cur.close()
    return render_template("editar_producto.html", producto=producto)

@principal.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    sql = "UPDATE productos SET borrado=1 WHERE id_producto=%s"
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/productos")

# ----------- RUTAS DE DETALLES -----------

@principal.route("/detalle_factura/<int:id_factura>", methods=["GET", "POST"])
def detalle_factura(id_factura):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        id_producto = request.form.get("producto_id")
        cantidad = request.form.get("cantidad")
        precio_unitario = request.form.get("precio_unitario")
        sql = "INSERT INTO detalle_factura (factura, id_producto, cant, precio) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (id_factura, id_producto, cantidad, precio_unitario))
        mysql.connection.commit()
    sql = "SELECT * FROM detalle_factura WHERE factura=%s"
    cur.execute(sql, (id_factura,))
    detalles = cur.fetchall()
    cur.close()
    return render_template("detalle_factura.html", detalles=detalles, id_factura=id_factura)

@principal.route("/detalle_pedido/<int:id_pedido>", methods=["GET", "POST"])
def detalle_pedido(id_pedido):
    if not session.get('login'):
        return redirect("/")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        id_producto = request.form.get("producto_id")
        cantidad = request.form.get("cantidad")
        valor = request.form.get("valor")
        sql = "INSERT INTO detalle_pedido (id_pedido, id_producto, cant, valor) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (id_pedido, id_producto, cantidad, valor))
        mysql.connection.commit()
    sql = "SELECT * FROM detalle_pedido WHERE id_pedido=%s"
    cur.execute(sql, (id_pedido,))
    detalles = cur.fetchall()
    cur.close()
    return render_template("detalle_pedido.html", detalles=detalles, id_pedido=id_pedido)

if __name__ == "__main__":
    principal.run(debug=True)