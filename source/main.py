from import_shape.Shape import Shape
from  mapping.Map import Map
import pandas as pd
import webbrowser
if __name__ == '__main__':
    df_route = None
    # ---- Generate by .shp file ----
    # newShape = Shape()
    # df_route = newShape.create_df_base()
    # ---- Generate by Read a data frame with the infromation ----
    # df_route_name = "df_route.csv" # Name of the df_route file
    # df_route = pd.read_csv(df_route_name, delimiter=",")
    if len(df_route) > 0:
        map_name = "map"
        newMap = Map(df_route)
        newMap.create_map()
        webbrowser.open_new_tab(map_name + ".html")