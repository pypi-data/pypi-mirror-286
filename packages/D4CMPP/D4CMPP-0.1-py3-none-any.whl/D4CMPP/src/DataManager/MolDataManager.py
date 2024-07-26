import os
import pandas as pd
import numpy as np
from tqdm import tqdm

import torch
from torch.utils.data import Dataset, DataLoader
from dgl.data.utils import save_graphs, load_graphs
from sklearn.model_selection import train_test_split

from .GraphGenerator.MolGraphGenerator import MolGraphGenerator
from .Dataset.GraphDataset import GraphDataset, GraphDataset_withSolv

from src.utils.scaler import Scaler

import hashlib


class MolDataManager:
    def __init__(self, config):
        self.config = config
        self.data = config["data"]
        self.target = config["target"]
        self.scaler = Scaler(config.get("scaler","identity"))
        self.molecule_columns = ['compound']
        self.molecule_smiles = {}
        self.molecule_graphs = {}
        self.valid_smiles = {}
        self.random_seed = config.get("random_seed",42)
        self.set = None

        self.import_others()
        config.update({"node_dim":self.gg.node_dim, "edge_dim":self.gg.edge_dim})

    def import_others(self):
        self.graph_type = 'mol'
        self.gg =MolGraphGenerator()
        self.dataset =GraphDataset
        self.unwrapper = self.dataset.unwrapper

    def init_temp_data(self,smiles_list):
        self.molecule_smiles['compound'] = np.array(smiles_list)
        self.target_value = np.zeros((len(smiles_list),self.config["target_dim"]))
        self.gg.verbose= False
        self.generate_graph('compound')
        return self.valid_smiles

    def init_data(self):
        self.load_data()
        self.prepare_graph()

    def load_csv(self):
        try:
            self.df = pd.read_csv(os.path.join(self.config['DATA_PATH']),encoding='utf-8')
        except:
            try:
                self.df = pd.read_csv(os.path.join(self.config['DATA_PATH']),encoding='cp949')
            except:
                self.df = pd.read_csv(os.path.join(self.config['DATA_PATH']),encoding='euc-kr')

    def load_data(self):
        self.load_csv()
        for col in self.molecule_columns:
            if col in self.df.columns:
                self.molecule_smiles[col] = np.array(list(self.df[col]))
            else:
                raise ValueError(f"{col} is not in the dataframe")
        if torch.tensor(self.df[self.target].values).dim() == 1:
            self.target_value = self.scaler.fit_transform(torch.tensor(self.df[self.target].values).float().unsqueeze(1))
        else:
            self.target_value = self.scaler.fit_transform(torch.tensor(self.df[self.target].values).float())
        self.config.update({"target_dim":self.target_value.shape[1]})
        self.set = self.df.get("set",None)

    def prepare_graph(self):
        for col in self.molecule_columns:
            if os.path.exists(os.path.join(self.config['GRAPH_PATH'],self.data+"_"+col+"_"+self.graph_type+".bin")):
                self.load_graphs(col)
            else:
                self.generate_graph(col)
                self.save_graphs(col)

    def generate_graph(self,col,graphs=None):
        self.molecule_graphs[col] = []
        self.valid_smiles[col] = []
        invalids = []
        if graphs is not None:
            for smi,g in zip(self.molecule_smiles[col],graphs):
                self.molecule_graphs[col].append(g)
                self.valid_smiles[col].append(smi)
            return
        for smi in tqdm(self.molecule_smiles[col],desc=f"Generating {col} graphs"):
            graphgenerator = self.gg
            if col == 'solvent' and hasattr(self,'gg_solv'):
                graphgenerator = self.__getattribute__('gg_solv')
            else:
                graphgenerator = self.gg
            try:
                g=graphgenerator.get_graph(smi)
            except Exception as e:
                g = graphgenerator.get_empty_graph()
                invalids.append(pd.DataFrame({'smiles':[smi],'type':[col],'reason':[str(e)]}))

            if g.number_of_nodes()>0:
                self.valid_smiles[col].append(smi)
            self.molecule_graphs[col].append(g)
        if len(invalids)>0:
            invalids = pd.concat(invalids)
            invalids.to_csv("graph_error.csv",index=False)
        
    def save_graphs(self,col):
        hash_smiles = torch.tensor([hash(smi) for smi in self.molecule_smiles[col]])
        save_graphs(os.path.join(self.config['GRAPH_PATH'],self.data+"_"+col+"_"+self.graph_type+".bin"), self.molecule_graphs[col],{'smiles':hash_smiles})

    def load_graphs(self,col):
        self.molecule_graphs[col],molecule_smiles= load_graphs(os.path.join(self.config['GRAPH_PATH'],self.data+"_"+col+"_"+self.graph_type+".bin"))
        if len(self.molecule_graphs[col]) != len(self.molecule_smiles[col]):    
            raise ValueError("Graphs and smiles are not matched")
        for i in range(len(self.molecule_graphs[col])):
            if hash(self.molecule_smiles[col][i]) != int(molecule_smiles['smiles'][i]):
                print(hash(self.molecule_smiles[col][i]),int(molecule_smiles['smiles'][i]), self.molecule_smiles[col][i])
                raise ValueError("Graphs and smiles are not matched")


    def drop_none_graph(self):
        _masks = []
        for col in self.molecule_columns:
            _masks.append([g.number_of_nodes()>0 for g in self.molecule_graphs[col]])
        mask = np.all(_masks,axis=0)
        self.masking(mask)

    def drop_nan_value(self):
        mask = np.array(~torch.isnan(torch.tensor(self.target_value)).all(dim=1))
        self.masking(mask)

    def masking(self,mask):
        self.target_value = self.target_value[mask]
        if self.set is not None:
            self.set = self.set[mask]
        for col in self.molecule_columns:
            self.molecule_smiles[col] = self.molecule_smiles[col][mask]
            self.molecule_graphs[col] = [g for i,g in enumerate(self.molecule_graphs[col]) if mask[i]]

    def prepare_dataset(self,temp=False):
        self.drop_none_graph()
        if not temp:
            self.drop_nan_value()
        self.whole_dataset = self.init_dataset()

    def init_dataset(self):
        return self.dataset(self.molecule_graphs['compound'], self.target_value, self.molecule_smiles['compound'])
        
    def split_data(self):
        if self.set is None:
            train_dataset, test_dataset = train_test_split(self.whole_dataset, test_size=0.1, random_state=self.random_seed)
            train_dataset, val_dataset = train_test_split(train_dataset, test_size=1/9, random_state=self.random_seed)
            self.train_dataset, self.val_dataset, self.test_dataset = self.dataset(),self.dataset(),self.dataset()
            self.train_dataset.reload(list(zip(*train_dataset)))
            self.val_dataset.reload(list(zip(*val_dataset)))
            self.test_dataset.reload(list(zip(*test_dataset)))
        else:
            import copy
            self.train_dataset,self.val_dataset,self.test_dataset = copy.deepcopy(self.whole_dataset),copy.deepcopy(self.whole_dataset),copy.deepcopy(self.whole_dataset)
            
            self.train_dataset.subDataset([i for i,s in enumerate(self.set) if s=="train"])
            self.val_dataset.subDataset([i for i,s in enumerate(self.set) if s=="val"])
            self.test_dataset.subDataset([i for i,s in enumerate(self.set) if s=="test"])
        print(f"Train: {len(self.train_dataset)}, Val: {len(self.val_dataset)}, Test: {len(self.test_dataset)}")
    
    def init_Dataloader(self,set=None,partial_train=None, shuffle=None):
        if set=="train":
            if partial_train and partial_train<1.0:
                self.train_dataset.subDataset(np.random.choice(len(self.train_dataset),int(len(self.train_dataset)*partial_train),replace=False))
                print(f"Partial Training: {len(self.train_dataset)}")
            elif partial_train and partial_train>1:
                self.train_dataset.subDataset(np.random.choice(len(self.train_dataset),partial_train,replace=False))
                print(f"Partial Training: {len(self.train_dataset)}")
            dataset = self.train_dataset
            shuffle = self.config.get('shuffle',True) if shuffle is None else shuffle
        elif set=="val":
            dataset = self.val_dataset
            shuffle = False
        elif set=="test":
            dataset = self.test_dataset
            shuffle = False
        else:
            dataset = self.whole_dataset
            shuffle = False

        return DataLoader(dataset, 
                        batch_size=self.config.get('batch_size',32), 
                        shuffle=shuffle,
                        collate_fn=self.dataset.collate, 
                        pin_memory=self.config.get('pin_memory',True),
                        num_workers=self.config.get('num_workers',0))

    def get_Dataloaders(self, temp=False):
        self.prepare_dataset(temp=temp)

        if temp:
            loader = self.init_Dataloader(shuffle=False)
            return loader
        else:
            self.split_data()
            self.train_loader = self.init_Dataloader("train",partial_train=self.config.get('partial_train',1.0))
            self.val_loader = self.init_Dataloader("val")
            self.test_loader = self.init_Dataloader("test")

            return self.train_loader, self.val_loader, self.test_loader
  

class MolDataManager_withSolv(MolDataManager):
    def __init__(self, config):
        super(MolDataManager_withSolv, self).__init__(config)
        self.molecule_columns.append('solvent')

    def import_others(self):
        self.graph_type = 'mol'
        self.gg =MolGraphGenerator()
        self.gg_solv =MolGraphGenerator()
        self.dataset =GraphDataset_withSolv
        self.unwrapper = self.dataset.unwrapper
        
    def init_temp_data(self,smiles,solvents):
        self.molecule_smiles['compound'] = np.array(smiles)
        self.molecule_smiles['solvent'] = np.array(solvents)
        self.target_value = np.zeros((len(smiles),self.config["target_dim"]))
        self.gg.verbose= False
        self.generate_graph('compound')
        self.generate_graph('solvent')
        return self.valid_smiles

    def init_dataset(self):
        return self.dataset(self.molecule_graphs['compound'], self.molecule_graphs['solvent'], self.target_value, self.molecule_smiles['compound'], self.molecule_smiles['solvent'])
    
def hash(s):
    md5_hash = hashlib.md5()
    md5_hash.update(s.encode('utf-8'))
    hex_digest = md5_hash.hexdigest()
    decimal_hash = int(hex_digest, 16) % (10**12+7)
    
    return decimal_hash
