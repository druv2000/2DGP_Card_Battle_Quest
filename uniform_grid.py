# uniform_grid.py

class UniformGrid:
    def __init__(self, width, height, cell_size):
        self.cell_size = cell_size
        self.grid_width = width // cell_size + 1
        self.grid_height = height // cell_size + 1
        self.grid = [[[] for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def add_object(self, obj):
        if obj.can_target:
            cell_x, cell_y = self._get_cell(obj.x, obj.y)
            self.grid[cell_y][cell_x].append(obj)

    def remove_object(self, obj):
        if obj.can_target:
            cell_x, cell_y = self._get_cell(obj.x, obj.y)
            if obj in self.grid[cell_y][cell_x]:
                self.grid[cell_y][cell_x].remove(obj)

    def update_object(self, obj):
        self.remove_object(obj)
        self.add_object(obj)

    def get_nearby_objects(self, x, y, radius):
        start_cell_x, start_cell_y = self._get_cell(x - radius, y - radius)
        end_cell_x, end_cell_y = self._get_cell(x + radius, y + radius)

        nearby_objects = []
        for cell_y in range(max(0, start_cell_y), min(self.grid_height, end_cell_y + 1)):
            for cell_x in range(max(0, start_cell_x), min(self.grid_width, end_cell_x + 1)):
                nearby_objects.extend(self.grid[cell_y][cell_x])

        return nearby_objects

    def _get_cell(self, x, y):
        return int(x // self.cell_size), int(y // self.cell_size)