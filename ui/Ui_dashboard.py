# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDoubleSpinBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 894)
        MainWindow.setMinimumSize(QSize(980, 680))
        MainWindow.setStyleSheet(u"\n"
"/* ===== Base ===== */\n"
"QMainWindow {\n"
"    background-color: #F4F0F8;\n"
"}\n"
"\n"
"QWidget {\n"
"    font-family: \"Segoe UI\";\n"
"    color: #1A1030;\n"
"}\n"
"\n"
"QMessageBox {\n"
"    background-color: #3D1A6B;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QMessageBox QLabel {\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* ===== Cabe\u00e7alho ===== */\n"
"QFrame#header {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #1A0A30, stop:1 #3D1A6B);\n"
"    border-radius: 14px;\n"
"}\n"
"\n"
"QLabel#lbl_titulo {\n"
"    color: #FFFFFF;\n"
"    font-size: 25px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel#lbl_subtitulo {\n"
"    color: #B8A0D4;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QLabel#lbl_status_comunicacao {\n"
"    color: #B8A0D4;\n"
"    font-size: 12px;\n"
"    font-weight: 600;\n"
"    background: rgba(255,255,255,0.08);\n"
"    border: 1px solid rgba(184, 160, 212, 0.35);\n"
"    border-radius: 12px;\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QLabel#lbl_status_comun"
                        "icacao[state=\"on\"] {\n"
"    color: #A78BFA;\n"
"    border-color: rgba(167, 139, 250, 0.5);\n"
"}\n"
"\n"
"QLabel#lbl_status_comunicacao[state=\"off\"] {\n"
"    color: #E1B8B4;\n"
"    border-color: rgba(225, 184, 180, 0.4);\n"
"}\n"
"\n"
"/* ===== Cards de m\u00e9trica ===== */\n"
"QFrame.metricCard {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #DCD0E8;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QFrame#grupo_tensao { border-left: 4px solid #6D28D9; }\n"
"QFrame#grupo_corrente { border-left: 4px solid #7C3AED; }\n"
"QFrame#grupo_potencia { border-left: 4px solid #8B5CF6; }\n"
"QFrame#grupo_potencia[alerta=\"true\"] { border-left: 4px solid #EA580C; background: #FFF7ED; }\n"
"\n"
"QLabel.metricTitle {\n"
"    color: #6B5B7A;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 1px;\n"
"}\n"
"\n"
"QLabel.metricValue {\n"
"    color: #1A1030;\n"
"    font-size: 29px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel.metricUnit {\n"
"    color: #6B5B7A;\n"
"    font-size: "
                        "13px;\n"
"    font-weight: 600;\n"
"}\n"
"\n"
"QLabel.metricFooter {\n"
"    color: #8B7A9A;\n"
"    font-size: 11px;\n"
"}\n"
"\n"
"/* ===== Pain\u00e9is gen\u00e9ricos ===== */\n"
"QFrame.panel {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #DCD0E8;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QLabel.panelTitle {\n"
"    color: #1A1030;\n"
"    font-size: 15px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel.panelSubtitle {\n"
"    color: #8B7A9A;\n"
"    font-size: 11px;\n"
"}\n"
"\n"
"/* ===== Card de status do disjuntor ===== */\n"
"QFrame#statusCard {\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QFrame#statusCard[estado=\"fechado\"] {\n"
"    background: #F0ECF5;\n"
"    border: 1px solid #D4C8E0;\n"
"}\n"
"\n"
"QFrame#statusCard[estado=\"aberto\"] {\n"
"    background: #FDECEC;\n"
"    border: 1px solid #F3C1BC;\n"
"}\n"
"\n"
"QLabel#lbl_status_disjuntor[estado=\"fechado\"] {\n"
"    color: #5B21B6;\n"
"    font-size: 18px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel#lbl_status_disjunt"
                        "or[estado=\"aberto\"] {\n"
"    color: #B42318;\n"
"    font-size: 18px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel#lbl_status_detalhe {\n"
"    color: #6B5B7A;\n"
"    font-size: 11px;\n"
"}\n"
"\n"
"QLabel#lbl_status_atualizacao {\n"
"    color: #8B7A9A;\n"
"    font-size: 10px;\n"
"}\n"
"\n"
"/* ===== Controles ===== */\n"
"QFrame#controlePanel {\n"
"    background-color: #F0ECF5;\n"
"    border: 1px solid #DCD0E8;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QLabel.controlTitle {\n"
"    color: #6B5B7A;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QDoubleSpinBox {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #D4C8E0;\n"
"    border-radius: 7px;\n"
"    padding: 6px 8px;\n"
"    min-height: 28px;\n"
"}\n"
"\n"
"QDoubleSpinBox:focus {\n"
"    border: 1px solid #6D28D9;\n"
"}\n"
"\n"
"QDoubleSpinBox::up-button,\n"
"QDoubleSpinBox::down-button {\n"
"    width: 0px;\n"
"    height: 0px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QPushButton {\n"
""
                        "    background-color: #FFFFFF;\n"
"    color: #1A1030;\n"
"    border: 1px solid #D4C8E0;\n"
"    border-radius: 7px;\n"
"    padding: 9px 14px;\n"
"    font-weight: 600;\n"
"    min-height: 18px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #F0ECF5;\n"
"    border-color: #8B5CF6;\n"
"}\n"
"\n"
"QPushButton#btn_configuracao,\n"
"QPushButton#btn_comunicacao {\n"
"    background-color: #3D1A6B;\n"
"    color: #FFFFFF;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton#btn_configuracao:hover,\n"
"QPushButton#btn_comunicacao:hover {\n"
"    background-color: #4D2A7B;\n"
"}\n"
"\n"
"QPushButton#btn_corte_emergencia {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"        stop:0 #E23B32, stop:1 #B91C1C);\n"
"    color: #FFFFFF;\n"
"    border: none;\n"
"    font-size: 14px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QPushButton#btn_corte_emergencia:hover {\n"
"    background: #C0271F;\n"
"}\n"
"\n"
"QPushButton#btn_corte_emergencia:pressed {\n"
"    background: #9E1B15;\n"
"}\n"
"\n"
"/*"
                        " ===== Hist\u00f3rico ===== */\n"
"QFrame#historicoPanel {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #DCD0E8;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QTableWidget {\n"
"    background-color: #FFFFFF;\n"
"    border: none;\n"
"    gridline-color: #EDE8F0;\n"
"    selection-background-color: #DDD0E8;\n"
"    selection-color: #1A1030;\n"
"    alternate-background-color: #F8F4FA;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #F0ECF5;\n"
"    color: #6B5B7A;\n"
"    border: none;\n"
"    border-bottom: 1px solid #DCD0E8;\n"
"    padding: 8px;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QStatusBar {\n"
"    background-color: #EDE8F0;\n"
"    color: #6B5B7A;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    width: 7px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #D4C8E0;\n"
"    border-radius: 3px;\n"
"    min-height: 25px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #8B5CF6;\n"
""
                        "}\n"
"   ")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layout_principal = QVBoxLayout(self.centralwidget)
        self.layout_principal.setSpacing(12)
        self.layout_principal.setObjectName(u"layout_principal")
        self.layout_principal.setContentsMargins(20, 16, 20, 12)
        self.header = QFrame(self.centralwidget)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 78))
        self.layout_header = QHBoxLayout(self.header)
        self.layout_header.setObjectName(u"layout_header")
        self.layout_header.setContentsMargins(20, -1, 20, -1)
        self.layout_header_text = QVBoxLayout()
        self.layout_header_text.setSpacing(2)
        self.layout_header_text.setObjectName(u"layout_header_text")
        self.lbl_titulo = QLabel(self.header)
        self.lbl_titulo.setObjectName(u"lbl_titulo")

        self.layout_header_text.addWidget(self.lbl_titulo)

        self.lbl_subtitulo = QLabel(self.header)
        self.lbl_subtitulo.setObjectName(u"lbl_subtitulo")

        self.layout_header_text.addWidget(self.lbl_subtitulo)


        self.layout_header.addLayout(self.layout_header_text)

        self.spacer_header = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_header.addItem(self.spacer_header)

        self.lbl_status_comunicacao = QLabel(self.header)
        self.lbl_status_comunicacao.setObjectName(u"lbl_status_comunicacao")
        self.lbl_status_comunicacao.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.layout_header.addWidget(self.lbl_status_comunicacao)


        self.layout_principal.addWidget(self.header)

        self.layout_metricas = QHBoxLayout()
        self.layout_metricas.setSpacing(10)
        self.layout_metricas.setObjectName(u"layout_metricas")
        self.grupo_tensao = QFrame(self.centralwidget)
        self.grupo_tensao.setObjectName(u"grupo_tensao")
        self.grupo_tensao.setMinimumSize(QSize(0, 105))
        self.layout_tensao = QVBoxLayout(self.grupo_tensao)
        self.layout_tensao.setObjectName(u"layout_tensao")
        self.layout_tensao.setContentsMargins(16, 14, 16, 12)
        self.lbl_tensao_titulo = QLabel(self.grupo_tensao)
        self.lbl_tensao_titulo.setObjectName(u"lbl_tensao_titulo")

        self.layout_tensao.addWidget(self.lbl_tensao_titulo)

        self.layout_tensao_valor = QHBoxLayout()
        self.layout_tensao_valor.setSpacing(0)
        self.layout_tensao_valor.setObjectName(u"layout_tensao_valor")
        self.lbl_valor_tensao = QLabel(self.grupo_tensao)
        self.lbl_valor_tensao.setObjectName(u"lbl_valor_tensao")

        self.layout_tensao_valor.addWidget(self.lbl_valor_tensao)

        self.lbl_tensao_unidade = QLabel(self.grupo_tensao)
        self.lbl_tensao_unidade.setObjectName(u"lbl_tensao_unidade")
        self.lbl_tensao_unidade.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.layout_tensao_valor.addWidget(self.lbl_tensao_unidade)

        self.spacer_tensao = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_tensao_valor.addItem(self.spacer_tensao)


        self.layout_tensao.addLayout(self.layout_tensao_valor)


        self.layout_metricas.addWidget(self.grupo_tensao)

        self.grupo_corrente = QFrame(self.centralwidget)
        self.grupo_corrente.setObjectName(u"grupo_corrente")
        self.grupo_corrente.setMinimumSize(QSize(0, 105))
        self.layout_corrente = QVBoxLayout(self.grupo_corrente)
        self.layout_corrente.setObjectName(u"layout_corrente")
        self.layout_corrente.setContentsMargins(16, 14, 16, 12)
        self.lbl_corrente_titulo = QLabel(self.grupo_corrente)
        self.lbl_corrente_titulo.setObjectName(u"lbl_corrente_titulo")

        self.layout_corrente.addWidget(self.lbl_corrente_titulo)

        self.layout_corrente_valor = QHBoxLayout()
        self.layout_corrente_valor.setSpacing(0)
        self.layout_corrente_valor.setObjectName(u"layout_corrente_valor")
        self.lbl_valor_corrente = QLabel(self.grupo_corrente)
        self.lbl_valor_corrente.setObjectName(u"lbl_valor_corrente")

        self.layout_corrente_valor.addWidget(self.lbl_valor_corrente)

        self.lbl_corrente_unidade = QLabel(self.grupo_corrente)
        self.lbl_corrente_unidade.setObjectName(u"lbl_corrente_unidade")
        self.lbl_corrente_unidade.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.layout_corrente_valor.addWidget(self.lbl_corrente_unidade)

        self.spacer_corrente = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_corrente_valor.addItem(self.spacer_corrente)


        self.layout_corrente.addLayout(self.layout_corrente_valor)


        self.layout_metricas.addWidget(self.grupo_corrente)

        self.grupo_potencia = QFrame(self.centralwidget)
        self.grupo_potencia.setObjectName(u"grupo_potencia")
        self.grupo_potencia.setMinimumSize(QSize(0, 105))
        self.layout_potencia = QVBoxLayout(self.grupo_potencia)
        self.layout_potencia.setObjectName(u"layout_potencia")
        self.layout_potencia.setContentsMargins(16, 14, 16, 12)
        self.lbl_potencia_titulo = QLabel(self.grupo_potencia)
        self.lbl_potencia_titulo.setObjectName(u"lbl_potencia_titulo")

        self.layout_potencia.addWidget(self.lbl_potencia_titulo)

        self.layout_potencia_valor = QHBoxLayout()
        self.layout_potencia_valor.setSpacing(0)
        self.layout_potencia_valor.setObjectName(u"layout_potencia_valor")
        self.lbl_valor_potencia = QLabel(self.grupo_potencia)
        self.lbl_valor_potencia.setObjectName(u"lbl_valor_potencia")

        self.layout_potencia_valor.addWidget(self.lbl_valor_potencia)

        self.lbl_potencia_unidade = QLabel(self.grupo_potencia)
        self.lbl_potencia_unidade.setObjectName(u"lbl_potencia_unidade")
        self.lbl_potencia_unidade.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.layout_potencia_valor.addWidget(self.lbl_potencia_unidade)

        self.spacer_potencia = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_potencia_valor.addItem(self.spacer_potencia)


        self.layout_potencia.addLayout(self.layout_potencia_valor)


        self.layout_metricas.addWidget(self.grupo_potencia)


        self.layout_principal.addLayout(self.layout_metricas)

        self.layout_monitoramento = QHBoxLayout()
        self.layout_monitoramento.setSpacing(10)
        self.layout_monitoramento.setObjectName(u"layout_monitoramento")
        self.grupo_grafico = QFrame(self.centralwidget)
        self.grupo_grafico.setObjectName(u"grupo_grafico")
        self.grupo_grafico.setMinimumSize(QSize(560, 280))
        self.layout_grafico = QVBoxLayout(self.grupo_grafico)
        self.layout_grafico.setObjectName(u"layout_grafico")
        self.layout_grafico.setContentsMargins(16, 14, 16, 12)
        self.lbl_grafico_titulo = QLabel(self.grupo_grafico)
        self.lbl_grafico_titulo.setObjectName(u"lbl_grafico_titulo")

        self.layout_grafico.addWidget(self.lbl_grafico_titulo)

        self.lbl_grafico_subtitulo = QLabel(self.grupo_grafico)
        self.lbl_grafico_subtitulo.setObjectName(u"lbl_grafico_subtitulo")

        self.layout_grafico.addWidget(self.lbl_grafico_subtitulo)

        self.widget_grafico = QWidget(self.grupo_grafico)
        self.widget_grafico.setObjectName(u"widget_grafico")
        self.widget_grafico.setMinimumSize(QSize(0, 190))

        self.layout_grafico.addWidget(self.widget_grafico)


        self.layout_monitoramento.addWidget(self.grupo_grafico)

        self.statusCard = QFrame(self.centralwidget)
        self.statusCard.setObjectName(u"statusCard")
        self.statusCard.setMinimumSize(QSize(280, 280))
        self.layout_status = QVBoxLayout(self.statusCard)
        self.layout_status.setObjectName(u"layout_status")
        self.layout_status.setContentsMargins(18, 14, 18, 14)
        self.lbl_disjuntor_titulo = QLabel(self.statusCard)
        self.lbl_disjuntor_titulo.setObjectName(u"lbl_disjuntor_titulo")

        self.layout_status.addWidget(self.lbl_disjuntor_titulo)

        self.spacer_status_1 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout_status.addItem(self.spacer_status_1)

        self.lbl_status_disjuntor = QLabel(self.statusCard)
        self.lbl_status_disjuntor.setObjectName(u"lbl_status_disjuntor")
        self.lbl_status_disjuntor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_status.addWidget(self.lbl_status_disjuntor)

        self.lbl_status_detalhe = QLabel(self.statusCard)
        self.lbl_status_detalhe.setObjectName(u"lbl_status_detalhe")
        self.lbl_status_detalhe.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status_detalhe.setWordWrap(True)

        self.layout_status.addWidget(self.lbl_status_detalhe)

        self.spacer_status_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout_status.addItem(self.spacer_status_2)

        self.lbl_status_atualizacao = QLabel(self.statusCard)
        self.lbl_status_atualizacao.setObjectName(u"lbl_status_atualizacao")
        self.lbl_status_atualizacao.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_status.addWidget(self.lbl_status_atualizacao)


        self.layout_monitoramento.addWidget(self.statusCard)


        self.layout_principal.addLayout(self.layout_monitoramento)

        self.controlePanel = QFrame(self.centralwidget)
        self.controlePanel.setObjectName(u"controlePanel")
        self.layout_controles = QHBoxLayout(self.controlePanel)
        self.layout_controles.setObjectName(u"layout_controles")
        self.layout_controles.setContentsMargins(14, 10, 14, 10)
        self.layout_limite = QVBoxLayout()
        self.layout_limite.setSpacing(2)
        self.layout_limite.setObjectName(u"layout_limite")
        self.lbl_limite_titulo = QLabel(self.controlePanel)
        self.lbl_limite_titulo.setObjectName(u"lbl_limite_titulo")

        self.layout_limite.addWidget(self.lbl_limite_titulo)

        self.spin_limite_potencia = QDoubleSpinBox(self.controlePanel)
        self.spin_limite_potencia.setObjectName(u"spin_limite_potencia")
        self.spin_limite_potencia.setMinimum(0.000000000000000)
        self.spin_limite_potencia.setMaximum(999999.000000000000000)
        self.spin_limite_potencia.setValue(2000.000000000000000)

        self.layout_limite.addWidget(self.spin_limite_potencia)


        self.layout_controles.addLayout(self.layout_limite)

        self.spacer_controles = QSpacerItem(30, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_controles.addItem(self.spacer_controles)

        self.btn_configuracao = QPushButton(self.controlePanel)
        self.btn_configuracao.setObjectName(u"btn_configuracao")
        self.btn_configuracao.setMinimumSize(QSize(145, 36))

        self.layout_controles.addWidget(self.btn_configuracao)

        self.btn_comunicacao = QPushButton(self.controlePanel)
        self.btn_comunicacao.setObjectName(u"btn_comunicacao")
        self.btn_comunicacao.setMinimumSize(QSize(145, 36))

        self.layout_controles.addWidget(self.btn_comunicacao)

        self.btn_corte_emergencia = QPushButton(self.controlePanel)
        self.btn_corte_emergencia.setObjectName(u"btn_corte_emergencia")
        self.btn_corte_emergencia.setMinimumSize(QSize(200, 36))

        self.layout_controles.addWidget(self.btn_corte_emergencia)


        self.layout_principal.addWidget(self.controlePanel)

        self.historicoPanel = QFrame(self.centralwidget)
        self.historicoPanel.setObjectName(u"historicoPanel")
        self.historicoPanel.setMinimumSize(QSize(0, 170))
        self.layout_historico = QVBoxLayout(self.historicoPanel)
        self.layout_historico.setObjectName(u"layout_historico")
        self.layout_historico.setContentsMargins(14, 10, 14, 10)
        self.lbl_historico_titulo = QLabel(self.historicoPanel)
        self.lbl_historico_titulo.setObjectName(u"lbl_historico_titulo")

        self.layout_historico.addWidget(self.lbl_historico_titulo)

        self.tabela_registros = QTableWidget(self.historicoPanel)
        if (self.tabela_registros.columnCount() < 4):
            self.tabela_registros.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tabela_registros.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tabela_registros.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tabela_registros.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tabela_registros.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tabela_registros.setObjectName(u"tabela_registros")
        self.tabela_registros.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabela_registros.setAlternatingRowColors(True)
        self.tabela_registros.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela_registros.setSortingEnabled(True)
        self.tabela_registros.setRowCount(0)
        self.tabela_registros.setColumnCount(4)
        self.tabela_registros.horizontalHeader().setDefaultSectionSize(150)
        self.tabela_registros.horizontalHeader().setStretchLastSection(True)
        self.tabela_registros.verticalHeader().setVisible(False)

        self.layout_historico.addWidget(self.tabela_registros)


        self.layout_principal.addWidget(self.historicoPanel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Supervis\u00e3o de Energia", None))
        self.lbl_titulo.setText(QCoreApplication.translate("MainWindow", u"Supervis\u00e3o de Energia", None))
        self.lbl_subtitulo.setText(QCoreApplication.translate("MainWindow", u"Monitor de Consumo e Qualidade de Energia - Smart Grid", None))
        self.lbl_status_comunicacao.setText(QCoreApplication.translate("MainWindow", u"Comunica\u00e7\u00e3o: DESCONECTADO", None))
        self.grupo_tensao.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricCard", None))
        self.lbl_tensao_titulo.setText(QCoreApplication.translate("MainWindow", u"TENS\u00c3O RMS", None))
        self.lbl_tensao_titulo.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricTitle", None))
        self.lbl_valor_tensao.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.lbl_valor_tensao.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricValue", None))
        self.lbl_tensao_unidade.setText(QCoreApplication.translate("MainWindow", u"V", None))
        self.lbl_tensao_unidade.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricUnit", None))
        self.grupo_corrente.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricCard", None))
        self.lbl_corrente_titulo.setText(QCoreApplication.translate("MainWindow", u"CORRENTE RMS", None))
        self.lbl_corrente_titulo.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricTitle", None))
        self.lbl_valor_corrente.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.lbl_valor_corrente.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricValue", None))
        self.lbl_corrente_unidade.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.lbl_corrente_unidade.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricUnit", None))
        self.grupo_potencia.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricCard", None))
        self.grupo_potencia.setProperty(u"alerta", QCoreApplication.translate("MainWindow", u"false", None))
        self.lbl_potencia_titulo.setText(QCoreApplication.translate("MainWindow", u"POT\u00caNCIA ATIVA ", None))
        self.lbl_potencia_titulo.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricTitle", None))
        self.lbl_valor_potencia.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.lbl_valor_potencia.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricValue", None))
        self.lbl_potencia_unidade.setText(QCoreApplication.translate("MainWindow", u"W", None))
        self.lbl_potencia_unidade.setProperty(u"class", QCoreApplication.translate("MainWindow", u"metricUnit", None))
        self.grupo_grafico.setProperty(u"class", QCoreApplication.translate("MainWindow", u"panel", None))
        self.lbl_grafico_titulo.setText(QCoreApplication.translate("MainWindow", u"Curva de demanda de pot\u00eancia", None))
        self.lbl_grafico_titulo.setProperty(u"class", QCoreApplication.translate("MainWindow", u"panelTitle", None))
        self.lbl_grafico_subtitulo.setText(QCoreApplication.translate("MainWindow", u"\u00daltimas 24 horas \u00b7 hist\u00f3rico pr\u00e9-carregado", None))
        self.lbl_grafico_subtitulo.setProperty(u"class", QCoreApplication.translate("MainWindow", u"panelSubtitle", None))
        self.statusCard.setProperty(u"estado", QCoreApplication.translate("MainWindow", u"fechado", None))
        self.lbl_disjuntor_titulo.setText(QCoreApplication.translate("MainWindow", u"Prote\u00e7\u00e3o geral", None))
        self.lbl_disjuntor_titulo.setProperty(u"class", QCoreApplication.translate("MainWindow", u"panelTitle", None))
        self.lbl_status_disjuntor.setText(QCoreApplication.translate("MainWindow", u"DISJUNTOR: FECHADO", None))
        self.lbl_status_disjuntor.setProperty(u"estado", QCoreApplication.translate("MainWindow", u"fechado", None))
        self.lbl_status_detalhe.setText(QCoreApplication.translate("MainWindow", u"Instala\u00e7\u00e3o energizada. Prote\u00e7\u00e3o monitorada em tempo real.", None))
        self.lbl_status_atualizacao.setText(QCoreApplication.translate("MainWindow", u"\u00daltima atualiza\u00e7\u00e3o: --:--:--", None))
        self.lbl_limite_titulo.setText(QCoreApplication.translate("MainWindow", u"LIMITE DE ALERTA DE POT\u00caNCIA", None))
        self.lbl_limite_titulo.setProperty(u"class", QCoreApplication.translate("MainWindow", u"controlTitle", None))
        self.spin_limite_potencia.setSuffix(QCoreApplication.translate("MainWindow", u" W", None))
        self.btn_configuracao.setText(QCoreApplication.translate("MainWindow", u"CONFIGURA\u00c7\u00d5ES", None))
        self.btn_comunicacao.setText(QCoreApplication.translate("MainWindow", u"COMUNICA\u00c7\u00c3O", None))
        self.btn_corte_emergencia.setText(QCoreApplication.translate("MainWindow", u"\u26a0  CORTE DE EMERG\u00caNCIA", None))
        self.lbl_historico_titulo.setText(QCoreApplication.translate("MainWindow", u"Hist\u00f3rico de eventos e auditoria", None))
        self.lbl_historico_titulo.setProperty(u"class", QCoreApplication.translate("MainWindow", u"panelTitle", None))
        ___qtablewidgetitem = self.tabela_registros.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Data / Hora", None))
        ___qtablewidgetitem1 = self.tabela_registros.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Tipo de Evento", None))
        ___qtablewidgetitem2 = self.tabela_registros.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Valor Medido", None))
        ___qtablewidgetitem3 = self.tabela_registros.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Descri\u00e7\u00e3o", None))
    # retranslateUi

