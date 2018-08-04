import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from gui import guiLayout
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
import staticValues
import subprocess
import domainExtractor
import Utilities
import json
from collections import OrderedDict
from domain_explorer import Selector
from domain_extractor import MapperTools


class Log(object):

    def __init__(self, edit, isStdout):
        """
        This class helps to write stdout, stderr to a textbox.

        :param edit: TextBrowser of the UI.
        :param isStdout: True for Stdout and False for Stderr.
        """
        if isStdout:
            self.out = sys.stdout
        else:
            self.out = sys.stderr
        self.textBrowser = edit

    def write(self, message):
        """
        Writing output messages to console and to the UI.
        :param message: contents to be displayed.
        :return:
        """
        # write to console
        self.out.write(message)
        # write to text browser of the UI.
        self.textBrowser.insertPlainText(message)


class guiExtractor(QMainWindow):
    def __init__(self):
        """
        Initialising all the required variables.
        """
        QMainWindow.__init__(self)
        self.ui = guiLayout.Ui_MainWindow()
        self.ui.setupUi(self)

        # setting stdout to Log object so that when something is written to stdout,
        # write function of Log object is called.
        sys.stdout = Log(self.ui.TerminalWindow, True)
        # setting stderr to Log object so that when something is written to stderr,
        # write function of Log object is called.
        sys.stderr = Log(self.ui.TerminalWindow, False)

        # Setting all the language dropdowns to the available languages.
        for lang in staticValues.LANGUAGES_AVAILABLE:
            self.ui.LanguageCombo.addItem(lang)
            self.ui.DomainLanguageCombo.addItem(lang)
            self.ui.CheckOntologyLanguageCombo.addItem(lang)

        # Load mappers from custom_mappers.json
        self.custom_mappers = Utilities.Utilities.load_custom_mappers()
        self.static_mappers = [ "FILMOGRAPHY", "DISCOGRAPHY", "CONCERT_TOURS",
            "STAFF", "HONORS", "CONTRIBUTORS","OTHER_LITERATURE_DETAILS"]
        # load domain to mappers list from configs.json file
        self.domains = Utilities.Utilities.load_settings()

        self.refresh_mappers_list()

        self.extractor_checkBoxes = [self.ui.extractor_checkBox_1, self.ui.extractor_checkBox_2, self.ui.extractor_checkBox_3,
                                        self.ui.extractor_checkBox_4, self.ui.extractor_checkBox_5, self.ui.extractor_checkBox_6]

        self.refresh_domains_list()

        # linking buttons to their corresponding events
        self.ui.ExploreBtn.clicked.connect(self.exploreDomain)
        self.ui.saveBtn.clicked.connect(self.saveDomainSettingsFile)
        self.ui.ExtractBtn.clicked.connect(self.extractTriples)
        self.ui.ShowMappersBtn.clicked.connect(self.showMappers)
        self.ui.SaveMapperBtn.clicked.connect(self.updateMapper)
        self.ui.ShowDomainBtn.clicked.connect(self.showDomain)
        self.ui.SaveDomainBtn.clicked.connect(self.updateDomain)
        self.ui.CheckBtn.clicked.connect(self.checkOntology)
        self.ui.ShowResourcesBtn.clicked.connect(self.getResourceList)

        header = QTreeWidgetItem(["Section/Header", "Property"])
        self.ui.DomainSettingsTreeWidget.setHeaderItem(header)
        self.ui.DomainSettingsTreeWidget.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.setAttribute(Qt.WA_DeleteOnClose)


    def exploreDomain(self):
        """
        Triggers when explore button is clicked. This method collects all the inputs required
        for executing domain_explorer.py and executes the domain exploring command. The command outputs
        domain_settings.py file. Later the contents of domain_settings.py is shown in the UI.

        :return:
        """

        # get the resource/domain to be explored.
        resource = str(self.ui.ResourceField.text())
        # strip if has any whitespaces.
        resource = resource.strip()
        # get the collect_mode according the radio box selected.
        if self.ui.CollectmodeSBtn.isChecked():
            collect_mode = "s"
        if self.ui.CollectmodeTBtn.isChecked():
            collect_mode = "t"
        # get the language from the text edit
        language = str(self.ui.LanguageCombo.currentText())
        # get what to extract
        if self.ui.listsCheckBox.isChecked():
            toExtractLists = "true"
        else:
            toExtractLists = "false"
        if self.ui.tablesCheckBox.isChecked():
            toExtractTables = "true"
        else:
            toExtractTables = "false"

        self.ui.ExploreDomainMessageLabel.clear()

        # validate the resource string
        if resource is None or resource == "":
            self.ui.ExploreDomainMessageLabel.setText('Error in resource name.')
            self.ui.ExploreDomainMessageLabel.setStyleSheet('color: red')
            return

        if toExtractTables == "false" and toExtractLists == "false":
            self.ui.ExploreDomainMessageLabel.setText('Select tables/lists to extract')
            self.ui.ExploreDomainMessageLabel.setStyleSheet('color: red')
            return

        try:
            # try spawning a new subprocess for executing the command
            proc = subprocess.Popen(['python','domainExplorer.py', collect_mode, resource, language,
                                     "-t", toExtractTables, "-l", toExtractLists],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
            for line in iter(proc.stdout.readline, b''):
                print(line.rstrip())
            proc.wait() # wait for the subprocess to exit
        except Exception as e:
            print(e)
            self.ui.ExploreDomainMessageLabel.setText('Exception during spawning a new process.')
            return

        self.openDomainSettingsFile()

    def openDomainSettingsFile(self):
        """
        This method reads the domain_settings.py file and displays the content in tree format in the GUI.
        :return:
        """

        # get the mappings from domain_settings.py file.
        new_mappings = MapperTools.MapperTools.read_mapping_rules()
        # get the parameters.
        resource, language, collect_mode, resource_file, toExtractTables, toExtractLists = Utilities.Utilities.read_parameters_research()
        self.domainParameters = [resource, language, collect_mode, resource_file, toExtractTables, toExtractLists]

        # clear the tree widget contents.
        self.ui.DomainSettingsTreeWidget.clear()

        if new_mappings:
            # if the file is not empty, display the contents in tree format.
            for mapper, mapping_rules in list(new_mappings.items()):
                root = QTreeWidgetItem(self.ui.DomainSettingsTreeWidget, [mapper])
                for key, value in list(mapping_rules.items()):
                    item = QTreeWidgetItem(root, [key, value])
            # link every item to onDoubleClick event.
            self.ui.DomainSettingsTreeWidget.itemDoubleClicked.connect(self.onDoubleClick)

    def onDoubleClick(self, item, column_number):
        """
        Allow only ontology field to be edited by the user.

        :param item: tree widget item which has been double clicked.
        :param column_number: the column number of the item.
        :return:
        """

        # make it editable only if it is a ontology field, which is column number 1.
        if column_number == 1:
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        else:
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def saveDomainSettingsFile(self):
        """
        This method is triggered when save button is clicked, after appropriate changes by the user.
        It reads the tree widget and prints the contents back to the domain_settings.py file.

        :return:
        """

        # open domain_settings.py file
        with open(staticValues.FILE_PATH_DOMAIN_EXPLORED,'w') as file:
            # write file header
            self.write_file_heading(file)
            # get top level item counts in tree widget
            numberOfTopLevelItems = self.ui.DomainSettingsTreeWidget.topLevelItemCount()
            for i in range(numberOfTopLevelItems):
                # get the parent item
                parent = self.ui.DomainSettingsTreeWidget.topLevelItem(i)
                file.write(parent.text(0) + " = {\n")
                for j in range(parent.childCount()):
                    # get the child item
                    child = parent.child(j)
                    key = child.text(0)
                    value = child.text(1)
                    # write to the file
                    file.write("'" + key + "': '" + value + "'" + ", \n")
                file.write("} \n")
            file.write(staticValues.END_OF_FILE)
            print("domain_settings.py file saved")

    def write_file_heading(self, domain_explored_file):
        """
        Write file heading.
        File heading holds information about user's parameters:
        - coding type.
        - domain explored.
        - chapter, language defined.
        - research type, that can be single resource, sparql where or dbpedia ontology class.
        - resource file, that contains all resources involved in user's research.
        - output format value defined.
        - comments to facilitate user's work.
        :param domain_explored_file: reference to the output file

        :return:
        """
        domain_explored_file.write(staticValues.CODING_DOMAIN + "\n")
        domain_explored_file.write(staticValues.FIRST_COMMENT + "\n")
        domain_explored_file.write(staticValues.DOMAIN_TITLE + ' = "' + self.domainParameters[0] + '" \n')
        domain_explored_file.write(staticValues.CHAPTER + ' = "' + self.domainParameters[1] + '" \n')
        domain_explored_file.write(staticValues.COLLECT_MODE + ' = "' + self.domainParameters[2] + '" \n')
        domain_explored_file.write(staticValues.RESOURCE_FILE + ' = "' + self.domainParameters[3] + '" \n\n')
        domain_explored_file.write(staticValues.TABLES_INCLUDED + ' = "' + self.domainParameters[4] + '" \n')
        domain_explored_file.write(staticValues.LISTS_INCLUDED + ' = "' + self.domainParameters[5] + '" \n')
        domain_explored_file.write(staticValues.COMMENT_SECTION_PROPERTY + "\n\n")
        domain_explored_file.write(staticValues.COMMENT_STRUCTURE + "\n\n")
        domain_explored_file.write(staticValues.COMMENT_FILLED_ELEMENT + "\n\n")

    def extractTriples(self):
        """
        This method is triggered when "extract" button is clicked.
        Calls the domainExtractor's main function for extracting triples.

        :return:
        """

        self.domain_extractor = domainExtractor.main()

    def showMappers(self):
        """
        Get the mapper selected by the user and displays the mapper in the GUI.

        :return:
        """

        # get the mapper from the combo box
        mapper = str(self.ui.ListOfMappersCombo.currentText())
        # get the mapper details
        current_mapper = self.custom_mappers[mapper]
        # clear the message label
        self.ui.UpdateMapperMessageLabel.clear()
        # display the mapper name
        self.ui.MapperNameLineEdit.setText(mapper)
        # display the list headers
        self.ui.ListHeadersTextEdit.setText(json.dumps(current_mapper['list_headers'], indent = 2))
        # display the table sections
        self.ui.TableSectionsTextEdit.setText(json.dumps(current_mapper['table_sections'], indent = 2))
        # get the extractors associated with the mapper
        extractors = current_mapper['extractors']

        # for every extractor mark the checkbox
        for extractor in extractors:
            self.extractor_checkBoxes[extractor-1].setChecked(True)

        if current_mapper['years'] == 'Yes':
            self.ui.YearsYesRadio.setChecked(True)
        else:
            self.ui.YearsNoRadio.setChecked(True)

        # display the ontologies associated with the mapper
        self.ui.OntologyTextEdit.setText(json.dumps(current_mapper['ontology'], indent = 2))

    def updateMapper(self):
        """
        Updates the mapper details edited by the user.

        :return:
        """

        mapper_function = OrderedDict()
        # get mapper name
        mapper_name = str(self.ui.MapperNameLineEdit.text()).strip()
        # validate mapper name
        if mapper_name == None or mapper_name == "":
            self.ui.UpdateMapperMessageLabel.setText("Mapper Name is Null/Empty")
            self.ui.UpdateMapperMessageLabel.setStyleSheet('color: red')
            return

        # get the list headers from the text edit and check if it is in valid json format or not.
        try:
            list_headers = json.loads(str(self.ui.ListHeadersTextEdit.toPlainText()))
        except ValueError:
            self.ui.UpdateMapperMessageLabel.setText("List Headers are not in JSON format.")
            self.ui.UpdateMapperMessageLabel.setStyleSheet('color: red')
            return

        # get the table sections from the text edit and check if it is in valid json format or not.
        try:
            table_sections = json.loads(str(self.ui.TableSectionsTextEdit.toPlainText()))
        except ValueError:
            self.ui.UpdateMapperMessageLabel.setText("table sections are not in JSON format.")
            self.ui.UpdateMapperMessageLabel.setStyleSheet('color: red')
            return

        # get the selected extractors
        extractors=[]
        i=1
        for extractor in self.extractor_checkBoxes:
            if extractor.isChecked():
                extractors.append(i)
            i+=1

        # get the "include years" radio box
        if self.ui.YearsYesRadio.isChecked():
            years = 'Yes'
        else:
            years = 'No'

        # get the ontology mappings from the text edit and check if it is in valid json format or not.
        try:
            ontology = json.loads(str(self.ui.OntologyTextEdit.toPlainText()))
        except ValueError:
            self.ui.UpdateMapperMessageLabel.setText("Ontology is not in JSON format.")
            self.ui.UpdateMapperMessageLabel.setStyleSheet('color: red')
            return

        mapper_function['table_sections'] = table_sections
        mapper_function['list_headers'] = list_headers
        mapper_function['extractors'] = extractors
        mapper_function['ontology'] = ontology
        mapper_function['years'] = years

        # overwrite the mappers with the updated one
        self.dump_custom_mappers(mapper_name, mapper_function)

        # refresh mappers list present elsewhere in the GUI
        self.refresh_mappers_list()
        self.ui.UpdateMapperMessageLabel.setText("Changes Saved.")
        self.ui.UpdateMapperMessageLabel.setStyleSheet('color: green')

    def dump_custom_mappers(self, mapper_name, mapper_function):
        """
        This method saves the modified custom mappers into the ``custom_mappers.json`` file and \
        makes a call to ``load_custom_mappers()`` and ``merge_mappers()`` to reload the ``custom_mappers`` \
        file to reflect updated changes.

        :param mapper_name: the mapper function name to be saved.
        :param mapper_function: the mapper function dict, containing settings related to the mapper function.

        :return: void.
        """

        self.custom_mappers[mapper_name] = mapper_function
        custom_mappers_file = open("custom_mappers.json", "w+")
        custom_mappers_file.write(json.dumps(self.custom_mappers, indent = 4))  #save the new mapper function on file
        custom_mappers_file.close()
        self.custom_mappers = Utilities.Utilities.load_custom_mappers() #reload the mapper functions file in the memory
        return

    def dump_settings(self, new_settings):
        """
        This method save the modified settings into the ``setting.json`` file and makes call to \
        ``load_settings()`` which reloads the settings file to reflect the updated changes.

        :param new_settings: the updated settings dict to be saved.

        :return: void.
        """

        settings_file = open("configs.json", "w+")
        settings={}
        settings['MAPPING'] = new_settings
        settings_file.write(json.dumps(settings, indent = 4)) #saves/updates the existing settings
        settings_file.close()
        self.domains = Utilities.Utilities.load_settings() #reload the saved settings into the memory
        return

    def refresh_mappers_list(self):
        """
        reload the mappers and diaplay them.

        :return:
        """
        self.ui.ListOfMappersCombo.clear()
        for mapper in self.custom_mappers:
            self.ui.ListOfMappersCombo.addItem(mapper)

    def refresh_domains_list(self):
        """
        reload the domains list and display them

        :return:
        """
        self.ui.DomainsListCombo.clear()
        for domain in self.domains:
            self.ui.DomainsListCombo.addItem(domain)

    def showDomain(self):
        """
        Display the mappers associated with the given domain.

        :return:
        """

        # get the domain name
        domain = str(self.ui.DomainsListCombo.currentText())
        self.ui.DomainNameLineEdit.setText(domain)

        self.ui.UpdateDomainMessageLabel.clear()

        self.mapperListModel = QStandardItemModel()
        # get all the mappers list
        all_mappers = list(self.custom_mappers.keys()) + self.static_mappers
        # keep only the associated mappers in check state.
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
        """
        After user edits the mappings associated with the domain, sve them in the original file.

        :return:
        """

        # get domain name
        domain = str(self.ui.DomainNameLineEdit.text()).strip()

        # validate domain name
        if domain == None or domain == "":
            self.ui.UpdateDomainMessageLabel.setText('Domain name is null/empty.')
            self.ui.UpdateDomainMessageLabel.setStyleSheet('color: red')
            return

        # get mappers list
        model = self.ui.MappersListView.model()
        mappers=[]
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.checkState() == Qt.Checked:
                mappers.append(str(item.text()))

        self.domains[domain] = mappers
        # update the configs.json file
        self.dump_settings(self.domains)
        # refresh all the domains list wherever present in the GUI
        self.refresh_domains_list()
        self.ui.UpdateDomainMessageLabel.setText('Changes Saved.')
        self.ui.UpdateDomainMessageLabel.setStyleSheet('color: green')

    def checkOntology(self):
        """
        check if an ontology id a valid Dbpedia ontology or not.

        :return:
        """

        # get ontology
        ontology = str(self.ui.CheckOntologyField.text())
        # get language
        language = str(self.ui.CheckOntologyLanguageCombo.currentText())
        # validate ontology
        if ontology == "" :
            message = "Ontology cannot be empty"
            color = 'red'
            self.ui.CheckOntologyResult.setText(message)
            self.ui.CheckOntologyResult.setStyleSheet('color: ' + color)
            return

        # create utils instance
        utils = Utilities.Utilities(language, None, None, True)
        # query sparql endpoint
        query = staticValues.SPARQL_CHECK_IN_ONTOLOGY[0] + ontology + staticValues.SPARQL_CHECK_IN_ONTOLOGY[1]
        url = utils.url_composer(query, "dbpedia")
        # get response of request
        response = utils.json_answer_getter(url)['boolean']
        # if property isn't defined in ontology, i delete it
        if not response:
            message = "Property doesn't exist in dbpedia ontology."
            color='red'
        else:
            message = "Property exists"
            color = 'green'
        self.ui.CheckOntologyResult.setText(message)
        self.ui.CheckOntologyResult.setStyleSheet('color: '+color)

    def getResourceList(self):
        """
        Get all the resources associated with a particular domain and display them.

        :return:
        """

        # get domain name
        domain = str(self.ui.DomainLineEdit.text())
        # get language
        language = str(self.ui.DomainLanguageCombo.currentText())
        # validate domain name
        if domain == "" :
            self.ui.ResourcesListResult.setText("Domain cannot be empty!")
            return

        # create an utils instance
        utils = Utilities.Utilities(language, domain, 't', True)
        selector = Selector.Selector(utils)

        if selector.tot_res_interested > 0:
            selector.collect_resources()
            uri_resource_file = selector.res_list_file
            # open file containing the resources list
            contents = open(uri_resource_file).read().split('\n')
            contents = contents[:-1]

            self.resourcesListModel = QStandardItemModel()
            # display the contents
            for content in contents:
                item = QStandardItem(content)
                item.setEditable(False)
                self.resourcesListModel.appendRow(item)
            self.ui.ResoucesListView.setModel(self.resourcesListModel)
            self.ui.ResourcesListResult.setText("Total resources found: "+str(selector.tot_res_interested))


        else:
            self.ui.ResourcesListResult.setText("No resources found.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = guiExtractor()
    MainWindow.show()
    sys.exit(app.exec_())