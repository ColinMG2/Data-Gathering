#!/opt/moose/miniconda/bin/python
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html

import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import os

# Input absolute file path for the csv file extracted from DataAcquistion
input_data1 = input("Path of extracted data: ")
data0 = np.genfromtxt(input_data1, delimiter=',', names=True)

# Create figure (parameters for labels, title, and legend can be edited as desired)
plt.figure()
mpl.rcParams.update({'font.size': 10})
plt.xlabel("Strain [%]")
plt.ylabel("Stress [MPa]")
plt.title("Graph Title")
plt.grid(True)
plt.plot(data0['x'], data0['y'], color='r', label='Data')
plt.legend(loc='best')

# Saves output image in the output data images folder and names it the same as the input csv file
output_name = os.path.splitext(os.path.basename(input_data1))[0]
output_dir_name = "output data images"
output_path = os.path.join(output_dir_name, f'{output_name}.png')
plt.savefig(output_path)
print(f'File saved to: {output_path}')
plt.show()
