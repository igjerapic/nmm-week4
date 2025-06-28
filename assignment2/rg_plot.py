import numpy as np
import beadspring as bsa
import MDAnalysis as mda
from cycler import cycler

import matplotlib.pyplot as plt

##plt.style.use('../../scripts/default.mplstyle')
plt.style.use("/home/ilija/uni/nanoscale/nmm-week4/scripts/default.mplstyle")
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
def main():
    # Define the topology and trajectory files
    topology = 'graphene_flat.data'
    trajectory = 'trajectory.dat'


   # u = bsa.setup_universe(topology, trajectory)
    u = mda.Universe(topology, trajectory, format="LAMMPSDUMP", atom_style= "id type x y z vx vy vz potEngAtom stressx c_4[2] c_4[3]", dt = 0.001)

    N_FRAMES = u.trajectory.n_frames
    N_ATOMS = u.atoms.n_atoms

    # Initialise the position and time arrays
    positions = np.zeros((N_FRAMES, N_ATOMS, 3))
    time = np.zeros(N_FRAMES)

    # Loop over the trajectory and load the positions
    for i,traj in enumerate(u.trajectory):                          
        positions[i] = u.atoms.positions   
        time[i] = u.trajectory.ts.data['time']

    # Now use bsa to calculate the hydrodynamics radius
    rgs = np.zeros(N_FRAMES)
    for i, frame in enumerate(positions):
        _, eig_vals = bsa.compute_gyration_tensor(frame)
        rgs[i] = bsa.calculate_rg2(*eig_vals)
    # you can save the time average with np.mean(rhydro)

    plt.plot(time, rgs)
    plt.xlabel("Time (fs)")
    plt.ylabel("Gyration Radius ($\AA$)")
    plt.tight_layout()
    plt.savefig("rg-v-time.png", dpi=300)
    plt.show()
if __name__ == '__main__':
    main()