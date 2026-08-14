from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql
from conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "SIGIREC_CAMBIAR_ESTA_CLAVE"

# ==========================================
# INICIO
# ==========================================
@app.route("/")
def index():
    return redirect(url_for("login"))

# ==========================================
# LOGIN
# ==========================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        numero_identificacion = request.form.get("numero_identificacion", "").strip()

        if not numero_identificacion:
            flash("Debes ingresar tu número de identificación.", "danger")
            return redirect(url_for("login"))

        conexion = obtener_conexion()

        if conexion is None:
            flash("No fue posible conectar con la base de datos.", "danger")
            return redirect(url_for("login"))

        cursor = conexion.cursor(dictionary=True)

        try:
            consulta = """
                SELECT
                    id_usuario,
                    numero_identificacion,
                    nombre_completo,
                    correo,
                    telefono,
                    rol,
                    programa_formacion,
                    numero_ficha,
                    tipo_usuario
                FROM usuarios
                WHERE numero_identificacion = %s
            """

            cursor.execute(
                consulta,
                (numero_identificacion,)
            )

            usuario = cursor.fetchone()

            if usuario is None:
                flash("No existe un usuario con esa identificación.", "danger")
                return redirect(url_for("login"))

            session["id_usuario"] = usuario["id_usuario"]
            session["nombre_completo"] = usuario["nombre_completo"]
            session["numero_identificacion"] = usuario["numero_identificacion"]
            session["tipo_usuario"] = usuario["tipo_usuario"]
            session["rol"] = usuario["rol"]

            if usuario["tipo_usuario"] == "ADMINISTRADOR":
                return redirect(url_for("admin_dashboard"))

            return redirect(url_for("dashboard"))

        except Exception as e:
            print("ERROR LOGIN:", e)
            flash(f"Ocurrió un error al iniciar sesión: {e}", "danger")
            return redirect(url_for("login"))

        finally:
            cursor.close()
            conexion.close()

    return render_template("auth/login.html")

# ==========================================
# REGISTER
# ==========================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre_completo = request.form.get("nombre_completo", "").strip()
        numero_identificacion = request.form.get("numero_identificacion", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()
        rol = request.form.get("rol", "").strip()
        programa_formacion = request.form.get("programa_formacion", "").strip()
        numero_ficha = request.form.get("numero_ficha", "").strip()

        if not all([
            nombre_completo,
            numero_identificacion,
            correo,
            rol,
            programa_formacion,
            numero_ficha
        ]):
            flash("Completa todos los campos obligatorios.", "danger")
            return redirect(url_for("register"))

        roles_validos = [
            "APRENDIZ",
            "INSTRUCTOR",
            "AREA_ADMINISTRATIVA",
            "EXTERNO"
        ]

        if rol not in roles_validos:
            flash("El rol seleccionado no es válido.", "danger")
            return redirect(url_for("register"))

        conexion = obtener_conexion()

        if conexion is None:
            flash("No fue posible conectar con la base de datos.", "danger")
            return redirect(url_for("register"))

        cursor = conexion.cursor()

        try:
            consulta = """
                INSERT INTO usuarios (
                    numero_identificacion,
                    nombre_completo,
                    correo,
                    telefono,
                    rol,
                    programa_formacion,
                    numero_ficha
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                numero_identificacion,
                nombre_completo,
                correo,
                telefono,
                rol,
                programa_formacion,
                numero_ficha
            )

            cursor.execute(
                consulta,
                valores
            )

            conexion.commit()

            flash(
                "Cuenta creada correctamente. Ya puedes iniciar sesión.",
                "success"
            )

            return redirect(url_for("login"))

        except Exception as e:
            conexion.rollback()

            print("ERROR REGISTRO:", e)

            if "Duplicate entry" in str(e):
                flash(
                    "La identificación o el correo ya están registrados.",
                    "danger"
                )
            else:
                flash(
                    f"No fue posible crear la cuenta: {e}",
                    "danger"
                )

            return redirect(url_for("register"))

        finally:
            cursor.close()
            conexion.close()

    return render_template("auth/register.html")

# ==========================================
# DASHBOARD USUARIO
# ==========================================
@app.route("/dashboard")
def dashboard():

    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") == "ADMINISTRADOR":
        return redirect(url_for("admin_dashboard"))

    conexion = obtener_conexion()

    if conexion is None:
        flash(
            "No fue posible conectar con la base de datos.",
            "danger"
        )
        return redirect(url_for("login"))

    cursor = conexion.cursor(dictionary=True)

    try:
        consulta = """
            SELECT
                u.id_usuario,
                u.nombre_completo,
                u.numero_identificacion,

                COALESCE(
                    (
                        SELECT SUM(mp1.puntos)
                        FROM movimientos_puntos mp1
                        WHERE mp1.id_usuario = u.id_usuario
                    ),
                    0
                ) AS puntos_totales,

                COALESCE(
                    (
                        SELECT COUNT(*)
                        FROM movimientos_puntos mp2
                        WHERE mp2.id_usuario = u.id_usuario
                        AND mp2.tipo_movimiento = 'RECICLAJE'
                    ),
                    0
                ) AS botellas_recicladas,

                COALESCE(
                    (
                        SELECT SUM(mp3.puntos)
                        FROM movimientos_puntos mp3
                        WHERE mp3.id_usuario = u.id_usuario
                        AND mp3.tipo_movimiento = 'RECICLAJE'
                    ),
                    0
                ) AS puntos_obtenidos,

                (
                    SELECT MAX(mp4.fecha_movimiento)
                    FROM movimientos_puntos mp4
                    WHERE mp4.id_usuario = u.id_usuario
                    AND mp4.tipo_movimiento = 'RECICLAJE'
                ) AS ultimo_reciclaje

            FROM usuarios u
            WHERE u.id_usuario = %s
        """

        cursor.execute(
            consulta,
            (session["id_usuario"],)
        )

        usuario = cursor.fetchone()

        if usuario is None:
            session.clear()

            flash(
                "El usuario no existe.",
                "danger"
            )

            return redirect(url_for("login"))

        return render_template(
            "usuario/dashboard.html",
            usuario=usuario
        )

    except Exception as e:
        print("ERROR DASHBOARD:", e)

        flash(
            f"Error al cargar el dashboard: {e}",
            "danger"
        )

        return redirect(url_for("login"))

    finally:
        cursor.close()
        conexion.close()

# ==========================================
# INFORMACIÓN SIGIREC
# ==========================================
@app.route("/informacion")
def informacion():

    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") == "ADMINISTRADOR":
        return redirect(url_for("admin_dashboard"))

    return render_template(
        "usuario/informacion.html"
    )

# ==========================================
# DASHBOARD ADMINISTRADOR
# ==========================================
@app.route("/admin")
def admin_dashboard():

    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") != "ADMINISTRADOR":
        return redirect(url_for("dashboard"))

    conexion = obtener_conexion()

    if conexion is None:
        flash(
            "No fue posible conectar con la base de datos.",
            "danger"
        )
        return redirect(url_for("login"))

    cursor = conexion.cursor(dictionary=True)

    try:
        consulta = """
            SELECT
                (SELECT COUNT(*) FROM usuarios) AS usuarios_total,

                (SELECT COUNT(*) FROM analisis_ia) AS escaneos_ia,

                (
                    SELECT COALESCE(SUM(puntos), 0)
                    FROM movimientos_puntos
                    WHERE tipo_movimiento = 'RECICLAJE'
                ) AS puntos_entregados,

                (SELECT COUNT(*) FROM productos) AS productos_total
        """

        cursor.execute(consulta)

        estadisticas = cursor.fetchone()

        return render_template(
            "admin/dashboard.html",
            estadisticas=estadisticas
        )

    except Exception as e:
        print(
            "ERROR DASHBOARD ADMIN:",
            e
        )

        flash(
            f"Error al cargar el dashboard: {e}",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    finally:
        cursor.close()
        conexion.close()

# ==========================================
# GESTIÓN DE USUARIOS
# ==========================================
@app.route("/admin/usuarios")
def admin_usuarios():
    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") != "ADMINISTRADOR":
        return redirect(url_for("dashboard"))

    conexion = obtener_conexion()

    if conexion is None:
        flash("No fue posible conectar con la base de datos.", "danger")
        return redirect(url_for("admin_dashboard"))

    cursor = conexion.cursor(dictionary=True)

    try:
        consulta = """
            SELECT
                u.id_usuario,
                u.nombre_completo,
                u.numero_identificacion,
                u.correo,
                u.telefono,
                u.rol,
                u.programa_formacion,
                u.numero_ficha,
                u.tipo_usuario,

                COALESCE(
                    (
                        SELECT SUM(mp.puntos)
                        FROM movimientos_puntos mp
                        WHERE mp.id_usuario = u.id_usuario
                    ),
                    0
                ) AS puntos_totales,

                (
                    SELECT COUNT(*)
                    FROM analisis_ia ai
                    WHERE ai.id_usuario = u.id_usuario
                ) AS escaneos_ia

            FROM usuarios u
            ORDER BY u.id_usuario DESC
        """

        cursor.execute(consulta)
        usuarios = cursor.fetchall()

        return render_template(
            "admin/usuarios.html",
            usuarios=usuarios
        )

    except Exception as e:
        print("ERROR GESTION USUARIOS:", e)
        flash(f"Error al cargar los usuarios: {e}", "danger")
        return redirect(url_for("admin_dashboard"))

    finally:
        cursor.close()
        conexion.close()

# ==========================================
# EDITAR USUARIO
# ==========================================
@app.route(
    "/admin/usuarios/editar/<int:id_usuario>",
    methods=["GET", "POST"]
)
def admin_editar_usuario(id_usuario):

    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") != "ADMINISTRADOR":
        return redirect(url_for("dashboard"))

    conexion = obtener_conexion()

    if conexion is None:
        flash(
            "No fue posible conectar con la base de datos.",
            "danger"
        )
        return redirect(
            url_for("admin_usuarios")
        )

    cursor = conexion.cursor(dictionary=True)

    try:

        if request.method == "GET":

            consulta = """
                SELECT
                    id_usuario,
                    numero_identificacion,
                    nombre_completo,
                    correo,
                    telefono,
                    rol,
                    programa_formacion,
                    numero_ficha,
                    tipo_usuario
                FROM usuarios
                WHERE id_usuario = %s
            """

            cursor.execute(
                consulta,
                (id_usuario,)
            )

            usuario = cursor.fetchone()

            if usuario is None:

                flash(
                    "El usuario no existe.",
                    "danger"
                )

                return redirect(
                    url_for("admin_usuarios")
                )

            return render_template(
                "admin/usuarios.html",
                usuarios=[usuario],
                editar=True,
                usuario_editar=usuario,
                busqueda=""
            )

        # ==================================
        # DATOS DEL FORMULARIO
        # ==================================

        nombre_completo = request.form.get(
            "nombre_completo",
            ""
        ).strip()

        numero_identificacion = request.form.get(
            "numero_identificacion",
            ""
        ).strip()

        correo = request.form.get(
            "correo",
            ""
        ).strip()

        telefono = request.form.get(
            "telefono",
            ""
        ).strip()

        rol = request.form.get(
            "rol",
            ""
        ).strip()

        programa_formacion = request.form.get(
            "programa_formacion",
            ""
        ).strip()

        numero_ficha = request.form.get(
            "numero_ficha",
            ""
        ).strip()

        tipo_usuario = request.form.get(
            "tipo_usuario",
            "USUARIO"
        ).strip()

        # ==================================
        # VALIDACIONES
        # ==================================

        if not all([
            nombre_completo,
            numero_identificacion,
            correo,
            rol,
            programa_formacion,
            numero_ficha
        ]):

            flash(
                "Completa todos los campos obligatorios.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin_editar_usuario",
                    id_usuario=id_usuario
                )
            )

        roles_validos = [
            "APRENDIZ",
            "INSTRUCTOR",
            "AREA_ADMINISTRATIVA",
            "EXTERNO"
        ]

        if rol not in roles_validos:

            flash(
                "El rol seleccionado no es válido.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin_editar_usuario",
                    id_usuario=id_usuario
                )
            )

        tipos_validos = [
            "USUARIO",
            "ADMINISTRADOR"
        ]

        if tipo_usuario not in tipos_validos:

            flash(
                "El tipo de usuario seleccionado no es válido.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin_editar_usuario",
                    id_usuario=id_usuario
                )
            )

        # ==================================
        # EVITAR QUE EL ADMIN SE ELIMINE
        # SU PROPIO ACCESO
        # ==================================

        if (
            id_usuario == session["id_usuario"]
            and tipo_usuario != "ADMINISTRADOR"
        ):

            flash(
                "No puedes quitarte a ti mismo el acceso de administrador.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin_editar_usuario",
                    id_usuario=id_usuario
                )
            )

        # ==================================
        # ACTUALIZAR
        # ==================================

        consulta = """
            UPDATE usuarios
            SET
                numero_identificacion = %s,
                nombre_completo = %s,
                correo = %s,
                telefono = %s,
                rol = %s,
                programa_formacion = %s,
                numero_ficha = %s,
                tipo_usuario = %s
            WHERE id_usuario = %s
        """

        valores = (
            numero_identificacion,
            nombre_completo,
            correo,
            telefono,
            rol,
            programa_formacion,
            numero_ficha,
            tipo_usuario,
            id_usuario
        )

        cursor.execute(
            consulta,
            valores
        )

        conexion.commit()

        # Si el administrador editó su propia información,
        # actualizamos también la sesión.
        if id_usuario == session["id_usuario"]:

            session["nombre_completo"] = nombre_completo
            session["numero_identificacion"] = numero_identificacion
            session["tipo_usuario"] = tipo_usuario
            session["rol"] = rol

        flash(
            "Usuario actualizado correctamente.",
            "success"
        )

        return redirect(
            url_for("admin_usuarios")
        )

    except Exception as e:

        conexion.rollback()

        print(
            "ERROR EDITANDO USUARIO:",
            e
        )

        if "Duplicate entry" in str(e):

            flash(
                "La identificación o el correo ya pertenecen a otro usuario.",
                "danger"
            )

        else:

            flash(
                f"No fue posible actualizar el usuario: {e}",
                "danger"
            )

        return redirect(
            url_for("admin_usuarios")
        )

    finally:
        cursor.close()
        conexion.close()

# ==========================================
# ELIMINAR USUARIO
# ==========================================
@app.route(
    "/admin/usuarios/eliminar/<int:id_usuario>",
    methods=["POST"]
)
def admin_eliminar_usuario(id_usuario):

    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") != "ADMINISTRADOR":
        return redirect(url_for("dashboard"))

    # ==================================
    # NO PERMITIR ELIMINARSE A SÍ MISMO
    # ==================================

    if id_usuario == session["id_usuario"]:

        flash(
            "No puedes eliminar tu propia cuenta de administrador.",
            "danger"
        )

        return redirect(
            url_for("admin_usuarios")
        )

    conexion = obtener_conexion()

    if conexion is None:
        flash(
            "No fue posible conectar con la base de datos.",
            "danger"
        )
        return redirect(
            url_for("admin_usuarios")
        )

    cursor = conexion.cursor()

    try:

        consulta = """
            DELETE FROM usuarios
            WHERE id_usuario = %s
        """

        cursor.execute(
            consulta,
            (id_usuario,)
        )

        if cursor.rowcount == 0:

            flash(
                "El usuario no existe.",
                "danger"
            )

            return redirect(
                url_for("admin_usuarios")
            )

        conexion.commit()

        flash(
            "Usuario eliminado correctamente.",
            "success"
        )

        return redirect(
            url_for("admin_usuarios")
        )

    except Exception as e:

        conexion.rollback()

        print(
            "ERROR ELIMINANDO USUARIO:",
            e
        )

        flash(
            "No se pudo eliminar el usuario. "
            "Es posible que tenga registros relacionados "
            "en otras tablas.",
            "danger"
        )

        return redirect(
            url_for("admin_usuarios")
        )

    finally:
        cursor.close()
        conexion.close()


# ==========================================
# GESTIÓN DE USUARIOS
# ==========================================
@app.route("/admin/usuarios")


# ==========================================
# EDITAR USUARIO
# ==========================================
@app.route("/admin/usuarios/editar/<int:id_usuario>", methods=["POST"])
def editar_usuario(id_usuario):
    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") != "ADMINISTRADOR":
        return redirect(url_for("dashboard"))

    nombre_completo = request.form.get("nombre_completo", "").strip()
    numero_identificacion = request.form.get("numero_identificacion", "").strip()
    correo = request.form.get("correo", "").strip()
    telefono = request.form.get("telefono", "").strip()
    rol = request.form.get("rol", "").strip()
    programa_formacion = request.form.get("programa_formacion", "").strip()
    numero_ficha = request.form.get("numero_ficha", "").strip()
    tipo_usuario = request.form.get("tipo_usuario", "").strip()

    roles_validos = [
        "APRENDIZ",
        "INSTRUCTOR",
        "AREA_ADMINISTRATIVA",
        "EXTERNO"
    ]

    tipos_usuario_validos = [
        "USUARIO",
        "ADMINISTRADOR"
    ]

    if not all([
        nombre_completo,
        numero_identificacion,
        correo,
        rol,
        programa_formacion,
        numero_ficha
    ]):
        flash("Completa todos los campos obligatorios.", "danger")
        return redirect(url_for("admin_usuarios"))

    if rol not in roles_validos:
        flash("El rol seleccionado no es válido.", "danger")
        return redirect(url_for("admin_usuarios"))

    if tipo_usuario not in tipos_usuario_validos:
        flash("El tipo de usuario seleccionado no es válido.", "danger")
        return redirect(url_for("admin_usuarios"))

    conexion = obtener_conexion()

    if conexion is None:
        flash("No fue posible conectar con la base de datos.", "danger")
        return redirect(url_for("admin_usuarios"))

    cursor = conexion.cursor()

    try:
        consulta = """
            UPDATE usuarios
            SET
                nombre_completo = %s,
                numero_identificacion = %s,
                correo = %s,
                telefono = %s,
                rol = %s,
                programa_formacion = %s,
                numero_ficha = %s,
                tipo_usuario = %s
            WHERE id_usuario = %s
        """

        valores = (
            nombre_completo,
            numero_identificacion,
            correo,
            telefono,
            rol,
            programa_formacion,
            numero_ficha,
            tipo_usuario,
            id_usuario
        )

        cursor.execute(consulta, valores)
        conexion.commit()

        flash("Usuario actualizado correctamente.", "success")

    except Exception as e:
        conexion.rollback()

        print("ERROR EDITANDO USUARIO:", e)

        if "Duplicate entry" in str(e):
            flash(
                "La identificación o el correo ya pertenecen a otro usuario.",
                "danger"
            )
        else:
            flash(
                f"No fue posible actualizar el usuario: {e}",
                "danger"
            )

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("admin_usuarios"))


# ==========================================
# AGREGAR PUNTOS
# ==========================================
@app.route("/admin/usuarios/puntos/agregar/<int:id_usuario>", methods=["POST"])
def agregar_puntos(id_usuario):
    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") != "ADMINISTRADOR":
        return redirect(url_for("dashboard"))

    try:
        puntos = int(request.form.get("puntos", 0))
    except (ValueError, TypeError):
        puntos = 0

    motivo = request.form.get("motivo", "").strip()

    if puntos <= 0:
        flash("La cantidad de puntos debe ser mayor que 0.", "danger")
        return redirect(url_for("admin_usuarios"))

    conexion = obtener_conexion()

    if conexion is None:
        flash("No fue posible conectar con la base de datos.", "danger")
        return redirect(url_for("admin_usuarios"))

    cursor = conexion.cursor()

    try:
        consulta = """
            INSERT INTO movimientos_puntos (
                id_usuario,
                tipo_movimiento,
                puntos,
                motivo,
                id_usuario_admin
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            id_usuario,
            "BONIFICACION",
            puntos,
            motivo if motivo else "Bonificación manual realizada por administrador",
            session["id_usuario"]
        )

        cursor.execute(consulta, valores)
        conexion.commit()

        flash(
            f"Se agregaron {puntos} SIGIPUNTOS correctamente.",
            "success"
        )

    except Exception as e:
        conexion.rollback()
        print("ERROR AGREGANDO PUNTOS:", e)
        flash(f"No fue posible agregar los puntos: {e}", "danger")

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("admin_usuarios"))


# ==========================================
# QUITAR PUNTOS
# ==========================================
@app.route("/admin/usuarios/puntos/quitar/<int:id_usuario>", methods=["POST"])
def quitar_puntos(id_usuario):
    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") != "ADMINISTRADOR":
        return redirect(url_for("dashboard"))

    try:
        puntos = int(request.form.get("puntos", 0))
    except (ValueError, TypeError):
        puntos = 0

    motivo = request.form.get("motivo", "").strip()

    if puntos <= 0:
        flash("La cantidad de puntos debe ser mayor que 0.", "danger")
        return redirect(url_for("admin_usuarios"))

    conexion = obtener_conexion()

    if conexion is None:
        flash("No fue posible conectar con la base de datos.", "danger")
        return redirect(url_for("admin_usuarios"))

    cursor = conexion.cursor(dictionary=True)

    try:
        consulta_saldo = """
            SELECT COALESCE(SUM(puntos), 0) AS saldo
            FROM movimientos_puntos
            WHERE id_usuario = %s
        """

        cursor.execute(consulta_saldo, (id_usuario,))
        resultado = cursor.fetchone()

        saldo_actual = resultado["saldo"]

        if puntos > saldo_actual:
            flash(
                f"El usuario solamente tiene {saldo_actual} SIGIPUNTOS.",
                "danger"
            )
            return redirect(url_for("admin_usuarios"))

        consulta = """
            INSERT INTO movimientos_puntos (
                id_usuario,
                tipo_movimiento,
                puntos,
                motivo,
                id_usuario_admin
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            id_usuario,
            "PENALIZACION",
            -puntos,
            motivo if motivo else "Descuento manual realizado por administrador",
            session["id_usuario"]
        )

        cursor.execute(consulta, valores)
        conexion.commit()

        flash(
            f"Se quitaron {puntos} SIGIPUNTOS correctamente.",
            "success"
        )

    except Exception as e:
        conexion.rollback()
        print("ERROR QUITANDO PUNTOS:", e)
        flash(f"No fue posible quitar los puntos: {e}", "danger")

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("admin_usuarios"))


# ==========================================
# LOGOUT
# ==========================================
@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )



@app.route("/admin/reciclajes")
def admin_reciclajes():

    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") != "ADMINISTRADOR":
        return redirect(url_for("dashboard"))

    conexion = None
    cursor = None

    try:

        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sigirec"
        )

        cursor = conexion.cursor(dictionary=True)

        # ==========================================
        # RECICLAJES REGISTRADOS MEDIANTE IA
        # ==========================================

        cursor.execute("""
            SELECT
                ri.id_registro,
                ri.id_usuario,
                ri.id_botella,
                ri.imagen_analizada,
                ri.color_detectado,
                ri.altura_detectada,
                ri.etiqueta_detectada,
                ri.tapa_detectada,
                ri.coincidencia,
                ri.puntos_asignados,
                ri.fecha,

                u.nombre_completo,
                u.numero_identificacion,

                b.marca,
                b.color AS color_botella,
                b.puntos AS puntos_botella

            FROM registros_ia ri

            INNER JOIN usuarios u
                ON ri.id_usuario = u.id_usuario

            LEFT JOIN botellas b
                ON ri.id_botella = b.id_botella

            ORDER BY ri.fecha DESC
        """)

        reciclajes = cursor.fetchall()


        # ==========================================
        # BOTELLAS NO REGISTRADAS
        # ==========================================

        cursor.execute("""
            SELECT
                bnr.id_no_registrada,
                bnr.id_usuario,
                bnr.imagen,
                bnr.color_detectado,
                bnr.altura_detectada,
                bnr.etiqueta_detectada,
                bnr.tapa_detectada,
                bnr.estado,
                bnr.fecha,

                u.nombre_completo,
                u.numero_identificacion

            FROM botellas_no_registradas bnr

            INNER JOIN usuarios u
                ON bnr.id_usuario = u.id_usuario

            ORDER BY bnr.fecha DESC
        """)

        botellas_no_registradas = cursor.fetchall()


        # ==========================================
        # MOSTRAR VISTA
        # ==========================================

        return render_template(
            "admin/admin_reciclajes.html",
            reciclajes=reciclajes,
            botellas_no_registradas=botellas_no_registradas
        )


    except Exception as e:

        print("ERROR RECICLAJES ADMIN:", e)

        return render_template(
            "admin/admin_reciclajes.html",
            reciclajes=[],
            botellas_no_registradas=[]
        )


    finally:

        if cursor:
            cursor.close()

        if conexion:
            conexion.close()






@app.route("/admin/catalogo")
def admin_catalogo():

    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") != "ADMINISTRADOR":
        return redirect(url_for("dashboard"))

    conexion = obtener_conexion()

    if conexion is None:
        flash(
            "No fue posible conectar con la base de datos.",
            "danger"
        )
        return redirect(url_for("login"))

    cursor = conexion.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                id_producto,
                nombre,
                descripcion,
                imagen,
                costo_puntos,
                stock,
                fecha_registro
            FROM productos
            ORDER BY fecha_registro DESC
        """)

        productos = cursor.fetchall()

        print("PRODUCTOS CATALOGO:", productos)

        return render_template(
            "admin/admin_catalogo.html",
            productos=productos
        )

    except Exception as e:

        print("ERROR CATALOGO ADMIN:", e)

        flash(
            f"Error al cargar el catálogo: {e}",
            "danger"
        )

        return render_template(
            "admin/admin_catalogo.html",
            productos=[]
        )

    finally:

        cursor.close()
        conexion.close()



# ==========================================
# AUDITORÍAS
# ==========================================
@app.route("/admin/auditorias")
def admin_auditorias():

    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if session.get("tipo_usuario") != "ADMINISTRADOR":
        return redirect(url_for("dashboard"))

    conexion = None
    cursor = None

    try:

        conexion = obtener_conexion()

        if conexion is None:
            flash(
                "No fue posible conectar con la base de datos.",
                "danger"
            )
            return redirect(url_for("admin_dashboard"))

        cursor = conexion.cursor(dictionary=True)

        # ==========================================
        # AUDITORÍAS
        # ==========================================

        cursor.execute("""
            SELECT
                a.id_auditoria,
                a.id_usuario,
                a.accion,
                a.tabla_afectada,
                a.id_registro,
                a.descripcion,
                a.ip,
                a.fecha,

                u.nombre_completo,
                u.numero_identificacion

            FROM auditoria a

            LEFT JOIN usuarios u
                ON a.id_usuario = u.id_usuario

            ORDER BY a.fecha DESC
        """)

        auditorias = cursor.fetchall()

        # ==========================================
        # ESTADÍSTICAS
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM auditoria
        """)

        total = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM auditoria
            WHERE tabla_afectada = 'usuarios'
        """)

        usuarios = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM auditoria
            WHERE tabla_afectada = 'registros_ia'
        """)

        reciclajes = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM auditoria
            WHERE tabla_afectada = 'productos'
        """)

        catalogo = cursor.fetchone()["total"]

        estadisticas = {
            "total": total,
            "usuarios": usuarios,
            "reciclajes": reciclajes,
            "catalogo": catalogo
        }

        return render_template(
            "admin/admin_auditoria.html",
            auditorias=auditorias,
            estadisticas=estadisticas
        )

    except Exception as e:

        print("ERROR AUDITORIAS ADMIN:", e)

        return render_template(
            "admin/admin_auditoria.html",
            auditorias=[],
            estadisticas={
                "total": 0,
                "usuarios": 0,
                "reciclajes": 0,
                "catalogo": 0
            }
        )

    finally:

        if cursor:
            cursor.close()

        if conexion:
            conexion.close()

# ==========================================
# EJECUTAR
# ==========================================
if __name__ == "__main__":
    app.run(
        debug=True
    )

