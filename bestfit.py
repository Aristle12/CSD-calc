###Program to calculate the best-fit lines (up to 2) through the calculated CSDs and plot them
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import math

###Regression functions
def squared_error (y_orig, y_line):
    return sum((y_orig - y_line)**2)
def r_squared(y_orig, y_line):
    y_mean_line = [np.mean(y_orig) for y in y_orig]
    se_reg = squared_error (y_orig, y_line)
    se_mean = squared_error (y_orig, y_mean_line)
    if se_mean == 0:
        return 1
    else:
        return 1-(se_reg/se_mean)
###Line functions
def fun(x, m, b):
    line=[]
    for ele in x:
        line.append((ele*m)+b)
    return line
##Calculating and plotting best fit lines (upto two)
names = pd.read_csv("name_sec.csv")
name = names['Sample']
plot_color = plt.get_cmap("Set1")
reg_df = pd.DataFrame(columns = ('Name', 'm1', 'm2', 'b1', 'b2', 'r1', 'r2'), index = [])
for i in range(0, names.shape[0]):
    plot_data = pd.read_csv("output_data/binned_data/"+name[i]+".csv")
    x = plot_data['size']
    y = plot_data['pop_density']
    e = plot_data['2sigma']
    index = len(x)
    n = 3
    m1 = []
    b1 = []
    m2 = []
    b2 = []
    r1 = []
    r2 = []
    j1 = []
    tr = []
    print(name[i])
    df = pd.DataFrame({'Name':name[i]}, index = [0])
    for j in range(0, index):
        if n<(index-3):
            j1.append(n)
            ma, ba = np.polyfit(x[0:n], y[0:n], deg=1)
            mb, bb = np.polyfit(x[n:index], y[n:index], deg=1)
            f1 = fun(x, ma, ba)
            f2 = fun(x, mb, bb)
            ra = r_squared(y[0:n],f1[0:n])
            rb = r_squared(y[n:index], f2[n:index])
            m1.append(ma)
            b1.append(ba)
            m2.append(mb)
            b2.append(bb)
            r1.append(ra)
            r2.append(rb)
            r_mean = np.mean([ra, rb])
            tr.append(r_mean)
        elif n>(index-3):
            j1.append(index)
            ma, mb = np.polyfit(x, y, deg=1)
            f1 = fun(x, ma, ba)
            ra = r_squared(y,f1)
            m1.append(ma)
            m2.append(0)
            b2.append(0)
            b1.append(ba)
            r1.append(ra)
            r2.append(0)
            tr.append(ra)
        n = n+1
    #print(tr)
    tr1 = max(tr)
    #print(tr1)
    #print(j1)
    for l in range(0, len(x)):
        if tr1==tr[l]:
            ma = m1[l]
            mb = m2[l]
            ra = r1[l]
            rb = r2[l]
            ba = b1[l]
            bb = b2[l]
            n = j1[l]
            f1 = fun(x, ma, ba)
            f2 = fun(x, mb, bb)
            break
        else:
            pass
    df['m1'] = ma
    df['m2'] = mb
    df['b1'] = ba
    df['b2'] = bb
    df['r1'] = ra
    df['r2'] = rb
    print(n)
    reg_df = reg_df.append(df, ignore_index = True)[df.columns.tolist()]
    plt.plot(x,y, '-o', label=name[i])
    plt.plot(x[0:(n+1)], f1[0:(n+1)], label=ra)
    if n<=12:
        plt.plot(x[(n-1):index], f2[(n-1):index], label=rb)
    plt.errorbar(x, y, yerr = e, fmt = '|')
    plt.title(name[i])
    plt.legend()
    plt.xlabel("Crystal size")
    plt.ylabel("Population Density (ln(n))")
    plt.savefig("output_data/plot_individual/"+name[i]+".png", format='png')
    plt.close()
reg_df.drop(reg_df.index[0])
reg_df.reset_index(drop=True)
print(reg_df)
reg_df.to_csv("output_data/reg_data/reg_data_best_fit.csv")
## Plotting kinked best fit graph
plt.figure(figsize=(20, 16))
for i in range(0, names.shape[0]):
    plot_data = pd.read_csv("output_data/binned_data/"+name[i]+".csv")
    x = plot_data['size']
    y = plot_data['pop_density']
    slope1 = reg_df['m1'][i]
    slope2 = reg_df['m2'][i]
    intercept1 = reg_df['b1'][i]
    intercept2 = reg_df['b2'][i]
    if slope2==0:
        plt.gcf()
        plt.plot(x, fun(x, slope1, intercept1), c = plot_color(i), label = name[i])
    elif slope2!=0:
        a1 = 0-slope1
        a2 = 0-slope2
        A = np.array([[a1,1], [a2,1]])
        B = np.array([intercept1, intercept2])
        kink = np.linalg.solve(A, B)
        kink_x = kink[0]
        kink_y = kink[1]
        print(kink)
        x1 = []
        x2 = []
        x2a = []
        #Separating x based on kinks
        for j in range (0, len(x)):
            if x[j] <= kink_x:
                x1.append(x[j])
            elif x[j] > kink_x:
                x2a.append(x[j])
        x1.append(kink_x)
        x2.append(kink_x)
        x2.extend(x2a)
        plt.plot(x1, fun(x1, slope1, intercept1), c = plot_color(i), label = name[i])
        plt.plot(x2, fun(x2, slope2, intercept2), c = plot_color(i))
        x1.clear()
        x2.clear()
        x2a.clear()
plt.legend()
plt.xlabel("Crystal size")
plt.ylabel("Population Density (ln(n))")
plt.savefig("output_data/best_fit.png", format = 'png')
plt.show()
plt.close()
        


            
    