import unittest
from ahorro_final import guardar_datos, cargar_datos, editar_saldo, registrar_gasto, eliminar_gasto
import json
from datetime import datetime

class TestGestorDeDinero(unittest.TestCase):

    def test_guardar_datos(self):
        # Set up some test data
        global saldo_actual, gastos
        saldo_actual = 100.0
        gastos = [{"descripcion": "Test", "costo": 50.0, "fecha": datetime.now(), "categoria": "Test"}]

        # Call the function to save the data
        guardar_datos()

        # Check if the data was saved correctly
        with open("datos.json", "r") as archivo:
            datos = json.load(archivo)
            self.assertEqual(datos["saldo_actual"], 100.0)
            self.assertEqual(len(datos["gastos"]), 1)
            self.assertEqual(datos["gastos"][0]["descripcion"], "Test")
            self.assertEqual(datos["gastos"][0]["costo"], 50.0)

    def test_cargar_datos(self):
        # Set up some test data
        with open("datos.json", "w") as archivo:
            json.dump({"saldo_actual": 100.0, "gastos": [{"descripcion": "Test", "costo": 50.0, "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "categoria": "Test"}]}, archivo)

        # Call the function to load the data
        cargar_datos()

        # Check if the data was loaded correctly
        self.assertEqual(saldo_actual, 100.0)
        self.assertEqual(len(gastos), 1)
        self.assertEqual(gastos[0]["descripcion"], "Test")
        self.assertEqual(gastos[0]["costo"], 50.0)

    def editar_saldo(monto):
        global saldo_actual
        saldo_actual += monto

    def registrar_gasto(descripcion, costo, fecha, categoria):
        global gastos
        gastos.append({"descripcion": descripcion, "costo": costo, "fecha": fecha, "categoria": categoria})

    def test_cargar_datos(self):
        cargar_datos()
        self.assertEqual(saldo_actual, 100.0)

    def test_editar_saldo(self):
        cargar_datos()
        editar_saldo(50.0)
        self.assertEqual(saldo_actual, 150.0)

    def test_eliminar_gasto(self):
        cargar_datos()
        gastos.append({"descripcion": "Test", "costo": 50.0, "fecha": datetime.now(), "categoria": "porro"})
        eliminar_gasto(0)
        self.assertEqual(len(gastos), 0)

    def test_registrar_gasto(self):
        cargar_datos()
        registrar_gasto("Test", 50.0, datetime.now(), "Test")
        self.assertEqual(len(gastos), 1)

if __name__ == "__main__":
    unittest.main()