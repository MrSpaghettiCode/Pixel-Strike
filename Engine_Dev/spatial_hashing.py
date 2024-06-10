from math import floor

"""
http://mauveweb.co.uk/posts/2011/05/introduction-to-spatial-hashes.html
"""
class Collision_map:
    cell_size = 0
    cells = {}

    @staticmethod
    def initialize(cell_size):
        Collision_map.cell_size = cell_size
        Collision_map.cells = {}

    @staticmethod
    def add_rect(rect, obj):
        """Add an object obj with bounds r."""
        cells = Collision_map._cells_for_rect(rect)
        for c in cells:
            Collision_map._add(c, obj)

    @staticmethod
    def remove_rect(rect, obj):
        """Remove an object obj which had bounds r."""
        cells = Collision_map._cells_for_rect(rect)
        for c in cells:
            Collision_map._remove(c, obj)

    @staticmethod
    def reset():
        Collision_map.cells = {}

    @staticmethod
    def _add(cell_coord, o):
        """Add the object o to the cell at cell_coord."""
        #try:
        Collision_map.cells.setdefault(cell_coord, set()).add(o)
        #except KeyError:
        #    Collision_map.cells[cell_coord] = set((o,))

    @staticmethod
    def _cells_for_rect(rect):
        """Return a set of the cells into which the rect extends."""
        cells = set()
        cy = floor(rect[1] / Collision_map.cell_size)
        while (cy * Collision_map.cell_size) <= rect[3]: #while cell y position is less than the height of the rect
            cx = floor(rect[0] / Collision_map.cell_size)
            while (cx * Collision_map.cell_size) <= rect[2]:
                cells.add((int(cx), int(cy)))
                cx += 1.0
            cy += 1.0
        return cells
    
    @staticmethod
    def potential_collisions(rect, obj):
        """Get a set of all objects that potentially intersect obj."""
        cells = Collision_map._cells_for_rect(rect)

        potentials = set()
        for c in cells:
            cell = Collision_map.cells.get(c, set())
            potentials.update(cell)
        potentials.discard(obj) # obj cannot intersect itself
        return potentials

    @staticmethod
    def _remove(cell_coord, o):
        """Remove the object o from the cell at cell_coord."""
        cell = Collision_map.cells[cell_coord]
        cell.remove(o)

        # Delete the cell from the hash if it is empty.
        if not cell:
            del(Collision_map.cells[cell_coord])
