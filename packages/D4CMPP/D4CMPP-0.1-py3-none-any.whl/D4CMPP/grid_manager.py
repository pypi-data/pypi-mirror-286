import pandas as pd
import os
import re
import shutil
import argparse


def clear_grids(base):

    targets = []
    for i in os.listdir('_Models/'):
        if len(re.findall(base+"_",i)):
            targets.append(i)

    min_mae= 999
    for i in targets:
        try:
            metric = pd.read_csv('_Models/'+i+'/metrics.csv')
            if min_mae > metric.loc[0,'val_mae']:
                min_mae = metric.loc[0,'val_mae']
                min_model = i
        except:
            pass

    for i in targets:
        if i!=min_model:
            if os.path.isdir('_Models/'+i):
                shutil.rmtree('_Models/'+i,)
                print(i)

    if not os.path.isdir('_Models/grid_searched/'):
        os.mkdir('_Models/grid_searched/')
    shutil.move('_Models/'+min_model, '_Models/grid_searched/'+min_model)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--model", help="Model to be cleared")

    args = parser.parse_args()
    if args.model:
        base = args.mode
    else:
        raise ValueError("Please provide the model name")
    clear_grids(base)