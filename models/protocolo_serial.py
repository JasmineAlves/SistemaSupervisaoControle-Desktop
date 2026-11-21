# Checksum = valor calculado a partir dos dados transmitidos, p/ conerir se teve alguma alteração 
# durante a comunicação

class ProtocoloSerial:
    @staticmethod
    def calcular_checksum(dados: str) -> int:
        checksum = 0

        for caractere in dados:
            # Realiza xor entre checksum atual e valor ascii do caractere
            checksum ^= ord(caractere)
        # Volta o checksum calculado
        return checksum

    @classmethod
    def interpretar(cls, mensagem: str) -> dict:
        # Remove espaços+quebra de linha no início e final da mensagem
        mensagem = mensagem.strip()
        # Conf se mensagem tem identificador esperado
        if not mensagem.startswith("$DAT,"):
            raise ValueError("Identificador de mensagem inválido")
        # Conf se existe separador entre dados e o checksum
        if "*" not in mensagem:
            raise ValueError("Checksum ausente")

        # Separa dados da mensagemm do checksum recebido e remove '$' (caractere inicial) antes
        dados, checksum_recebido = mensagem[1:].split("*", 1)

        # Conf se checksum tem 2 caracteres pra dar certo
        if len(checksum_recebido) != 2:
            raise ValueError("Checksum em formato inválido")

        try:
            # Converte checksum de hexa pra int
            checksum_recebido = int(checksum_recebido, 16)
        except ValueError:
            # Se checksum não é um hexa válido
            raise ValueError("Checksum hexadecimal inválido")

        # Calcula checksum dnv com dados recebidos
        checksum_calculado = cls.calcular_checksum(dados)

        # Compara calculado com recebido
        if checksum_calculado != checksum_recebido:
            raise ValueError("Checksum incorreto")
        # Separa em campos usando vírgula
        campos = dados.split(",")

        # Se quant de campos recebidos é a esperada
        if len(campos) != 5:
            raise ValueError("Quantidade de campos inválida")

        # Atribui campo à respectiva var
        identificador, a0, a1, status_rele, status_botao = campos

        if identificador != "DAT":
            raise ValueError("Identificador de dados inválido")

        # Converte valores recebidos de str pra int
        try:
            a0 = int(a0)
            a1 = int(a1)
            status_rele = int(status_rele)
            status_botao = int(status_botao)
        except ValueError:
            # Se algum campo n possui valor num válido
            raise ValueError("Dados numéricos inválidos")
        # Conf se valor do canal a0 e a1 estão dentro da faixa do adc
        if not 0 <= a0 <= 1023:
            raise ValueError("Valor A0 fora da faixa")
        if not 0 <= a1 <= 1023:
            raise ValueError("Valor A1 fora da faixa")
        # Conf se estado do relé é válido
        if status_rele not in (0, 1):
            raise ValueError("Status do relé inválido")
        # COnf se estado do botão é valido
        if status_botao not in (0, 1):
            raise ValueError("Status do botão inválido")

        # Retorna dados
        return {
            "a0": a0,
            "a1": a1,
            "status_rele": status_rele,
            "status_botao": status_botao
        }