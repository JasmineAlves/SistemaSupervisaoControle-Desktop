from database.connection import Database

# Salva e consulta os limites de segurança no SQLite
class LimitesRepository:

    @staticmethod
    def obter():
        conn = Database.get_connection()
        try:
            # Consulta os limites armazenados
            resultado = conn.execute(
                """
                SELECT tensao_max, corrente_max, potencia_max
                FROM limites
                WHERE id = 1
                """
            ).fetchone()
            # 'fetchone()' = retorna apenas uma linha
            # Retorna os limites encontrados ou None
            return resultado
        finally:
            conn.close()

    @staticmethod
    def salvar(tensao: float, corrente: float, potencia: float):
        conn = Database.get_connection()
        try:
            # Att os limites
            with conn:
                cursor = conn.execute(
                    """
                    UPDATE limites
                    SET tensao_max = ?,
                        corrente_max = ?,
                        potencia_max = ?
                    WHERE id = 1
                    """,
                    (tensao, corrente, potencia)
                )
                # Informa se o registro não existe
                if cursor.rowcount != 1:
                    raise RuntimeError(
                        "Não foi possível atualizar os limites de segurança."
                    )
        finally:
            conn.close()
