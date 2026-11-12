from recursos import *
from encriptacion import Mensaje

#Encriptar mensaje
a = Mensaje("RSA",367,373,17)
encriptacion = a.desencriptar()
print(a.get_resultado())

#Desencriptar mensaje
b = Mensaje("026054 123875",367,373,17,False,3)
desencriptacion = b.desencriptar()
print(b.get_resultado())