import unittest

from models.protocolo_serial import ProtocoloSerial


class TestProtocoloSerial(unittest.TestCase):

    @staticmethod
    def criar_mensagem(a0=512, a1=512, rele=0, botao=0):
        dados = f"DAT,{a0},{a1},{rele},{botao}"
        checksum = ProtocoloSerial.calcular_checksum(dados)
        return f"${dados}*{checksum:02X}"

    def test_calcular_checksum(self):
        dados = "DAT,512,512,0,0"

        resultado = ProtocoloSerial.calcular_checksum(dados)

        self.assertIsInstance(resultado, int)
        self.assertEqual(resultado, 0x51)

    def test_interpretar_mensagem_valida(self):
        mensagem = self.criar_mensagem(
            a0=512,
            a1=600,
            rele=1,
            botao=0
        )

        resultado = ProtocoloSerial.interpretar(mensagem)

        self.assertEqual(resultado, {
            "a0": 512,
            "a1": 600,
            "status_rele": 1,
            "status_botao": 0
        })

    def test_interpretar_mensagem_com_quebra_de_linha(self):
        mensagem = self.criar_mensagem() + "\r\n"

        resultado = ProtocoloSerial.interpretar(mensagem)

        self.assertEqual(resultado["a0"], 512)

    def test_identificador_invalido(self):
        mensagem = self.criar_mensagem().replace("$DAT,", "$ERR,")

        with self.assertRaises(ValueError):
            ProtocoloSerial.interpretar(mensagem)

    def test_checksum_ausente(self):
        mensagem = "$DAT,512,512,0,0"

        with self.assertRaises(ValueError):
            ProtocoloSerial.interpretar(mensagem)

    def test_checksum_incorreto(self):
        mensagem = self.criar_mensagem()
        mensagem = mensagem[:-2] + "FF"

        with self.assertRaises(ValueError):
            ProtocoloSerial.interpretar(mensagem)

    def test_checksum_formato_invalido(self):
        mensagem = self.criar_mensagem()[:-2] + "GG"

        with self.assertRaises(ValueError):
            ProtocoloSerial.interpretar(mensagem)

    def test_quantidade_campos_invalida(self):
        dados = "DAT,512,512,0"
        checksum = ProtocoloSerial.calcular_checksum(dados)
        mensagem = f"${dados}*{checksum:02X}"

        with self.assertRaises(ValueError):
            ProtocoloSerial.interpretar(mensagem)

    def test_dados_nao_numericos(self):
        dados = "DAT,ABC,512,0,0"
        checksum = ProtocoloSerial.calcular_checksum(dados)
        mensagem = f"${dados}*{checksum:02X}"

        with self.assertRaises(ValueError):
            ProtocoloSerial.interpretar(mensagem)

    def test_adc_a0_fora_da_faixa(self):
        mensagem = self.criar_mensagem(a0=1024)

        with self.assertRaises(ValueError):
            ProtocoloSerial.interpretar(mensagem)

    def test_adc_a1_fora_da_faixa(self):
        mensagem = self.criar_mensagem(a1=-1)

        with self.assertRaises(ValueError):
            ProtocoloSerial.interpretar(mensagem)

    def test_status_rele_invalido(self):
        mensagem = self.criar_mensagem(rele=2)

        with self.assertRaises(ValueError):
            ProtocoloSerial.interpretar(mensagem)

    def test_status_botao_invalido(self):
        mensagem = self.criar_mensagem(botao=2)

        with self.assertRaises(ValueError):
            ProtocoloSerial.interpretar(mensagem)


if __name__ == "__main__":
    unittest.main()