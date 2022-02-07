from cmath import pi
import numpy as np
import pandas as pd 
from scipy.signal import *


def numerical_rate(data,time):
    time_in_basin_list = []
    step = data['ps'].iloc[1]-data['ps'].iloc[0]
    for i in range(len(time)-1):
        bin_data = data.loc[(data['ps']<time[i+1]) & (data['ps']>=time[i])]
        time_in_basin_bin = bin_data.loc[bin_data['x']<0].count().iloc[0]*step
        time_in_basin_list.append(time_in_basin_bin)

    total_time_in_basin = np.sum(time_in_basin_list)
    return total_time_in_basin
    print("Total time = %s ps.\nTotal time spending in basin (x<0) = %s ps"%(time[-1],total_time_in_basin))        
    

def analytic_rate(g_dagger,friction_coeff,omega_R,omega_B):
    kramers_rate = (1/(2*np.pi))*np.sqrt(omega_R*abs(omega_B))*np.exp(-g_dagger*friction_coeff)
    return kramers_rate

## INPUT ##
friction_coeff = 1  #/picosecond
g_dagger = 4  #kBT
omega_Reaction=16
omega_Barrier=16
timesplit = 5

data = pd.read_csv("input.dat",sep='\t')
output = open("output_rate.dat", 'w')
output.write("Basin_time\tn_jump\trate\tLag_time\n")

# CALCULATIONS ##
analytical = analytic_rate(g_dagger,friction_coeff,omega_Reaction,omega_Barrier)
print("The analytical rate (jumps/ps) by Kramers' Theory is "+str(analytical))

selected_time = 10000       #ps
time=np.linspace(0.02,selected_time,timesplit)
numerical = numerical_rate(data,time) 

bin_data = data.query('ps<=%s'%(selected_time))
X =bin_data['x']
jump_list = []
relax_list = []

peakind,_ = find_peaks(X,height=1)
results_full = peak_widths(X, peakind, rel_height=1)
prominences = peak_prominences(X, peakind)[0]
print("The most prominence peak= %s"%(len(prominences)))

lag_time = np.linspace(0,5000,11)
for j in lag_time:
    jump_list2 = []
    for i in range(len(results_full[0])):
        if results_full[0][i]>=j:
            jump_list2.append(1)
        else:
            jump_list2.append(0)


    # print("Python counts %s jumps in %s ps. Rate = %s. Stable time = %s"%(np.sum(jump_list2),numerical,np.sum(jump_list2)/numerical,j*0.02))
    output.write("%s\t%s\t%s\t%s\n"%(np.sum(jump_list2),numerical,np.sum(jump_list2)/numerical,j*0.02))

output.close()

