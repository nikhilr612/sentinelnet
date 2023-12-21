# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'listdialogEGUjiX.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_NodeListDialog(object):
    def setupUi(self, NodeListDialog):
        if not NodeListDialog.objectName():
            NodeListDialog.setObjectName(u"NodeListDialog")
        NodeListDialog.resize(427, 330)
        self.verticalFrame = QFrame(NodeListDialog)
        self.verticalFrame.setObjectName(u"verticalFrame")
        self.verticalFrame.setGeometry(QRect(0, 0, 431, 331))
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalFrame.sizePolicy().hasHeightForWidth())
        self.verticalFrame.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.verticalFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.verticalFrame)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.listWidget = QListWidget(self.verticalFrame)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalWidget = QWidget(self.verticalFrame)
        self.horizontalWidget.setObjectName(u"horizontalWidget")
        self.horizontalWidget.setMinimumSize(QSize(0, 0))
        self.horizontalWidget.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout = QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.horizontalWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 20))

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.horizontalWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 20))

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addWidget(self.horizontalWidget)

        self.buttonBox = QDialogButtonBox(self.verticalFrame)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(NodeListDialog)

        QMetaObject.connectSlotsByName(NodeListDialog)
    # setupUi

    def retranslateUi(self, NodeListDialog):
        NodeListDialog.setWindowTitle(QCoreApplication.translate("NodeListDialog", u"Node List", None))
        self.label_2.setText(QCoreApplication.translate("NodeListDialog", u"Node List", None))
        self.pushButton.setText(QCoreApplication.translate("NodeListDialog", u"Search", None))
    # retranslateUi

