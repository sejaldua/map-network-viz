import streamlit as st
import networkx as nx
import osmnx as ox
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.lines import Line2D
from geopy import geocoders
import matplotlib.pyplot as plt
import re
from pprint import pprint

def geocode_poi(poi):
    """
    Geocode a point of interest from the Photon geocoder, built on top of OpenStreetMap.

    Parameters:
    poi (str): The point of interest to geocode.
    
    Returns:
    tuple: The latitude and longitude of the point of interest.
    """

    geo_obj = geocoders.Photon()
    cleaned_poi = re.sub(r'[^\w\s]','',poi).replace(' ', '+').lower()
    result = geo_obj.geocode(cleaned_poi, exactly_one=True)
    pprint(result.raw)
    return (result.latitude, result.longitude)


st.set_page_config(page_title='Map Maker', page_icon='globe')

container1 = st.sidebar.container()
container2 = st.sidebar.container()

color_code_by = container2.selectbox('Color Code By', ['Road Type', 'Road Length'])
PALETTE = ["#FFB7C3", "#750d37", "#F57A80", "#F6BD60", "#AAE28D", "#aadaba", "#17BEBB", "#F0F2A6"]
BACKGROUND_COLOR = '#1C3144'
BACKGROUND_COLOR = container2.color_picker('Background Color', BACKGROUND_COLOR)
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



plt.ioff()
st.title('Map Maker')

include_legend = container2.toggle('Include legend', value=True)
query = container1.text_input("Enter a city name or point of interest")
container1.caption('Note: specify the state and/or country for more precise results')
col1, col2 = container1.columns(2)
latitude, longitude = None, None
if query != "":
    latitude, longitude = geocode_poi(query)
    latitude = col1.number_input('Latitude', value=latitude)
    longitude = col2.number_input("Longitude", value=longitude)
dist = container1.number_input('Distance (square meters) from center', value=5000)
if query != "" or (latitude is not None and longitude is not None):
    street_names = set()
    if container1.button('Make Map!'):
        st.toast('Getting map data from geopandas')
        with st.spinner():
            G = ox.graph_from_point((latitude, longitude), dist, network_type="all", retain_all=True, simplify=False)
            st.write(ox.stats.basic_stats(G))
  
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
                else:
                    color = BACKGROUND_COLOR
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
                else:
                    color = BACKGROUND_COLOR
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
            bgcolor = BACKGROUND_COLOR, 
            save=False, 
            edge_color=roadColors, 
            edge_linewidth=roadWidths, 
            edge_alpha=1
        );

        # text and marker size
        markersize = 12
        fontsize = 12

        if include_legend:
            if color_code_by == 'Road Length':
                legend_elements = [Line2D([0], [0], marker='s', color="#061529", label= 'Length < 100 m', markerfacecolor=PALETTE[0], markersize=markersize), 
                        Line2D([0], [0], marker='s', color="#061529", label= 'Length between 100-200 m', markerfacecolor=PALETTE[1], markersize=markersize), 
                        Line2D([0], [0], marker='s', color="#061529", label= 'Length between 200-400 m', markerfacecolor=PALETTE[2], markersize=markersize), 
                        Line2D([0], [0], marker='s', color="#061529", label= 'Length between 400-800 m', markerfacecolor=PALETTE[3], markersize=markersize), 
                        Line2D([0], [0], marker='s', color="#061529", label= 'Length > 800 m', markerfacecolor=PALETTE[4], markersize=markersize)]  
            else:
                legend_elements = [Line2D([0], [0], marker='s', color="#061529", label= 'Footway', markerfacecolor=PALETTE[0], markersize=markersize), 
                        Line2D([0], [0], marker='s', color="#061529", label= 'Primary', markerfacecolor=PALETTE[1], markersize=markersize), 
                        Line2D([0], [0], marker='s', color="#061529", label= 'Secondary', markerfacecolor=PALETTE[2], markersize=markersize), 
                        Line2D([0], [0], marker='s', color="#061529", label= 'Tertiary', markerfacecolor=PALETTE[3], markersize=markersize), 
                        Line2D([0], [0], marker='s', color="#061529", label= 'Cycleway', markerfacecolor=PALETTE[4], markersize=markersize),
                        Line2D([0], [0], marker='s', color="#061529", label= 'Motorway', markerfacecolor=PALETTE[5], markersize=markersize), 
                        Line2D([0], [0], marker='s', color="#061529", label= 'Residential', markerfacecolor=PALETTE[6], markersize=markersize),
                        Line2D([0], [0], marker='s', color="#061529", label= 'Other', markerfacecolor=PALETTE[7], markersize=markersize)]     
            l = ax.legend(handles=legend_elements, bbox_to_anchor=(0.0, 0.0), frameon=True, ncol=1, facecolor = '#061529', framealpha = 0.9, loc='lower left',  fontsize = fontsize, prop={'family':"Georgia", 'size':fontsize})  

            # legend font color
            for text in l.get_texts():
                text.set_color("w")

        st.pyplot(fig)
        name = re.sub(r'[^\w\s]','',query).replace(' ', '_')
        fn = f'{name}.png'
        plt.savefig(fn, dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=False)
        with open(fn, "rb") as img:
            btn = st.download_button(
                label="Download Map",
                data=img,
                file_name=fn,
                mime="image/png"
            )