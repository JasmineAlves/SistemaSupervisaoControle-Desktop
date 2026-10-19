import sqlite3
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from database.connection import Database
from models.registro_repository import RegistroRepository


class TestCorteEmergencial(unittest.TestCase):
    def setUp(self):
        self.pasta_temporaria = tempfile.TemporaryDirectory()
        self.db_original = Database.DB_NAME
        self.dir_original = Database.DIR_DADOS

        Database.DIR_DADOS = Path(self.pasta_temporaria.name)
        Database.DB_NAME = Path(self.pasta_temporaria.name) / "teste.db"
        Database.init_db()

        conn = Database.get_connection()
        try:
            conn.execute(
                """
                INSERT INTO dispositivos (tag, tipo, status)
                VALUES (?, ?, ?)
                """,
                ("DISJUNTOR_PRINCIPAL", "Disjuntor", "FECHADO")
            )
            conn.execute(
                """
                CREATE TRIGGER falhar_evento_teste
                BEFORE INSERT ON historico_eventos
                WHEN NEW.descricao = 'FORCAR_FALHA_TESTE'
                BEGIN
                    SELECT RAISE(ABORT, 'falha simulada');
                END
                """
            )
            conn.commit()
        finally:
            conn.close()

    def tearDown(self):
        Database.DB_NAME = self.db_original
        Database.DIR_DADOS = self.dir_original
        self.pasta_temporaria.cleanup()

    def test_rollback_se_evento_falhar(self):
        registro = SimpleNamespace(
            timestamp=datetime.now(),
            tipo="Alerta",
            valor="teste",
            descricao="FORCAR_FALHA_TESTE"
        )

        with self.assertRaises(sqlite3.IntegrityError):
            RegistroRepository.registrar_corte(
                aberto=True,
                registro=registro
            )

        conn = Database.get_connection()
        try:
            dispositivo = conn.execute(
                """
                SELECT status FROM dispositivos
                WHERE tag = ?
                """,
                ("DISJUNTOR_PRINCIPAL",)
            ).fetchone()

            quantidade_eventos = conn.execute(
                "SELECT COUNT(*) FROM historico_eventos"
            ).fetchone()[0]

            self.assertEqual(dispositivo["status"], "FECHADO")
            self.assertEqual(quantidade_eventos, 0)
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
