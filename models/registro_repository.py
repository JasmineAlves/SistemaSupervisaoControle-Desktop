# OBS: Abre a conexão: sempre 'conn = Database.get_connection()'
from datetime import datetime
from database.connection import Database

# Salva e consulta eventos
class RegistroRepository:
    @staticmethod
    def inserir(registro, dispositivo_id=None):
        # Faz insert de evento, com id opcional (eventos podem n pertencer a dispositivo)
        conn = Database.get_connection()
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO historico_eventos (
                        data_hora,
                        tipo_evento,
                        valor_medido,
                        descricao,
                        dispositivo_id
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        registro.timestamp.isoformat(),
                        registro.tipo,
                        registro.valor,
                        registro.descricao,
                        dispositivo_id
                    )
                )
                # Retorna id pro evento
                return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        # Faz query de todos os eventos
        conn = Database.get_connection()
        try:
            registros = conn.execute(
                """
                SELECT
                    id,
                    data_hora,
                    tipo_evento,
                    valor_medido,
                    descricao,
                    dispositivo_id
                FROM historico_eventos
                ORDER BY data_hora DESC, id DESC
                """
            ).fetchall()
            # 'fetchall()' = recupera todas as linhas da consulta (lista de registros)
            return registros
        finally:
            conn.close()

    
    @staticmethod
    def registrar_corte(aberto, registro):
        # Converte o estado recebido para os valores aceitos pela tabela
        status = "ABERTO" if aberto else "FECHADO"
        # Id fixa p/ localizar sempre o mesmo disjuntor
        tag_disjuntor = "DISJUNTOR_PRINCIPAL"
        conn = Database.get_connection()
        try:
            with conn:
                # Garante que o disjuntor exista
                conn.execute(
                    """
                    INSERT OR IGNORE INTO dispositivos (tag, tipo, status)
                    VALUES (?, ?, ?)
                    """,
                    (tag_disjuntor, "Disjuntor", "FECHADO")
                )
                # Localiza o id do disjuntor usado pelo histórico de eventos
                dispositivo = conn.execute(
                    """
                    SELECT id
                    FROM dispositivos
                    WHERE tag = ?
                    """,
                    (tag_disjuntor,)
                ).fetchone()
                # Interrompe a operação caso o dispositivo n seja encontrado
                if dispositivo is None:
                    raise RuntimeError("Não foi possível localizar o disjuntor.")
                # Atualiza o estado + data da última alteração
                cursor = conn.execute(
                    """
                    UPDATE dispositivos
                    SET status = ?, ultima_atualizacao = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (status, dispositivo["id"])
                )
                # Verifica se estado foi atualizado
                if cursor.rowcount != 1:
                    raise RuntimeError("Não foi possível atualizar o estado do disjuntor.")
                # Registra o evento
                cursor = conn.execute(
                    """
                    INSERT INTO historico_eventos (
                        data_hora,
                        tipo_evento,
                        valor_medido,
                        descricao,
                        dispositivo_id
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        registro.timestamp.isoformat(),
                        registro.tipo,
                        registro.valor,
                        registro.descricao,
                        dispositivo["id"]
                    )
                )
                # Retorna id pro evento
                id_registro = cursor.lastrowid
            return id_registro
        finally:
            conn.close()