import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import os
from cycler import cycler


plt.style.use('../scripts/default.mplstyle')

plt.rcParams['axes.prop_cycle'] = plt.cycler(cycler(color = ['#CC6677', 
                                    '#332288', 
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


    counter = 0
    for ice in [3, 4]:
        for i,  time in enumerate(np.arange(0, 501, 100)):
            file_name = f"ice{ice}_RDF/RDF_ice{ice}.{time}.txt" 

            data = np.loadtxt(file_name, skiprows=2).T
            log_rdf = np.log10(data[1]) 
            # replacing values of log(rdf == 0) with 0
            idxs = np.where(log_rdf <= -1)
            for idx in idxs:
                log_rdf[idx] = -1
                data[1][idx] = 0.11

            plt.plot(data[0], data[1], label = f"T={time}K")
            #plt.plot(data[0], rdf, label = f"T={time}K")


        plt.xlabel(r"$r$ ($\AA$)")
        plt.ylabel(r"$g(r)$")
        plt.ylim(0.1, 100)
        plt.yscale("log")
        plt.legend(ncols = 2)
        plt.tight_layout()
        plt.savefig(f"RDF_ice{ice}.svg", dpi=300)
        plt.show()

if __name__=="__main__":
    main()