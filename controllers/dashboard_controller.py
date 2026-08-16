# Controle da supervisão do sistema

import random
from datetime import datetime, timedelta
import pyqtgraph as pg
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from ui.Ui_dashboard import Ui_MainWindow
from models.medicao import Medicao
from models.registro import Registro


class DashController(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Faz a simulação de uma medição inicial
        self.medicao_atual = Medicao(
            v=220.0,
            i=8.0,
            disjuntor=True
        )

        # Guarda as medições utilizadas no gráfico
        self.historico_potencia = []

        # Guarda os registros de eventos do sistema
        self.registros = []

        # Guarda o estado anterior do disjuntor
        self.disjuntor_anterior = self.medicao_atual.disjuntor

        # Guarda se o limite de potência já foi ultrapassado
        self.limite_ultrapassado = False

        # Configura o gráfico
        self.configurar_grafico()

        # Carrega dados iniciais para o gráfico
        self.carregar_historico_inicial()

        # Configura a tabela de registros
        self.configurar_tabela()

        # Registra a inicialização do sistema
        self.adicionar_registro(
            tipo="Status",
            descricao="Sistema de supervisão iniciado.",
            valor=self.formatar_medicao()
        )

        # Temporizador que atualiza periodicamente
        self.timer = QTimer()

        self.timer.timeout.connect(
            self.atualizar_medicao
        )

        # Medição inicial
        self.atualizar_dashboard()

        # Att a telemetria a cada 1s
        self.timer.start(1000)

    def configurar_grafico(self):
        # Cria o gráfico de demanda de potência

        self.grafico = pg.PlotWidget()

        self.grafico.setBackground("w")

        self.grafico.setTitle(
            "Demanda de potência",
            color="#24343B",
            size="12pt"
        )

        self.grafico.setLabel(
            "left",
            "Potência",
            units="W"
        )

        self.grafico.setLabel(
            "bottom",
            "Tempo"
        )

        self.grafico.showGrid(
            x=True,
            y=True,
            alpha=0.15
        )

        self.grafico.setMinimumHeight(190)

        # Coloca o gráfico na área reservada da dashboard
        layout = self.ui.widget_grafico.layout()

        if layout is None:
            from PySide6.QtWidgets import QVBoxLayout

            layout = QVBoxLayout(
                self.ui.widget_grafico
            )

        layout.addWidget(self.grafico)

        # Cria a curva de potência
        self.curva_potencia = self.grafico.plot(
            pen=pg.mkPen(
                color="#245A63",
                width=2
            )
        )

    def carregar_historico_inicial(self):
        # Cria dados simulados das últimas 24 horas

        agora = datetime.now()

        quantidade_pontos = 48

        for indice in range(quantidade_pontos):

            momento = agora - timedelta(
                hours=24 - (indice * 0.5)
            )

            tensao = random.uniform(
                218.0,
                222.0
            )

            corrente = random.uniform(
                5.0,
                10.0
            )

            potencia = tensao * corrente

            self.historico_potencia.append(
                {
                    "timestamp": momento,
                    "potencia": potencia
                }
            )

        # Att o gráfico com os dados iniciais
        self.atualizar_grafico()

    def atualizar_grafico(self):
        # Att a curva de demanda de potência

        valores = [
            item["potencia"]
            for item in self.historico_potencia
        ]

        tempos = list(
            range(len(valores))
        )

        self.curva_potencia.setData(
            tempos,
            valores
        )

    def atualizar_medicao(self):
        # Simula uma nova medição recebida, como se fosse um hardware

        tensao = random.uniform(
            218.0,
            222.0
        )

        corrente = random.uniform(
            7.0,
            10.0
        )

        self.medicao_atual = Medicao(
            v=tensao,
            i=corrente,
            disjuntor=True
        )

        # Adiciona a nova potência ao histórico
        self.historico_potencia.append(
            {
                "timestamp": self.medicao_atual.timestamp,
                "potencia": self.medicao_atual.potencia
            }
        )

        # Limita a quantidade de pontos armazenados
        if len(self.historico_potencia) > 1000:
            self.historico_potencia.pop(0)

        # Verifica se aconteceu algum evento
        self.verificar_eventos()

        # Att os dados da interface
        self.atualizar_dashboard()

        # Att o gráfico
        self.atualizar_grafico()

    def atualizar_dashboard(self):
        # Exibe na interface oq veio da medição

        medicao = self.medicao_atual

        # Att tensão
        self.ui.lbl_valor_tensao.setText(
            f"{medicao.tensao:.1f}"
        )

        # Att corrente
        self.ui.lbl_valor_corrente.setText(
            f"{medicao.corrente:.1f}"
        )

        # Att potência
        self.ui.lbl_valor_potencia.setText(
            f"{medicao.potencia:.1f}"
        )

        # Att estado do disjuntor
        if medicao.disjuntor:
            self.ui.lbl_status_disjuntor.setText(
                "●  FECHADO / NORMAL"
            )

            self.ui.lbl_status_detalhe.setText(
                "Instalação energizada e proteção disponível."
            )

        else:
            self.ui.lbl_status_disjuntor.setText(
                "●  ABERTO / PROTEÇÃO ATIVADA"
            )

            self.ui.lbl_status_detalhe.setText(
                "A instalação encontra-se desenergizada."
            )

        # Att o horário da última medição
        horario = medicao.timestamp.strftime(
            "%H:%M:%S"
        )

        self.ui.lbl_status_atualizacao.setText(
            f"Última atualização: {horario}"
        )

    def verificar_eventos(self):
        # Verifica se aconteceu alguma mudança relevante

        medicao = self.medicao_atual

        # Verifica mudança no estado do disjuntor
        if medicao.disjuntor != self.disjuntor_anterior:

            if medicao.disjuntor:
                self.adicionar_registro(
                    tipo="Status",
                    descricao="Disjuntor retornou ao estado normal.",
                    valor=self.formatar_medicao()
                )

            else:
                self.adicionar_registro(
                    tipo="Alerta",
                    descricao="Disjuntor aberto / proteção ativada.",
                    valor=self.formatar_medicao()
                )

            self.disjuntor_anterior = medicao.disjuntor

        # Pega o limite configurado na interface
        limite = self.ui.spin_limite_potencia.value()

        ultrapassou_limite = (
            medicao.potencia > limite
        )

        # Registra somente quando entra na condição de alerta
        if (
            ultrapassou_limite
            and not self.limite_ultrapassado
        ):
            self.adicionar_registro(
                tipo="Alerta",
                descricao="Limite de potência ultrapassado.",
                valor=self.formatar_medicao()
            )

        self.limite_ultrapassado = ultrapassou_limite

    def adicionar_registro(
        self,
        tipo,
        descricao,
        valor
    ):
        # Cria um novo registro de evento

        registro = Registro(
            tipo=tipo,
            descricao=descricao,
            valor=valor
        )

        self.registros.append(registro)

        # Att a tabela de histórico
        self.atualizar_tabela()

    def atualizar_tabela(self):
        # Att a tabela com os registros do sistema

        self.ui.tabela_registros.setRowCount(0)

        for registro in self.registros:

            linha = self.ui.tabela_registros.rowCount()

            self.ui.tabela_registros.insertRow(
                linha
            )

            # Data e hora
            self.ui.tabela_registros.setItem(
                linha,
                0,
                QTableWidgetItem(
                    registro.timestamp.strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )
                )
            )

            # Tipo
            self.ui.tabela_registros.setItem(
                linha,
                1,
                QTableWidgetItem(
                    registro.tipo
                )
            )

            # Valor medido
            self.ui.tabela_registros.setItem(
                linha,
                2,
                QTableWidgetItem(
                    registro.valor
                )
            )

            # Descrição
            self.ui.tabela_registros.setItem(
                linha,
                3,
                QTableWidgetItem(
                    registro.descricao
                )
            )

        # Ajusta as colunas ao conteúdo
        self.ui.tabela_registros.resizeColumnsToContents()

    def configurar_tabela(self):
        # Configura o tamanho das colunas da tabela

        self.ui.tabela_registros.setColumnWidth(
            0,
            150
        )

        self.ui.tabela_registros.setColumnWidth(
            1,
            100
        )

        self.ui.tabela_registros.setColumnWidth(
            2,
            180
        )

        self.ui.tabela_registros.setColumnWidth(
            3,
            500
        )

    def formatar_medicao(self):
        # Formata a medição para mostrar nos registros

        return (
            f"{self.medicao_atual.tensao:.1f} V / "
            f"{self.medicao_atual.corrente:.1f} A / "
            f"{self.medicao_atual.potencia:.1f} W"
        )