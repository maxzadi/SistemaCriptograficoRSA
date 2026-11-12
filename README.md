# Sistema Criptográfico RSA

**Universidad del Valle de Guatemala**  
**Curso:** MM2015 - Matemática Discreta 1  
**Proyecto:** Encriptación y desencriptación RSA

## 1. Descripción del proyecto

Aplicación desarrollada en Python con una interfaz gráfica mediante Streamlit que permite encriptar y desencriptar mensajes de texto utilizando el algoritmo criptográfico RSA.

El programa permite consultar los resultados de cada operación, los parámetros matemáticos utilizados, las conversiones de caracteres a códigos ASCII y los bloques numéricos generados durante el proceso.

## 2. Integrantes

- [Nombre completo del integrante 1]
- [Nombre completo del integrante 2]

**Grupo:** [Número de grupo]

## 3. Requisitos

Para ejecutar el programa se necesita:

- Python 3.10 o superior.
- Un navegador web.
- La biblioteca Streamlit, incluida en `requirements.txt`.

La aplicación se ejecuta localmente y no requiere conexión a Internet después de instalar las dependencias.

## 4. Instalación y ejecución

**Paso 1.** Extraer el archivo ZIP del proyecto en una carpeta de la computadora.

**Paso 2.** Abrir una terminal dentro de la carpeta extraída, donde se encuentra `main.py`.

**Paso 3.** Instalar las dependencias necesarias:

```bash
python -m pip install -r requirements.txt
```

**Paso 4.** Ejecutar la aplicación:

```bash
python -m streamlit run main.py
```

La interfaz se abrirá automáticamente en el navegador web. Si no ocurre, ingresar a la dirección que aparece en la terminal, normalmente `http://localhost:8501`.

Para detener la aplicación, presionar `Ctrl + C` en la terminal.

## 5. Instrucciones de uso

### 5.1. Encriptación

1. Ingresar dos números primos distintos, `p` y `q`, y el exponente público `e`.
2. Seleccionar la operación **Encriptar**.
3. Escribir el mensaje original.
4. Presionar **Encriptar mensaje**.
5. Consultar el mensaje cifrado `C`, la longitud original `L`, la llave pública `(e, n)` y los valores matemáticos calculados.
6. Desplegar la sección **Ver procedimiento matemático y conversión ASCII** para consultar las conversiones y los bloques generados.

### 5.2. Desencriptación

1. Introducir los mismos parámetros `p`, `q` y `e` utilizados durante la encriptación.
2. Seleccionar la operación **Desencriptar**.
3. Ingresar el mensaje cifrado `C` y la longitud original `L`.
4. Presionar **Desencriptar mensaje**.
5. Consultar el mensaje original recuperado, el exponente privado `d` y los cálculos realizados.

La aplicación también incluye el botón **Pasar estos datos a desencriptación**, que transfiere automáticamente el mensaje cifrado, la longitud original y los parámetros RSA después de una encriptación exitosa.

## 6. Ejemplo de funcionamiento

Se utiliza el ejemplo de referencia proporcionado en las instrucciones del proyecto.

| Dato | Valor |
|---|---|
| Mensaje original | `RSA` |
| Número primo p | 367 |
| Número primo q | 373 |
| Exponente público e | 17 |
| Módulo n | 136891 |
| Función φ(n) | 136152 |
| Longitud original L | 3 |
| Bloques numéricos | `082083 065032` |
| Mensaje cifrado C | `026054 123875` |
| Llave pública (e, n) | `(17, 136891)` |
| Exponente privado d | 8009 |
| Mensaje recuperado | `RSA` |

### Funcionamiento del relleno

El programa trabaja con bloques de dos caracteres. Cada carácter se convierte en su código ASCII de tres dígitos.

Si el mensaje tiene una longitud impar, se agrega exactamente un espacio al final para completar el último bloque.

Por ejemplo, el mensaje `RSA` tiene tres caracteres, por lo que se transforma temporalmente en `RSA `.

Durante la desencriptación, el programa utiliza la longitud original `L = 3` para retirar únicamente el espacio agregado y recuperar exactamente `RSA`.

Los espacios originales del mensaje se conservan, incluidos los que se encuentran al inicio o al final.

## 7. Condiciones y validaciones

El programa comprueba las siguientes condiciones:

- Los valores `p`, `q` y `e` deben ser enteros.
- Los valores `p` y `q` deben ser números primos distintos.
- El módulo debe cumplir `126126 < n < 1000000`.
- El exponente público debe cumplir `e > 1` y `MCD(e, φ) = 1`.
- Los mensajes deben contener únicamente caracteres ASCII imprimibles, con códigos del 32 al 126.
- Cada bloque cifrado debe contener exactamente seis dígitos decimales.
- Los bloques cifrados deben ser menores que `n`.
- La longitud original `L` debe ser coherente con la cantidad de bloques cifrados.
- Los caracteres recuperados deben pertenecer al conjunto ASCII permitido.
- Cuando existe relleno, se comprueba y retira únicamente el espacio adicional.

Cuando se introducen datos inválidos, la interfaz muestra un mensaje de error comprensible sin cerrar la aplicación.

## 8. Implementación matemática

La lógica matemática del proyecto se encuentra separada de la interfaz gráfica.

**`recursos.py`**

Contiene los algoritmos matemáticos auxiliares utilizados para el funcionamiento de RSA:

- Comprobación de números primos.
- Cálculo del máximo común divisor mediante el algoritmo de Euclides.
- Algoritmo extendido de Euclides.
- Cálculo del inverso modular.
- Exponenciación modular.

**`encriptacion.py`**

Contiene la clase `Mensaje`, encargada de validar los datos, convertir caracteres a códigos ASCII, formar bloques numéricos y realizar las operaciones de encriptación y desencriptación.

**`main.py`**

Contiene la interfaz gráfica desarrollada con Streamlit, que permite ingresar los datos, ejecutar las operaciones y visualizar los resultados y procedimientos matemáticos.

**`consola.py`**

Contiene funciones de ejecución y pruebas desde la consola.

Los algoritmos matemáticos RSA se implementan en Python sin utilizar bibliotecas externas de criptografía.

## 9. Estructura del proyecto

```text
SistemaCriptograficoRSA/
├── main.py
├── encriptacion.py
├── recursos.py
├── consola.py
├── requirements.txt
└── README.md
```

- `main.py`: archivo principal de la aplicación.
- `encriptacion.py`: lógica de encriptación y desencriptación RSA.
- `recursos.py`: algoritmos matemáticos auxiliares.
- `consola.py`: ejecución y pruebas desde consola.
- `requirements.txt`: dependencias externas.
- `README.md`: documentación e instrucciones de uso.

## 10. Pruebas de funcionamiento

Se realizaron pruebas para verificar:

- Encriptación y desencriptación del ejemplo oficial `RSA`.
- Recuperación de mensajes de longitud par e impar.
- Conservación de espacios originales al inicio, entre palabras y al final.
- Visualización de códigos ASCII, bloques numéricos y resultados matemáticos.
- Rechazo de números primos inválidos o iguales.
- Rechazo de exponentes públicos inválidos.
- Rechazo de caracteres no admitidos.
- Rechazo de bloques cifrados mal formados.
- Rechazo de longitudes inconsistentes.
- Manejo de errores sin cierre inesperado de la aplicación.

Estas comprobaciones permiten evaluar el funcionamiento del sistema y la recuperación exacta del mensaje original.

## 11. Dependencias

Las dependencias externas necesarias para ejecutar la aplicación están especificadas en el archivo `requirements.txt`.

La interfaz utiliza Streamlit, mientras que los algoritmos matemáticos RSA están implementados directamente en Python.
