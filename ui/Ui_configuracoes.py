# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuracoes.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(560, 440)
        Dialog.setMinimumSize(QSize(520, 420))
        Dialog.setStyleSheet(u"\n"
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
"/* ===== Painel de regras ===== */\n"
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
""
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
"/* ===== Painel de previs\u00e3o calculada ===== */\n"
"QFrame#previsaoCard {\n"
"    background-color: #F0ECF5;\n"
"    border: 1px solid #D4C8E0;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QLabel#lbl_previsao_titulo {\n"
"    color: #6B5B7A;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 1px;\n"
"}\n"
"\n"
"QLabel#lbl_potencia_calculada {\n"
"    color: #5B21B6;\n"
"    font-size: 22px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"/* ===== Campos ===== */\n"
"QDoubleSpinBox {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #D4C8E0;\n"
"    border-radius: 7px;\n"
"    padding: 6px 10px;\n"
"    min-height: 30px;\n"
"}\n"
"\n"
"QDoubleSpinBox:focus {\n"
"    border: 1px solid #6D28D9;\n"
"}\n"
"\n"
"QDoubleSpinBox::up-button, QDoubleSpinBox::down"
                        "-button {\n"
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
"    border-color: #8B5CF6;\n"
"}\n"
"\n"
"QPushButton#btn_salvar {\n"
"    background-color: #3D1A6B;\n"
"    color: #FFFFFF;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton#btn_salvar:hover {\n"
"    background-color: #4D2A7B;\n"
"}\n"
"\n"
"QPushButton#btn_cancelar {\n"
"    color: #6B5B7A;\n"
"}\n"
"   ")
        self.layout_principal = QVBoxLayout(Dialog)
        self.layout_principal.setSpacing(14)
        self.layout_principal.setObjectName(u"layout_principal")
        self.layout_principal.setContentsMargins(22, 18, 22, 18)
        self.header = QFrame(Dialog)
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

        self.grupo_regras = QFrame(Dialog)
        self.grupo_regras.setObjectName(u"grupo_regras")
        self.layout_regras = QVBoxLayout(self.grupo_regras)
        self.layout_regras.setSpacing(14)
        self.layout_regras.setObjectName(u"layout_regras")
        self.layout_regras.setContentsMargins(20, 16, 20, 18)
        self.lbl_regras_titulo = QLabel(self.grupo_regras)
        self.lbl_regras_titulo.setObjectName(u"lbl_regras_titulo")

        self.layout_regras.addWidget(self.lbl_regras_titulo)

        self.layout_campos = QHBoxLayout()
        self.layout_campos.setSpacing(14)
        self.layout_campos.setObjectName(u"layout_campos")
        self.layout_tensao = QVBoxLayout()
        self.layout_tensao.setSpacing(4)
        self.layout_tensao.setObjectName(u"layout_tensao")
        self.lbl_tensao_titulo = QLabel(self.grupo_regras)
        self.lbl_tensao_titulo.setObjectName(u"lbl_tensao_titulo")

        self.layout_tensao.addWidget(self.lbl_tensao_titulo)

        self.spin_tensao_max = QDoubleSpinBox(self.grupo_regras)
        self.spin_tensao_max.setObjectName(u"spin_tensao_max")
        self.spin_tensao_max.setMaximum(9999.000000000000000)
        self.spin_tensao_max.setValue(240.000000000000000)

        self.layout_tensao.addWidget(self.spin_tensao_max)


        self.layout_campos.addLayout(self.layout_tensao)

        self.layout_corrente = QVBoxLayout()
        self.layout_corrente.setSpacing(4)
        self.layout_corrente.setObjectName(u"layout_corrente")
        self.lbl_corrente_titulo = QLabel(self.grupo_regras)
        self.lbl_corrente_titulo.setObjectName(u"lbl_corrente_titulo")

        self.layout_corrente.addWidget(self.lbl_corrente_titulo)

        self.spin_corrente_max = QDoubleSpinBox(self.grupo_regras)
        self.spin_corrente_max.setObjectName(u"spin_corrente_max")
        self.spin_corrente_max.setMaximum(9999.000000000000000)
        self.spin_corrente_max.setValue(10.000000000000000)

        self.layout_corrente.addWidget(self.spin_corrente_max)


        self.layout_campos.addLayout(self.layout_corrente)


        self.layout_regras.addLayout(self.layout_campos)


        self.layout_principal.addWidget(self.grupo_regras)

        self.previsaoCard = QFrame(Dialog)
        self.previsaoCard.setObjectName(u"previsaoCard")
        self.previsaoCard.setMinimumSize(QSize(0, 62))
        self.layout_previsao = QHBoxLayout(self.previsaoCard)
        self.layout_previsao.setObjectName(u"layout_previsao")
        self.layout_previsao.setContentsMargins(18, 10, 18, 10)
        self.layout_previsao_texto = QVBoxLayout()
        self.layout_previsao_texto.setSpacing(2)
        self.layout_previsao_texto.setObjectName(u"layout_previsao_texto")
        self.lbl_previsao_titulo = QLabel(self.previsaoCard)
        self.lbl_previsao_titulo.setObjectName(u"lbl_previsao_titulo")

        self.layout_previsao_texto.addWidget(self.lbl_previsao_titulo)

        self.lbl_potencia_calculada = QLabel(self.previsaoCard)
        self.lbl_potencia_calculada.setObjectName(u"lbl_potencia_calculada")

        self.layout_previsao_texto.addWidget(self.lbl_potencia_calculada)

        self.lbl_aviso_manual = QLabel(self.previsaoCard)
        self.lbl_aviso_manual.setObjectName(u"lbl_aviso_manual")
        self.lbl_aviso_manual.setWordWrap(True)

        self.layout_previsao_texto.addWidget(self.lbl_aviso_manual)


        self.layout_previsao.addLayout(self.layout_previsao_texto)

        self.spacer_previsao = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_previsao.addItem(self.spacer_previsao)


        self.layout_principal.addWidget(self.previsaoCard)

        self.spacer_meio = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout_principal.addItem(self.spacer_meio)

        self.layout_acoes = QHBoxLayout()
        self.layout_acoes.setSpacing(10)
        self.layout_acoes.setObjectName(u"layout_acoes")
        self.spacer_acoes = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_acoes.addItem(self.spacer_acoes)

        self.btn_cancelar = QPushButton(Dialog)
        self.btn_cancelar.setObjectName(u"btn_cancelar")
        self.btn_cancelar.setMinimumSize(QSize(110, 40))

        self.layout_acoes.addWidget(self.btn_cancelar)

        self.btn_salvar = QPushButton(Dialog)
        self.btn_salvar.setObjectName(u"btn_salvar")
        self.btn_salvar.setMinimumSize(QSize(110, 40))

        self.layout_acoes.addWidget(self.btn_salvar)


        self.layout_principal.addLayout(self.layout_acoes)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Configura\u00e7\u00e3o de Limites", None))
        self.lbl_titulo.setText(QCoreApplication.translate("Dialog", u"Configura\u00e7\u00e3o de Limites", None))
        self.lbl_subtitulo.setText(QCoreApplication.translate("Dialog", u"Par\u00e2metros de alerta para tens\u00e3o e corrente", None))
        self.grupo_regras.setProperty(u"class", QCoreApplication.translate("Dialog", u"panel", None))
        self.lbl_regras_titulo.setText(QCoreApplication.translate("Dialog", u"Regras de alerta", None))
        self.lbl_regras_titulo.setProperty(u"class", QCoreApplication.translate("Dialog", u"panelTitle", None))
        self.lbl_tensao_titulo.setText(QCoreApplication.translate("Dialog", u"REGRA 1 \u00b7 TENS\u00c3O M\u00c1XIMA", None))
        self.lbl_tensao_titulo.setProperty(u"class", QCoreApplication.translate("Dialog", u"fieldLabel", None))
        self.spin_tensao_max.setSuffix(QCoreApplication.translate("Dialog", u" V", None))
        self.lbl_corrente_titulo.setText(QCoreApplication.translate("Dialog", u"REGRA 2 \u00b7 CORRENTE M\u00c1XIMA", None))
        self.lbl_corrente_titulo.setProperty(u"class", QCoreApplication.translate("Dialog", u"fieldLabel", None))
        self.spin_corrente_max.setSuffix(QCoreApplication.translate("Dialog", u" A", None))
        self.lbl_previsao_titulo.setText(QCoreApplication.translate("Dialog", u"LIMITE DE POT\u00caNCIA RESULTANTE (P = V \u00d7 I)", None))
        self.lbl_potencia_calculada.setText(QCoreApplication.translate("Dialog", u"2400.0 W", None))
        self.lbl_aviso_manual.setText("")
        self.lbl_aviso_manual.setStyleSheet(QCoreApplication.translate("Dialog", u"color: #EA580C; font-size: 10px; font-weight: 600;", None))
        self.btn_cancelar.setText(QCoreApplication.translate("Dialog", u"Cancelar", None))
        self.btn_salvar.setText(QCoreApplication.translate("Dialog", u"Salvar", None))
    # retranslateUi

