# route-graph-generator
This project is about create a program that generate a chart of routes

## Usage

The read .shp option
conditions:
- must have all .shp file and other important file (.prj,.cpg,.dbf,.xml,.shx) in shp path

```python
newShape = Shape()
df_route = newShape.create_df_base()
if len(df_route) > 0:
    map_name = "map" # put file map name
    newMap = Map(df_route) 
    newMap.create_map()
    webbrowser.open_new_tab(map_name + ".html") # automatically open in browser
```

The read file with information option
conditions:
- csv
- coords column: latitude, longitude
- route column
- other group (optional if want to separate the routem in stops)
- important have the file outside of source path

```python
df_route_name = "df_route.csv" # Name of the df_route file
df_route = pd.read_csv(df_route_name, delimiter=",")
if len(df_route) > 0:
    map_name = "map" # put file map name
    newMap = Map(df_route) 
    newMap.create_map()
    webbrowser.open_new_tab(map_name + ".html") # automatically open in browser
```
