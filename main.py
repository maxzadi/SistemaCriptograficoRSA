
"""Interfaz grafica del proyecto RSA desarrollada con Streamlit."""

import streamlit as st
from encriptacion import Mensaje


st.set_page_config(
    page_title="Sistema de criptografia RSA",
    page_icon="🔐",
    layout="wide",
)


# ---------------------------------------------------------
# 1. Estado inicial de la aplicacion
# ---------------------------------------------------------

DEFAULTS = {
    "p": "",
    "q": "",
    "e": "",
    "mensaje": "",
    "cifrado_entrada": "",
    "longitud_entrada": "",
    "resultado_cifrado": None,
    "resultado_descifrado": None,
    "vista": "Encriptar",
}

for clave, valor in DEFAULTS.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor


# ---------------------------------------------------------
# 2. Funciones auxiliares de la interfaz
# ---------------------------------------------------------

def limpiar_cifrado():
    """Elimina resultados anteriores de encriptacion."""
    st.session_state.resultado_cifrado = None


def limpiar_descifrado():
    """Elimina resultados anteriores de desencriptacion."""
    st.session_state.resultado_descifrado = None


def limpiar_ambos():
    """Limpia resultados si cambian los parametros RSA."""
    limpiar_cifrado()
    limpiar_descifrado()


def pasar_a_desencriptacion():
    """Transfiere los datos de encriptacion a desencriptacion."""

    resultado = st.session_state.resultado_cifrado

    if resultado is None:
        return

    p, q, e = resultado["parametros"]

    st.session_state.p = str(p)
    st.session_state.q = str(q)
    st.session_state.e = str(e)

    st.session_state.cifrado_entrada = resultado["cifrado"]
    st.session_state.longitud_entrada = str(resultado["longitud"])

    st.session_state.resultado_descifrado = None
    st.session_state.vista = "Desencriptar"


def leer_parametros():
    """Convierte los parametros ingresados a numeros enteros."""

    valores = []

    for nombre in ("p", "q", "e"):
        texto = st.session_state[nombre].strip()

        try:
            valores.append(int(texto))
        except ValueError:
            raise ValueError(
                f"{nombre} debe ser un numero entero."
            ) from None

    return valores


def tabla_bloques(bloques_numericos, bloques_cifrados):
    """Construye la tabla explicativa de conversiones ASCII."""

    filas = []

    for indice, (m, c) in enumerate(
        zip(bloques_numericos, bloques_cifrados),
        start=1,
    ):
        ascii_1 = m[:3]
        ascii_2 = m[3:]

        caracteres = chr(int(ascii_1)) + chr(int(ascii_2))

        filas.append({
            "Bloque": indice,
            "Caracteres (␠ = espacio)": caracteres.replace(" ", "␠"),
            "Codigos ASCII": f"{ascii_1} {ascii_2}",
            "Bloque numerico (m)": m,
            "Bloque cifrado (c)": c,
        })

    return filas


def detalles_rsa(datos, cifrado, mensaje_bloques, operacion):
    """Muestra los calculos y conversiones del procedimiento RSA."""

    with st.expander(
        "Ver procedimiento matematico y conversion ASCII",
        expanded=False,
    ):

        st.write("**Parametros y calculos RSA**")

        st.write(datos["Entradas RSA"])
        st.write(datos["Valores calculados"])
        st.write(datos["Longitud y relleno"])

        if operacion == "Desencriptar":
            st.write(datos["Exponente privado"])

        st.write("**Conversiones y bloques**")

        if mensaje_bloques:
            filas = tabla_bloques(
                mensaje_bloques,
                cifrado.split(" "),
            )

            st.dataframe(
                filas,
                hide_index=True,
                use_container_width=True,
            )

        else:
            st.info("No hay bloques para mostrar.")

        st.caption(
            "Cada caracter se representa con tres digitos ASCII. "
            "Cada pareja forma un bloque numerico de seis digitos."
        )


# ---------------------------------------------------------
# 3. Encabezado de la aplicacion
# ---------------------------------------------------------

st.title("🔐 Sistema de criptografia RSA")

st.write(
    "El programa permite encriptar y desencriptar mensajes de texto "
    "utilizando el algoritmo RSA. También es posible consultar los cálculos "
    "matemáticos y las conversiones realizadas durante el proceso."
)

st.info(
    "Se admiten letras inglesas, numeros, espacios y signos "
    "ASCII (codigos 32 a 126). "
    "No se admiten tildes, ñ ni saltos de linea."
)


# ---------------------------------------------------------
# 4. Paso 1: Parametros RSA
# ---------------------------------------------------------

st.subheader("Paso 1. Parámetros RSA")

col_p, col_q, col_e = st.columns(3)

with col_p:
    st.text_input(
        "Número primo p",
        key="p",
        placeholder="Ejemplo: 367",
        help="Debe ser primo y distinto de q.",
        on_change=limpiar_ambos,
    )

with col_q:
    st.text_input(
        "Número primo q",
        key="q",
        placeholder="Ejemplo: 373",
        help="Debe ser primo y distinto de p.",
        on_change=limpiar_ambos,
    )

with col_e:
    st.text_input(
        "Exponente público e",
        key="e",
        placeholder="Ejemplo: 17",
        help="Debe ser mayor que 1 y coprimo con phi.",
        on_change=limpiar_ambos,
    )

st.caption(
    "Los valores p y q deben ser números primos distintos. "
    "El exponente e debe ser mayor que 1 y cumplir las condiciones del algoritmo RSA."
)

# ---------------------------------------------------------
# 5. Paso 2: Seleccion de operacion
# ---------------------------------------------------------

st.divider()

st.subheader("Paso 2. Selecciona la operacion")

operacion = st.radio(
    "Operacion",
    ["Encriptar", "Desencriptar"],
    horizontal=True,
    key="vista",
)


# ---------------------------------------------------------
# 6. ENCRIPTACION
# ---------------------------------------------------------

if operacion == "Encriptar":

    st.text_input(
        "Mensaje original",
        key="mensaje",
        placeholder="Escribe aquí el mensaje que deseas encriptar",
        help="Los espacios al inicio y al final se conservan.",
        on_change=limpiar_cifrado,
    )

    if st.button(
        "🔒 Encriptar mensaje",
        type="primary",
        use_container_width=True,
    ):

        limpiar_cifrado()

        try:
            p, q, e = leer_parametros()

            mensaje = st.session_state.mensaje

            # Validacion de mensaje vacio
            if mensaje == "":
                raise ValueError(
                    "Introduce un mensaje antes de encriptar."
                )

            # Utilizar el algoritmo RSA
            rsa = Mensaje(mensaje, p, q, e)

            cifrado, longitud, llave_publica = rsa.encriptar()

            datos = rsa.get_resultado()

            st.session_state.resultado_cifrado = {
                "cifrado": cifrado,
                "longitud": longitud,
                "llave": llave_publica,
                "n": rsa.n,
                "phi": rsa.phi,
                "relleno": rsa.relleno,
                "datos": datos,
                "bloques": datos["Bloques del mensaje"].split(),
                "parametros": (p, q, e),
            }

        except (ValueError, TypeError, OverflowError) as error:
            st.error(f"No se pudo encriptar: {error}")

    resultado = st.session_state.resultado_cifrado

    if resultado is not None:

        st.divider()

        st.subheader("Paso 3. Resultado de encriptacion")

        st.success("Mensaje encriptado correctamente.")

        st.code(
            resultado["cifrado"],
            language=None,
        )

        st.caption(
            "Cifrado C: copia exactamente estos bloques "
            "de seis digitos, separados por un espacio."
        )

        col_a, col_b, col_c = st.columns(3)

        col_a.metric(
            "Longitud original L",
            resultado["longitud"],
        )

        col_b.metric(
            "Modulo n",
            resultado["n"],
        )

        col_c.metric(
            "Funcion φ(n)",
            resultado["phi"],
        )

        st.write(
            f"**Llave publica (e, n):** {resultado['llave']}"
        )

        if resultado["relleno"]:
            st.write(
                "**Relleno agregado:** Si, un espacio al final."
            )
        else:
            st.write("**Relleno agregado:** No.")

        detalles_rsa(
            resultado["datos"],
            resultado["cifrado"],
            resultado["bloques"],
            "Encriptar",
        )

        st.button(
            "➡️ Pasar estos datos a desencriptacion",
            use_container_width=True,
            on_click=pasar_a_desencriptacion,
        )


# ---------------------------------------------------------
# 7. DESENCRIPTACION
# ---------------------------------------------------------

else:

    st.text_input(
        "Mensaje cifrado C",
        key="cifrado_entrada",
        placeholder="Ejemplo: 123456 789012 345678",
        help=(
            "Cada bloque debe tener exactamente seis digitos "
            "y estar separado por un solo espacio."
        ),
        on_change=limpiar_descifrado,
    )

    st.text_input(
        "Longitud original L",
        key="longitud_entrada",
        help=(
            "Es la longitud original antes de agregar relleno. "
            "Se obtiene al encriptar."
        ),
        on_change=limpiar_descifrado,
    )

    if st.button(
        "🔓 Desencriptar mensaje",
        type="primary",
        use_container_width=True,
    ):

        limpiar_descifrado()

        try:
            p, q, e = leer_parametros()

            cifrado = st.session_state.cifrado_entrada

            # Validacion de cifrado vacio
            if cifrado == "":
                raise ValueError(
                    "Introduce un mensaje cifrado antes de desencriptar."
                )

            try:
                longitud = int(
                    st.session_state.longitud_entrada.strip()
                )
            except ValueError:
                raise ValueError(
                    "L debe ser un numero entero."
                ) from None

            # Utilizar el algoritmo RSA 
            rsa = Mensaje(
                cifrado,
                p,
                q,
                e,
                False,
                longitud,
            )

            d, mensaje = rsa.desencriptar()

            datos = rsa.get_resultado()

            st.session_state.resultado_descifrado = {
                "mensaje": mensaje,
                "d": d,
                "n": rsa.n,
                "phi": rsa.phi,
                "longitud": longitud,
                "relleno": rsa.relleno,
                "cifrado": rsa.C,
                "datos": datos,
                "bloques": datos["Bloques del mensaje"].split(),
            }

        except (ValueError, TypeError, OverflowError) as error:
            st.error(f"No se pudo desencriptar: {error}")

    resultado = st.session_state.resultado_descifrado

    if resultado is not None:

        st.divider()

        st.subheader("Paso 3. Resultado de desencriptacion")

        st.success("Mensaje recuperado correctamente.")

        st.code(
            resultado["mensaje"],
            language=None,
        )

        st.caption(
            "El mensaje conserva exactamente los espacios originales, "
            "incluidos los del inicio y del final."
        )

        col_a, col_b, col_c = st.columns(3)

        col_a.metric(
            "Exponente privado d",
            resultado["d"],
        )

        col_b.metric(
            "Modulo n",
            resultado["n"],
        )

        col_c.metric(
            "Funcion φ(n)",
            resultado["phi"],
        )

        st.write(
            f"**Longitud original L:** {resultado['longitud']}"
        )

        if resultado["relleno"]:
            st.write(
                "**Relleno retirado:** Si, un espacio final."
            )
        else:
            st.write("**Relleno retirado:** No.")

        detalles_rsa(
            resultado["datos"],
            resultado["cifrado"],
            resultado["bloques"],
            "Desencriptar",
        )


# ---------------------------------------------------------
# 8. Pie de pagina
# ---------------------------------------------------------

st.divider()

st.caption(
    "Proyecto RSA · Matemática Discreta I · "
    "Implementacion matematica en Python"
)
