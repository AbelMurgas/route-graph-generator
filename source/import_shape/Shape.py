from datetime import datetime
import glob
import os
# Reading shape files
import shapefile as sf

# Data handling
import pandas as pd
import numpy as np

class Shape:

    def __init__(self):
        self.SHP_WINDOW_VALUE = 0.70

    def create_df_base(self) -> pd.DataFrame: 
        """
        This is the principal method of this class, uses all steps to create the df_route final
        """
        self.df_shp_files_unread = self.__obtain_shape_file()
        if len(self.df_shp_files_unread) > 0:
            self.df_shp_files = self.__read_shape_files()
            return self.df_shp_files
        else:
            print("Not have shapes in input/shp")
            return None

    def __obtain_shape_file(self) -> pd.DataFrame:
        """
        Reading the shapefiles from the directory

        Returns:
            pd.DataFrame: data frame with the shape list
        """
        shp_files = glob.glob('./input/shp/' + '*.shp') 
        if len(shp_files):
            df_shp_files = pd.DataFrame(shp_files, columns=['shape_files'])
            df_shp_files['route'] = df_shp_files['shape_files'] \
                .apply(lambda x: os.path.basename(x)) \
                .str.replace('.shp', '', regex=False).str.replace('_', '-', regex=False)
            # column RouteName with the filename only
            df_shp_files['RouteName'] = df_shp_files['shape_files'] \
                .apply(lambda x: os.path.basename(x)) \
                .str.replace('.shp', '', regex=False)
            return df_shp_files
        else:
            return None

    def __read_shape_files(self) -> pd.DataFrame:
        """
        Reading all shapefiles from their files and concatenating
        into new dataframe.

        Returns:
            pd.DataFrame: dataframe with all shapes read
        """
        def read_shapes(row):
            """
            Reads all shapefiles and Creates a dataframe for each route
            and returns it.

            Parameters:
                row (int): index of current row
            """
            shp = sf.Reader(row['shape_files']).shapes()
            df = pd.DataFrame(shp[0].points,
                              columns=['longitude', 'latitude'])
            df['route'] = row['route']
            df['sn'] = df.index + 1

            return df

        # First, we create a Series with a DataFrame for each route
        # containing the shapefile points.
        sr_shp_points = self.df_shp_files_unread.apply(
            lambda x: read_shapes(x),
            axis=1)
        # Second, using a list comprehension, we concatenate all
        # DataFrames in the Series into a single DataFrame
        df_shp_files_concat = pd.concat(
            [df for df in sr_shp_points], ignore_index=True)
        # Third, we merge the DataFrame with all individual routes
        # with all the shapefiles points for each route.
        df_shp_files = self.df_shp_files_unread.merge(
            df_shp_files_concat, on='route')
        return df_shp_files