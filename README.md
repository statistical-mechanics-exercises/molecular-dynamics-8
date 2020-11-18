# Testing your implementation

In this final exercise, I would like to finish by exploring how we can ensure that we have implemented the thermostat correctly.  I have already alluded the first test you should perform on any code in the previous exercise.  You should ensure that the average kinetic energy has a value that is consistent with the predictions of equipartition.  Equipartition states that a system with N momentum coordinates should have an average kinetic energy of ![](https://render.githubusercontent.com/render/math?math=\frac{Nk_BT}{2}).  If the average kinetic energy does not fluctuate around this value then we know that our thermostat is implemented wrongly.

The second thing that needs to be checked is whether or not an appropriate conserved quantity has been conserved.  It is hopefully obvious that the total energy (i.e. the sum of the kinetic and potential energies) is not conserved when we run this sort of constant temperature molecular dynamics.  After all, energy is exchanged between the system and the reservoir whenever the thermostat changes the velocities of the atoms.  There is, however, no way that energy can leave the coupled system composed of the atoms and thermostat.  If we thus track how much energy is transferred from the atoms to the thermostat over the course of the simulation and add this to the total energy of the atoms this final quantity should be conserved.     

To check the energy is conserved we, therefore:

1. Introduce a variable called `therm` and set its value equal to zero before our main MD loop.
2. Before applying the equation for the thermostat below:

![](https://render.githubusercontent.com/render/math?math=v_\textrm{new}=v_\textrm{old}e^{-\gamma\delta}%2B\sqrt{\frac{k_BT(1-e^{-2\gamma\delta})}{m}}N(0,1))

We compute the total kinetic energy of the particles and add it to the variable called `therm`.

Then after applying the equation for the thermostat we compute the kinetic energy again and subtract it from `therm`.

Notice, furthermore, that this business of updating therm must be done twice during the main MD loop as the thermostat is applied at the start and end of each iteration.

The final conserved quantity is computed by adding together the kinetic and potential energies of the particles and the variable called `therm`.  This quantity is conserved because, if `therm` is computed using the scheme described above, then this variable tracks the total amount of energy that has been transferred from the system to the thermostat's heat bath.  

To get you started on implementing a constant temperature MD code that checks for a conserved quantity I have written the outline code in the cell on the left.  As in previous exercises to complete this code you will need to:

* Write a function called `potential` that computes the potential energy and the forces for each of the configurations you generate.
* Write a function called `kinetic` that calculates the instantaneous kinetic energy.
* Use your potential function to write code that uses the velocity Verlet algorithm to integrate the equations of motion.
* Every 10 MD steps store the instantaneous values of the potential, kinetic and conserved quantity in the lists called `p_energy`, `k_energy` and `conserved`.

If the code is completed correctly a graph should be generated that shows that the conserved quantity does not change with time over the course of the simulation.  Small fluctuations in the value of the conserved quantity are inevitable due to machine error.  This quantity should not drift upwards or downwards with time, however. 



