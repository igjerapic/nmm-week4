# nmm-week4

Welcome to Classical hell! From this week we forget about electrons and embrace the simpler times when particles were particles and waves were waves. In other words, Molecular Dynamics (MD) based on classical equations of motion. This allows our models to reach larger scales of atomistic processes. We can also do crazy things like increasing temperature above 0K and pushing stuff! Week 4 in particular is dedicated to all-atom simulations, the critical importance of MD force fields, and atomistic processes of relevance for nanomaterials.

Ovito visualization tips: to preserve bonds while looking at dump files, load the data file first, then use the modification "load trajectory". If you save unwrapped coordinates (useful for calculating properties like the MSD), remember to add the modification "wrap at periodic boundaries". When coloring by particle properties, remember to adjust the range to get meaningful gradients.

Post-processing tips: static properties can be measured from single frames, but time averages provide better sampling (as long as the system is equilibrated). Dynamics properties are functions of time, some of them (like the MSD) are better observed on a log scale. 

## Assignment 1 - The Icebreaker

Let's use your first MD assignment to break the ice. Literally! In this assignment you will play with phase changes of water and how they depend on the chosen water model and simulation setup.

### Instructions

1a. Visualize the data file ice3.data, containing a structure of Ih ice that uses the TIP3P model for water. The structure was generated using [GenIce](https://github.com/vitroid/GenIce). Calculate the [radial distribution function g(r)](https://en.wikipedia.org/wiki/Radial_distribution_function) of the structure with Ovito or Bead Spring Analytics and report which peaks correspond to which physical distances. 

1b. Run the LAMMPS simulation water-TIP3P.in, which gradually raises the temperature of the system up to 1000K.

(i) Check the radial distribution function of the last simulation frame. How does it compare to that of the initial structure?

(ii) Estimate the melting temperature of this simulation (HEADS UP: expect some pretty surprising results...). One rough way is to do it by visual inspection of the trajectory. For a better estimate, you can track the amount of O-H intermolecular bonds over time. O-H intermolecular bonds are the stabilizing hallmark of the Ih hexagonal ice structure, and we can consider the system melted once this quantity reaches a new equilibrium value. You can also look at how the peaks of the g(r) change with increasing temperature.

To generate the plot of O-H intermolecular bonds over time in Ovito: Add the 'Create Bonds' modifier and select the Pair-wise cutoff option. Change the O-H cutoff value to the average distance between O and H atoms (1.82). The number of bonds created in each frame is visible in the 'Global Attributes panel' at the bottom. Use the save icon to export the number of bonds and the timestep for every frame to one `.txt` file. Now you can use Python to read this file (`bonds = numpy.loadtxt('bonds.txt', skiprows=1)`) and plot the results.

1c. Now switch to the more complex tip4p model, using the ice4.data starting file and the water-TIP4P.in input file. Run the simulation and repeat your estimate of the melting temperature.

(i) How do the models compare in terms of efficiency (steps/s)?

(ii) How do the melting temperatures of the two models compare to each other? And to the [experimental data](https://sciencenotes.org/melting-point-of-water-in-celsius-fahrenheit-and-kelvin/) and [modeling literature](https://pubs.aip.org/aip/jcp/article/122/11/114507/929655)?
How do you explain these discrepancies?

## Assignment 2 - Out of Flatland

Back to graphene, now much larger and without perfect periodic lattice conditions! In the real world, graphene is not an infinite 2D plane and [graphene sheets tend to form twisted or crumpled structures](https://doi.org/10.1016/j.mattod.2015.10.002). While relevant for electronic properties, let's simply see how crumpling affects the energy and mechanical stresses of a graphene sheet. 
Assignment and scripts inspired by and adapted from [Eric N. Hahn's tutorial](https://www.ericnhahn.com/tutorials/lammps-tutorials/crumpled-graphene).

### Instructions

2a. Check the simulation script crumplingSphere.in. Answer a few questions on the model implemented (you can also do this after running the simulation and visual inspection):

(i) what force field is used?

(ii) how many covalent bonds are present in the graphene sheet created? Does it make sense?

(iii) what is the key command line used to deform the graphene sheet?

2b. Run the simulation (the CH.airebo-m file is also needed) and make a movie/a few snapshots of the process using Ovito for your report. Always start by visually inspecting your simulation! 

(i) Color particles by potential energy. What do you notice? Careful: this is sensitive to the boundary values you select for the coloring scheme.

(ii) Plot the potential energy and the radius of gyration of the system over time. Note that the first one is an output of the thermo command in the LAMMPS output file, 
     while for the second one you need BeadSpring Analytics or any other post-processing tool of your choice. 

2c. Now modify the "fix indenter" line and try to make a cylindrical nanotube out of your initial sheet. 
    Report again your final structure and the variation in potential energy and radius of gyration. How does it compare to the previous simulation?     
    NOTE: No need to create a perfect nanotube, which would be very challenging and requires additional tricks to set up. But the closest structure to a perfect nanotube reported by the weekly deadline gets a non-grade-related prize!

2c. Instead of a "fix indenter", now use the "fix deform" command to perform uniaxial extension of your graphene sheet along the x (or y) axis. 
    Look at the LAMMPS documentation to implement it, and take care particularly of the "erate" and "remap" keywords. 
    Run the simulation again. What happens after a while? Briefly discuss if it makes sense physically, both from an experimental point of view and within the framework of the model used. 
    Pro tip: per/atom stress is saved in the trajectory file, so you can use it to color particles based on stress.

## Assignment 3 - Go with the Flow

Transport and adsorption/absorption phenomena are of critical importance for nanomaterials, from batteries to functionalized surfaces. Let's play with them using what you are already familiar with: water and graphene! This assignment goes over the diffusion of water molecules in a graphene-confined nanochannel. LAMMPS code adapted from [Simon Gravelle's original script](https://github.com/simongravelle/lammps-input-files/tree/main/inputs/water-in-graphene-slit).

### Instructions

3a. Look at the input files waterFlow.in, PARAM.lammps, and channel.data and answer a few questions:

(i) what force fields are used to simulate water and graphene? How do they compare to the ones used in the first two assignments?

(ii) what is the value of the interaction energy epsilon between oxygen and carbon atoms?

(iii) which command enforces the flow of water in the channel?

3b. Run the simulation. Calculate a few properties from the trajectory: 

(i) the layer-by-layer distribution of water molecules' mass and velocity profiles along the z-axis. How does the velocity profile compare to what is expected for [macroscopic laminar flow](http://hyperphysics.phy-astr.gsu.edu/hbase/pfric.html)? What is the [reason](https://doi.org/10.1016/j.apsusc.2022.154477) for the discrepancy?

* You can use `mass_profile.py` script as-is, if you have set up the `bsa` environment. However, if you are running the script on Habrok, you might enconuter the error: `QWidget: Cannot create a QWidget without QApplication`. In that case, modify the script to save the data to a file and generate the plot locally on your own machine.

> **Hints for the velocity profile:** Have a look at the [MDAnalysis documentation](https://userguide.mdanalysis.org/stable/selections.html) and use an appropriate atom selection criterion to select the particles based on their z-coordinate. Once you load the universe with `bsa.setup_universe()`, you can loop over the trajectory and load the positions and velocities of the selected atoms only. Start by dividing the range from `zmin` to `zmax` into equal-width bins. For each frame in the trajectory, extract the positions and velocities of the atoms. Use the z-position of each atom to figure out which bin it belongs to. Then, compute the speed (magnitude of the velocity vector) for each atom and add it to the total for the corresponding bin. Also keep track of how many atoms fall into each bin. After processing all frames, compute the average speed in each bin by dividing the total speed by the number of atoms in that bin. Be careful to avoid dividing by zero. Finally, return the center position of each bin along with the average speeds and atom counts.

(ii) To obtain Poiseuille flow, a bound layer of fluid is expected to be present near the tube walls. Where does this effect come from, and how would you address this in your simulation? 

3c (OPTIONAL, HARD). Adapt the simulation to obtain the proper flow velocity profile expected for Poiseuille flow.
