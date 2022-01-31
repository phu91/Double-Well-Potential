## Import
from sys import stdout
import numpy as np
from simtk.openmm import *
from simtk.openmm.app import *
from simtk.openmm.openmm import BrownianIntegrator, Context, LangevinIntegrator
from simtk.unit import *
from sys import stdout

class ForceReporter(object):
    def __init__(self, file, reportInterval):
        self._out = open(file, 'w')
        self._out.write("ps\tposX_nm\tkBT\n")
        self._reportInterval = reportInterval
        
    def __del__(self):
        self._out.close()

    def describeNextReport(self, simulation):
        steps = self._reportInterval - simulation.currentStep%self._reportInterval
        return (steps, True, False, True, True, None)

    def report(self, simulation, state):
        forces = state.getForces().value_in_unit(kilojoules/mole/nanometer)
        position=state.getPositions().value_in_unit(nanometer)
        energy = state.getPotentialEnergy().value_in_unit(kilojoules/mole)
        time = state.getTime().value_in_unit(picosecond)
        for i in range(len(forces)):
            self._out.write('%g\t%g\t%g\n' % (time,position[0][i],energy/2.479))


## Physical parameters
temperature = 298 * kelvin

## Simulation parameters
## box_size = 150 * angstrom  # initial value only
# cutoff = 3 * sigma
natom = 1
n_steps = 50000000
#platform = Platform.getPlatformByName('CPU')

## Define a system
system = System()
system.addParticle(1)  # added particle with a unit mass

## Add external FORCE 
# http://docs.openmm.org/7.1.0/api-python/generated/simtk.openmm.openmm.CustomExternalForce.html
# Parameter = energy (string) – an algebraic expression 
# giving the potential energy of each particle as a function 
# of its x, y, and z coordinates
print("Adding Force ...")
g_dagger=1
energy_func = 'step(abs(x))*(step(f)*v+step(-f)*u);f=abs(x)-1/2;u=u0*'+str(g_dagger)+';v=v0*'+str(g_dagger)+';u0=-2*x^2;v0=2*(abs(x)-1)^2-1'

force = CustomExternalForce(energy_func) 
force.addParticle(0, [])
system.addForce(force)

## Metadynamics
# cv = BiasVariable()
# metadynamics.Metadynamics(system, cv, temperature, biasFactor, height, frequency, saveFrequency=None, biasDir=None)

## Integrator
integrator = LangevinIntegrator(temperature,1/picosecond,0.002*picosecond)       ## Langevin integrator with 500K temperature, gamma=1, step size = 0.02

## Assembly system as an context object
simulation = Simulation(system,system,integrator)
simulation.context.setPositions([[-1, 0, 0]])		# nanometer
simulation.context.setVelocitiesToTemperature(temperature)

## Simulation over n_steps
simulation.reporters.append(StateDataReporter(stdout, 10, step=True, progress=True,potentialEnergy=False, totalSteps=n_steps))
simulation.reporters.append(ForceReporter('g_dagger_'+str(g_dagger)+'_100ns.dat', 10))
simulation.reporters.append(CheckpointReporter('state_'+str(g_dagger)+'.chk', 5000))


print("Running Simulation...")
simulation.step(n_steps)


print("Saving Output...")
simulation.saveState('output_'+str(g_dagger)+'.xml')
    
print("Simulation Done")
