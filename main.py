import matplotlib.pyplot as plt
import numpy as np

def potential(x) :
  energy = 0 
  forces = np.zeros([7,2])
  # Your code to calculate the potential goes here
  for i in range(1,7) :
      for j in range(i) :
          d = x[i,:]-x[j,:]
          r2 = sum(d*d)
          r6 = r2*r2*r2
          r12 = r6*r6
          energy = energy + 4/r12 - 4/r6
          pref = 4*( 6/(r6*r2) - 12/(r12*r2) )
          forces[i,:] =  forces[i,:] - pref*d
          forces[j,:] =  forces[j,:] + pref*d 
  return energy, forces
  
def kinetic(v) :
  ke = 0
  # Your code to calculate the kinetic energy from the velocities goes here
  for vel in v : ke = ke + 0.5*sum(vel*vel)
  return ke
  
# This command reads in the positions that are contained in the file called positions.txt
pos = np.loadtxt( "positions.txt" )
# This command reads in the velocities that are contained in the file called velocities.txt
vel = np.loadtxt( "velocities.txt" )

# This is the value to use for the timestep (the delta in the equations on the other side)
timestep = 0.005
# This is the value of the temperature
temperature = 1.0 
# This is the value of the friction for the thermostate (the \gamma in the equations on the other side)
friction = 2.0
# This calculates the initial values for the forces
eng, forces = potential(pos)
# This is the variable that you should use to keep track of the quantity of energy that is exchanged with 
# the reservoir of the thermostat.
therm = 0
therm1 = np.exp( -friction*timestep / 2 )
therm2 = np.sqrt( temperature*(1-therm1*therm1) )

# We now run 500 steps of molecular dynamics
nsteps = 500
times = np.zeros(int(nsteps/10))
conserved_quantity = np.zeros(int(nsteps/10))
for step in range(nsteps) :
  # Apply the thermostat for a half timestep 
  for i in range(7) :
    therm = therm + 0.5*vel[i][0]*vel[i][0] + 0.5*vel[i][1]*vel[i][1] 
    vel[i][0] = vel[i][0]*therm1 + therm2*np.random.normal()
    vel[i][1] = vel[i][1]*therm1 + therm2*np.random.normal()
    therm = therm - 0.5*vel[i][0]*vel[i][0] - 0.5*vel[i][1]*vel[i][1]
  
  # Update the velocities a half timestep
  # fill in the blanks in the code here
  for i in range(7) : 
    vel[i][0] = vel[i][0] + 0.5*timestep*forces[i][0]
    vel[i][1] = vel[i][1] + 0.5*timestep*forces[i][1]
    
  # Now update the positions using the new velocities
  # You need to add code here
  for i in range(7) :
    pos[i][0] = pos[i][0] + timestep*vel[i][0]
    pos[i][1] = pos[i][1] + timestep*vel[i][1]
  
  # Recalculate the forces at the new position
  # You need to add code here
  eng, forces =  potential(pos)
  
  # Update the velocities another half timestep
  # You need to add code here
  for i in range(7) :
    vel[i][0] = vel[i][0] + 0.5*timestep*forces[i][0]
    vel[i][1] = vel[i][1] + 0.5*timestep*forces[i][1]


  # And finish by applying the thermostat for the second half timestep 
  for i in range(7) :
    therm = therm + 0.5*vel[i][0]*vel[i][0] + 0.5*vel[i][1]*vel[i][1] 
    vel[i][0] = vel[i][0]*therm1 + therm2*np.random.normal()
    vel[i][1] = vel[i][1]*therm1 + therm2*np.random.normal()
    therm = therm - 0.5*vel[i][0]*vel[i][0] - 0.5*vel[i][1]*vel[i][1]

  # This is where we want to store the energies and times
  if step%10==0 : 
    times[int(step/10)] = step
    # Write code to ensure the proper values are saved here
    conserved_quantity[int(step/10)] = eng + kinetic(vel) + therm
   
   
# This will plot the kinetic energy as a function of time
plt.plot( times, conserved_quantity, 'r-' )
plt.ylim([min(conserved_quantity)-0.05, max(conserved_quantity)+0.05 ])
plt.savefig( "conserved_quantity.png" )
