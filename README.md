# Data-Gathering

Inside of this repository, you will find these different subfolders:
1. input data images
2. output data csv files
3. output data images
Outside of these folders and within the PoResearch directory itself, there are 2 python scripts:
1. DataAcquisition
2. DataPlotting

Inside the "input data images" are screenshots taken from multiple different published articles. The source articles can be found with citations provided below:
1. "CLAM steel Data.png" -> "The dislocation-based fatigue deformation mechanism of a RAFM steel under multi-axial loadings"
   LINK: https://doi.org/10.1016/j.jnucmat.2021.153324

    This data in the image is for path E (where only pure axial strain is being applied). The other paths may be interesting to investigate, but I found this to be the most useful
    graph from the report with regards to LCF strain-controlled testing.
   
3. "RAFM Steel Data.png" & "RAFM Steel Data 2.png" -> "High temperature deformation and damage behavior of RAFM steels under low cyclic fatigue loading: Experiments and modeling"
   LINK: doi:10.1016/j.fusengdes.2006.03.002

    RAFM Steel Data.png contains strain-controlled hysteresis loop data for EUROFER97 at 550C and a hold time of 3 minutes in tension (red dashed line) or compression (blue line). The plot is also
    at the Nf/2 cycle (half the number of cycles until failure). For RAFM Steel Data 2.png, the plot shows the same conditions except that it is comparing a hold time in compression (blue) and a hold
    time in tension-compression (green dashed).

4. "V44 Tensile Strength Data.png" -> "Mechanical characterisation of V-4Cr-4Ti alloy: Tensile tests under high energy synchrotron diffraction"
   LINK: https://doi.org/10.1016/j.jnucmat.2022.153911

    The mechanical properties of V44 were investigated using a technique known as in-situ high energy X-ray diffraction (XRD) tensile testing at varying temperatures. This paper also gives the yield
    strength and ultimate tensile strength for V44 at varying temperatures. 

# Getting Started
Ensure that you have ```git``` installed on your system. To check, type ```git --version``` in your terminal and it should output whatever version of git you have on your system. If you do not have git installed, download the proper version for your OS following the link [here](https://git-scm.com/install/).

Once you have ```git``` installed, click on the **green** box that says **Code** and copy the ***https*** link. It should look like this:
> https://github.com/ColinMG2/Data-Gathering.git

Once you have this link, navigate to your desired project directory and perform the following commands:
```
git init
git clone https://github.com/ColinMG2/Data-Gathering.git
```

You should then have the github repository copied as a folder named the repository name, **Data-Gathering**, and be able to open it in your code editor of choice. If you do not have Python installed on your system, you will also need to do so. Download python locally to your computer by following the link [here](https://www.python.org/downloads/) and then add the paths to where python was locally installed, both the entire folder and the scripts folder, to the **Path** environment variable.

# How to use Data Gathering tool
DataAcquisition can be ran from the terminal using the command ```python <filename>.py``` and it will prompt you to input an image path. Copy the absolute path to avoid errors and then click enter. Then, a window 
of the image will appear and it will prompt you to click on the image at the start of the x-axis and the end of the x-axis. Then you must manually type the value into the terminal as it appears on the graph. Then it will 
prompt you to do the same for the y-axis. Once that is complete, you can click on the pixels of the image with the data you want to extract. It is best to choose fairly sparsed out points to get the overall 
trend of the data. Once you have extrapolated all the points you need, simply close the plot windows and the script will print which points it found and tell you that a .csv file has been saved to a certain path. 
The code is setup in such a way that the .csv file is saved with the same name as the image name. In addition, it automatically gets put into the ```output data csv files``` directory. From this point, the DataPlotting 
script is needed to verify how well the data was extracted from the original image.

DataPlotting simply asks for an input csv file (copy the absolute path of whatever file you want to plot) and then hit enter. From there, it will generate a plot of the data that was extracted and stored in the csv file
from the process described above in the DataAcquisition code. The DataPlotting script can be modified for desired axis labels, legend, title, and other parameters. Similarly, the output image is saved automatically in the 
```output data images``` directory with the same name as the .csv file.