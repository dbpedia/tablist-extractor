# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiLayout.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1144, 806)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(8, 0, 1121, 791))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 830))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.frame = QtGui.QFrame(self.tab)
        self.frame.setEnabled(True)
        self.frame.setMinimumSize(QtCore.QSize(990, 735))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame_3 = QtGui.QFrame(self.frame)
        self.frame_3.setMaximumSize(QtCore.QSize(300, 510))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.formLayout = QtGui.QFormLayout(self.frame_3)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.Step1Label = QtGui.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.Step1Label.setFont(font)
        self.Step1Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Step1Label.setObjectName(_fromUtf8("Step1Label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.Step1Label)
        self.ResourceLabel = QtGui.QLabel(self.frame_3)
        self.ResourceLabel.setObjectName(_fromUtf8("ResourceLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.ResourceLabel)
        self.ResourceField = QtGui.QLineEdit(self.frame_3)
        self.ResourceField.setStatusTip(_fromUtf8(""))
        self.ResourceField.setText(_fromUtf8(""))
        self.ResourceField.setObjectName(_fromUtf8("ResourceField"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.ResourceField)
        self.CollectModeLabel = QtGui.QLabel(self.frame_3)
        self.CollectModeLabel.setObjectName(_fromUtf8("CollectModeLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.CollectModeLabel)
        self.CollectmodeSBtn = QtGui.QRadioButton(self.frame_3)
        self.CollectmodeSBtn.setChecked(True)
        self.CollectmodeSBtn.setObjectName(_fromUtf8("CollectmodeSBtn"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.CollectmodeSBtn)
        self.CollectmodeTBtn = QtGui.QRadioButton(self.frame_3)
        self.CollectmodeTBtn.setObjectName(_fromUtf8("CollectmodeTBtn"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.CollectmodeTBtn)
        self.Languagelabel = QtGui.QLabel(self.frame_3)
        self.Languagelabel.setObjectName(_fromUtf8("Languagelabel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.Languagelabel)
        self.LanguageCombo = QtGui.QComboBox(self.frame_3)
        self.LanguageCombo.setObjectName(_fromUtf8("LanguageCombo"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.LanguageCombo)
        self.ExploreBtn = QtGui.QPushButton(self.frame_3)
        self.ExploreBtn.setObjectName(_fromUtf8("ExploreBtn"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.ExploreBtn)
        self.line = QtGui.QFrame(self.frame_3)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.SpanningRole, self.line)
        self.Step2Label = QtGui.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.Step2Label.setFont(font)
        self.Step2Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Step2Label.setObjectName(_fromUtf8("Step2Label"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.SpanningRole, self.Step2Label)
        self.Step2Infolabel = QtGui.QLabel(self.frame_3)
        self.Step2Infolabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Step2Infolabel.setWordWrap(False)
        self.Step2Infolabel.setObjectName(_fromUtf8("Step2Infolabel"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.SpanningRole, self.Step2Infolabel)
        self.saveBtn = QtGui.QPushButton(self.frame_3)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.SpanningRole, self.saveBtn)
        self.line_2 = QtGui.QFrame(self.frame_3)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.formLayout.setWidget(12, QtGui.QFormLayout.SpanningRole, self.line_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(13, QtGui.QFormLayout.SpanningRole, spacerItem)
        self.Step3Label = QtGui.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.Step3Label.setFont(font)
        self.Step3Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Step3Label.setObjectName(_fromUtf8("Step3Label"))
        self.formLayout.setWidget(14, QtGui.QFormLayout.SpanningRole, self.Step3Label)
        self.ExtractBtn = QtGui.QPushButton(self.frame_3)
        self.ExtractBtn.setObjectName(_fromUtf8("ExtractBtn"))
        self.formLayout.setWidget(15, QtGui.QFormLayout.SpanningRole, self.ExtractBtn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(16, QtGui.QFormLayout.SpanningRole, spacerItem1)
        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.frame)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 1, 1, 1, 1)
        self.TerminalWindow = QtGui.QTextBrowser(self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(33, 255, 6))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 255, 6))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(128, 128, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(236, 236, 236))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.TerminalWindow.setPalette(palette)
        self.TerminalWindow.setObjectName(_fromUtf8("TerminalWindow"))
        self.gridLayout.addWidget(self.TerminalWindow, 2, 0, 1, 2)
        self.horizontalLayout_4.addWidget(self.frame)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame_6 = QtGui.QFrame(self.tab_2)
        self.frame_6.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.formLayout_2 = QtGui.QFormLayout(self.frame_6)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.updateMapperLabel = QtGui.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.updateMapperLabel.setFont(font)
        self.updateMapperLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.updateMapperLabel.setObjectName(_fromUtf8("updateMapperLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.SpanningRole, self.updateMapperLabel)
        self.ListOfMappersLabel = QtGui.QLabel(self.frame_6)
        self.ListOfMappersLabel.setObjectName(_fromUtf8("ListOfMappersLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.ListOfMappersLabel)
        self.ListOfMappersCombo = QtGui.QComboBox(self.frame_6)
        self.ListOfMappersCombo.setObjectName(_fromUtf8("ListOfMappersCombo"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.ListOfMappersCombo)
        self.ShowMappersBtn = QtGui.QPushButton(self.frame_6)
        self.ShowMappersBtn.setObjectName(_fromUtf8("ShowMappersBtn"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.ShowMappersBtn)
        self.MapperNameLabel = QtGui.QLabel(self.frame_6)
        self.MapperNameLabel.setObjectName(_fromUtf8("MapperNameLabel"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.MapperNameLabel)
        self.ListSectionsLabel = QtGui.QLabel(self.frame_6)
        self.ListSectionsLabel.setObjectName(_fromUtf8("ListSectionsLabel"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.ListSectionsLabel)
        self.ListHeadersTextEdit = QtGui.QTextEdit(self.frame_6)
        self.ListHeadersTextEdit.setObjectName(_fromUtf8("ListHeadersTextEdit"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.ListHeadersTextEdit)
        self.TableHeadersLabel = QtGui.QLabel(self.frame_6)
        self.TableHeadersLabel.setObjectName(_fromUtf8("TableHeadersLabel"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.TableHeadersLabel)
        self.TableSectionsTextEdit = QtGui.QTextEdit(self.frame_6)
        self.TableSectionsTextEdit.setObjectName(_fromUtf8("TableSectionsTextEdit"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.TableSectionsTextEdit)
        self.frame_11 = QtGui.QFrame(self.frame_6)
        font = QtGui.QFont()
        font.setKerning(True)
        self.frame_11.setFont(font)
        self.frame_11.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_11.setMidLineWidth(-2)
        self.frame_11.setObjectName(_fromUtf8("frame_11"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_11)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.ExtractorsLabel = QtGui.QLabel(self.frame_11)
        self.ExtractorsLabel.setObjectName(_fromUtf8("ExtractorsLabel"))
        self.horizontalLayout_3.addWidget(self.ExtractorsLabel)
        self.extractor_checkBox_1 = QtGui.QCheckBox(self.frame_11)
        self.extractor_checkBox_1.setObjectName(_fromUtf8("extractor_checkBox_1"))
        self.horizontalLayout_3.addWidget(self.extractor_checkBox_1)
        self.extractor_checkBox_2 = QtGui.QCheckBox(self.frame_11)
        self.extractor_checkBox_2.setObjectName(_fromUtf8("extractor_checkBox_2"))
        self.horizontalLayout_3.addWidget(self.extractor_checkBox_2)
        self.extractor_checkBox_3 = QtGui.QCheckBox(self.frame_11)
        self.extractor_checkBox_3.setObjectName(_fromUtf8("extractor_checkBox_3"))
        self.horizontalLayout_3.addWidget(self.extractor_checkBox_3)
        self.extractor_checkBox_4 = QtGui.QCheckBox(self.frame_11)
        self.extractor_checkBox_4.setObjectName(_fromUtf8("extractor_checkBox_4"))
        self.horizontalLayout_3.addWidget(self.extractor_checkBox_4)
        self.extractor_checkBox_5 = QtGui.QCheckBox(self.frame_11)
        self.extractor_checkBox_5.setObjectName(_fromUtf8("extractor_checkBox_5"))
        self.horizontalLayout_3.addWidget(self.extractor_checkBox_5)
        self.extractor_checkBox_6 = QtGui.QCheckBox(self.frame_11)
        self.extractor_checkBox_6.setObjectName(_fromUtf8("extractor_checkBox_6"))
        self.horizontalLayout_3.addWidget(self.extractor_checkBox_6)
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.SpanningRole, self.frame_11)
        self.frame_10 = QtGui.QFrame(self.frame_6)
        self.frame_10.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_10.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_10.setObjectName(_fromUtf8("frame_10"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_10)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.YearsLabel = QtGui.QLabel(self.frame_10)
        self.YearsLabel.setObjectName(_fromUtf8("YearsLabel"))
        self.horizontalLayout_2.addWidget(self.YearsLabel)
        self.YearsYesRadio = QtGui.QRadioButton(self.frame_10)
        self.YearsYesRadio.setObjectName(_fromUtf8("YearsYesRadio"))
        self.horizontalLayout_2.addWidget(self.YearsYesRadio)
        self.YearsNoRadio = QtGui.QRadioButton(self.frame_10)
        self.YearsNoRadio.setObjectName(_fromUtf8("YearsNoRadio"))
        self.horizontalLayout_2.addWidget(self.YearsNoRadio)
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.SpanningRole, self.frame_10)
        self.OntologyLabel = QtGui.QLabel(self.frame_6)
        self.OntologyLabel.setObjectName(_fromUtf8("OntologyLabel"))
        self.formLayout_2.setWidget(8, QtGui.QFormLayout.LabelRole, self.OntologyLabel)
        self.OntologyTextEdit = QtGui.QTextEdit(self.frame_6)
        self.OntologyTextEdit.setObjectName(_fromUtf8("OntologyTextEdit"))
        self.formLayout_2.setWidget(8, QtGui.QFormLayout.FieldRole, self.OntologyTextEdit)
        self.SaveMapperBtn = QtGui.QPushButton(self.frame_6)
        self.SaveMapperBtn.setObjectName(_fromUtf8("SaveMapperBtn"))
        self.formLayout_2.setWidget(9, QtGui.QFormLayout.FieldRole, self.SaveMapperBtn)
        self.MapperNameLineEdit = QtGui.QLineEdit(self.frame_6)
        self.MapperNameLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.MapperNameLineEdit.setObjectName(_fromUtf8("MapperNameLineEdit"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.MapperNameLineEdit)
        self.horizontalLayout.addWidget(self.frame_6)
        self.frame_4 = QtGui.QFrame(self.tab_2)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.formLayout_3 = QtGui.QFormLayout(self.frame_4)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.UpdateDomainLabel = QtGui.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.UpdateDomainLabel.setFont(font)
        self.UpdateDomainLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.UpdateDomainLabel.setObjectName(_fromUtf8("UpdateDomainLabel"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.SpanningRole, self.UpdateDomainLabel)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout_3.setItem(1, QtGui.QFormLayout.SpanningRole, spacerItem2)
        self.DomainsListLabel = QtGui.QLabel(self.frame_4)
        self.DomainsListLabel.setObjectName(_fromUtf8("DomainsListLabel"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.DomainsListLabel)
        self.DomainsListCombo = QtGui.QComboBox(self.frame_4)
        self.DomainsListCombo.setObjectName(_fromUtf8("DomainsListCombo"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.DomainsListCombo)
        self.ShowDomainBtn = QtGui.QPushButton(self.frame_4)
        self.ShowDomainBtn.setObjectName(_fromUtf8("ShowDomainBtn"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.ShowDomainBtn)
        self.DomainNameLabel = QtGui.QLabel(self.frame_4)
        self.DomainNameLabel.setObjectName(_fromUtf8("DomainNameLabel"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.LabelRole, self.DomainNameLabel)
        self.DomainNameLineEdit = QtGui.QLineEdit(self.frame_4)
        self.DomainNameLineEdit.setObjectName(_fromUtf8("DomainNameLineEdit"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.FieldRole, self.DomainNameLineEdit)
        self.AddDomainMappersLabel = QtGui.QLabel(self.frame_4)
        self.AddDomainMappersLabel.setObjectName(_fromUtf8("AddDomainMappersLabel"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.LabelRole, self.AddDomainMappersLabel)
        self.MappersListView = QtGui.QListView(self.frame_4)
        self.MappersListView.setObjectName(_fromUtf8("MappersListView"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.FieldRole, self.MappersListView)
        self.SaveDomainBtn = QtGui.QPushButton(self.frame_4)
        self.SaveDomainBtn.setObjectName(_fromUtf8("SaveDomainBtn"))
        self.formLayout_3.setWidget(7, QtGui.QFormLayout.FieldRole, self.SaveDomainBtn)
        self.line_3 = QtGui.QFrame(self.frame_4)
        self.line_3.setMinimumSize(QtCore.QSize(50, 20))
        self.line_3.setLineWidth(2)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.formLayout_3.setWidget(9, QtGui.QFormLayout.SpanningRole, self.line_3)
        self.label_10 = QtGui.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_3.setWidget(11, QtGui.QFormLayout.SpanningRole, self.label_10)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout_3.setItem(12, QtGui.QFormLayout.SpanningRole, spacerItem3)
        self.CheckOntologyLabel = QtGui.QLabel(self.frame_4)
        self.CheckOntologyLabel.setObjectName(_fromUtf8("CheckOntologyLabel"))
        self.formLayout_3.setWidget(13, QtGui.QFormLayout.LabelRole, self.CheckOntologyLabel)
        self.CheckOntologyField = QtGui.QLineEdit(self.frame_4)
        self.CheckOntologyField.setObjectName(_fromUtf8("CheckOntologyField"))
        self.formLayout_3.setWidget(13, QtGui.QFormLayout.FieldRole, self.CheckOntologyField)
        self.CheckBtn = QtGui.QPushButton(self.frame_4)
        self.CheckBtn.setObjectName(_fromUtf8("CheckBtn"))
        self.formLayout_3.setWidget(15, QtGui.QFormLayout.FieldRole, self.CheckBtn)
        self.ResultLabel = QtGui.QLabel(self.frame_4)
        self.ResultLabel.setObjectName(_fromUtf8("ResultLabel"))
        self.formLayout_3.setWidget(16, QtGui.QFormLayout.LabelRole, self.ResultLabel)
        self.CheckOntologyLanguageCombo = QtGui.QComboBox(self.frame_4)
        self.CheckOntologyLanguageCombo.setObjectName(_fromUtf8("CheckOntologyLanguageCombo"))
        self.formLayout_3.setWidget(14, QtGui.QFormLayout.FieldRole, self.CheckOntologyLanguageCombo)
        self.CheckOntologyLanguageLabel = QtGui.QLabel(self.frame_4)
        self.CheckOntologyLanguageLabel.setObjectName(_fromUtf8("CheckOntologyLanguageLabel"))
        self.formLayout_3.setWidget(14, QtGui.QFormLayout.LabelRole, self.CheckOntologyLanguageLabel)
        self.CheckOntologyResult = QtGui.QLabel(self.frame_4)
        self.CheckOntologyResult.setText(_fromUtf8(""))
        self.CheckOntologyResult.setObjectName(_fromUtf8("CheckOntologyResult"))
        self.formLayout_3.setWidget(16, QtGui.QFormLayout.FieldRole, self.CheckOntologyResult)
        self.horizontalLayout.addWidget(self.frame_4)
        self.frame_5 = QtGui.QFrame(self.tab_2)
        self.frame_5.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.formLayout_4 = QtGui.QFormLayout(self.frame_5)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.ResourcesListLabel = QtGui.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.ResourcesListLabel.setFont(font)
        self.ResourcesListLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ResourcesListLabel.setObjectName(_fromUtf8("ResourcesListLabel"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.SpanningRole, self.ResourcesListLabel)
        self.DomainLabel = QtGui.QLabel(self.frame_5)
        self.DomainLabel.setObjectName(_fromUtf8("DomainLabel"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.DomainLabel)
        self.DomainLineEdit = QtGui.QLineEdit(self.frame_5)
        self.DomainLineEdit.setObjectName(_fromUtf8("DomainLineEdit"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.DomainLineEdit)
        self.DomainLanguageLabel = QtGui.QLabel(self.frame_5)
        self.DomainLanguageLabel.setObjectName(_fromUtf8("DomainLanguageLabel"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.DomainLanguageLabel)
        self.ResoucesListView = QtGui.QListView(self.frame_5)
        self.ResoucesListView.setMinimumSize(QtCore.QSize(0, 500))
        self.ResoucesListView.setObjectName(_fromUtf8("ResoucesListView"))
        self.formLayout_4.setWidget(5, QtGui.QFormLayout.SpanningRole, self.ResoucesListView)
        self.ShowResourcesBtn = QtGui.QPushButton(self.frame_5)
        self.ShowResourcesBtn.setObjectName(_fromUtf8("ShowResourcesBtn"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.FieldRole, self.ShowResourcesBtn)
        self.ResourcesListResult = QtGui.QLabel(self.frame_5)
        self.ResourcesListResult.setText(_fromUtf8(""))
        self.ResourcesListResult.setObjectName(_fromUtf8("ResourcesListResult"))
        self.formLayout_4.setWidget(4, QtGui.QFormLayout.FieldRole, self.ResourcesListResult)
        self.DomainLanguageCombo = QtGui.QComboBox(self.frame_5)
        self.DomainLanguageCombo.setObjectName(_fromUtf8("DomainLanguageCombo"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.DomainLanguageCombo)
        self.horizontalLayout.addWidget(self.frame_5)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Tablist-Extractor", None))
        self.Step1Label.setText(_translate("MainWindow", "STEP 1", None))
        self.ResourceLabel.setText(_translate("MainWindow", "Resource :", None))
        self.ResourceField.setToolTip(_translate("MainWindow", "Enter the Resource/Domain name for which the triples should be extracted.\n"
"\n"
"For eg., \"Kobe_Bryant\", \"William_Gibson\" for single resources.\n"
"              \"BasketballPlayer\", \"Writer\" for group of resources.", None))
        self.CollectModeLabel.setText(_translate("MainWindow", "Collect Mode :", None))
        self.CollectmodeSBtn.setToolTip(_translate("MainWindow", "Select if it is a single resource", None))
        self.CollectmodeSBtn.setText(_translate("MainWindow", "Single", None))
        self.CollectmodeTBtn.setToolTip(_translate("MainWindow", "Select if it is a group of resources", None))
        self.CollectmodeTBtn.setText(_translate("MainWindow", "Topic/Domain", None))
        self.Languagelabel.setText(_translate("MainWindow", "Language :", None))
        self.LanguageCombo.setToolTip(_translate("MainWindow", "Enter Language of wiki pages", None))
        self.ExploreBtn.setText(_translate("MainWindow", "Explore", None))
        self.Step2Label.setText(_translate("MainWindow", "STEP 2", None))
        self.Step2Infolabel.setText(_translate("MainWindow", "Add/Edit ontology mappings as \n"
"required in the edit box right side.\n"
"After editing, click the \n"
"save button to update mappings.", None))
        self.saveBtn.setText(_translate("MainWindow", "Save", None))
        self.Step3Label.setText(_translate("MainWindow", "STEP 3", None))
        self.ExtractBtn.setText(_translate("MainWindow", "Extract Triples", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.updateMapperLabel.setText(_translate("MainWindow", "Add/Edit Mappers", None))
        self.ListOfMappersLabel.setText(_translate("MainWindow", "List of Mappers:", None))
        self.ShowMappersBtn.setText(_translate("MainWindow", "Show", None))
        self.MapperNameLabel.setText(_translate("MainWindow", "Mapper Name:", None))
        self.ListSectionsLabel.setText(_translate("MainWindow", "List Headers:", None))
        self.TableHeadersLabel.setText(_translate("MainWindow", "Table Sections:", None))
        self.ExtractorsLabel.setText(_translate("MainWindow", "Extractors:", None))
        self.extractor_checkBox_1.setText(_translate("MainWindow", "1", None))
        self.extractor_checkBox_2.setText(_translate("MainWindow", "2", None))
        self.extractor_checkBox_3.setText(_translate("MainWindow", "3", None))
        self.extractor_checkBox_4.setText(_translate("MainWindow", "4", None))
        self.extractor_checkBox_5.setText(_translate("MainWindow", "5", None))
        self.extractor_checkBox_6.setText(_translate("MainWindow", "6", None))
        self.YearsLabel.setText(_translate("MainWindow", "Includes Years:", None))
        self.YearsYesRadio.setText(_translate("MainWindow", "Yes", None))
        self.YearsNoRadio.setText(_translate("MainWindow", "No", None))
        self.OntologyLabel.setText(_translate("MainWindow", "Ontology:", None))
        self.SaveMapperBtn.setText(_translate("MainWindow", "Save", None))
        self.UpdateDomainLabel.setText(_translate("MainWindow", "Add/Edit Domain", None))
        self.DomainsListLabel.setText(_translate("MainWindow", "Domains:", None))
        self.ShowDomainBtn.setText(_translate("MainWindow", "Show", None))
        self.DomainNameLabel.setText(_translate("MainWindow", "Domain:", None))
        self.AddDomainMappersLabel.setText(_translate("MainWindow", "Mappers:", None))
        self.SaveDomainBtn.setText(_translate("MainWindow", "Save", None))
        self.label_10.setText(_translate("MainWindow", "Check Existence of Ontology", None))
        self.CheckOntologyLabel.setText(_translate("MainWindow", "Ontology:", None))
        self.CheckBtn.setText(_translate("MainWindow", "Check", None))
        self.ResultLabel.setText(_translate("MainWindow", "Result:", None))
        self.CheckOntologyLanguageCombo.setToolTip(_translate("MainWindow", "Enter Language of wiki pages", None))
        self.CheckOntologyLanguageLabel.setText(_translate("MainWindow", "Language :", None))
        self.ResourcesListLabel.setText(_translate("MainWindow", "List of Resources in a Domain", None))
        self.DomainLabel.setText(_translate("MainWindow", "Domain:", None))
        self.DomainLanguageLabel.setText(_translate("MainWindow", "Language :", None))
        self.ShowResourcesBtn.setText(_translate("MainWindow", "Show Resources", None))
        self.DomainLanguageCombo.setToolTip(_translate("MainWindow", "Enter Language of wiki pages", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

