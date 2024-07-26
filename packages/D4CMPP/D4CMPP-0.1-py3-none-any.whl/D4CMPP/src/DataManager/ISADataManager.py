from .MolDataManager import MolDataManager
from src.utils import PATH

from .GraphGenerator.ISAGraphGenerator import ISAGraphGenerator
from .Dataset.ISAGraphDataset import ISAGraphDataset

class ISADataManager(MolDataManager):
    def import_others(self):
        sculptor_index = self.config.get('sculptor_index',[6,1,0])
        self.graph_type = 'img'+str(sculptor_index[0])+str(sculptor_index[1])+str(sculptor_index[2])
        self.gg = ISAGraphGenerator(
            self.config.get('frag_ref',self.config['FRAG_REF']),
            sculptor_index
        )
        self.dataset =ISAGraphDataset
        self.unwrapper = self.dataset.unwrapper