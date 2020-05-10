
tile_width = 36
tile_height = 18


def get_pixel_coords(x_tile, y_tile):
    """magic formula math for converting tile
       coordinates to screen coordinates"""
    x = ((x_tile - y_tile) * int(tile_width / 2)) - int(tile_width / 2)
    y = ((y_tile + x_tile) * int(tile_height / 2))
    return (int(x), int(y))


def get_map_coords(pos, x_shift, y_shift, background_x_middle):
    x_true = (pos[0] - x_shift) - (background_x_middle - x_shift)
    y_true = pos[1] - y_shift
    x = (x_true / tile_width / 2 + y_true / tile_height / 2) / 2
    y = (y_true / tile_height / 2 - x_true / tile_width / 2) / 2
    return (int(x), int(y))
