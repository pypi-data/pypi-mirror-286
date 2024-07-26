import DLOS

configs = [
    {
    "data": "HOMOLUMO_final",
    "target": ["HOMO_neat"],
    "network": "GCNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["HOMO_neat"],
    "network": "GATwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["HOMO_neat"],
    "network": "DMPNNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':4,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["HOMO_neat"],
    "network": "MPNNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},
{
    "data": "HOMOLUMO_final",
    "target": ["LUMO_neat"],
    "network": "GCNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["LUMO_neat"],
    "network": "GATwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["LUMO_neat"],
    "network": "DMPNNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':4,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["LUMO_neat"],
    "network": "MPNNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["gap"],
    "network": "GCNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["gap"],
    "network": "GATwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["gap"],
    "network": "DMPNNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':4,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["gap"],
    "network": "MPNNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["gap_neat"],
    "network": "GCNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["gap_neat"],
    "network": "GATwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["gap_neat"],
    "network": "DMPNNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':4,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},

{
    "data": "HOMOLUMO_final",
    "target": ["gap_neat"],
    "network": "MPNNwS",

    "scaler": "standard",
    "optimizer": "Adam",

    "max_epoch": 2000,
    "batch_size": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.0005,
    "lr_patience": 80,
    "early_stopping_patience": 200,
    'min_lr': 1e-6,

    "device": "cuda:0",
    "pin_memory": False,

    'hidden_dim': 256,
    'conv_layers':6,
    'linear_layers': 3,
    'dropout': 0.1,

    'solv_hidden_dim': 64,
    'solv_conv_layers': 4,
    'solv_linear_layers': 2,
},




]

if __name__ == '__main__':
    for config in configs:
        DLOS.main(config, use_argparser=False)