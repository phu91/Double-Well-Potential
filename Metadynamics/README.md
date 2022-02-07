# Requirements 
***Consulting OpenMM website for more details [http://docs.openmm.org/6.2.0/userguide/index.html]***

Conda installation recommendation. 

## OpenMM  
### Installation

`conda install -c conda-forge openmm`
Utilizing OpenMM engine to simulate double well potential with overdamped Langevine dynamics or Brownian Dynamics. 

## openmm-plumed plugin
The plugin should be installed on the same conda environmemnt as OpenMM. The plugin helps in communication between PLUMED and OpenMM. 
https://github.com/openmm/openmm-plumed
### Installation
`conda install -c conda-forge openmm-plumed`

### Usage:

`from openmmplumed import PlumedForce`
```# Metadynamics 
script = """
a: FIXEDATOM AT=1,0,0 
d: DISTANCE ATOMS=a,1 
metad: METAD ...
   ARG=d SIGMA=1.2 HEIGHT=2 BIASFACTOR=20 TEMP=300.0 PACE=500 
   GRID_MIN=0 GRID_MAX=20 GRID_BIN=150
   CALC_RCT 
...
uwall: UPPER_WALLS ARG=d AT=20 KAPPA=150.0
PRINT ARG=* STRIDE=10 FILE=2-2WElls/sim3/COLVAR
""" 
system.addForce(PlumedForce(script))
