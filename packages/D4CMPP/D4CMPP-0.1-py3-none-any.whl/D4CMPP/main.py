import yaml
import os
import traceback
import importlib
from src.utils import argparser
from src.utils import PATH
from src.PostProcessor import PostProcessor

config0 = {
    "data": None,
    "target": None,
    "network": None,

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 128,
    "learning_rate": 0.001,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-5,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 32,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
}


def train(**kwargs):
    config = set_config(kwargs)
    run(config)

def set_config(kwargs):    
    config = config0.copy()
    config.update(kwargs)
    if kwargs.get('use_argparser',False):
        args = argparser.parse_args()
        config.update(vars(args))   
    config = {k: v for k, v in config.items() if v is not None}

    if config.get('LOAD_PATH',None) is not None:
        config['LOAD_PATH'] = PATH.find_model_path(config['LOAD_PATH'] , config)
        config['MODEL_PATH'] = config['LOAD_PATH']
        _config = yaml.load(open(os.path.join(config['LOAD_PATH'],'config.yaml'), 'r'), Loader=yaml.FullLoader)
        _config.update(config)
        config = _config

    PATH.init_path(config)

    if config.get('LOAD_PATH',None) is None:
        with open(config['NET_REFER'], "r") as file:
            network_refer = yaml.safe_load(file)[config['network']]
        config.update(network_refer)
        config['MODEL_PATH'] = PATH.get_model_path(config)
    PATH.check_path(config)
    return config


def run(config, transfer_learn=False):
    print(config['MODEL_PATH'])
    dm, nm, tm, pp = None, None, None, None
    train_loaders, val_loaders, test_loaders = None, None, None

    try:
        dm = getattr(importlib.import_module("src.DataManager."+config['data_manager_module']),config['data_manager_class'])(config)
        dm.init_data()
        train_loaders, val_loaders, test_loaders = dm.get_Dataloaders()
        
        nm = getattr(importlib.import_module("src.NetworkManager."+config['network_manager_module']),config['network_manager_class'])(config, tf=transfer_learn, unwrapper = dm.unwrapper)

        tm = getattr(importlib.import_module("src.TrainManager."+config['train_manager_module']),config['train_manager_class'])(config)
        tm.train(nm, train_loaders, val_loaders)
    except:
        print(traceback.format_exc())
        return
    if tm.train_error is not None:
        return

    pp = PostProcessor(config)
    pp.postprocess(dm, nm, tm, train_loaders, val_loaders, test_loaders)

if __name__ == "__main__":
    train(**config0, use_argparser=True)