import folium
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches

from department import Department
import pandas as pd
import geopandas as gpd
from simulated_annealing import simulated_annealing
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def get_departments_list():
    departments_data = pd.read_csv("data/departamentos.csv")
    departments_list = []
    for i in range(len(departments_data["Departamentos"])):
        name = departments_data["Departamentos"][i]
        location = tuple(map(float, departments_data["Location"][i].split(', ')))
        departments_list.append(Department(name, location))
    return departments_list


def save_html_map(route):
    peru_map = folium.Map(location=[-9.497415, -75.142212], zoom_start=6)
    for i in range(len(route)):
        folium.Circle(
            route[i].location,
            radius=10000,
            popup=route[i].name,
            color="crimson",
            fill=True,
        ).add_to(peru_map)
        if i < len(route) - 1:
            folium.PolyLine(
                [route[i].location, route[i + 1].location],
                color="blue",
                weight=2.5,
                opacity=1
            ).add_to(peru_map)
        else:
            folium.PolyLine(
                [route[i].location, route[0].location],
                color="blue",
                weight=2.5,
                opacity=1
            ).add_to(peru_map)
    peru_map.save("peru_map.html")


def draw_complete_map(route, temp, distance, i_best, cooling_index):
    url_data = "https://raw.githubusercontent.com/juaneladio/peru-geojson/master/peru_departamental_simple.geojson"
    region_geojson = gpd.read_file(url_data)
    c_map = ListedColormap(['white' for _ in range(25)], name='test')
    region_geojson.plot(figsize=(20, 20), edgecolor='black', cmap=c_map)
    plt.xlabel('longitude')
    plt.ylabel('latitude')

    for i in range(len(route) - 1):
        plt.plot(route[i].longitude, route[i].latitude, marker='o', color="red")
        x_values = [route[i].longitude, route[i + 1].longitude]
        y_values = [route[i].latitude, route[i + 1].latitude]
        plt.plot(x_values, y_values)
    plt.plot(route[len(route) - 1].longitude, route[len(route) - 1].latitude, marker='o', color="red")
    x_values = [route[len(route) - 1].longitude, route[0].longitude]
    y_values = [route[len(route) - 1].latitude, route[0].latitude]
    plt.plot(x_values, y_values)
    red_patch = mpatches.Patch(color="red", label=f'Temperatura: {temp:.20f}')
    blue_patch = mpatches.Patch(color="blue",label=f'Distancia: {round(distance, 6)} Km')
    green_patch = mpatches.Patch(color="green",label=f'Iteracion: {i_best}')
    teal_patch = mpatches.Patch(color="teal",label=f'Indice de enfriamiento: {cooling_index}')
    plt.legend(handles=[red_patch,blue_patch, green_patch, teal_patch])
    plt.show()


def main():
    departments = get_departments_list()
    best_route, temp, distance, i_best, cooling_index  = simulated_annealing(departments, 20000)
    save_html_map(best_route)
    draw_complete_map(best_route, temp, distance, i_best, cooling_index)

if __name__ == '__main__':
    main()
   
  



