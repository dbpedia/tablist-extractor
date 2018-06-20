import sys
from gui import guiLayout
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import settings
import subprocess
import domainExtractor

class Log(object):
    def __init__(self, edit, isStdout):
    	if isStdout:
        	self.out = sys.stdout
        else:
        	self.out = sys.stderr
        self.textBrowser = edit

	def __del__(self):
		# Restore sys.stdout
		if isStdout:
			sys.stdout = sys.__stdout__
		else:
			sys.stderr = sys.__stderr__
    def write(self, message):
        self.out.write(message)
        self.textBrowser.insertPlainText(message)

class guiExtractor:
	def __init__(self):
		app = QtGui.QApplication(sys.argv)
		MainWindow = QtGui.QMainWindow()
		self.ui = guiLayout.Ui_MainWindow()
		self.ui.setupUi(MainWindow)

		sys.stdout = Log(self.ui.TerminalWindow, True)
		sys.stderr = Log(self.ui.TerminalWindow, False)

		for lang in settings.LANGUAGES_AVAILABLE:
			self.ui.LanguageCombo.addItem(lang)

		self.ui.ExploreBtn.clicked.connect(self.exploreDomain)
		self.ui.saveBtn.clicked.connect(self.saveDomainSettingsFile)
		self.ui.ExtractBtn.clicked.connect(self.extractTriples)

		MainWindow.show()
		sys.exit(app.exec_())

	def exploreDomain(self):
		
		resource = str(self.ui.ResourceField.text())
		if self.ui.CollectmodeSBtn.isChecked():
			collect_mode = "s"
		if self.ui.CollectmodeTBtn.isChecked():
			collect_mode = "t"
		language = str(self.ui.LanguageCombo.currentText())

		try:
			proc = subprocess.Popen(['python','domainExplorer.py', collect_mode, resource, language], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
			# while proc.poll() is None:
			# 	l = proc.stdout.readline().rstrip() # This blocks until it receives a newline.
			# 	if not l:
			# 		break
			# 	print(l)
			for line in iter(proc.stdout.readline, b''):
				print line.rstrip()
			proc.wait() # wait for the subprocess to exit
		except Exception as e:
			print(e)
			sys.exit(0)

		self.openDomainSettingsFile()

	def openDomainSettingsFile(self):
		with open(settings.FILE_PATH_DOMAIN_EXPLORED,'r') as file:
			data = file.read()
			self.ui.textEdit.setText(data)

	def saveDomainSettingsFile(self):
		data = self.ui.textEdit.toPlainText()
		with open(settings.FILE_PATH_DOMAIN_EXPLORED,'w') as file:
			file.write(data)
		print("domain_settings.py file saved")

	def extractTriples(self):
		self.domain_extractor = domainExtractor.main()

if __name__ == '__main__':
    extractor = guiExtractor()