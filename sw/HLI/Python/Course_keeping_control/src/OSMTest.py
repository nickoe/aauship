'''
Created on 2012.11.01.

@author: Fodi
'''

import OsmApi as Osm
import numpy
import matplotlib.pyplot as plt
import FunctionLibrary as FL


MapObj = Osm.OsmApi();

'''Laeso'''
#Terkep = MapObj.Map(57.187, 10.826, 57.335, 11.214);
Terkep = MapObj.Map(11.1668, 57.2774, 11.1824, 57.2842);

longitudes = numpy.zeros(len(Terkep)-3);
latitudes = numpy.zeros(len(Terkep)-3);
ids = numpy.zeros(len(Terkep)-3);
i = 0;

while i < len(Terkep)-3:
    
    longitudes[i] = Terkep[i]['data']['lon'];
    latitudes[i] = Terkep[i]['data']['lat'];
    ids[i] = Terkep[i]['data']['id'];
    i = i + 1;
   
    
id_start = min(ids);

print(Terkep[i]['data']['nd']);

way = Terkep[len(Terkep)-3]['data']['nd'];
longitudes_2 = numpy.zeros(len(Terkep)-3);
latitudes_2 = numpy.zeros(len(Terkep)-3);
i = 0;

while i < len(Terkep)-3:
    longitudes_2[i] = 0.5 * longitudes[FL.find_id_index(ids, way[i])];
    latitudes_2[i] = latitudes[FL.find_id_index(ids, way[i])];
    i = i + 1;        
    print(i);


print(ids);
plt.plot(longitudes_2,latitudes_2);
plt.axes().set_aspect('equal');
plt.show();