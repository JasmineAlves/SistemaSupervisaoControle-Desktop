# Worker de persistência: roda em uma QThread própria, isolando as
# gravações e consultas no SQLite da GUI thread. A dashboard só se comunica
# com ele por sinais (solicita trabalho, recebe o resultado quando pronto)
import logging
import sqlite3
from PySide6.QtCore import QObject, Signal, Slot
from models.leitura_repository import LeituraRepository

logger = logging.getLogger(__name__)


class PersistenciaWorker(QObject):
    # Emitido quando o snapshot das últimas 24h (consulta histórica) está pronto
    historico_24h_carregado = Signal(list)
    # Emitido quando o histórico filtrado por data está pronto
    historico_filtrado_carregado = Signal(list)
    # Emitido quando qualquer operação deste worker falha
    falha = Signal(str)

    @Slot(object)
    def gravar_leitura(self, medicao):
        # Persiste uma medição processada, fora da GUI thread
        try:
            LeituraRepository.inserir(medicao)
        except sqlite3.Error:
            logger.exception("Falha ao persistir leitura no SQLite")
            self.falha.emit("Falha ao persistir leitura no SQLite")

    @Slot(object, object)
    def carregar_historico_24h(self, desde, limite):
        # Recupera o snapshot usado pelo modo "24 Horas" (consulta histórica,
        # não cabe em memória como buffer ao vivo na taxa de amostragem real)
        try:
            if desde is not None:
                registros = LeituraRepository.listar_desde(desde, limite=limite)
            else:
                registros = LeituraRepository.listar_ultimas(limite)
        except sqlite3.Error:
            logger.exception("Falha ao carregar histórico de leituras persistido")
            self.falha.emit("Falha ao carregar histórico de leituras persistido")
            return

        self.historico_24h_carregado.emit(registros)

    @Slot(object, object)
    def consultar_periodo(self, data_inicio, data_fim):
        # Recupera o histórico de um intervalo de datas (modo de consulta histórica)
        try:
            registros = LeituraRepository.listar_por_periodo(data_inicio, data_fim)
        except sqlite3.Error:
            logger.exception("Falha ao consultar leituras do período selecionado")
            self.falha.emit("Falha ao consultar leituras do período selecionado")
            return

        self.historico_filtrado_carregado.emit(registros)
