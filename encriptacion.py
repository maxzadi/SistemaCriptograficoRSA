from recursos import *

class Mensaje:
    def __init__(self, mensaje, p, q, e, encriptar=True, L=None):
        self.validar(mensaje, p, q, e, encriptar, L)

        self.p = p
        self.q = q
        self.e = e

        self.n = p * q
        self.phi = (p - 1) * (q - 1)

        self.L = len(mensaje) if encriptar else L
        self.relleno = self.L % 2 != 0

        if encriptar:
            self.mensaje = mensaje + " " if self.relleno else mensaje
            self.C = None
        else:
            self.mensaje = None
            self.C = mensaje
            
        self.resultados = None
            
    def validar(self, mensaje, p, q, e, encriptar=True, L=None):
        # Validaciones comunes
        for nombre, valor in (("p", p), ("q", q), ("e", e)):
            if type(valor) is not int:
                raise ValueError(f"{nombre} debe ser un entero.")

        if not es_primo(p) or not es_primo(q):
            raise ValueError("p y q deben ser números primos.")

        if p == q:
            raise ValueError("p y q deben ser distintos.")

        n = p * q
        phi = (p - 1) * (q - 1)

        if not 126126 < n < 1000000:
            raise ValueError("n debe cumplir: 126126 < n < 1000000.")

        if e <= 1:
            raise ValueError("e debe ser mayor que 1.")

        if mcd(e, phi) != 1:
            raise ValueError("e y phi deben ser primos relativos.")
        
        if not isinstance(mensaje, str):
            raise ValueError("El mensaje o cifrado debe ser una cadena.")

        # Validaciones para encriptar
        if encriptar:
            for posicion, caracter in enumerate(mensaje, start=1):
                if not 32 <= ord(caracter) <= 126:
                    raise ValueError(
                        f"Carácter no admitido en la posición "
                        f"{posicion}: {caracter!r}."
                    )

        # Validaciones para desencriptar
        else:
            if type(L) is not int:
                raise ValueError("L debe ser un entero.")

            # Un cifrado vacío se admite únicamente con L = 0.
            bloques = [] if mensaje == "" else mensaje.split(" ")

            for posicion, bloque in enumerate(bloques, start=1):
                if (
                    len(bloque) != 6
                    or any(c not in "0123456789" for c in bloque)
                ):
                    raise ValueError(
                        f"El bloque {posicion} debe contener exactamente "
                        "seis dígitos del 0 al 9. Separa los bloques "
                        "con un solo espacio."
                    )

                if int(bloque) >= n:
                    raise ValueError(
                        f"El bloque {posicion} debe ser menor que n ({n})."
                    )

            k = len(bloques)

            if k == 0:
                if L != 0:
                    raise ValueError("Un cifrado vacío requiere L = 0.")
            elif L not in (2 * k, 2 * k - 1):
                raise ValueError(
                    f"Para {k} bloques, L debe ser "
                    f"{2 * k} o {2 * k - 1}."
                )
             
    #Funcion que convierte un par de caracteres en un bloque numérico
    def format(self,cadena):
        return "".join(list(map(lambda i:str(ord(i)).rjust(3,"0"),cadena)))
        
    def encriptar(self):
        #Separa el mensaje en parejas de caracteres y concatena los codigos ASCII 
        m = []
        for i in range(0,self.L,2):
            m.append(self.format(self.mensaje[i:i+2]))
            
        #Calcula el cifrado por bloque y lo junta en el cifrado final
        c = list(map(lambda i: str(exponenciacion_modular(int(i),self.e,self.n)).rjust(6,"0"), m))
        self.C = " ".join(c)
        
        #Guarda los datos de resultado
        self.resultados = {
            "Mensaje original": f'"{self.mensaje[:self.L]}"',

            "Entradas RSA": (
                f"p = {self.p}, q = {self.q}, e = {self.e}"
            ),

            "Valores calculados": (
                f"n = {self.n}, φ = {self.phi}, "
                f"MCD(e, φ) = {mcd(self.e, self.phi)}"
            ),

            "Longitud y relleno": (
                f'L = {self.L}; '
                f'relleno: {"Sí" if self.relleno else "No"}; '
                f'mensaje con relleno: "{self.mensaje}"'
            ),

            "Bloques del mensaje": " ".join(m),

            "Cifrado C": self.C,

            "Llave pública": f"({self.e}, {self.n})"
        }
        
        # (Mensaje cifrado completo, longitud original, llave pública(e,n))
        return (self.C,self.L,(self.e,self.n))
    
    def desencriptar(self):
        self.d = inverso_modular(self.e,self.phi)
        c = self.C.split()

        #Recuperacion del bloque m
        m = list(map(lambda i: str(exponenciacion_modular(int(i),self.d,self.n)).rjust(6,"0"),c))
        self.mensaje = ""
        #Conversion de bloque m a caracteres
        for i in range(len(m)):
            a,b=m[i][:3],m[i][3:]
            if not 32 <= int(a) <= 126:
                raise ValueError(
                    f"Carácter no admitido en la posición "
                    f"{i*2+1}: {a}."
                                )
            elif not 32 <= int(b) <= 126:
                raise ValueError(
                    f"Carácter no admitido en la posición "
                    f"{(i+1)*2}: {b}."
                                )
            else:
                #Si la cadena es impar no agrega el ultimo caracter
                if i==len(m)-1 and self.L%2==1:
                    if int(b) != 32:
                        raise ValueError(
                            "El último carácter recuperado debe "
                            "ser un espacio de relleno."
                        )
                        
                    self.mensaje += chr(int(a))
                else:
                    self.mensaje+=chr(int(a))+chr(int(b))
            
        #Guarda los datos de resultado
        self.resultados = {
            "Entradas RSA": (
                f"p = {self.p}, q = {self.q}, e = {self.e}"
            ),

            "Valores calculados": (
                f"n = {self.n}, φ = {self.phi}, "
                f"MCD(e, φ) = {mcd(self.e, self.phi)}"
            ),

            "Longitud y relleno": (
                f'L = {self.L}; '
                f'relleno: {"Sí" if self.relleno else "No"}'
            ),

            "Bloques del mensaje": " ".join(m),

            "Cifrado C": self.C,

            "Exponente privado": f"d = {self.d}",

            "Mensaje recuperado": f'"{self.mensaje}"'
        }
        
        return (self.d, self.mensaje)
    
    def get_resultado(self):
        return self.resultados