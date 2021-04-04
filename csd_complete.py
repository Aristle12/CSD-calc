##Program to calculate, bin and plot CSDs, determine the best fit lines through them and plot the best fit lines
##Output folders required 
###1 binned data
###2 regressed data
###3 plotted individual regressed data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##Volume correction function
def vol_corr(n_per_unit_area, bins_mid, bins_width):
    num_vol = n_per_unit_area/bins_mid
    num_dens_vol = num_vol/bins_width
    return num_vol, num_dens_vol

##Best fit regression functions
def squared_error (y_orig, y_line):
    return sum((y_orig - y_line)**2)

def r_squared(y_orig, y_line):
    y_mean_line = [np.mean(y_orig) for y in y_orig]
    se_reg = squared_error (y_orig, y_line)
    se_mean = squared_error (y_orig, y_mean_line)
    return 1-(se_reg/se_mean)
  

##2D array search function
def twoD (array, search_val):
    for i, e in enumerate(array):
        try:
            return i, e.index(search_val)
        except ValueError:
            pass
    raise ValueError("{} is not in list".format(repr(search_val)))

##Line function
def line(m, b, ecks):
    gee = []
    for element in ecks:
        gee.append(m*element + b)
    return gee
##Getting names file
names = pd.read_csv("E:/Project/Hardik_CSD/csd_results/name_sec.csv") ####
name = names['Sample']#Check this#
depth = names['Depth']#And this#
f_depth = names['Depth In Flow']#And this#
plt.figure(figsize=(16,10))
plot_color = plt.get_cmap('RdBu')

#Binning data
for i in range(0, names.shape[0]):
    plot_data = pd.read_csv("input_data/"+name[i]+'.csv') ####
    reg_data = pd.DataFrame(columns=('size', 'num_vol', 'pop_density', '2sigma', 'total_area', 'number_per_unit_area', 'max_l', 'avg_l'))
    length = plot_data['Length']
    total_area = plot_data['total_area'][0]
    min_val = max(length.min(), 3)
    max_val = length.max()
    bins = np.geomspace(min_val, max_val, 16)
    count, divisions = np.histogram(length, bins = bins)
    bins_index = []
    bins_width =[]
    for k in range(0, len(bins)-1):
            bins_index.append((bins[k]+bins[k+1]/2))
            bins_width.append(bins[k+1]-bins[k])
    n_per_unit_area = count/total_area
    error = 2*(np.sqrt(n_per_unit_area))
    num_vol, num_dens_vol = vol_corr(n_per_unit_area, bins_index, bins_width)
    ln_n = np.log(num_dens_vol)
    reg_data['size'] = np.array(bins_index)
    reg_data['num_vol'] = np.array(num_dens_vol)
    reg_data['pop_density'] = ln_n
    reg_data['2sigma'] = error
    reg_data['total_area'] = total_area
    reg_data['number_per_unit_area'] = n_per_unit_area
    reg_data['max_l'][0] = max(length)
    reg_data['avg_l'][0] = np.mean(length)
    reg_data.to_csv("output_data/binned_data/"+name[i]+'.csv')
    #Plotting data
    plt.gcf()
    plt.plot(bins_index, ln_n, c = plot_color(i*15), label = names['Sample'][i])
plt.gcf()
plt.xlabel("Crystal Size")
plt.ylabel('population Density (ln(n))')
plt.legend()
plt.savefig('output_data/csd_all_plots.png', format = 'png') ####
plt.close()