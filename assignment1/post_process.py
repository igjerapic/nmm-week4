import sys
import pickle as pkl

import numpy as np
import beadspring as bsa

def main(argv):
    # Define the topology and trajectory files

    topology = argv[-1]
    traj = "traj.dat"

    u = bsa.setup_universe(topology, traj)

    N_FRAMES = u.trajectory.n_frames
    N_ATOMS = u.atoms.n_atoms

    # Initialise the position and time arrays
    positions = np.zeros((N_FRAMES, N_ATOMS, 3))
    time = np.zeros(N_FRAMES)

    # Loop over the trajectory and load the positions
    for i,traj in enumerate(u.trajectory):                          
        positions[i] = u.atoms.positions   
        time[i] = u.trajectory.ts.data['time']
    
    # cubic box based on the dimensions of the simulation box
    box = bsa.setup_freud_box(u.dimensions[0])

    # Computing RDF from initial timesnap
    rdf_bincenters_init, rdf_init, r_min, r_peak = bsa.compute_rdf(positions[0], box, r_max=10, bins=200)

    # computing RDF from final timesnap
    rdf_bincenters_final, rdf_final, r_min, r_peak = bsa.compute_rdf(positions[-1], box, r_max=10, bins=200)

    df_post_process = { "rdf_bincenters_init": rdf_bincenters_init,
                        "rdf_init": rdf_init,
                        "rdf_bincenters_final": rdf_bincenters_final,
                        "rdf_final": rdf_final,
                        }
    
    with open("post_process.pkl", "wb") as f:
        pkl.dump(df_post_process, f)


if __name__ == '__main__':
    main(sys.argv)
