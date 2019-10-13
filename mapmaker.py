import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.lines import Line2D
from PIL import Image, ImageOps, ImageColor, ImageFont, ImageDraw

# define city/cities
while True:
        try:
                city = input("Please enter a city (e.g. Los Angeles, California, USA \n OR Tokyo, Japan) ")
                G = ox.graph_from_place(city, network_type="all", simplify=True)
                break
        except:
                city = input("Sorry, that format was not recognized by OpenStreetMap. Try again. ")
                G = ox.graph_from_place(city, network_type = "all", simplify = True)


#city = ["Portland, Oregon, USA"]

print("data: obtained")

# unpack data
u = []
v = []
key = []
data = []
for uu, vv, kkey, ddata in G.edges(keys = True, data = True):
        u.append(uu)
        v.append(vv)
        key.append(kkey)
        data.append(ddata)

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

# Center of map
latitude = 45.5051
longitude = -122.6750

# Bbox sides
north = latitude + 0.035
south = latitude - 0.035
east = longitude + 0.05
west = longitude - 0.05

print("drawing map")

# Make Map
fig, ax = ox.plot_graph(G, node_size=0, bbox = (north, south, east, west), margin = 0, fig_height=30, fig_width=30, dpi = 300,  bgcolor = "#061529", save=False, edge_color=roadColors, edge_linewidth=roadWidths, edge_alpha=1)

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
fig.savefig(city.split()[0][:-1] + ".png", dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=True)


