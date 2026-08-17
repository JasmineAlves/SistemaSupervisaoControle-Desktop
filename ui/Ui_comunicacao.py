# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'comunicacao.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(560, 460)
        Form.setMinimumSize(QSize(520, 440))
        Form.setStyleSheet(u"\n"
"/* ===== Base (mesmos tokens do dashboard) ===== */\n"
"QDialog {\n"
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
"    font-size: 20px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel#lbl_subtitulo {\n"
"    color: #B8A0D4;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"/* ===== Painel de status da conex\u00e3o ===== */\n"
"QFrame#statusCard {\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QFrame#statusCard[estado=\"conectado\"] {\n"
"    background: #F0ECF5;\n"
"    border: 1px solid #D4C8E0;\n"
"}\n"
"\n"
"QFrame#statusCard[estado=\"descon"
                        "ectado\"] {\n"
"    background: #FDECEC;\n"
"    border: 1px solid #F3C1BC;\n"
"}\n"
"\n"
"QLabel#lbl_status[estado=\"conectado\"] {\n"
"    color: #5B21B6;\n"
"    font-size: 15px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel#lbl_status[estado=\"desconectado\"] {\n"
"    color: #B42318;\n"
"    font-size: 15px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"/* ===== Painel de par\u00e2metros ===== */\n"
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
"QLabel.fieldLabel {\n"
"    color: #6B5B7A;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 1px;\n"
"}\n"
"\n"
"/* ===== Campos ===== */\n"
"QComboBox, QSpinBox, QDoubleSpinBox {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #D4C8E0;\n"
"    border-ra"
                        "dius: 7px;\n"
"    padding: 6px 10px;\n"
"    min-height: 30px;\n"
"}\n"
"\n"
"QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {\n"
"    border: 1px solid #6D28D9;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 22px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #DCD0E8;\n"
"    selection-background-color: #F0ECF5;\n"
"    selection-color: #1A1030;\n"
"    outline: none;\n"
"}\n"
"\n"
"QSpinBox::up-button, QSpinBox::down-button,\n"
"QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {\n"
"    width: 0px; height: 0px; border: none; background: transparent;\n"
"}\n"
"\n"
"/* ===== Bot\u00f5es ===== */\n"
"QPushButton {\n"
"    background-color: #FFFFFF;\n"
"    color: #1A1030;\n"
"    border: 1px solid #D4C8E0;\n"
"    border-radius: 7px;\n"
"    padding: 10px 16px;\n"
"    font-weight: 600;\n"
"    min-height: 18px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #F0ECF5;\n"
"    border-color: #8B5CF6;"
                        "\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: #B7ABC4;\n"
"    background-color: #F7F4FA;\n"
"    border-color: #E6DEEE;\n"
"}\n"
"\n"
"QPushButton#btn_conectar {\n"
"    background-color: #3D1A6B;\n"
"    color: #FFFFFF;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton#btn_conectar:hover {\n"
"    background-color: #4D2A7B;\n"
"}\n"
"\n"
"QPushButton#btn_conectar:disabled {\n"
"    background-color: #C9BEDC;\n"
"    color: #F4F0F8;\n"
"}\n"
"\n"
"QPushButton#btn_desconectar {\n"
"    color: #B42318;\n"
"    border: 1px solid #F3C1BC;\n"
"}\n"
"\n"
"QPushButton#btn_desconectar:hover {\n"
"    background-color: #FDECEC;\n"
"    border-color: #E23B32;\n"
"}\n"
"\n"
"QPushButton#btn_fechar {\n"
"    background: transparent;\n"
"    border: none;\n"
"    color: #6B5B7A;\n"
"}\n"
"\n"
"QPushButton#btn_fechar:hover {\n"
"    color: #3D1A6B;\n"
"    text-decoration: underline;\n"
"}\n"
"   ")
        self.layout_principal = QVBoxLayout(Form)
        self.layout_principal.setSpacing(14)
        self.layout_principal.setObjectName(u"layout_principal")
        self.layout_principal.setContentsMargins(22, 18, 22, 18)
        self.header = QFrame(Form)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 72))
        self.header.setMaximumSize(QSize(16777215, 72))
        self.layout_header = QVBoxLayout(self.header)
        self.layout_header.setSpacing(2)
        self.layout_header.setObjectName(u"layout_header")
        self.layout_header.setContentsMargins(20, 0, 20, 0)
        self.spacer_header_top = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout_header.addItem(self.spacer_header_top)

        self.lbl_titulo = QLabel(self.header)
        self.lbl_titulo.setObjectName(u"lbl_titulo")

        self.layout_header.addWidget(self.lbl_titulo)

        self.lbl_subtitulo = QLabel(self.header)
        self.lbl_subtitulo.setObjectName(u"lbl_subtitulo")

        self.layout_header.addWidget(self.lbl_subtitulo)

        self.spacer_header_bottom = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout_header.addItem(self.spacer_header_bottom)


        self.layout_principal.addWidget(self.header)

        self.statusCard = QFrame(Form)
        self.statusCard.setObjectName(u"statusCard")
        self.statusCard.setMinimumSize(QSize(0, 56))
        self.layout_status = QHBoxLayout(self.statusCard)
        self.layout_status.setObjectName(u"layout_status")
        self.layout_status.setContentsMargins(18, 8, 18, 8)
        self.lbl_status = QLabel(self.statusCard)
        self.lbl_status.setObjectName(u"lbl_status")

        self.layout_status.addWidget(self.lbl_status)


        self.layout_principal.addWidget(self.statusCard)

        self.grupo_parametros = QFrame(Form)
        self.grupo_parametros.setObjectName(u"grupo_parametros")
        self.layout_parametros = QVBoxLayout(self.grupo_parametros)
        self.layout_parametros.setSpacing(12)
        self.layout_parametros.setObjectName(u"layout_parametros")
        self.layout_parametros.setContentsMargins(20, 16, 20, 18)
        self.lbl_parametros_titulo = QLabel(self.grupo_parametros)
        self.lbl_parametros_titulo.setObjectName(u"lbl_parametros_titulo")

        self.layout_parametros.addWidget(self.lbl_parametros_titulo)

        self.layout_porta = QVBoxLayout()
        self.layout_porta.setSpacing(4)
        self.layout_porta.setObjectName(u"layout_porta")
        self.lbl_porta_titulo = QLabel(self.grupo_parametros)
        self.lbl_porta_titulo.setObjectName(u"lbl_porta_titulo")

        self.layout_porta.addWidget(self.lbl_porta_titulo)

        self.combo_porta = QComboBox(self.grupo_parametros)
        self.combo_porta.setObjectName(u"combo_porta")

        self.layout_porta.addWidget(self.combo_porta)


        self.layout_parametros.addLayout(self.layout_porta)

        self.layout_baud_timeout = QHBoxLayout()
        self.layout_baud_timeout.setSpacing(12)
        self.layout_baud_timeout.setObjectName(u"layout_baud_timeout")
        self.layout_baud = QVBoxLayout()
        self.layout_baud.setSpacing(4)
        self.layout_baud.setObjectName(u"layout_baud")
        self.lbl_baud_titulo = QLabel(self.grupo_parametros)
        self.lbl_baud_titulo.setObjectName(u"lbl_baud_titulo")

        self.layout_baud.addWidget(self.lbl_baud_titulo)

        self.combo_baud = QComboBox(self.grupo_parametros)
        self.combo_baud.addItem("")
        self.combo_baud.addItem("")
        self.combo_baud.setObjectName(u"combo_baud")

        self.layout_baud.addWidget(self.combo_baud)


        self.layout_baud_timeout.addLayout(self.layout_baud)

        self.layout_timeout = QVBoxLayout()
        self.layout_timeout.setSpacing(4)
        self.layout_timeout.setObjectName(u"layout_timeout")
        self.lbl_timeout_titulo = QLabel(self.grupo_parametros)
        self.lbl_timeout_titulo.setObjectName(u"lbl_timeout_titulo")

        self.layout_timeout.addWidget(self.lbl_timeout_titulo)

        self.spin_timeout = QSpinBox(self.grupo_parametros)
        self.spin_timeout.setObjectName(u"spin_timeout")
        self.spin_timeout.setMinimum(1)
        self.spin_timeout.setMaximum(60)
        self.spin_timeout.setValue(1)

        self.layout_timeout.addWidget(self.spin_timeout)


        self.layout_baud_timeout.addLayout(self.layout_timeout)


        self.layout_parametros.addLayout(self.layout_baud_timeout)


        self.layout_principal.addWidget(self.grupo_parametros)

        self.spacer_meio = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout_principal.addItem(self.spacer_meio)

        self.layout_acoes = QHBoxLayout()
        self.layout_acoes.setSpacing(10)
        self.layout_acoes.setObjectName(u"layout_acoes")
        self.btn_fechar = QPushButton(Form)
        self.btn_fechar.setObjectName(u"btn_fechar")

        self.layout_acoes.addWidget(self.btn_fechar)

        self.spacer_acoes = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_acoes.addItem(self.spacer_acoes)

        self.btn_desconectar = QPushButton(Form)
        self.btn_desconectar.setObjectName(u"btn_desconectar")
        self.btn_desconectar.setMinimumSize(QSize(130, 40))

        self.layout_acoes.addWidget(self.btn_desconectar)

        self.btn_conectar = QPushButton(Form)
        self.btn_conectar.setObjectName(u"btn_conectar")
        self.btn_conectar.setMinimumSize(QSize(130, 40))

        self.layout_acoes.addWidget(self.btn_conectar)


        self.layout_principal.addLayout(self.layout_acoes)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Comunica\u00e7\u00e3o Serial", None))
        self.lbl_titulo.setText(QCoreApplication.translate("Form", u"Comunica\u00e7\u00e3o Serial", None))
        self.lbl_subtitulo.setText(QCoreApplication.translate("Form", u"Configura\u00e7\u00e3o da conex\u00e3o com o microcontrolador", None))
        self.statusCard.setProperty(u"estado", QCoreApplication.translate("Form", u"desconectado", None))
        self.lbl_status.setText(QCoreApplication.translate("Form", u"\u25cf  Status : Desconectado", None))
        self.lbl_status.setProperty(u"estado", QCoreApplication.translate("Form", u"desconectado", None))
        self.grupo_parametros.setProperty(u"class", QCoreApplication.translate("Form", u"panel", None))
        self.lbl_parametros_titulo.setText(QCoreApplication.translate("Form", u"Par\u00e2metros de conex\u00e3o", None))
        self.lbl_parametros_titulo.setProperty(u"class", QCoreApplication.translate("Form", u"panelTitle", None))
        self.lbl_porta_titulo.setText(QCoreApplication.translate("Form", u"PORTA COM", None))
        self.lbl_porta_titulo.setProperty(u"class", QCoreApplication.translate("Form", u"fieldLabel", None))
        self.lbl_baud_titulo.setText(QCoreApplication.translate("Form", u"BAUD RATE", None))
        self.lbl_baud_titulo.setProperty(u"class", QCoreApplication.translate("Form", u"fieldLabel", None))
        self.combo_baud.setItemText(0, QCoreApplication.translate("Form", u"9600", None))
        self.combo_baud.setItemText(1, QCoreApplication.translate("Form", u"115200", None))

        self.lbl_timeout_titulo.setText(QCoreApplication.translate("Form", u"TIMEOUT (s)", None))
        self.lbl_timeout_titulo.setProperty(u"class", QCoreApplication.translate("Form", u"fieldLabel", None))
        self.btn_fechar.setText(QCoreApplication.translate("Form", u"Fechar", None))
        self.btn_desconectar.setText(QCoreApplication.translate("Form", u"Desconectar", None))
        self.btn_conectar.setText(QCoreApplication.translate("Form", u"Conectar", None))
    # retranslateUi

