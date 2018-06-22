import sys
from gui import guiLayout
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import settings
import subprocess
import domainExtractor
import Utilities
import json
from collections import OrderedDict


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

		self.custom_mappers = Utilities.Utilities.load_custom_mappers()
		self.static_mappers = [ "FILMOGRAPHY", "DISCOGRAPHY", "CONCERT_TOURS",
            "STAFF", "HONORS", "CONTRIBUTORS","OTHER_LITERATURE_DETAILS"]
		self.domains = Utilities.Utilities.load_settings()

		self.refresh_mappers_list()

		self.ui.ListOfMappersCombo.setDuplicatesEnabled(False)

		self.extractor_checkBoxes = [self.ui.extractor_checkBox_1, self.ui.extractor_checkBox_2, self.ui.extractor_checkBox_3,
										self.ui.extractor_checkBox_4, self.ui.extractor_checkBox_5, self.ui.extractor_checkBox_6]

		self.refresh_domains_list()

		self.ui.ExploreBtn.clicked.connect(self.exploreDomain)
		self.ui.saveBtn.clicked.connect(self.saveDomainSettingsFile)
		self.ui.ExtractBtn.clicked.connect(self.extractTriples)
		self.ui.ShowMappersBtn.clicked.connect(self.showMappers)
		self.ui.SaveMapperBtn.clicked.connect(self.updateMapper)
		self.ui.ShowDomainBtn.clicked.connect(self.showDomain)
		self.ui.SaveDomainBtn.clicked.connect(self.updateDomain)
		self.ui.CheckBtn.clicked.connect(self.checkOntology)

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

	def showMappers(self):
		mapper = str(self.ui.ListOfMappersCombo.currentText())
		current_mapper = self.custom_mappers[mapper]

		self.ui.MapperNameLineEdit.setText(mapper)
		self.ui.ListHeadersTextEdit.setText(json.dumps(current_mapper['list_headers'], indent = 2))
		self.ui.TableSectionsTextEdit.setText(json.dumps(current_mapper['table_sections'], indent = 2))

		extractors = current_mapper['extractors']

		for extractor in extractors:
			self.extractor_checkBoxes[extractor-1].setChecked(True)

		if current_mapper['years'] == 'Yes':
			self.ui.YearsYesRadio.setChecked(True)
		else:
			self.ui.YearsNoRadio.setChecked(True)

		self.ui.OntologyTextEdit.setText(json.dumps(current_mapper['ontology'], indent = 2))

	def updateMapper(self):
		mapper_function = OrderedDict()
		mapper_name = str(self.ui.MapperNameLineEdit.text())
		list_headers = json.loads(str(self.ui.ListHeadersTextEdit.toPlainText()))
		table_sections = json.loads(str(self.ui.TableSectionsTextEdit.toPlainText()))

		extractors=[]
		i=1
		for extractor in self.extractor_checkBoxes:
			if extractor.isChecked():
				extractors.append(i)
			i+=1

		if self.ui.YearsYesRadio.isChecked():
			years = 'Yes'
		else:
			years = 'No'

		ontology = json.loads(str(self.ui.OntologyTextEdit.toPlainText()))

		mapper_function['table_sections'] = table_sections
		mapper_function['list_headers'] = list_headers
		mapper_function['extractors'] = extractors
		mapper_function['ontology'] = ontology
		mapper_function['years'] = years

		self.dump_custom_mappers(mapper_name, mapper_function)

		self.refresh_mappers_list()

	def dump_custom_mappers(self, mapper_name, mapper_function):
		''' This method saves the modified custom mappers into the ``custom_mappers.json`` file and \
		makes a call to ``load_custom_mappers()`` and ``merge_mappers()`` to reload the ``custom_mappers`` \
		file to reflect updated changes.

		:param mapper_name: the mapper function name to be saved.
		:param mapper_function: the mapper function dict, containing settings related to the mapper function.

		:return: void.
		'''
		self.custom_mappers[mapper_name] = mapper_function
		custom_mappers_file = open("custom_mappers.json", "w+")
		custom_mappers_file.write(json.dumps(self.custom_mappers, indent = 4))  #save the new mapper function on file
		custom_mappers_file.close()
		self.custom_mappers = Utilities.Utilities.load_custom_mappers() #reload the mapper functions file in the memory
		return

	def dump_settings(self, new_settings):
		''' This method save the modified settings into the ``setting.json`` file and makes call to \
		``load_settings()`` which reloads the settings file to reflect the updated changes.

		:param new_settings: the updated settings dict to be saved.

		:return: void.
		'''
		settings_file = open("configs.json", "w+")
		settings={}
		settings['MAPPING'] = new_settings
		settings_file.write(json.dumps(settings, indent = 4)) #saves/updates the existing settings
		settings_file.close()
		self.domains = Utilities.Utilities.load_settings() #reload the saved settings into the memory
		return

	def refresh_mappers_list(self):
		self.ui.ListOfMappersCombo.clear()
		for mapper in self.custom_mappers:
			self.ui.ListOfMappersCombo.addItem(mapper)

	def refresh_domains_list(self):
		self.ui.DomainsListCombo.clear()
		for domain in self.domains:
			self.ui.DomainsListCombo.addItem(domain)

	def showDomain(self):
		domain = str(self.ui.DomainsListCombo.currentText())
		self.ui.DomainNameLineEdit.setText(domain)

		self.mapperListModel = QStandardItemModel()
		all_mappers = self.custom_mappers.keys() + self.static_mappers
		for mapper in all_mappers:
			item = QStandardItem(mapper)
			item.setEditable(False)
			if mapper in self.domains[domain]:
				item.setCheckState(Qt.Checked)
			else:
				item.setCheckState(Qt.Unchecked)
			item.setCheckable(True)
			self.mapperListModel.appendRow(item)
		self.ui.MappersListView.setModel(self.mapperListModel)

	def updateDomain(self):
		domain = str(self.ui.DomainNameLineEdit.text())

		model = self.ui.MappersListView.model()
		mappers=[]
		for index in range(model.rowCount()):
			item = model.item(index)
			if item.checkState() == QtCore.Qt.Checked:
				mappers.append(str(item.text()))

		self.domains[domain] = mappers
		self.dump_settings(self.domains)
		self.refresh_domains_list()

	def checkOntology(self):
		ontology = str(self.ui.CheckOntologyField.text())
		language = "en"

		query = settings.SPARQL_CHECK_PROPERTY[0] +\
				'{' + settings.SPARQL_CHECK_PROPERTY[1] + '"' + ontology + '"@' + language + "} UNION " +\
				'{' + settings.SPARQL_CHECK_PROPERTY[1] + '"' + ontology.lower() + '"@' + language + "}" +\
				settings.SPARQL_CHECK_PROPERTY[2]
		utils = Utilities.Utilities(language, None, None)
		utils.language = "en"
		utils.dbpedia_sparql_url = utils.dbpedia_selection()
		url = utils.url_composer(query, "dbpedia")
		answer = utils.json_answer_getter(url)
		print(answer)


if __name__ == '__main__':
    extractor = guiExtractor()