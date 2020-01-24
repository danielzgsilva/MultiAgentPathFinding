class ReservationTable:
    '''
    3D Time-Space reservation table used to avoid agent collisions
    '''

    def __init__(self, cols, rows, time):
        self.cols = cols
        self.rows = rows
        self.time = time

        # Create empty 3d time space table. True means available
        self.table = [[[True for _ in range(cols)] for _ in range(rows)] for _ in range(time)]

    def set_blocked(self, x, y, t):
        if t < self.time and x >= 0 and y >= 0 and x < self.cols and y < self.rows:
            self.table[t][y][x] = False
        else:
            assert ValueError('Reservation out of range')

    def is_blocked(self, x, y, t):
        return not self.table[t][y][x]

