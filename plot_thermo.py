import pickle as pkl
from cycler import cycler
import sys
from os.path import dirname, abspath

import pandas as pd
import matplotlib.pyplot as plt

d = dirname(abspath(__file__))
plt.style.use(d + '/default.mplstyle')

plt.rcParams['axes.prop_cycle'] = plt.cycler(cycler(color = ['#332288', 
                                    '#CC6677',
                                    '#88CCEE',
                                    '#DDCC77', 
                                    '#117733', 
                                    '#882255', 
                                    '#44AA99', 
                                    '#999933', 
                                    '#AA4499',
                                    '#DDDDDD'
                                ]))

def plot(df, y_axis):
    try:
            df.plot(x="Time", y=y_axis)
            plt.show()
    except KeyError:
        print(f"[[ERROR]] KeyError: '{y_axis}' is invalid key. Valid keys are:\n\t {df.columns}")

def main(argv):
    file = sys.argv[-3]
    y_axis  = sys.argv[-2]
    stage = sys.argv[-1]

    with open(file, "rb") as f:
        data = pkl.load(f)

    df_minmize = pd.DataFrame(data = data[0]["data"], columns = data[0]["keywords"])
    df_relax = pd.DataFrame(data = data[1]["data"], columns = data[1]["keywords"])
    df_run = pd.DataFrame(data = data[2]["data"], columns = data[2]["keywords"])

    match stage:
        case "minimize":
            df = pd.DataFrame(data = data[0]["data"], columns = data[0]["keywords"])
            plot(df, y_axis)
        case "relax":
            df = pd.DataFrame(data = data[1]["data"], columns = data[1]["keywords"])
            plot(df, y_axis)
        case "run":
            df = pd.DataFrame(data = data[2]["data"], columns = data[2]["keywords"])
            plot(df, y_axis)
        case _:
            print("Not a valid stage: Please use 'minimize', 'relax', or 'production'")
    
            
if __name__ == '__main__':
    main(sys.argv)