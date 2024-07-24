from geometry_lib.shapes import Shape

def calculate_area(shape: Shape):
    if isinstance(shape, Shape):
        return shape.area_calc()
    else:
        raise TypeError("Unsupported shape type")