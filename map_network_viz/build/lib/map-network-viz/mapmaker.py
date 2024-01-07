#imports
import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.lines import Line2D
from geopy import geocoders
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from pprint import pprint

PALETTE_A = ["#AAE28D", "#37D2BB", "#E76F51", "#27BACE", "#ED4591"]
PALETTE_B = ["#FFB7C3", "#F57A80", "#F6BD60", "#17BEBB", "#F0F2A6"]
PALETTE_C = ["#FFB7C3", "#750d37", "#F57A80", "#F6BD60", "#AAE28D", "#aadaba", "#27BACE", "#F0F2A6"]
PALETTE = PALETTE_C

def graph_city(city, PALETTE, distance_km=3000, color_code_by='road-type', save=True):
    """
    """
    
    plt.ioff()
    legend = True
    geolocator = Nominatim(user_agent="sejaldua@gmail.com")

    while True:
        try:
            city = input("Please enter a city (e.g. Los Angeles, California, USA OR Tokyo, Japan) ")
            loc = geolocator.geocode(city)
            latitude = loc.latitude
            longitude = loc.longitude
            G = ox.graph_from_point((latitude, longitude), distance_km, network_type="all", retain_all=True, simplify=False)
            print(ox.stats.basic_stats(G))
            break
        except:
            print("Sorry, that format was not recognized by OpenStreetMap. Try again.")

    u, v, key, data = [], [], [], []
    for u_elem, v_elem, key_elem, data_elem in G.edges(keys = True, data = True):
            u.append(u_elem)
            v.append(v_elem)
            key.append(key_elem)
            data.append(data_elem)

    roadColors = []
    if color_code_by == 'length':
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
    elif color_code_by == 'road-type':
        for item in data:
            if "highway" in item.keys() and item['highway'] != 'service':
                if item["highway"] in ['footway', 'pedestrian']:
                    color = PALETTE[0]
                elif item["highway"] in ['primary', 'primary_link']:
                    color = PALETTE[1]
                elif item["highway"] in ['secondary', 'secondary_link']:
                    color = PALETTE[2]
                elif item["highway"] in ['tertiary', 'tertiary_link']:
                    color = PALETTE[3]
                elif item["highway"] == 'cycleway':
                    color = PALETTE[4]
                elif item["highway"] in ['motorway', 'motorway_link']:
                    color = PALETTE[5]
                elif item["highway"] == 'residential':
                    color = PALETTE[6]
                else:
                    color = PALETTE[7]
            roadColors.append(color)

    roadWidths = [1 if item['highway'] == 'footway' else 2.5 for item in data]

    # Make Map
    fig, ax = ox.plot_graph(G, 
        node_size=0, 
        # bbox = (north, south, east, west), 
        figsize=(40,40), 
        dpi = 300,  
        bgcolor = "#1C3144", 
        save=False, 
        edge_color=roadColors, 
        edge_linewidth=roadWidths, 
        edge_alpha=1
    );

    if legend:
        # text and marker size
        markersize = 10
        fontsize = 10

        # add legend
        legend_elements = [Line2D([0], [0], marker='s', color="#061529", label= 'Length < 100 m', markerfacecolor="#d40a47", markersize=markersize), 
                Line2D([0], [0], marker='s', color="#061529", label= 'Length between 100-200 m', markerfacecolor="#e78119", markersize=markersize), 
                Line2D([0], [0], marker='s', color="#061529", label= 'Length between 200-400 m', markerfacecolor="#30bab0", markersize=markersize), 
                Line2D([0], [0], marker='s', color="#061529", label= 'Length between 400-800 m', markerfacecolor="#bbbbbb", markersize=markersize), 
                Line2D([0], [0], marker='s', color="#061529", label= 'Length > 800 m', markerfacecolor="w", markersize=markersize)]                 
        l = ax.legend(handles=legend_elements, bbox_to_anchor=(0.0, 0.0), frameon=True, ncol=1, facecolor = '#061529', framealpha = 0.9, loc='lower left',  fontsize = fontsize, prop={'family':"Georgia", 'size':fontsize})  

        # legend font color
        for text in l.get_texts():
            text.set_color("w")

    # save figure
    if save:
        name = city[0:(city.find(','))]
        name = name.replace(" ", "_")
        suffix = "_B" if PALETTE == PALETTE_B else '_A' 
        fig.savefig(f'./maps/{name}{suffix}.png', dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=False);


