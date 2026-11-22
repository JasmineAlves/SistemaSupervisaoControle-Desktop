# Representa uma medição elétrica realizada pelo sistema
# Armazena valores brutos dos sensores, grandezas elétricas e momento da medição
from datetime import datetime
import math

class Medicao:
    # Parâmetros de conversão dos sensors q devem ser definidos conforme o circuito de condicionamento e calibração
    # tensão do sistema de 0-12v pois acima pode danificar
    FATOR_TENSAO = 12.0 / 1023.0
    OFFSET_TENSAO = 0.0

    # 0A centro analógico prox a 2,5v e 512 no conversor adc, acima + e abaixo -
    FATOR_CORRENTE = 30.0 / 512.0
    OFFSET_CORRENTE = 512

    # Referência e resolução do adc
    REFERENCIA_ADC = 3.3
    RESOLUCAO_ADC = 1023

    def __init__(
        self,
        v=None,
        i=None,
        disjuntor=False,
        timestamp=None,
        adc_tensao=None,
        adc_corrente=None
    ):
        self.adc_tensao = adc_tensao
        self.adc_corrente = adc_corrente

        self.tensao = v
        self.corrente = i
        self.potencia = v * i if v is not None and i is not None else None

        self.disjuntor = disjuntor
        self.timestamp = timestamp or datetime.now()

    @classmethod
    def validar_adc(cls, valor):
        valor = float(valor)

        if not valor.is_integer():
            raise ValueError("Valor ADC deve ser inteiro")

        valor = int(valor)

        if not 0 <= valor <= cls.RESOLUCAO_ADC:
            raise ValueError("Valor ADC fora da faixa permitida")

        return valor

    @classmethod
    def converter_adc(cls, adc, fator, offset, permitir_negativo=False):
        if fator is None:
            return None

        valor = adc * fator + offset

        if not math.isfinite(valor):
            raise ValueError("Valor convertido inválido")

        if permitir_negativo:
            return valor

        return max(0.0, valor)

    @classmethod
    def a_partir_dos_dados_brutos(
        cls,
        adc_tensao,
        adc_corrente,
        disjuntor,
        timestamp=None
    ):
        adc_tensao = cls.validar_adc(adc_tensao)
        adc_corrente = cls.validar_adc(adc_corrente)

        tensao = cls.converter_adc(
            adc_tensao,
            cls.FATOR_TENSAO,
            cls.OFFSET_TENSAO
        )

        corrente = cls.converter_adc(
            adc_corrente - cls.OFFSET_CORRENTE,
            cls.FATOR_CORRENTE,
            0.0,
            permitir_negativo=True
        )

        return cls(
            v=tensao,
            i=corrente,
            disjuntor=disjuntor,
            timestamp=timestamp,
            adc_tensao=adc_tensao,
            adc_corrente=adc_corrente
        )
