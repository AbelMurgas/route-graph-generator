from import_shape.Shape import Shape

if __name__ == '__main__':
    newShape = Shape()
    df_route = newShape.create_df_base()
    if len(df_route) > 0:
        print(df_route)