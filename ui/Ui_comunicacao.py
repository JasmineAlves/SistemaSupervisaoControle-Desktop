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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 0, 611, 261))
        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(11, 31, 591, 211))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 2, 2)
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.spin_timeout = QSpinBox(self.widget)
        self.spin_timeout.setObjectName(u"spin_timeout")
        self.spin_timeout.setValue(1)

        self.gridLayout.addWidget(self.spin_timeout, 5, 1, 1, 1)

        self.combo_porta = QComboBox(self.widget)
        self.combo_porta.setObjectName(u"combo_porta")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.combo_porta.sizePolicy().hasHeightForWidth())
        self.combo_porta.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.combo_porta, 0, 1, 1, 1)

        self.combo_baud = QComboBox(self.widget)
        self.combo_baud.addItem("")
        self.combo_baud.addItem("")
        self.combo_baud.setObjectName(u"combo_baud")

        self.gridLayout.addWidget(self.combo_baud, 3, 1, 1, 1)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 10)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.lbl_status = QLabel(self.widget)
        self.lbl_status.setObjectName(u"lbl_status")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(5)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lbl_status.sizePolicy().hasHeightForWidth())
        self.lbl_status.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.lbl_status)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btn_desconectar = QPushButton(self.widget)
        self.btn_desconectar.setObjectName(u"btn_desconectar")

        self.horizontalLayout_6.addWidget(self.btn_desconectar)

        self.btn_conectar = QPushButton(self.widget)
        self.btn_conectar.setObjectName(u"btn_conectar")

        self.horizontalLayout_6.addWidget(self.btn_conectar)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 3)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Configura\u00e7\u00e3o de Comunica\u00e7\u00e3o Serial", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Timeout (s):", None))
        self.combo_baud.setItemText(0, QCoreApplication.translate("Form", u"9600", None))
        self.combo_baud.setItemText(1, QCoreApplication.translate("Form", u"115200", None))

        self.label_3.setText(QCoreApplication.translate("Form", u"Baud Rate:", None))
        self.label.setText(QCoreApplication.translate("Form", u"Porta COM:", None))
        self.lbl_status.setText(QCoreApplication.translate("Form", u"Status : Desconectado", None))
        self.btn_desconectar.setText(QCoreApplication.translate("Form", u"Desconectar", None))
        self.btn_conectar.setText(QCoreApplication.translate("Form", u"Conectar", None))
    # retranslateUi

