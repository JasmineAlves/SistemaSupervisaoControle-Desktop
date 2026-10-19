from database.connection import Database

# Salva e consulta os limites de segurança no SQLite
class LimitesRepository:

    @staticmethod
    def obter():
        conn = Database.get_connection()
        try:
            # Consulta os limites armazenados
            return conn.execute(
                """
                SELECT tensao_max, corrente_max, potencia_max
                FROM limites
                WHERE id = ?
                """,
                (1,)
            ).fetchone()
             # 'fetchone()' = retorna apenas uma linha
            # Retorna os limites encontrados ou None
        finally:
            conn.close()

    @staticmethod
    def salvar(tensao: float, corrente: float, potencia: float):
        conn = Database.get_connection()
        try:
            # Att os limites
            with conn:
                conn.execute(
                    """
                    INSERT INTO limites (
                        id, tensao_max, corrente_max, potencia_max
                    )
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        tensao_max = excluded.tensao_max,
                        corrente_max = excluded.corrente_max,
                        potencia_max = excluded.potencia_max
                    """,
                    (1, tensao, corrente, potencia)
                )
        finally:
            conn.close()