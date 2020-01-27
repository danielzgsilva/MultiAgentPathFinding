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
        '''
        Reserve coordinate (x,y) at time t
        '''

        if self.in_range(x, y, t):
            self.table[t][y][x] = False
        else:
            assert ValueError('Reservation out of range')

    def is_blocked(self, x, y, t):
        '''
        Returns true if coordinate (x,y) is blocked at time t
        '''

        if self.in_range(x, y, t):
            return not self.table[t][y][x]
        else:
            assert ValueError('Could not determine if cell is occupied because input was out of range')

    def unblock(self, x, y, t):
        '''
        Set coordinate (x,y) to available at time t
        '''

        if self.in_range(x, y, t):
            self.table[t][y][x] = True
        else:
            assert ValueError('Reservation out of range')

    def in_range(self, x, y ,t):
        '''
        Ensures parameters x, y, and t are not out of bounds
        '''

        return t < self.time and x >= 0 and y >= 0 and x < self.cols and y < self.rows

