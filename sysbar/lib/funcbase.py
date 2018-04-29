import os
class SbFuncBase():

    def check_directory(self, directory, dirFile):
        caminho = os.path.abspath('..') + directory
        if not os.path.exists(caminho):
            os.makedirs(caminho)
        
        arquivo = caminho + dirFile
        if not os.path.exists(arquivo):
            return False
        return True