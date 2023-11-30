# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Navigation.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTabWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 614)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(50, 0, 751, 611))
        self.stackedWidget = QStackedWidget(self.widget_3)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(-21, 9, 751, 551))
        self.homePage = QWidget()
        self.homePage.setObjectName(u"homePage")
        self.tabWidgetHome = QTabWidget(self.homePage)
        self.tabWidgetHome.setObjectName(u"tabWidgetHome")
        self.tabWidgetHome.setGeometry(QRect(-10, 0, 751, 591))
        self.tabWidgetHome.setTabShape(QTabWidget.Rounded)
        self.liveViewTab = QWidget()
        self.liveViewTab.setObjectName(u"liveViewTab")
        font = QFont()
        font.setBold(False)
        self.liveViewTab.setFont(font)
        self.liveViewTab.setAutoFillBackground(False)
        self.layoutWidget = QWidget(self.liveViewTab)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(50, 10, 661, 91))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.startEntTextLayout = QVBoxLayout()
        self.startEntTextLayout.setObjectName(u"startEntTextLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.startEntTextLayout.addWidget(self.label)

        self.entInfo = QLabel(self.layoutWidget)
        self.entInfo.setObjectName(u"entInfo")

        self.startEntTextLayout.addWidget(self.entInfo)


        self.horizontalLayout_2.addLayout(self.startEntTextLayout)

        self.startEnTBtn = QPushButton(self.layoutWidget)
        self.startEnTBtn.setObjectName(u"startEnTBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startEnTBtn.sizePolicy().hasHeightForWidth())
        self.startEnTBtn.setSizePolicy(sizePolicy)
        self.startEnTBtn.setMinimumSize(QSize(50, 50))
        font1 = QFont()
        font1.setBold(True)
        self.startEnTBtn.setFont(font1)

        self.horizontalLayout_2.addWidget(self.startEnTBtn)

        icon = QIcon()
        icon.addFile(u":/icons/img/stream.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidgetHome.addTab(self.liveViewTab, icon, "")
        self.tabWidgetHistory = QWidget()
        self.tabWidgetHistory.setObjectName(u"tabWidgetHistory")
        self.widgetLive = QWidget(self.tabWidgetHistory)
        self.widgetLive.setObjectName(u"widgetLive")
        self.widgetLive.setGeometry(QRect(29, 19, 711, 531))
        self.label_9 = QLabel(self.tabWidgetHistory)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(30, 0, 711, 16))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.label_9.setFont(font2)
        self.tabWidgetHome.addTab(self.tabWidgetHistory, "")
        self.stackedWidget.addWidget(self.homePage)
        self.statistikPage = QWidget()
        self.statistikPage.setObjectName(u"statistikPage")
        self.label_6 = QLabel(self.statistikPage)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(220, 150, 49, 16))
        self.stackedWidget.addWidget(self.statistikPage)
        self.impotPage = QWidget()
        self.impotPage.setObjectName(u"impotPage")
        self.pushButton = QPushButton(self.impotPage)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(490, 470, 231, 31))
        self.importAreaDragDrop = QWidget(self.impotPage)
        self.importAreaDragDrop.setObjectName(u"importAreaDragDrop")
        self.importAreaDragDrop.setGeometry(QRect(130, 90, 461, 261))
        self.importAreaDragDrop.setAcceptDrops(True)
        self.importAreaDragDrop.setStyleSheet(u"background-color:rgb(217, 217, 217)")
        self.label_8 = QLabel(self.importAreaDragDrop)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(180, 110, 181, 16))
        self.chooseFileFromExplorer = QPushButton(self.impotPage)
        self.chooseFileFromExplorer.setObjectName(u"chooseFileFromExplorer")
        self.chooseFileFromExplorer.setGeometry(QRect(130, 370, 221, 31))
        self.stackedWidget.addWidget(self.impotPage)
        self.pushButton.raise_()
        self.chooseFileFromExplorer.raise_()
        self.importAreaDragDrop.raise_()
        self.qrGenPage = QWidget()
        self.qrGenPage.setObjectName(u"qrGenPage")
        self.qrGenInfoPage = QWidget(self.qrGenPage)
        self.qrGenInfoPage.setObjectName(u"qrGenInfoPage")
        self.qrGenInfoPage.setGeometry(QRect(30, 50, 651, 441))
        self.infoBoxQr = QLabel(self.qrGenInfoPage)
        self.infoBoxQr.setObjectName(u"infoBoxQr")
        self.infoBoxQr.setGeometry(QRect(70, 70, 481, 371))
        self.layoutWidget1 = QWidget(self.qrGenInfoPage)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(50, 10, 531, 61))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.qrNrInputBox = QLineEdit(self.layoutWidget1)
        self.qrNrInputBox.setObjectName(u"qrNrInputBox")
        self.qrNrInputBox.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.qrNrInputBox)

        self.generateQrBtn = QPushButton(self.layoutWidget1)
        self.generateQrBtn.setObjectName(u"generateQrBtn")
        self.generateQrBtn.setMinimumSize(QSize(50, 0))
        self.generateQrBtn.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.generateQrBtn)

        self.label_2 = QLabel(self.qrGenPage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 20, 191, 16))
        self.stackedWidget.addWidget(self.qrGenPage)
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName(u"settingsPage")
        self.label_5 = QLabel(self.settingsPage)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(310, 150, 49, 16))
        self.stackedWidget.addWidget(self.settingsPage)
        self.leftNavigation = QWidget(self.centralwidget)
        self.leftNavigation.setObjectName(u"leftNavigation")
        self.leftNavigation.setGeometry(QRect(10, 0, 41, 601))
        self.layoutWidget2 = QWidget(self.leftNavigation)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(0, 0, 30, 171))
        self.leftNavigationVerticalLayout = QVBoxLayout(self.layoutWidget2)
        self.leftNavigationVerticalLayout.setObjectName(u"leftNavigationVerticalLayout")
        self.leftNavigationVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.homeBtn = QPushButton(self.layoutWidget2)
        self.homeBtn.setObjectName(u"homeBtn")
        icon1 = QIcon()
        icon1.addFile(u":/icons/img/homebig.png", QSize(), QIcon.Normal, QIcon.Off)
        self.homeBtn.setIcon(icon1)

        self.leftNavigationVerticalLayout.addWidget(self.homeBtn)

        self.statistik = QPushButton(self.layoutWidget2)
        self.statistik.setObjectName(u"statistik")
        icon2 = QIcon()
        icon2.addFile(u":/icons/img/graph-up.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.statistik.setIcon(icon2)

        self.leftNavigationVerticalLayout.addWidget(self.statistik)

        self.importBtn = QPushButton(self.layoutWidget2)
        self.importBtn.setObjectName(u"importBtn")
        icon3 = QIcon()
        icon3.addFile(u":/icons/img/import-1.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.importBtn.setIcon(icon3)

        self.leftNavigationVerticalLayout.addWidget(self.importBtn)

        self.qrGenBtn = QPushButton(self.layoutWidget2)
        self.qrGenBtn.setObjectName(u"qrGenBtn")
        icon4 = QIcon()
        icon4.addFile(u":/icons/img/qr-code-scanner.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.qrGenBtn.setIcon(icon4)
        self.qrGenBtn.setFlat(False)

        self.leftNavigationVerticalLayout.addWidget(self.qrGenBtn)

        self.settingsBtn = QPushButton(self.layoutWidget2)
        self.settingsBtn.setObjectName(u"settingsBtn")
        icon5 = QIcon()
        icon5.addFile(u":/icons/img/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsBtn.setIcon(icon5)

        self.leftNavigationVerticalLayout.addWidget(self.settingsBtn)

        self.modalDialogBackground = QWidget(self.centralwidget)
        self.modalDialogBackground.setObjectName(u"modalDialogBackground")
        self.modalDialogBackground.setGeometry(QRect(0, -1, 801, 611))
        self.modalDialogBackground.setMinimumSize(QSize(801, 0))
        self.modalDialogBackground.setStyleSheet(u"")
        self.modalDialog = QWidget(self.modalDialogBackground)
        self.modalDialog.setObjectName(u"modalDialog")
        self.modalDialog.setGeometry(QRect(200, 180, 401, 241))
        self.modalDialog.setStyleSheet(u"")
        self.modalBoxTextContent = QWidget(self.modalDialog)
        self.modalBoxTextContent.setObjectName(u"modalBoxTextContent")
        self.modalBoxTextContent.setGeometry(QRect(20, -40, 341, 201))
        self.modalBoxTextContent.setMinimumSize(QSize(200, 120))
        self.modalBoxTextContent.setStyleSheet(u"background-color: rgb(238, 238, 238);")
        self.modalBoxText = QLabel(self.modalBoxTextContent)
        self.modalBoxText.setObjectName(u"modalBoxText")
        self.modalBoxText.setGeometry(QRect(20, 50, 291, 131))
        self.footerWidgetDialogBox = QWidget(self.modalDialog)
        self.footerWidgetDialogBox.setObjectName(u"footerWidgetDialogBox")
        self.footerWidgetDialogBox.setGeometry(QRect(20, 160, 341, 41))
        self.layoutWidget3 = QWidget(self.footerWidgetDialogBox)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(0, 10, 341, 31))
        self.dialogBoxFooter = QHBoxLayout(self.layoutWidget3)
        self.dialogBoxFooter.setObjectName(u"dialogBoxFooter")
        self.dialogBoxFooter.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacerCloseBtn = QSpacerItem(258, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.dialogBoxFooter.addItem(self.horizontalSpacerCloseBtn)

        self.closeBtnModal = QPushButton(self.layoutWidget3)
        self.closeBtnModal.setObjectName(u"closeBtnModal")

        self.dialogBoxFooter.addWidget(self.closeBtnModal)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidgetHome.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(whatsthis)
        self.homePage.setWhatsThis(QCoreApplication.translate("MainWindow", u"HomePage", None))
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Erfassung & Tracking Application", None))
        self.entInfo.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.startEnTBtn.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.tabWidgetHome.setTabText(self.tabWidgetHome.indexOf(self.liveViewTab), QCoreApplication.translate("MainWindow", u"Home", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Live-Action in der Laborstra\u00dfe", None))
        self.tabWidgetHome.setTabText(self.tabWidgetHome.indexOf(self.tabWidgetHistory), QCoreApplication.translate("MainWindow", u"Live View", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Statistik", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Neu Experiment anlegen", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Drag and Drop", None))
        self.chooseFileFromExplorer.setText(QCoreApplication.translate("MainWindow", u"Dateil ausw\u00e4hlen", None))
        self.infoBoxQr.setText("")
        self.qrNrInputBox.setText("")
        self.qrNrInputBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Anzahl von QR Code eingeben", None))
        self.generateQrBtn.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"QR-Code Generator", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.homeBtn.setText("")
        self.statistik.setText("")
        self.importBtn.setText("")
        self.qrGenBtn.setText("")
        self.settingsBtn.setText("")
        self.modalBoxText.setText("")
        self.closeBtnModal.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

