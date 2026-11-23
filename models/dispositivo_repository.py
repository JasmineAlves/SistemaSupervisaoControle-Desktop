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
    def garantir_cadastro(tag: str, tipo: str, status: str = "FECHADO", conn=None) -> int:
        # Garante que o dispositivo exista (idempotente) e retorna seu id.
        # Aceita uma conexão externa para participar da mesma transação do chamador.
        conn_externa = conn is not None
        conn = conn or Database.get_connection()
        try:
            if conn_externa:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO dispositivos (tag, tipo, status)
                    VALUES (?, ?, ?)
                    """,
                    (tag, tipo, status)
                )
                dispositivo = conn.execute(
                    "SELECT id FROM dispositivos WHERE tag = ?",
                    (tag,)
                ).fetchone()
            else:
                with conn:
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO dispositivos (tag, tipo, status)
                        VALUES (?, ?, ?)
                        """,
                        (tag, tipo, status)
                    )
                    dispositivo = conn.execute(
                        "SELECT id FROM dispositivos WHERE tag = ?",
                        (tag,)
                    ).fetchone()

            if dispositivo is None:
                raise RuntimeError(f"Não foi possível localizar o dispositivo '{tag}'.")
            return dispositivo["id"]
        finally:
            if not conn_externa:
                conn.close()

    @staticmethod
    def atualizar_status(dispositivo_id: int, status: str, conn=None) -> bool:
        # Atualiza apenas o status (e a data da última alteração) de um dispositivo.
        # Aceita uma conexão externa para participar da mesma transação do chamador.
        conn_externa = conn is not None
        conn = conn or Database.get_connection()
        try:
            if conn_externa:
                cursor = conn.execute(
                    """
                    UPDATE dispositivos
                    SET status = ?, ultima_atualizacao = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (status, dispositivo_id)
                )
            else:
                with conn:
                    cursor = conn.execute(
                        """
                        UPDATE dispositivos
                        SET status = ?, ultima_atualizacao = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """,
                        (status, dispositivo_id)
                    )
            return cursor.rowcount > 0
        finally:
            if not conn_externa:
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
