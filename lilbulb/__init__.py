import os
import mimetypes
import uuid
import xml.etree.cElementTree as ET

class DatasetMetadata(object):
    def __init__(self, dataset_version: str = None, publishing_date: str = None, owner: str = None, file_path: str = None, project_name: str = None, linking_models: list = []):
        self.id = None
        self.file_type = None
        self.title = None
        self.file_path = file_path
        self.linking_models = linking_models
        self.project_name = project_name
        self.version = dataset_version
        self.publishing_date = publishing_date
        self.owner = owner

        self._create_from_file()

    def _create_from_file(self):
        file_name, file_extension = os.path.splitext(os.path.basename(self.file_path))

        self.file_type = self._file_usabiltyhub_type(file_extension)
        self.file_mimetype = self._file_mime_type(self.file_path)
        self.id = f"{self.project_name}.qgis_{self.file_type}_{file_name}"
        self.title = f"QGIS {self.file_type} file for {self.project_name} - {file_name}"

    def _file_usabiltyhub_type(self, extension: str = None) -> str:
        if extension == ".qml":
            return "layerstyle"
        if extension == ".yaml":
            return "projecttopping"
        if extension == ".ini":
            return "metaconfig"
        if extension == ".qlr":
            return "layerdefinition"
        if extension in [".xml",".xtf",".itf"]:
            return "referenceData"

    def _file_mime_type(self, file_path: str = None) -> str:
        mimetype = mimetypes.guess_type(file_path)
        if mimetype[0] is None:
            #ugly fallback
            return 'text/plain'
        return mimetype[0]

    def make_xml_element(self, element):

        ET.SubElement(element, "id").text = self.id
        ET.SubElement(element, "version").text = self.version
        ET.SubElement(element, "publishingDate").text = self.publishing_date
        ET.SubElement(element, "owner").text = self.owner

        title = ET.SubElement(element, "title")
        datsetidx16_multilingualtext = ET.SubElement( title, "DatasetIdx16.MultilingualText")
        localisedtext = ET.SubElement( datsetidx16_multilingualtext, "LocalisedText")
        datasetidx16_localisedtext = ET.SubElement( localisedtext, "DatasetIdx16.LocalisedText")
        ET.SubElement( datasetidx16_localisedtext, "Text").text = self.title

        categories = ET.SubElement(element, "categories")
        type_datasetidx16_code = ET.SubElement( categories, "DatasetIdx16.Code_")
        ET.SubElement( type_datasetidx16_code, "value").text = f"http://codes.interlis.ch/type/{self.file_type}"

        if self.file_type in ['metaconfig', 'layerdefinition']:
            for linking_model in self.linking_models:
                linking_model_datasetidx16_code = ET.SubElement( categories, "DatasetIdx16.Code_")
                ET.SubElement( linking_model_datasetidx16_code, "value").text = f"http://codes.interlis.ch/model/{linking_model}"


        files = ET.SubElement(element, "files")
        datsaetidx16_datafile = ET.SubElement( files, "DatasetIdx16.DataFile")
        ET.SubElement( datsaetidx16_datafile, "fileFormat").text = self.file_mimetype
        file = ET.SubElement( datsaetidx16_datafile, "file")
        datsetidx16_file = ET.SubElement( file, "DatasetIdx16.File")
        ET.SubElement( datsetidx16_file, "path").text = self.file_path


def make_ilidata( path: str = ".", project_name: str = None, owner: str = None, dataset_version: str = None, publishing_date: str = None, linking_models: list = []) -> str:

    transfer = ET.Element("TRANSFER", xmlns="http://www.interlis.ch/INTERLIS2.3")

    headersection = ET.SubElement(transfer, "HEADERSECTION", SENDER="signedav's lilbulb", VERSION="2.3")
    models = ET.SubElement(headersection, "MODELS")
    ET.SubElement(models,"MODEL", NAME="DatasetIdx16", VERSION="2018-11-21", URI="mailto:ce@eisenhutinformatik.ch")

    datasection = ET.SubElement(transfer,"DATASECTION")
    data_index = ET.SubElement(datasection,"DatasetIdx16.DataIndex", BID=str(uuid.uuid4()))

    for file_root, dirs, files in os.walk(path):
        for file in files:
            if os.path.basename(file) == "ilidata.xml":
                continue
            file_path =os.path.join(file_root, file)
            dataset_metadata_element = ET.SubElement(data_index, "DatasetIdx16.DataIndex.DatasetMetadata", TID=str(uuid.uuid4()))
            dataset = DatasetMetadata(dataset_version,publishing_date,owner,file_path,project_name,linking_models)
            dataset.make_xml_element(dataset_metadata_element)

    tree = ET.ElementTree(transfer)
    ilidata_path = os.path.join(path,"ilidata.xml")
    ET.indent(tree, space="\t", level=0)
    tree.write(ilidata_path, encoding="utf-8")
    print(f"Created {ilidata_path}")