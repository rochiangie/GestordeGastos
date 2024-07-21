import unittest
from unittest.mock import patch
import tkinter as tk
from tkinter import messagebox
from ahorro import registrar_gasto, ver_saldo, ver_gastos, configurar_presupuesto, saldo_actual, gastos

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global root
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal durante las pruebas

    @classmethod
    def tearDownClass(cls):
        if root.winfo_exists():
            root.update()  # Asegurarse de que todos los eventos pendientes se procesen
            root.destroy()

    def setUp(self):
        global saldo_actual, gastos
        saldo_actual = 1500000.0
        gastos = []

    @patch("tkinter.messagebox.showinfo")
    def test_registrar_gasto(self, mock_showinfo):
        if root.winfo_exists():
            registrar_gasto()
            ventana_gasto = root.winfo_children()[-1]
            
            descripcion_entry = ventana_gasto.winfo_children()[1]
            cantidad_entry = ventana_gasto.winfo_children()[3]
            
            descripcion_entry.insert(0, "Comida")
            cantidad_entry.insert(0, "100")
            
            guardar_btn = ventana_gasto.winfo_children()[4]
            guardar_btn.invoke()
            
            self.assertEqual(saldo_actual, 1499900.0)
            self.assertEqual(gastos, [{"descripcion": "Comida", "cantidad": 100.0}])
            mock_showinfo.assert_called_with("Info", "Gasto registrado con éxito")

    @patch("tkinter.messagebox.showinfo")
    def test_ver_saldo(self, mock_showinfo):
        if root.winfo_exists():
            ver_saldo()
            mock_showinfo.assert_called_with("Saldo Actual", "Tu saldo actual es: $1500000.00")

    def test_ver_gastos(self):
        if root.winfo_exists():
            gastos.append({"descripcion": "Comida", "cantidad": 100.0})
            ver_gastos()
            ventana_gastos = root.winfo_children()[-1]
            label_text = ventana_gastos.winfo_children()[0].cget("text")
            self.assertEqual(label_text, "Comida: $100.00")

    @patch("tkinter.messagebox.showinfo")
    def test_configurar_presupuesto(self, mock_showinfo):
        if root.winfo_exists():
            configurar_presupuesto()
            ventana_presupuesto = root.winfo_children()[-1]
            
            presupuesto_entry = ventana_presupuesto.winfo_children()[1]
            presupuesto_entry.insert(0, "2000000")
            
            guardar_btn = ventana_presupuesto.winfo_children()[3]
            guardar_btn.invoke()
            
            mock_showinfo.assert_called_with("Info", "Presupuesto configurado con éxito")

if __name__ == "__main__":
    unittest.main()

