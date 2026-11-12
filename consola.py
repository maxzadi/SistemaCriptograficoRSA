
from encriptacion import Mensaje

# Parametros del ejemplo oficial
p = 367
q = 373
e = 17
mensaje_original = "RSA"

# ENCRIPTACION
rsa = Mensaje(mensaje_original, p, q, e)
cifrado, longitud, llave_publica = rsa.encriptar()

print("===== ENCRIPTACION =====")
print(f"Mensaje original: {mensaje_original!r}")
print(f"Mensaje cifrado: {cifrado}")
print(f"Longitud original: {longitud}")
print(f"Llave publica: {llave_publica}")

# DESENCRIPTACION
rsa_descifrado = Mensaje(cifrado, p, q, e, False, longitud)
d, mensaje_recuperado = rsa_descifrado.desencriptar()

print("\n===== DESENCRIPTACION =====")
print(f"Exponente privado: {d}")
print(f"Mensaje recuperado: {mensaje_recuperado!r}")

# COMPROBACION
if mensaje_recuperado == mensaje_original:
    print("\nPRUEBA EXITOSA: El mensaje se recupero exactamente.")
else:
    print("\nERROR: El mensaje recuperado es diferente al original.")
