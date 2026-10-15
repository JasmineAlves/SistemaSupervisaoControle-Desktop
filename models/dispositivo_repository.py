# OBS: Abre a conexão: sempre 'conn = Database.get_connection()'
from database.connection import Database

# Operações de persistência dos dispositivos no SQLite
class DispositivoRepository:

    @staticmethod
    def inserir(tag: str, tipo: str, status: str = "FECHADO") -> int:
        # Faz insert para dispositvo e retorna id
        conn = Database.get_connection()
        # Inicia um insert mas reverte em caso de erro
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO dispositivos (tag, tipo, status)
                    VALUES (?, ?, ?)
                    """,
                    (tag, tipo, status)
                )
                return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        # Faz query para dispositivos cadastrados
        conn = Database.get_connection()
        try:
            return conn.execute(
                """
                SELECT id, tag, tipo, status, ultima_atualizacao
                FROM dispositivos
                ORDER BY id
                """
            ).fetchall()        
            # fetchall() = recupera todas as linhas da consulta (lista de registros)
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(dispositivo_id: int):
        # Faz query de dispositivo por id
        conn = Database.get_connection()
        try:
            return conn.execute(
                """
                SELECT id, tag, tipo, status, ultima_atualizacao
                FROM dispositivos
                WHERE id = ?
                """,
                (dispositivo_id,)
            ).fetchone()
            # 'fetchone()' = retorna apenas uma linha
        finally:
            conn.close()

    @staticmethod
    def atualizar(dispositivo_id: int, tag: str, tipo: str, status: str) -> bool:
        # Faz update de dados de dispositivo por id
        conn = Database.get_connection()
        try:
            with conn:
                cursor = conn.execute(
                    """
                    UPDATE dispositivos
                    SET tag = ?,
                        tipo = ?,
                        status = ?,
                        ultima_atualizacao = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (tag, tipo, status, dispositivo_id)
                )
                # 'rowcount' = quantas linhas foram afetadas
                return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def deletar(dispositivo_id: int) -> bool:
        # Faz delete de dispositivo por id
        conn = Database.get_connection()
        try:
            with conn:
                cursor = conn.execute(
                    """
                    DELETE FROM dispositivos
                    WHERE id = ?
                    """,
                    (dispositivo_id,)
                )
                # Informa se algum foi excluido
                return cursor.rowcount > 0
        finally:
            conn.close()
