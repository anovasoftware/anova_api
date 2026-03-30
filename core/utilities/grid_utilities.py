from apps.static.models import Grid


class GridUtility(object):
    def __init__(self, grid_id):
        self.grid_id = grid_id
        self.grid = None

    def get_grid(self):
        grid = Grid.objects.values(
            'grid_id',
            'description',
        ).get(
            pk=self.grid_id
        )
        return grid
