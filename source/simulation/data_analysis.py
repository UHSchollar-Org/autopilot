import statistics as st
import numpy as np
from pathlib import Path
import csv
import matplotlib.pyplot as plt
from scipy.stats import expon, geom
import numpy as np

data_path = Path.cwd() / 'data'

uk_accidents = data_path / 'uk_accidents'


def uber_datasets_analysis():
    uber_data = data_path / 'uber_dataset'
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
    
def nyc_yellow_cabs_analysis():
    """Using NYC Yellow Taxi Trip Data from the dataset dowloaded in 
       https://www.kaggle.com/datasets/ashvanths/nyc-yellow-taxi
       analyzes the length of the trips made by these taxis to then generate 
       a random variable that behaves according to the results obtained
    """
    nyc_yellow_cab = data_path / 'nyc_yellow_taxi_data'
    
    with open(nyc_yellow_cab / 'df_all.csv', 'r') as f:
        csv_reader = csv.DictReader(f)
        distances = []
        distances_count = {}
        count = 0
        for row in csv_reader:
            count+=1
            distance = round(float(row['trip_distance']),1)
            if distance<0:
                raise Exception("Negative distance")
            distances.append(distance)
            distances_count[distance] = distances_count.get(distance, 0) +1
            
        plt.bar(distances_count.keys(),distances_count.values())
        plt.show()
        print(count)
        #Mean and standard deviation
        mu = st.mean(distances)
        sigma = np.std(distances)
        
        print(mu,sigma)