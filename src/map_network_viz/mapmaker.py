#imports
import osmnx as ox
from matplotlib.lines import Line2D
from geopy import geocoders
import matplotlib.pyplot as plt
import re

# PALETTE_A = ["#AAE28D", "#37D2BB", "#E76F51", "#27BACE", "#ED4591"]
# PALETTE_B = ["#FFB7C3", "#F57A80", "#F6BD60", "#17BEBB", "#F0F2A6"]
DEFAULT_PALETTE = ["#FFB7C3", "#750d37", "#F57A80", "#F6BD60", "#AAE28D", "#aadaba", "#27BACE", "#F0F2A6"]

def geocode(query):
    """
    Geocode a point of interest from the Photon geocoder, built on top of OpenStreetMap.

    Parameters:
    query (str): The point of interest to geocode.
    
    Returns:
    tuple: The latitude and longitude of the point of interest.
    """

    geo_obj = geocoders.Photon()
    cleaned_str = re.sub(r'[^\w\s]','',query).replace(' ', '+').lower()
    try:
        result = geo_obj.geocode(cleaned_str, exactly_one=True)
    except:
        raise ValueError("The entered query was not recognized by the geocoder. Please try again.")
    return (result.latitude, result.longitude)

def generate_map(city, PALETTE=DEFAULT_PALETTE, distance_km=3000, color_code_by='road-type', include_legend=True, save=True):
    """
    Generates a graph of the city using OpenStreetMap and netowrkx functionality from the osmnx library.

    Parameters
    ----------
    city : str
        The city to graph.
    PALETTE : list
        The list of colors to use for the graph.
    distance_km : int
        The distance (in kilometers) within which to graph the city.
    color_code_by : str
        The type of attribute to use to color the graph. Options are 'road-type' or 'length'. Defaults to 'road-type'.
    include_legend : bool
        Whether or not to add a legend to the graph.
    save : bool
        Whether or not to save the graph as a png file.

    Returns
    -------
    The Matplotlib figure containing the graph.
    """
    
    plt.ioff()

    try:
        latitude, longitude = geocode(city)
        G = ox.graph_from_point((latitude, longitude), distance_km, network_type="all", retain_all=True, simplify=False)
    except:
        raise ValueError("City format was not recognized by OpenStreetMap. Please try specifying a city name in the format of 'City, State, Country'.")

    # get street data from the edges of the graph
    data = []
    for _, _, _, data_elem in G.edges(keys = True, data = True):
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

    if include_legend:
        markersize = 10
        fontsize = 10
        if color_code_by == 'length':
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

        for text in l.get_texts():
            text.set_color("w")

    if save:
        name = city[0:(city.find(','))].replace(" ", "_")
        fig.savefig(f'{name}.png', dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=False);

    return fig