import streamlit as st
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

st.set_page_config(page_title='Map Maker', page_icon='globe')

container1 = st.sidebar.container()
container2 = st.sidebar.container()

color_code_by = container2.selectbox('Color Code By', ['Road Type', 'Road Length'])
PALETTE = ["#FFB7C3", "#750d37", "#F57A80", "#F6BD60", "#AAE28D", "#aadaba", "#17BEBB", "#F0F2A6"]
col1, col2, col3 = container2.columns(3)
if color_code_by == 'Road Type':
    PALETTE[0] = col1.color_picker('Footway', PALETTE[0])
    PALETTE[1] = col2.color_picker('Primary', PALETTE[1])
    PALETTE[2] = col3.color_picker('Secondary', PALETTE[2])
    PALETTE[3] = col1.color_picker('Tertiary', PALETTE[3])
    PALETTE[4] = col2.color_picker('Cycleway', PALETTE[4])
    PALETTE[5] = col3.color_picker('Motorway', PALETTE[5])
    PALETTE[6] = col1.color_picker('Residential', PALETTE[6])
    PALETTE[7] = col2.color_picker('Other', PALETTE[7])
else:
    PALETTE[0] = col1.color_picker('< 100 meters', PALETTE[0])
    PALETTE[1] = col2.color_picker('100-200 meters', PALETTE[2])
    PALETTE[2] = col3.color_picker('200-400 meters', PALETTE[3])
    PALETTE[3] = col1.color_picker('400-800 meters', PALETTE[6])
    PALETTE[4] = col2.color_picker('> 800 meters', PALETTE[7])


legend_on = container2.toggle('Include legend', value=True)

plt.ioff()

geolocator = Nominatim(user_agent="sejaldua@gmail.com")


st.title('Map Maker')

mode = container1.selectbox('Choose map-maker mode', ['City Name', 'Geo-coordinates'])
city = ""
latitude, longitude = None, None
col1, col2 = container1.columns(2)
if mode == 'City Name':
    city = container1.text_input("Please enter a city (e.g. Los Angeles, California, USA OR Tokyo, Japan) ")
else:
    latitude = col1.number_input('Latitude')
    longitude = col2.number_input("longitude")
    dist = container1.number_input('Distance (square meters) from center', value=5000)
if city != "" or (latitude is not None and longitude is not None):
    if container1.button('Make Map!'):
        st.toast('Getting map data from geopandas')
        with st.spinner():
            if mode == 'City Name':
                loc = geolocator.geocode(city)
                latitude = loc.latitude
                longitude = loc.longitude
                dist = 5000
                G = ox.graph_from_point((latitude, longitude), dist, network_type="all", retain_all=True, simplify=False)
            else:
                G = ox.graph_from_point((latitude, longitude), dist, network_type="all", retain_all=True, simplify=False)
            print(ox.stats.basic_stats(G))

        st.toast('Color-coding streets and highways')
        u, v, key, data = [], [], [], []
        for u_elem, v_elem, key_elem, data_elem in G.edges(keys = True, data = True):
            u.append(u_elem)
            v.append(v_elem)
            key.append(key_elem)
            data.append(data_elem)

        roadColors = []
        if color_code_by == 'Road Length':
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
        elif color_code_by == 'Road Type':
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

        roadWidths = []
        for item in data:
            if "footway" in item["highway"]:
                linewidth = 0.8
            else:
                linewidth = 2

            roadWidths.append(linewidth)

        north = latitude + 0.035
        south = latitude - 0.035
        east = longitude + 0.05
        west = longitude - 0.05

        st.toast('Plotting map and legend')
        fig, ax = ox.plot_graph(G, 
            node_size=0, 
            # bbox = (north, south, east, west), 
            figsize=(12,12), 
            dpi = 300,  
            bgcolor = "#1C3144", 
            save=False, 
            edge_color=roadColors, 
            edge_linewidth=roadWidths, 
            edge_alpha=1
        );

        # text and marker size
        markersize = 12
        fontsize = 12

        if legend_on:
            # add legend
            legend_elements = [Line2D([0], [0], marker='s', color="#061529", label= 'Length < 100 m', markerfacecolor=PALETTE[0], markersize=markersize), 
                    Line2D([0], [0], marker='s', color="#061529", label= 'Length between 100-200 m', markerfacecolor=PALETTE[1], markersize=markersize), 
                    Line2D([0], [0], marker='s', color="#061529", label= 'Length between 200-400 m', markerfacecolor=PALETTE[2], markersize=markersize), 
                    Line2D([0], [0], marker='s', color="#061529", label= 'Length between 400-800 m', markerfacecolor=PALETTE[3], markersize=markersize), 
                    Line2D([0], [0], marker='s', color="#061529", label= 'Length > 800 m', markerfacecolor=PALETTE[4], markersize=markersize)]                 
            l = ax.legend(handles=legend_elements, bbox_to_anchor=(0.0, 0.0), frameon=True, ncol=1, facecolor = '#061529', framealpha = 0.9, loc='lower left',  fontsize = fontsize, prop={'family':"Georgia", 'size':fontsize})  

            # legend font color
            for text in l.get_texts():
                text.set_color("w")

        st.pyplot(fig)
        name = city[0:(city.find(','))]
        name = name.replace(" ", "_")
        # Save to file first or an image file has already existed.
        fn = f'{name}.png'
        plt.savefig(fn, dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=False)
        with open(fn, "rb") as img:
            btn = st.download_button(
                label="Download Map",
                data=img,
                file_name=fn,
                mime="image/png"
            )

