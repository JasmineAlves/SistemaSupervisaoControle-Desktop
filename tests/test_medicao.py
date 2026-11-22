# rodar teste: python3 -m unittest tests.test_medicao -v
import unittest
from models.medicao import Medicao


class TestMedicao(unittest.TestCase):

    def test_validar_adc_valido(self):
        self.assertEqual(Medicao.validar_adc(0), 0)
        self.assertEqual(Medicao.validar_adc(512), 512)
        self.assertEqual(Medicao.validar_adc(1023), 1023)

    def test_validar_adc_invalido(self):
        valores_invalidos = [-1, 1024, 1.5, "abc"]

        for valor in valores_invalidos:
            with self.subTest(valor=valor):
                with self.assertRaises((ValueError, TypeError)):
                    Medicao.validar_adc(valor)

    def test_converter_tensao(self):
        resultado = Medicao.converter_adc(
            512,
            12.0 / 1023.0,
            0.0
        )

        self.assertAlmostEqual(resultado, 6.006, places=3)

    def test_converter_adc_limita_valor_negativo(self):
        resultado = Medicao.converter_adc(
            0,
            1.0,
            -10.0
        )

        self.assertEqual(resultado, 0.0)

    def test_converter_corrente_permite_valor_negativo(self):
        resultado = Medicao.converter_adc(
            -512,
            30.0 / 512.0,
            0.0,
            permitir_negativo=True
        )

        self.assertAlmostEqual(resultado, -30.0)

    def test_converter_sem_calibracao(self):
        resultado = Medicao.converter_adc(
            512,
            None,
            0.0
        )

        self.assertIsNone(resultado)

    def test_calcular_potencia(self):
        medicao = Medicao(v=220.0, i=5.0)

        self.assertAlmostEqual(medicao.potencia, 1100.0)

    def test_potencia_sem_medicao_completa(self):
        medicao = Medicao(v=220.0, i=None)

        self.assertIsNone(medicao.potencia)

    def test_medicao_a_partir_dos_dados_brutos(self):
        medicao = Medicao.a_partir_dos_dados_brutos(
            adc_tensao=512,
            adc_corrente=512,
            disjuntor=False
        )

        self.assertAlmostEqual(medicao.tensao, 6.006, places=3)
        self.assertAlmostEqual(medicao.corrente, 0.0, places=3)
        self.assertAlmostEqual(medicao.potencia, 0.0, places=3)

    def test_medicao_corrente_negativa(self):
        medicao = Medicao.a_partir_dos_dados_brutos(
            adc_tensao=512,
            adc_corrente=256,
            disjuntor=False
        )

        self.assertAlmostEqual(medicao.corrente, -15.0, places=3)

    def test_medicao_corrente_positiva(self):
        medicao = Medicao.a_partir_dos_dados_brutos(
            adc_tensao=512,
            adc_corrente=768,
            disjuntor=False
        )

        self.assertAlmostEqual(medicao.corrente, 15.0, places=3)

    def test_medicao_preserva_dados_brutos(self):
        medicao = Medicao.a_partir_dos_dados_brutos(
            adc_tensao=700,
            adc_corrente=600,
            disjuntor=True
        )

        self.assertEqual(medicao.adc_tensao, 700)
        self.assertEqual(medicao.adc_corrente, 600)
        self.assertTrue(medicao.disjuntor)

    def test_medicao_bruta_adc_invalido(self):
        with self.assertRaises(ValueError):
            Medicao.a_partir_dos_dados_brutos(
                adc_tensao=1024,
                adc_corrente=512,
                disjuntor=False
            )

    def test_medicao_bruta_corrente_adc_invalido(self):
        with self.assertRaises(ValueError):
            Medicao.a_partir_dos_dados_brutos(
                adc_tensao=512,
                adc_corrente=-1,
                disjuntor=False
            )


if __name__ == "__main__":
    unittest.main()