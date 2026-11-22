# OBS: Abre a conexão: sempre 'conn = Database.get_connection()'
from database.connection import Database

# Salva e consulta o histórico de leituras (tensão, corrente e potência)
class LeituraRepository:
    # Colunas comuns às consultas de leituras, nesta ordem
    _COLUNAS = """
        id,
        data_hora,
        tensao,
        corrente,
        potencia,
        disjuntor_fechado,
        adc_tensao,
        adc_corrente
    """

    @staticmethod
    def inserir(medicao):
        # Persiste uma medição elétrica processada
        conn = Database.get_connection()
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO leituras (
                        data_hora,
                        tensao,
                        corrente,
                        potencia,
                        disjuntor_fechado,
                        adc_tensao,
                        adc_corrente
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        medicao.timestamp.isoformat(),
                        medicao.tensao,
                        medicao.corrente,
                        medicao.potencia,
                        1 if medicao.disjuntor else 0,
                        medicao.adc_tensao,
                        medicao.adc_corrente
                    )
                )
                # Retorna id da leitura
                return cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def listar_por_periodo(cls, data_inicio, data_fim, limite=5000):
        # Consulta as leituras dentro do intervalo de datas informado
        # Limitado para não travar a interface com períodos muito longos/densos
        conn = Database.get_connection()
        try:
            registros = conn.execute(
                f"""
                SELECT {cls._COLUNAS}
                FROM leituras
                WHERE date(data_hora) BETWEEN date(?) AND date(?)
                ORDER BY data_hora DESC, id DESC
                LIMIT ?
                """,
                (data_inicio.isoformat(), data_fim.isoformat(), limite)
            ).fetchall()
            return list(reversed(registros))
        finally:
            conn.close()

    @classmethod
    def listar_desde(cls, instante, limite=5000):
        # Consulta as leituras a partir de um instante (ex.: últimas 24h)
        # Limitado para não travar a interface quando há muitas leituras na janela
        conn = Database.get_connection()
        try:
            registros = conn.execute(
                f"""
                SELECT {cls._COLUNAS}
                FROM leituras
                WHERE data_hora >= ?
                ORDER BY data_hora DESC, id DESC
                LIMIT ?
                """,
                (instante.isoformat(), limite)
            ).fetchall()
            return list(reversed(registros))
        finally:
            conn.close()

    @classmethod
    def listar_ultimas(cls, limite=1000):
        # Consulta as leituras mais recentes, já em ordem cronológica
        conn = Database.get_connection()
        try:
            registros = conn.execute(
                f"""
                SELECT {cls._COLUNAS}
                FROM leituras
                ORDER BY data_hora DESC, id DESC
                LIMIT ?
                """,
                (limite,)
            ).fetchall()
            return list(reversed(registros))
        finally:
            conn.close()
