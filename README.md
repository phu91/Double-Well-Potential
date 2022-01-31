## Double-Well-Potential Simulation
 
### Utilizing OpenMM engine to simulate double well potential with overdamped Langevine dynamics or Brownian Dynamics. 

### For example, a symetric potential is given by a bistable matched-harmonic with 
<img src="https://latex.codecogs.com/svg.image?\bg_white&space;G_o(x)=\Delta&space;G^{\dagger}_o&space;f(x/x^{\dagger})" title="\bg_white G_o(x)=\Delta G^{\dagger}_o f(x/x^{\dagger})" />

where 

<img src="https://latex.codecogs.com/svg.image?\bg_white&space;f(x)=\begin{cases}-2x^2&space;&&space;\text{&space;if&space;}&space;0\le&space;|x|&space;\le&space;1/2&space;\\2(|x|-1)^2-1&space;&&space;\text{&space;if&space;}&space;1/2&space;<&space;|x|\end{cases}" title="\bg_white f(x)=\begin{cases}-2x^2 & \text{ if } 0\le |x| \le 1/2 \\2(|x|-1)^2-1 & \text{ if } 1/2 < |x|\end{cases}" />

### We can implement this external potential to any particle in OpenMM. 

## Requirements 
### ***Consulting OpenMM website for more details [http://docs.openmm.org/6.2.0/userguide/index.html]***

### OpenMM package. (Conda installation recommendation)

`conda install -c conda-forge openmm`

## Quantity	Units in OpenMM. 
### ***(Cannot be changed or NOT RECCOMENDATED TO CHANGE)***

### distance	   |   nm

### time	       |   ps

### mass	       |   atomic mass units

### charge	     |   proton charge

### temperature |	  Kelvin

### angle	      |   radians

### energy	     |   kJ/mol

