import yaml
import os
import traceback
import importlib
from src.utils import argparser
from src.utils import PATH
from src.PostProcessor import PostProcessor

from main import run

config0 = {
    # "data": 'HOMOLUMO_final',
    # "target": ['HOMO'],
    # "transfer": 'GCNwithSolv_model_DLOS_Abs_20240617_101423',
    # 'network': 'GCNwS',

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.001,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'lr_dict': {
        'GCNs': 0.0001,
    }
}


def transfer_learn(use_argparser=False,**kwargs):
    config = config0.copy()
    config.update(kwargs)
    if use_argparser:
        args = argparser.parse_args(transfer_learn=True)
        config.update(vars(args))
    config = {k: v for k, v in config.items() if v is not None}

    PATH.init_path(config)

    config['transfer'] = PATH.find_model_path(config['transfer'],config)
    if config.get('network', None):
        with open(config['NET_REFER'], "r") as file:
            network_refer = yaml.safe_load(file)[config['network']]
        config.update(network_refer)

    with open(config['transfer']+'/config.yaml', "r") as file:
        _config = yaml.safe_load(file)
    _config['LOAD_PATH'] = config['transfer']
    _config.update(config)
    config = _config
    config['MODEL_PATH'] = PATH.get_model_path(config)

    run(config, transfer_learn=True)


if __name__ == "__main__":
    transfer_learn(use_argparser=True, **config0)