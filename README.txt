Scripts developed for Monteiro et al. (). Please refer to the paper while using for publishing purposes.
This set of Python scripts calculates CSDs for any mineral. 
Note that the method for volumetric/ stereological corrections used in this script are crude (after Zieg and Marsh 2012).
This program is only suitable for analysis of CSDs from within the same igneous body and not for comparison between two or more bodies because of this.

Settinh up the program:
1. name_sec.csv
Fill in the columns with your own sample names. It is important that you do not change the file name or the column headers.
This will break the program
2. Put in the measurements in the format given in the input_data csv files. Please input only .csv files with the same format.
3. Run csd_complete.py 
4. Run bestfit.py and/or override_fit.py

Note 1:
If you have stereographically corrected data, you can arrange them in the output_data/binned_data/ folder with the sample name in .csv format,
the bestft.py and override_fit.py programs will use them for regression analysis.

Note 2:
The graphs use the 'RdBu' colour pallete from the matplotlib library. If you want to change this, you can do so in the code. 
Refer to the documentation link below for details:
https://matplotlib.org/stable/tutorials/colors/colormaps.html

Note 3:
You may get an Index Error while running the bestfit.py program. 
This is because the csd_complete.py has been programmed to automatically calculate logarithmic bin sizes.
This will cause it to sometimes create empty bins in between or at the end of the binned data.
A print command has been set to let users know which sample is being processed by the program. The sample will be printed before the 
error so users know which sample has the empty bins. 
You have to manually open the binned data in output_data/binned_data and delete the rows with empty bins and replace with the rows below.
It would be wise to leave the index in a continuous sequence till the end of the column and not more to avoid erroneous bestfit lines.