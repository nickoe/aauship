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
Terkep = MapObj.Map(-36.432, 65.675, -35.99, 66.029);

i = 0;
n = 0; ''' Number of Ways'''
ids = numpy.zeros(1000); ''' Way IDs'''
m = 0;

while i < len(Terkep):
    if 'nd' in Terkep[i]['data'].keys():
        ids[n] = Terkep[i]['data']['id'];
        n = n+1;
    i = i+1;

#print(ids)
    
while m < n:
    if ids[m] == 0:
        break;
    
    wayObj = MapObj.WayGet(ids[m]);
    
    way = wayObj['nd'];
    
    longitudes = numpy.zeros(len(way));
    latitudes = numpy.zeros(len(way));
    
    i = 0;
    
    while i < len(way):
        node = MapObj.NodeGet(way[i]);
        #print(node);
        longitudes[i] = node['lon'];
        latitudes[i] = node['lat'];
        i = i + 1;        
        #print(i);
    
    
    #print(ids);
    plt.plot(longitudes,latitudes, 'k');
    
    m = m + 1;

#plt.axes().set_aspect('equal'); 
plt.show();