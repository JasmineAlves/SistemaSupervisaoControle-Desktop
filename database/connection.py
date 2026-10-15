import sqlite3 
from pathlib import Path

# Centraliza operações relacionadas ao bd
class Database:
    DIR_PROJETO = Path(__file__).resolve().parent.parent
    DIR_DADOS = DIR_PROJETO / "data"
    DB_NAME = DIR_DADOS / "smartgrid.db"

    # Tempo máximo em segundos p/ bloqueio no bd antes de lançar erro
    TIMEOUT = 5.0

    @classmethod
    def get_connection(cls):
        # Cria e retorna uma conexão configurada com o SQLite
        cls.DIR_DADOS.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(
            str(cls.DB_NAME),
            timeout=cls.TIMEOUT
        )

        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @classmethod
    def init_db(cls):
        # Cria tabelas caso ainda não existam, solicitando conexão já configurada pelo get.connection()
        conn = cls.get_connection()

        try:
            with conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS dispositivos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tag TEXT NOT NULL UNIQUE,
                        tipo TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'FECHADO'
                            CHECK (status IN ('ABERTO', 'FECHADO')),
                        ultima_atualizacao TEXT NOT NULL
                            DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS historico_eventos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data_hora TEXT NOT NULL
                            DEFAULT CURRENT_TIMESTAMP,
                        tipo_evento TEXT NOT NULL,
                        valor_medido REAL,
                        descricao TEXT NOT NULL,
                        dispositivo_id INTEGER,
                        FOREIGN KEY (dispositivo_id)
                            REFERENCES dispositivos(id)
                            ON DELETE SET NULL
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS limites (
                        id INTEGER PRIMARY KEY CHECK (id = 1),
                        tensao_max REAL NOT NULL
                            CHECK (tensao_max >= 0),
                        corrente_max REAL NOT NULL
                            CHECK (corrente_max >= 0),
                        potencia_max REAL NOT NULL
                            CHECK (potencia_max >= 0)
                    )
                """)
                conn.execute("""
                    INSERT OR IGNORE INTO limites (
                        id,
                        tensao_max,
                        corrente_max,
                        potencia_max
                    )
                    VALUES (1, 0.0, 0.0, 0.0)
                """)
        finally:
            conn.close()
