import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import os
from cycler import cycler


plt.style.use('../scripts/default.mplstyle')

plt.rcParams['axes.prop_cycle'] = plt.cycler(cycler(color = [
                                    '#332288', 
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

def main():
    # change working director to that of file
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    for ice in [3, 4]:
        file_name = f"ice{ice}/O-H_bonds.txt" 
        n_bonds, T, _ = np.loadtxt(file_name, skiprows=2).T

        plt.plot(T, n_bonds)

        plt.xlabel(r"Temperature (K)")
        plt.ylabel(r"Num. O-H Bonds")
        plt.tight_layout()
        plt.savefig(f"OH_bonds_{ice}.svg", dpi=300)
        plt.clf()
        #plt.show()

if __name__=="__main__":
    main()