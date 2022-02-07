import numpy as np
from openmm import *
from openmm.app import *
# from simtk.openmm.openmm import *
from simtk.unit import *
from sys import stdout
from openmmplumed import PlumedForce

class Reporter(object):
    def __init__(self, file, reportInterval):
        self._out = open(file, 'w')
        self._out.write("ps\tx\ty\tz\n")
        self._reportInterval = reportInterval
        
    def __del__(self):
        self._out.close()

    def describeNextReport(self, simulation):
        steps = self._reportInterval - simulation.currentStep%self._reportInterval
        return (steps, True, False, True, True, None)

    def report(self, simulation, state):
        forces = state.getForces().value_in_unit(kilojoule/mole/nanometer)
        position=state.getPositions(asNumpy=False).value_in_unit(nanometer)
        energy = state.getPotentialEnergy()._value
        time = state.getTime().value_in_unit(picosecond)
        self._out.write('%g\t%g\t%g\t%g\n' % (time,position[0][0],position[0][1],position[0][2]))      #position[atom index][x,y,z]
        # print(time,position[0][0])      #position[atom index][x,y,z]

 
## Physical parameters
temperature = 298*kelvin
natom = 1
n_steps = 10000

## Define a system
system = System()

# for i in range(natom):
#     system.addParticle(mass)  # added particle with a unit mass
system.addParticle(1)   # 
# system.addParticle(0)   # particle 0 - mass 0 => no change in positions and velocity

## Add external FORCE 
## http://docs.openmm.org/7.1.0/api-python/generated/simtk.openmm.openmm.CustomExternalForce.html
## Parameter = energy (string) – an algebraic expression 
## giving the potential energy of each particle as a function 
## of its x, y, and z coordinates

print("Adding Force ...")
g_dagger_value = 4	#kBT
energy_func = 'step(abs(x))*(step(f)*v+step(-f)*u);f=abs(x)-1/2;u=u0*g_dagger;v=v0*g_dagger;u0=-2*x^2;v0=2*(abs(x)-1)^2-1'
force = CustomExternalForce(energy_func) 
force.addGlobalParameter("g_dagger",g_dagger_value)

for i in range(natom):
    force.addParticle(i,[])
    
system.addForce(force)

## Check system 
# print(XmlSerializer.serialize(system))

# Metadynamics 
script = """
a: FIXEDATOM AT=1,0,0 
d: DISTANCE ATOMS=a,1 
# metad: METAD ...
#    ARG=d SIGMA=1.2 HEIGHT=2 BIASFACTOR=20 TEMP=300.0 PACE=500 
#    GRID_MIN=0 GRID_MAX=20 GRID_BIN=150
#    CALC_RCT 
# ...
uwall: UPPER_WALLS ARG=d AT=20 KAPPA=150.0
PRINT ARG=* STRIDE=10 FILE=2-2WElls/sim3/COLVAR

"""

system.addForce(PlumedForce(script))

# # Integrator
integrator = BrownianIntegrator(temperature,1/picosecond,0.002*picosecond) 

## Assembly system as an context object
simulation = Simulation(system,system,integrator)
simulation.context.setPositions([[-1, 0, 0]])		# nanometer
simulation.context.setVelocitiesToTemperature(temperature)

# ## Simulation over n_steps
simulation.reporters.append(StateDataReporter(stdout, 10, step=False, progress=True,potentialEnergy=False, totalSteps=n_steps))
simulation.reporters.append(Reporter('metadynamics-'+str(g_dagger_value)+'.dat', 10))

print("Running Simulation...")
simulation.step(n_steps)


print("Saving Output...")
simulation.saveState('new_output_'+str(g_dagger_value)+'_2.xml')
simulation.reporters.append(CheckpointReporter('new_state_'+str(g_dagger_value)+'_2.chk', 5000))

print("Simulation Done")

