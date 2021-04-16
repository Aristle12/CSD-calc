Scripts developed for Monteiro et al. (). Please refer to the paper while using for publishing purposes.
This set of Python scripts calculates CSDs for any mineral. 
Note that the methode for volumetric/ stereological corrections used in this script are crude (after Zieg and Marsh 2012).
This program is only suitable for analysis of CSDs from within the same igneous body and not for comparison between two or more bodies because of this.

Settinh up the program:
1. name_sec.csv
Fill in the columns with your own sample names. It is important that you do not change the file name or the column headers.
This will break the program
2. Put in the measurements in the format given in the /input_data csv files. Please input only .csv files with the same format.
3. Run csd_complete.py 
4. Run bestfit.py and/or override_fit.py

Note 1:
If you have stereographically corrected data, you can arrange them in the output_data/binned_data/ folder with the sample name in .csv format,
the bestft.py and override_fit.py programs will use them for regression analysis.

Note two:
The graphs use the 'RdBu' colour pallete from the matplotlib library. If you want to change this, you can do so in the code. 
Refer to the documentation link below for details:
https://matplotlib.org/stable/tutorials/colors/colormaps.html