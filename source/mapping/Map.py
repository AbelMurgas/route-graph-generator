import folium
from folium import plugins
from branca.element import Figure
import pandas as pd
import numpy as np


class Map:
    def __init__(self, data: pd.DataFrame, route_name = "route_code",group_name = "route_code", graph_type = "lineal", latitude_name = "latitude", longitude_name = "longitude"):
        """
        Args:
            data (pd.DataFrame): data frame that contains all information to create the graph\n
            route_name (str, optional): the column name in the dataframe that contains the name of the route. Defaults to "route_code".\n
            group_name (str, optional): the group that use to separate the route, 
            if want to graph like arch must put the name of the stops 
            else if want to graph all the route use the same name of the route name\n. Defaults to "route_code" (graph only the route).
            graph_type (str, optional): Only have 3 type of graph 'lineal' , 'marker' or 'cirle' graph. Defaults to "lineal".\n
            latitude_name (str, optional): _description_. Defaults to "latitude".\n
            longitude_name (str, optional): _description_. Defaults to "longitude".
        """
        self.data = data
        self.map = folium.Map()
        fig5 = Figure(height=550, width=750)
        fig5.add_child(self.map)
        self.group = folium.FeatureGroup()
        self.route_name = route_name
        self.group_name = group_name
        self.latitude_name = latitude_name
        self.longitude_name = longitude_name
        self.graph_type = graph_type
        self.colors = ['red', 'blue', 'green', 'purple',
                       'orange', 'darkred', 'beige',
                       'darkblue', 'darkgreen', 'cadetblue',
                       'pink', 'lightblue', 'lightgreen', 'gray',
                       'black', 'lightgray']
        if self.__check_data():
            self.add_data_to_map(self.data)

    def __check_data(self) -> bool:
        data_pass = True
        for i in [self.group_name,self.latitude_name,self.longitude_name]:
            if not i in self.data:
                print(f"ERROR: Dataframe not have {i} column name") 
                data_pass = False
        if not self.graph_type == 'lineal' or not self.graph_type == 'marker' or not self.graph_type == 'circle':
            print(f"ERROR: The graph type only permits 'linear' type or 'point' type, the input received is: {self.graph_type}") 
            data_pass = False
        return data_pass 

    def __prepare_data(self):
        self.data['coords'] = self.data[['latitude', 'longitude']] \
            .apply(tuple, axis=1)
        if not self.route_name == self.group_name:
            self.data[self.group_name] = self.data[self.route_name] + "-" + self.data[self.group_name]
        self.data['sequence_group'] = pd.Series(
            pd.factorize(self.data.group_name)[0])
        self.data['sequence_group'] = self.data['sequence_group'].ffill()+1
        self.data['color'] = self.data['sequence_group'].apply(lambda x: self.__assign_color(x))
        
    def __assign_color(self,number):
        cant_color = len(self.colors)
        number = number - (int(number/cant_color))*cant_color
        return self.colors[int(number)]
            
    def add_data_to_map(self):
        if self.graph_type == "lineal":
            self.__generate_lineal_graph()
        elif self.graph_type == "marker":
            self.__generate_marker_graph()
        else:
            self.__generate_circle_graph()
        folium.LayerControl().add_to(self.map)
        sw = self.data[['latitude', 'longitude']].min().values.tolist()
        ne = self.data[['latitude', 'longitude']].max().values.tolist()
        self.map.fit_bounds([sw, ne], max_zoom=15)
        
    def __generate_lineal_graph(self):
        for i in self.data[self.group_name].unique():
            f = folium.FeatureGroup(i)
            df_viaje = self.data.loc[self.data.loc[:, self.group_name] == i]
            coords = df_viaje['coords'].tolist()
            v_popup = df_viaje['coords'].unique()
            v_color = df_viaje['color'].unique()
            plugins.AntPath(coords,
                            popup=i,
                            tooltip=v_popup[0],
                            hardware_acceleration=True,
                            delay=400,
                            dash_array=[10, 48],
                            weight=6.5,
                            opacity=0.70,
                            color=v_color[0],
                            pulse_color=v_color[0]
                            ).add_to(f)
            f.add_to(self.map)

    def __generate_marker_graph(self):
        for i in self.data[self.group_name].unique():
            f = folium.FeatureGroup(i)
            df_viaje = self.data.loc[self.data.loc[:, self.group_name] == i]
            coords = df_viaje['coords'].tolist()
            v_popup = df_viaje['coords'].unique()
            v_color = df_viaje['color'].unique()
            folium.Marker(coords,
                          popup=v_popup,
                          icon=folium.Icon(color=v_color, icon_color=v_color)).add_to(f)
            f.add_to(self.map)

    def __generate_circle_graph(self, data, name = 'coords'):
        for i in self.data[self.group_name].unique():
            f = folium.FeatureGroup(i)
            df_viaje = self.data.loc[self.data.loc[:, self.group_name] == i]
            coords = df_viaje['coords'].tolist()
            v_popup = df_viaje['coords'].unique()
            v_color = df_viaje['color'].unique()
            folium.CircleMarker(coords,
                                popup=v_popup,
                                color='black',
                                fill_color='black',
                                radius=10).add_to(f)
            f.add_to(self.map)

    def create_map(self, name="map"):
        self.map.save(f"{name}.html")
