### Overriding function to force a single best-fit line through the CSDs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##Best fit regression functions
def squared_error (y_orig, y_line):
    return sum((y_orig - y_line)**2)

def r_squared(y_orig, y_line):
    y_mean_line = [np.mean(y_orig) for y in y_orig]
    se_reg = squared_error (y_orig, y_line)
    se_mean = squared_error (y_orig, y_mean_line)
    return 1-(se_reg/se_mean)

def line(m, b, ecks):
    gee = []
    for element in ecks:
        gee.append(m*element + b)
    return gee

names = pd.read_csv("name_sec.csv")
name = names['Sample']
depth = names['Depth']
reg_data = pd.DataFrame(columns = ('Names', 'Depth', 'm', 'b', 'r'))
reg_data['Names'] = name
reg_data['Depth'] = depth
s = []
inte = []
c = []
for i in range(0, names.shape[0]):
    plot_data = pd.read_csv("output_data/binned_data/"+name[i]+".csv")
    x = plot_data['size']
    y = plot_data['pop_density']
    idx = np.isfinite(x) & np.isfinite(y)
    m, b = np.polyfit(x[idx], y[idx], deg = 1)
    f = lambda x: m*x + b
    r = r_squared(y[idx], line(m, b, x[idx]))
    print(m)
    print(b)
    print(r)
    s.append(m)
    inte.append(b)
    c.append(r)
    plt.plot(x, y, label = name[i])
    plt.plot(x, f(x), label = r)
    plt.legend()
    plt.xlabel("Crystal size")
    plt.ylabel("Population Density (ln(n))")
    plt.savefig('output_data/override_plots/'+name[i]+'.png', format = 'png')
    plt.close()
reg_data['m'] = s
reg_data['b'] = inte
reg_data['r'] = c
plt.figure(figsize=(20, 16))
plot_color = plt.get_cmap("Set1")
for i in range (0, names.shape[0]):
    plot_data = pd.read_csv("output_data/binned_data/"+name[i]+".csv")
    x = plot_data['size']
    ma = s[i]
    ba = inte[i]
    f = line(ma, ba, x)
    plt.gcf()
    plt.plot(x, f, label = name[i], c= plot_color(i))
plt.legend()
plt.xlabel("Crystal size")
plt.ylabel("Population Density (ln(n))")
plt.savefig('output_data/override_plots/override_bestfit.png', format = 'png')
#print(reg_data)
reg_data.to_csv('output_data/override_plots/reg.csv')