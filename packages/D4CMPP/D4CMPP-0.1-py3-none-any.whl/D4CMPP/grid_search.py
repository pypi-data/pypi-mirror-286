import yaml
import os
import traceback
from src.utils import argparser
from src.utils import PATH
from src import DataManager, NetworkManager, TrainManager, PostProcessor
import itertools

from main import run, set_config

def gridsearch(param_grid):
    keys, values = zip(*param_grid.items())
    
    for v in itertools.product(*values):
        yield dict(zip(keys, v))

config0 = {
    "data": None,
    "target": [],
    "network": None,

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.001,
    "weight_decay": 0.0005,
    "lr_patience": 40,
    "early_stopping_patience": 100,

    "device": "cuda:0",
    "pin_memory": False,

}

hyperparameters = {
    "sculptor_index":[[4,0,0],[6,2,0],[9,5,6]],
    "hidden_dim": [64, 128, 256],
    "conv_layers": [4, 6, 8],
    "linear_layers": [2, 4,],
}

def grid_search(hyperparameters, **kwargs):
    config0.update(kwargs)
    config = set_config(config0)

    for i,hp in enumerate(gridsearch(hyperparameters)):
        try:
            _config = config.copy()
            _config.update(hp)
            grid_id = ""
            for key in hp.keys():
                grid_id += f"_{key},{hp[key]}"
            _config['MODEL_PATH'] = _config['MODEL_PATH'] + grid_id
            
            run(_config)
        except:
            print(traceback.format_exc())
            continue


if __name__ == "__main__":
    grid_search(hyperparameters,config0)