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
1. Upload the image of interest into the ```input_data_images``` folder. Please name the file in such a way that it is clear what type of data it is (e.g, tensile, cyclic, creep). In additon, please name the file without any spaces. Use underscores instead as a spacer between words.

2. Run ```DataAcquisition.py``` by simply running in the terminal ```python DataAcquisition.py```. This will prompt you to input the data image path in the terminal. Please copy the input data image path into the terminal and press **ENTER** on your keyboard. A matplotlib window will pop up prompting you to manually click the ***start*** and ***end*** of the **x-axis** on the image. After that, it will prompt you in the terminal to manually type in the numerical value of the ***start*** of the **x-axis** and the ***end*** of the **x-axis**. It will prompt you to do the same process for the **y-axis**. Once that is complete, another window will pop up asking you to click on the data points of the graph that you want to capture (e.g. points of a line graph). Once you have clicked on all the points of the graph to get the overall trend of the data you wish to capture, simply close the matplotlib windows and the code will automatically print the **x data points** and **y data points**. It will also automatically save these **x-y data points** into a ```.csv``` file in the ```output_data_csv_files``` folder. The file will have the same name as the name you give the input data image.

3. To ensure that the data you captured in the ```<file_name>.csv``` file is accurate and what you want, you can run ```DataPlotting.py``` to visualize it. By typing ```python DataPlotting.py``` into the terminal, the script will prompt you through the terminal to input the path of the ```<file_name>.csv``` file. After hitting **ENTER** it will show the plot you created and save it as a ```.png``` file in the ```output_data_images``` folder.

# Contributing Data
Inside the ```input_data_images``` are screenshots taken from multiple different published articles. The source articles can be found with citations provided in ```citations.md```. If you are contributing more data to this repository, please update the ```citations.md``` file with the paper you took the data from in **APA7** format. In addition to that, please type a brief description of what the data is you captured in your ```input_data_image.png```. It should look something like this:
> 1. Zhao, Y., Cao, H., & Liu, S. (2022). The dislocation-based fatigue deformation mechanism of a RAFM steel under multi-axial loadings. Journal of Nuclear Materials, 558, 153324. https://doi.org/10.1016/j.jnucmat.2021.153324
    ```CLAM_steel_Data.png``` contains data for path E (where only pure axial strain is being applied). The data is a hysteresis loop for CLAM, a RAFM steel developed by the Chinese. The other paths may be interesting to investigate, but I found this to be the most useful graph from the report with regards to LCF strain-controlled testing.