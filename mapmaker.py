#imports
import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.lines import Line2D
from geopy import geocoders
from geopy.geocoders import Nominatim
from PIL import Image, ImageOps, ImageColor, ImageFont, ImageDraw
import matplotlib.pyplot as plt

PALETTE_A = ["#AAE28D", "#37D2BB", "#E76F51", "#27BACE", "#ED4591"]
PALETTE_B = ["#FFB7C3", "#F57A80", "#F6BD60", "#17BEBB", "#F0F2A6"]
PALETTE = PALETTE_B

plt.ioff()

geolocator = Nominatim(user_agent="sejaldua@gmail.com")

while True:
    try:
        city = input("Please enter a city (e.g. Los Angeles, California, USA OR Tokyo, Japan) ")
        G = ox.graph_from_place(city, network_type="all", simplify=True)
        print(ox.stats.basic_stats(G))
        break
    except:
        print("Sorry, that format was not recognized by OpenStreetMap. Try again.")

# locate latitude and longitude of the city to place it in the center of the map
loc = geolocator.geocode(city)
latitude = loc.latitude
longitude = loc.longitude
print('------------------------')
print('latitude:', latitude)
print('longitude:', longitude)
print('------------------------')

u, v, key, data = [], [], [], []
for u_elem, v_elem, key_elem, data_elem in G.edges(keys = True, data = True):
        u.append(u_elem)
        v.append(v_elem)
        key.append(key_elem)
        data.append(data_elem)

roadColors = []
print(data)
for item in data:
    if "length" in item.keys():
        if item["length"] <= 100:
            color = PALETTE[0]
        elif item["length"] > 100 and item["length"] <= 200:
            color = PALETTE[1]
        elif item["length"] > 200 and item["length"] <= 400:
            color = PALETTE[2]
        elif item["length"] > 400 and item["length"] <= 800:
            color = PALETTE[3]
        else:
            color = PALETTE[4]
    roadColors.append(color)

roadWidths = []
for item in data:
    if "footway" in item["highway"]:
        linewidth = 1
    else:
        linewidth = 2.5

    roadWidths.append(linewidth)

north = latitude + 0.035
south = latitude - 0.035
east = longitude + 0.05
west = longitude - 0.05

# Make Map
fig, ax = ox.plot_graph(G, node_size=0, bbox = (north, south, east, west), figsize=(40,40), dpi = 300,  
    bgcolor = "#1C3144", save=False, edge_color=roadColors, edge_linewidth=roadWidths, edge_alpha=1);

# text and marker size
# markersize = 12
# fontsize = 12

# add legend
# legend_elements = [Line2D([0], [0], marker='s', color="#061529", label= 'Length < 100 m', markerfacecolor="#d40a47", markersize=markersize), 
#         Line2D([0], [0], marker='s', color="#061529", label= 'Length between 100-200 m', markerfacecolor="#e78119", markersize=markersize), 
#         Line2D([0], [0], marker='s', color="#061529", label= 'Length between 200-400 m', markerfacecolor="#30bab0", markersize=markersize), 
#         Line2D([0], [0], marker='s', color="#061529", label= 'Length between 400-800 m', markerfacecolor="#bbbbbb", markersize=markersize), 
#         Line2D([0], [0], marker='s', color="#061529", label= 'Length > 800 m', markerfacecolor="w", markersize=markersize)]                 
# l = ax.legend(handles=legend_elements, bbox_to_anchor=(0.0, 0.0), frameon=True, ncol=1, facecolor = '#061529', framealpha = 0.9, loc='lower left',  fontsize = fontsize, prop={'family':"Georgia", 'size':fontsize})  

# legend font color
# for text in l.get_texts():
#     text.set_color("w")

# save figure
name = city[0:(city.find(','))]
name = name.replace(" ", "_")
suffix = "_B" if PALETTE == PALETTE_B else '_A' 
fig.savefig(f'./city_maps/{name}{suffix}.png', dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=False);

#--------------------------------------------------------------------


