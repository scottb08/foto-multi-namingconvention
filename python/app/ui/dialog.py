# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(658, 302)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.contentWidgetHolder = QWidget(Form)
        self.contentWidgetHolder.setObjectName(u"contentWidgetHolder")
        self.contentWidgetVerticalLayout = QVBoxLayout(self.contentWidgetHolder)
        self.contentWidgetVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.contentWidgetVerticalLayout.setObjectName(u"contentWidgetVerticalLayout")

        self.verticalLayout.addWidget(self.contentWidgetHolder)

        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.appComboBox = QComboBox(self.widget_2)
        self.appComboBox.addItem("")
        self.appComboBox.setObjectName(u"appComboBox")

        self.gridLayout.addWidget(self.appComboBox, 0, 1, 1, 1)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.tkTemplateComboBox = QComboBox(self.widget_2)
        self.tkTemplateComboBox.addItem("")
        self.tkTemplateComboBox.setObjectName(u"tkTemplateComboBox")

        self.gridLayout.addWidget(self.tkTemplateComboBox, 1, 1, 1, 1)

        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.extraTokensWidget = QWidget(self.widget_2)
        self.extraTokensWidget.setObjectName(u"extraTokensWidget")
        self.extraTokensWidgetLayout = QGridLayout(self.extraTokensWidget)
        self.extraTokensWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTokensWidgetLayout.setObjectName(u"extraTokensWidgetLayout")

        self.gridLayout.addWidget(self.extraTokensWidget, 4, 1, 1, 1)

        self.label_8 = QLabel(self.widget_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)

        self.descriptionLabel = QLabel(self.widget_2)
        self.descriptionLabel.setObjectName(u"descriptionLabel")

        self.gridLayout.addWidget(self.descriptionLabel, 2, 1, 1, 1)

        self.line_4 = QFrame(self.widget_2)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_4, 3, 0, 1, 2)


        self.verticalLayout.addWidget(self.widget_2)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.filePathWidgetGroup = QWidget(Form)
        self.filePathWidgetGroup.setObjectName(u"filePathWidgetGroup")
        self.gridLayout_3 = QGridLayout(self.filePathWidgetGroup)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.filePathLineEdit = QLineEdit(self.filePathWidgetGroup)
        self.filePathLineEdit.setObjectName(u"filePathLineEdit")
        self.filePathLineEdit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.filePathLineEdit, 2, 1, 1, 1)

        self.label_5 = QLabel(self.filePathWidgetGroup)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"color: rgb(67, 131, 168);\n"
"font: 75 10pt \"Arial\";")

        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_4 = QLabel(self.filePathWidgetGroup)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"color: rgb(67, 131, 168);\n"
"font: 75 10pt \"Arial\";")

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)

        self.directoryPathCopyButton = QPushButton(self.filePathWidgetGroup)
        self.directoryPathCopyButton.setObjectName(u"directoryPathCopyButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.directoryPathCopyButton.sizePolicy().hasHeightForWidth())
        self.directoryPathCopyButton.setSizePolicy(sizePolicy1)
        self.directoryPathCopyButton.setMaximumSize(QSize(35, 16777215))
        icon = QIcon()
        icon.addFile(u":/res/copy.png", QSize(), QIcon.Normal, QIcon.Off)
        self.directoryPathCopyButton.setIcon(icon)

        self.gridLayout_3.addWidget(self.directoryPathCopyButton, 1, 4, 1, 1)

        self.label_6 = QLabel(self.filePathWidgetGroup)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"color: rgb(67, 131, 168);\n"
"font: 75 10pt \"Arial\";")

        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)

        self.fileNameCopyButton = QPushButton(self.filePathWidgetGroup)
        self.fileNameCopyButton.setObjectName(u"fileNameCopyButton")
        sizePolicy1.setHeightForWidth(self.fileNameCopyButton.sizePolicy().hasHeightForWidth())
        self.fileNameCopyButton.setSizePolicy(sizePolicy1)
        self.fileNameCopyButton.setMaximumSize(QSize(35, 16777215))
        self.fileNameCopyButton.setIcon(icon)

        self.gridLayout_3.addWidget(self.fileNameCopyButton, 0, 4, 1, 1)

        self.createFileButton = QPushButton(self.filePathWidgetGroup)
        self.createFileButton.setObjectName(u"createFileButton")
        icon1 = QIcon()
        icon1.addFile(u":/res/plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.createFileButton.setIcon(icon1)

        self.gridLayout_3.addWidget(self.createFileButton, 2, 2, 1, 1)

        self.filePathCopyButton = QPushButton(self.filePathWidgetGroup)
        self.filePathCopyButton.setObjectName(u"filePathCopyButton")
        sizePolicy1.setHeightForWidth(self.filePathCopyButton.sizePolicy().hasHeightForWidth())
        self.filePathCopyButton.setSizePolicy(sizePolicy1)
        self.filePathCopyButton.setMaximumSize(QSize(35, 16777215))
        self.filePathCopyButton.setIcon(icon)

        self.gridLayout_3.addWidget(self.filePathCopyButton, 2, 4, 1, 1)

        self.filePathOpenButton = QPushButton(self.filePathWidgetGroup)
        self.filePathOpenButton.setObjectName(u"filePathOpenButton")
        icon2 = QIcon()
        icon2.addFile(u":/res/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.filePathOpenButton.setIcon(icon2)

        self.gridLayout_3.addWidget(self.filePathOpenButton, 2, 3, 1, 1)

        self.directoryPathOpenButton = QPushButton(self.filePathWidgetGroup)
        self.directoryPathOpenButton.setObjectName(u"directoryPathOpenButton")
        self.directoryPathOpenButton.setIcon(icon2)

        self.gridLayout_3.addWidget(self.directoryPathOpenButton, 1, 3, 1, 1)

        self.dirPathLineEdit = QLineEdit(self.filePathWidgetGroup)
        self.dirPathLineEdit.setObjectName(u"dirPathLineEdit")
        self.dirPathLineEdit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.dirPathLineEdit, 1, 1, 1, 2)

        self.fileNameLineEdit = QLineEdit(self.filePathWidgetGroup)
        self.fileNameLineEdit.setObjectName(u"fileNameLineEdit")
        self.fileNameLineEdit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.fileNameLineEdit, 0, 1, 1, 3)


        self.verticalLayout.addWidget(self.filePathWidgetGroup)

        self.line_5 = QFrame(Form)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"color: rgb(67, 131, 168);\n"
"font: 75 10pt \"Arial\";")

        self.horizontalLayout.addWidget(self.label_9)

        self.copyFileLineEdit = QLineEdit(Form)
        self.copyFileLineEdit.setObjectName(u"copyFileLineEdit")

        self.horizontalLayout.addWidget(self.copyFileLineEdit)

        self.copyFilePathOpenButton = QPushButton(Form)
        self.copyFilePathOpenButton.setObjectName(u"copyFilePathOpenButton")
        self.copyFilePathOpenButton.setIcon(icon2)

        self.horizontalLayout.addWidget(self.copyFilePathOpenButton)

        self.copyFileToFileButton = QPushButton(Form)
        self.copyFileToFileButton.setObjectName(u"copyFileToFileButton")
        self.copyFileToFileButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.copyFileToFileButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.appComboBox.setItemText(0, QCoreApplication.translate("Form", u"Select Application", None))

        self.label_3.setText(QCoreApplication.translate("Form", u"Extra Tokens:", None))
        self.label.setText(QCoreApplication.translate("Form", u"Application:", None))
        self.tkTemplateComboBox.setItemText(0, QCoreApplication.translate("Form", u"Select Template", None))

        self.label_7.setText(QCoreApplication.translate("Form", u"Toolkit Template:", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Template Description:", None))
        self.descriptionLabel.setText("")
        self.filePathLineEdit.setText("")
        self.label_5.setText(QCoreApplication.translate("Form", u"Directory Path:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"File Name:", None))
#if QT_CONFIG(tooltip)
        self.directoryPathCopyButton.setToolTip(QCoreApplication.translate("Form", u"Copy Path to Clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.directoryPathCopyButton.setText("")
        self.label_6.setText(QCoreApplication.translate("Form", u"File Path:", None))
#if QT_CONFIG(tooltip)
        self.fileNameCopyButton.setToolTip(QCoreApplication.translate("Form", u"Copy Path to Clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.fileNameCopyButton.setText("")
#if QT_CONFIG(tooltip)
        self.createFileButton.setToolTip(QCoreApplication.translate("Form", u"Create File on Disk", None))
#endif // QT_CONFIG(tooltip)
        self.createFileButton.setText("")
#if QT_CONFIG(tooltip)
        self.filePathCopyButton.setToolTip(QCoreApplication.translate("Form", u"Copy Path to Clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.filePathCopyButton.setText("")
#if QT_CONFIG(tooltip)
        self.filePathOpenButton.setToolTip(QCoreApplication.translate("Form", u"Open in File Browser", None))
#endif // QT_CONFIG(tooltip)
        self.filePathOpenButton.setText("")
#if QT_CONFIG(tooltip)
        self.directoryPathOpenButton.setToolTip(QCoreApplication.translate("Form", u"Open in File Browser", None))
#endif // QT_CONFIG(tooltip)
        self.directoryPathOpenButton.setText("")
        self.dirPathLineEdit.setText("")
        self.fileNameLineEdit.setText("")
        self.label_9.setText(QCoreApplication.translate("Form", u"Copy File To File Path", None))
#if QT_CONFIG(tooltip)
        self.copyFilePathOpenButton.setToolTip(QCoreApplication.translate("Form", u"Browse to a file to copy", None))
#endif // QT_CONFIG(tooltip)
        self.copyFilePathOpenButton.setText("")
#if QT_CONFIG(tooltip)
        self.copyFileToFileButton.setToolTip(QCoreApplication.translate("Form", u"Copy given file (left) to the file path described above", None))
#endif // QT_CONFIG(tooltip)
        self.copyFileToFileButton.setText("")
    # retranslateUi

