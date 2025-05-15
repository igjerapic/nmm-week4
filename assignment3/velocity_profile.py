import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import beadspring as bsa
from cycler import cycler


# plt.style.use('../scripts/default.mplstyle')

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
    # Define the topology and trajectory files
    topology = "channel.data"
    traj = "traj.dat"

    u = bsa.setup_universe(topology, traj, dt=0.002)

    # Set up binning along z-axis, values taken to match mass profile 
    bin_count = 50
    z_min = 0.0
    z_max = u.dimensions[2]
    z_edges = np.linspace(z_min, z_max, bin_count + 1)
    z_centers = 0.5 * (z_edges[:-1] + z_edges[1:])

    # initializing arrays
    accumulated_velocity = np.zeros(bin_count)
    n_atoms = np.zeros(bin_count)
    average_vel = np.zeros(bin_count)

    # Compute speeds for atoms in water molecules for each trajectory 
    for i, traj in enumerate(u.trajectory):
        waters = u.select_atoms("type 1 or type 2")
        positions = np.array(waters.positions.copy())
        velocities = np.array(waters.velocities.copy())
    
        # compute n_atoms and individual attom speed for each bin 
        for j in range(1, len(z_edges)):
            mask = (positions[:,-1] >= z_edges[j - 1]) & (positions[:,-1] <= z_edges[j])
            n_atoms[j - 1] += len(positions[mask])

            for velocity in velocities[mask]:
                accumulated_velocity[j - 1] += np.linalg.norm(velocity)
            
    # Average accumulated speeds by total number of atoms 
    for idx in np.nonzero(n_atoms):
        average_vel[idx] = accumulated_velocity[idx] / n_atoms[idx]

    # converting to meters per second
    average_vel = average_vel * 10**5

    # Plotting
    plt.figure(figsize=(4, 4))
    plt.plot(z_centers, average_vel)
    plt.xlabel("z-position")
    plt.ylabel("Average speed")
    plt.title("Velocity profile along z-axis")
    plt.tight_layout()
    plt.savefig("velocity_profile.png")

if __name__=="__main__":
    main()