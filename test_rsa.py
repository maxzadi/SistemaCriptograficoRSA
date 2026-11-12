import unittest

from encriptacion import Mensaje
from recursos import es_primo, mcd, inverso_modular, exponenciacion_modular

P, Q, E = 367, 373, 17


class PruebasRSA(unittest.TestCase):
    def cifrar_y_recuperar(self, texto):
        cifrado, longitud, llave = Mensaje(texto, P, Q, E).encriptar()
        d, recuperado = Mensaje(cifrado, P, Q, E, False, longitud).desencriptar()
        self.assertEqual(recuperado, texto)
        self.assertEqual(longitud, len(texto))
        self.assertEqual(llave, (17, 136891))
        self.assertEqual(d, 8009)
        self.assertEqual(len(cifrado.split()), (len(texto) + 1) // 2)
        self.assertTrue(all(len(b) == 6 and b.isdecimal() for b in cifrado.split()))

    def test_ejemplo_oficial(self):
        cifrado, longitud, llave = Mensaje('RSA', P, Q, E).encriptar()
        self.assertEqual(cifrado, '026054 123875')
        self.assertEqual(longitud, 3)
        self.assertEqual(llave, (17, 136891))
        self.cifrar_y_recuperar('RSA')

    def test_mensajes_validos(self):
        textos = ['HOLA', 'RSA', 'aB09!?', '  Hola  RSA  ', 'A ', ' A', '  ', '~!@#$%^&*()_+', ''.join(chr(i) for i in range(32, 127))]
        for texto in textos:
            with self.subTest(texto=repr(texto)):
                self.cifrar_y_recuperar(texto)

    def test_algoritmos(self):
        self.assertTrue(es_primo(367))
        self.assertFalse(es_primo(4))
        self.assertEqual(mcd(17, 136152), 1)
        self.assertEqual(inverso_modular(17, 136152), 8009)
        self.assertEqual(exponenciacion_modular(82083, 17, 136891), 26054)

    def test_parametros_invalidos(self):
        casos = [(4, Q, E), (P, P, E), (2, 3, E), (P, Q, 1), (P, Q, 2), ('367', Q, E)]
        for p, q, e in casos:
            with self.subTest(p=p, q=q, e=e):
                with self.assertRaises(ValueError):
                    Mensaje('RSA', p, q, e)

    def test_caracteres_invalidos(self):
        for texto in ['á', 'ñ', 'A\nB', 'A\tB', '🙂']:
            with self.subTest(texto=repr(texto)):
                with self.assertRaises(ValueError):
                    Mensaje(texto, P, Q, E)

    def test_cifrados_invalidos(self):
        casos = [('123 456789', 4), ('136891', 2), ('000001  000002', 4), ('000001 ', 2), ('000001', 3), ('026054 123875', 10), ('abcdef', 2), ('000001', '2'), ('', 2)]
        for cifrado, longitud in casos:
            with self.subTest(cifrado=cifrado, longitud=longitud):
                with self.assertRaises(ValueError):
                    Mensaje(cifrado, P, Q, E, False, longitud)

    def test_ascii_invalido_al_descifrar(self):
        # El bloque cifrado 000000 descifra a 000000: ASCII 000 no es válido.
        with self.assertRaises(ValueError):
            Mensaje('000000', P, Q, E, False, 2).desencriptar()

    def test_relleno_invalido_al_descifrar(self):
        # 'AB' tiene longitud par y no contiene espacio de relleno.
        cifrado, _, _ = Mensaje('AB', P, Q, E).encriptar()
        with self.assertRaises(ValueError):
            Mensaje(cifrado, P, Q, E, False, 1).desencriptar()


