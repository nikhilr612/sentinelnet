# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowipYJiY.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(618, 751)
        self.actionList_Nodes = QAction(MainWindow)
        self.actionList_Nodes.setObjectName(u"actionList_Nodes")
        self.actionGetNode = QAction(MainWindow)
        self.actionGetNode.setObjectName(u"actionGetNode")
        self.actionListOffenders = QAction(MainWindow)
        self.actionListOffenders.setObjectName(u"actionListOffenders")
        self.actionClearOffences = QAction(MainWindow)
        self.actionClearOffences.setObjectName(u"actionClearOffences")
        self.actionClearOffences.setMenuRole(QAction.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.infoFrame = QFrame(self.centralwidget)
        self.infoFrame.setObjectName(u"infoFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoFrame.sizePolicy().hasHeightForWidth())
        self.infoFrame.setSizePolicy(sizePolicy)
        self.infoFrame.setMinimumSize(QSize(240, 0))
        self.infoFrame.setMaximumSize(QSize(200, 16777215))
        self.infoFrame.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_3 = QVBoxLayout(self.infoFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lastconn_label = QLabel(self.infoFrame)
        self.lastconn_label.setObjectName(u"lastconn_label")
        self.lastconn_label.setFrameShape(QFrame.NoFrame)
        self.lastconn_label.setFrameShadow(QFrame.Plain)

        self.verticalLayout_3.addWidget(self.lastconn_label)

        self.label_4 = QLabel(self.infoFrame)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.offender_list = QListWidget(self.infoFrame)
        QListWidgetItem(self.offender_list)
        QListWidgetItem(self.offender_list)
        self.offender_list.setObjectName(u"offender_list")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.offender_list.sizePolicy().hasHeightForWidth())
        self.offender_list.setSizePolicy(sizePolicy1)
        self.offender_list.setMaximumSize(QSize(16777215, 16777215))
        self.offender_list.setLineWidth(1)

        self.verticalLayout_3.addWidget(self.offender_list)

        self.pushButton = QPushButton(self.infoFrame)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_3.addWidget(self.pushButton)


        self.horizontalLayout.addWidget(self.infoFrame)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label)

        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.plainTextEdit)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label1 = QLabel(self.centralwidget)
        self.label1.setObjectName(u"label1")
        font1 = QFont()
        font1.setPointSize(14)
        self.label1.setFont(font1)

        self.verticalLayout.addWidget(self.label1)

        self.graph_label = QLabel(self.centralwidget)
        self.graph_label.setObjectName(u"graph_label")
        self.graph_label.setMinimumSize(QSize(600, 360))

        self.verticalLayout.addWidget(self.graph_label)

        self.refresh_graph = QPushButton(self.centralwidget)
        self.refresh_graph.setObjectName(u"refresh_graph")
        self.refresh_graph.setMaximumSize(QSize(120, 16777215))

        self.verticalLayout.addWidget(self.refresh_graph)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 618, 22))
        self.menuQuery = QMenu(self.menubar)
        self.menuQuery.setObjectName(u"menuQuery")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuQuery.menuAction())
        self.menuQuery.addAction(self.actionList_Nodes)
        self.menuQuery.addAction(self.actionGetNode)
        self.menuQuery.addAction(self.actionListOffenders)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionList_Nodes.setText(QCoreApplication.translate("MainWindow", u"List Nodes", None))
#if QT_CONFIG(shortcut)
        self.actionList_Nodes.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+L", None))
#endif // QT_CONFIG(shortcut)
        self.actionGetNode.setText(QCoreApplication.translate("MainWindow", u"Get Node Data", None))
#if QT_CONFIG(shortcut)
        self.actionGetNode.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.actionListOffenders.setText(QCoreApplication.translate("MainWindow", u"List Offenders", None))
#if QT_CONFIG(shortcut)
        self.actionListOffenders.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+L", None))
#endif // QT_CONFIG(shortcut)
        self.actionClearOffences.setText(QCoreApplication.translate("MainWindow", u"ClearOffences", None))
#if QT_CONFIG(shortcut)
        self.actionClearOffences.setShortcut(QCoreApplication.translate("MainWindow", u"Shift+Del", None))
#endif // QT_CONFIG(shortcut)
        self.lastconn_label.setText(QCoreApplication.translate("MainWindow", u"Latest Connection:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Offenders", None))

        __sortingEnabled = self.offender_list.isSortingEnabled()
        self.offender_list.setSortingEnabled(False)
        ___qlistwidgetitem = self.offender_list.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"MAC1", None));
        ___qlistwidgetitem1 = self.offender_list.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"MAC2", None));
        self.offender_list.setSortingEnabled(__sortingEnabled)

        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Clear All", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Server Logs", None))
        self.label1.setText(QCoreApplication.translate("MainWindow", u"Graph", None))
        self.graph_label.setText(QCoreApplication.translate("MainWindow", u"Awaiting Graph", None))
        self.refresh_graph.setText(QCoreApplication.translate("MainWindow", u"Refresh Graph", None))
        self.menuQuery.setTitle(QCoreApplication.translate("MainWindow", u"Query", None))
    # retranslateUi

