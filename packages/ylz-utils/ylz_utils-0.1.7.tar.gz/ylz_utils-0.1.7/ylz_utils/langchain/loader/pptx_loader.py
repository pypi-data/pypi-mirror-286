from langchain_community.document_loaders import UnstructuredPowerPointLoader

class PptxLoader():
    @classmethod
    def loader(cls, filename: str):
        #"./example_data/fake-power-point.pptx"
        return UnstructuredPowerPointLoader(filename)
