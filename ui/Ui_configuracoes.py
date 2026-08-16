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
from PySide6.QtWidgets import (QApplication, QDialog, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(629, 182)
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 20, 561, 151))
        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 20, 541, 121))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.spin_tensao_max = QDoubleSpinBox(self.widget)
        self.spin_tensao_max.setObjectName(u"spin_tensao_max")

        self.gridLayout.addWidget(self.spin_tensao_max, 1, 1, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.spin_corrente_max = QDoubleSpinBox(self.widget)
        self.spin_corrente_max.setObjectName(u"spin_corrente_max")

        self.gridLayout.addWidget(self.spin_corrente_max, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 10)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btn_salvar = QPushButton(self.widget)
        self.btn_salvar.setObjectName(u"btn_salvar")

        self.horizontalLayout_6.addWidget(self.btn_salvar)

        self.btn_cancelar = QPushButton(self.widget)
        self.btn_cancelar.setObjectName(u"btn_cancelar")

        self.horizontalLayout_6.addWidget(self.btn_cancelar)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Configura\u00e7\u00e3o de Parametros", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Tens\u00e3o M\u00e1xima:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Corrente M\u00e1xima:", None))
        self.btn_salvar.setText(QCoreApplication.translate("Dialog", u"Salvar", None))
        self.btn_cancelar.setText(QCoreApplication.translate("Dialog", u"Cancelar", None))
    # retranslateUi

