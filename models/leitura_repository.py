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
    def _amostrar(cls, conn, clausula_where, parametros, limite):
        # Amostra até 'limite' leituras distribuídas por TODO o intervalo
        # filtrado (não só as mais recentes) - um ORDER BY DESC LIMIT puro
        # pegaria só o fim do período (a 200Hz, 5000 linhas = 25 segundos),
        # descartando tudo antes disso num período longo (ex.: 24h ou semanas)
        total = conn.execute(
            f"SELECT COUNT(*) FROM leituras WHERE {clausula_where}",
            parametros
        ).fetchone()[0]

        if total == 0:
            return []

        # Divide as leituras em até 'limite' "baldes" de tamanho igual ao
        # longo do período e mantém a primeira leitura de cada balde que
        # muda (balde = posição * limite // total). Evita o "efeito serrote"
        # de um passo fixo (ex.: ceil(total/limite)), que faz a quantidade
        # de pontos cair bruscamente sempre que o total cruza um múltiplo do
        # limite - aqui a contagem cresce suavemente conforme o período aumenta
        return conn.execute(
            f"""
            SELECT {cls._COLUNAS}
            FROM (
                SELECT {cls._COLUNAS},
                       (ROW_NUMBER() OVER (ORDER BY data_hora, id) - 1) AS rn
                FROM leituras
                WHERE {clausula_where}
            )
            WHERE rn = 0
               OR (rn * ?) / ? != ((rn - 1) * ?) / ?
            ORDER BY data_hora
            """,
            parametros + (limite, total, limite, total)
        ).fetchall()

    @classmethod
    def listar_por_periodo(cls, data_inicio, data_fim, limite=5000):
        # Consulta as leituras dentro do intervalo de data/horário informado
        # (comparação direta na string ISO, sem truncar pra granularidade de dia)
        conn = Database.get_connection()
        try:
            return cls._amostrar(
                conn,
                "data_hora BETWEEN ? AND ?",
                (data_inicio.isoformat(), data_fim.isoformat()),
                limite
            )
        finally:
            conn.close()

    @classmethod
    def listar_desde(cls, instante, limite=5000):
        # Consulta as leituras a partir de um instante (ex.: últimas 24h)
        conn = Database.get_connection()
        try:
            return cls._amostrar(
                conn,
                "data_hora >= ?",
                (instante.isoformat(),),
                limite
            )
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
