import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.lines import Line2D
from geopy import geocoders
from geopy.geocoders import Nominatim
from PIL import Image, ImageOps, ImageColor, ImageFont, ImageDraw
geolocator = Nominatim()

# define city/cities
while True:
        try:
                city = input("Please enter a city (e.g. Los Angeles, California, USA \n OR Tokyo, Japan) ")
                G = ox.graph_from_place(city, network_type="all", simplify=True)
                break
        except:
                print("Sorry, that format was not recognized by OpenStreetMap. Try again.")


# Center of map
loc = geolocator.geocode(city)
latitude = loc.latitude
longitude = loc.longitude

print("data: obtained")

# unpack data
u, v, key, data = [], [], [], []
for u_elem, v_elem, key_elem, data_elem in G.edges(keys = True, data = True):
        u.append(u_elem)
        v.append(v_elem)
        key.append(key_elem)
        data.append(data_elem)

print("data: unpacked")

# assign each segment a color based on its length
roadColors = []
for item in data:
    if "length" in item.keys():
        
        if item["length"] <= 100:
            color = "#d40a47"
            
        elif item["length"] > 100 and item["length"] <= 200:
            color = "#e78119"
            
        elif item["length"] > 200 and item["length"] <= 400:
            color = "#30bab0"
            
        elif item["length"] > 400 and item["length"] <= 800:
            color = "#bbbbbb"
            
        else:
            color = "w"
             
    roadColors.append(color)

# assign each segment a width based on its type
roadWidths = []
for item in data:
        if "footway" in item["highway"]:
                linewidth = 1
        else:
                linewidth = 2.5

        roadWidths.append(linewidth)

# Bbox sides
north = latitude + 0.035
south = latitude - 0.035
east = longitude + 0.05
west = longitude - 0.05

print("drawing map")

# Make Map
fig, ax = ox.plot_graph(G, node_size=0, bbox = (north, south, east, west), margin = 0, fig_height=40, fig_width=40, dpi = 300,  bgcolor = "#061529", save=False, edge_color=roadColors, edge_linewidth=roadWidths, edge_alpha=1)

print("plotted graph")

# Text and marker size
markersize = 12
fontsize = 12

# Add legend
legend_elements = [Line2D([0], [0], marker='s', color="#061529", label= 'Length < 100 m', markerfacecolor="#d40a47", markersize=markersize), Line2D([0], [0], marker='s', color="#061529", label= 'Length between 100-200 m', markerfacecolor="#e78119", markersize=markersize), Line2D([0], [0], marker='s', color="#061529", label= 'Length between 200-400 m', markerfacecolor="#30bab0", markersize=markersize), Line2D([0], [0], marker='s', color="#061529", label= 'Length between 400-800 m', markerfacecolor="#bbbbbb", markersize=markersize), Line2D([0], [0], marker='s', color="#061529", label= 'Length > 800 m', markerfacecolor="w", markersize=markersize)]    
                      
l = ax.legend(handles=legend_elements, bbox_to_anchor=(0.0, 0.0), frameon=True, ncol=1, facecolor = '#061529', framealpha = 0.9, loc='lower left',  fontsize = fontsize, prop={'family':"Georgia", 'size':fontsize})  

print("made the legend")
  
# Legend font color
for text in l.get_texts():
    text.set_color("w")
    
print("saving")

# Save figure
name = city[0:(city.find(','))]
name = name.replace(" ", "_")
fig.savefig(name + ".png", dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=True)


