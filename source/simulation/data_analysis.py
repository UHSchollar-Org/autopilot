import statistics as st
import numpy as np
from pathlib import Path
import csv
import matplotlib.pyplot as plt
from scipy.stats import expon, geom

data_path = Path.cwd() / 'data'
uber_data = data_path / 'uber_dataset'
uk_accidents = data_path / 'uk_accidents'

count_dif_min = {}
all_data = []
with open(uber_data / 'uber-raw-data-apr14.csv', 'r') as f:
    csv_reader = csv.DictReader(f)
    
    last = None
    for row in csv_reader:
        current = int(row['Date/Time'].split(' ')[1].split(':')[1])
        
        if last:
            if current < last:
                res = 60 + current - last
            else:
                res = current - last
                
            all_data.append(res)
            count_dif_min[res] = count_dif_min.get(res, 0) + 1
            last = current
        else:
            last = current

#plt.plot(count_dif_min.keys(), [count_dif_min[i] for i in count_dif_min.keys()])           
#plt.bar(x = count_dif_min.keys(),height = count_dif_min.values())

mean = st.mean(all_data)
var = st.variance(all_data, mean)

#a = geom.rvs(size = 100)
b = expon.rvs(size = 1000)
b = [round(i) for i in b]
#print(a)
print(b)
