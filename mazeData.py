class MazeData(object):
    def __init__(self, dims, boundaries, startCell, endCell):
        # dims must be a 2-tuple with form (rows, cols)
        # there will be rows*cols cells in the maze, indexed 0 to rows*cols
        # boundaries is a set of integers; the absolute value of the integer
        # represents a cell, positive values represent a boundary above,
        # and negative values represent a boundary to the left
        self.dims = dims
        self.startCell = startCell
        self.endCell = endCell
        self.boundaries = boundaries
    
    # helper functions for drawMaze
    def drawCellColors(self, canvas, margin, w, h, cell_w, cell_h):
        # draw checkerboard with grey squares
        for r in range(self.dims[0]):
            for c in range(self.dims[1]):
                if ((r % 2 == 0) and (c % 2 == 0)) or \
                    ((r % 2 != 0) and (c % 2 != 0)):
                    canvas.create_rectangle(margin + (c*cell_w),
                                            margin + (r*cell_h),
                                            margin + ((1+c)*cell_w),
                                            margin + ((1+r)*cell_h),
                                            fill='#e3e3e3',
                                            width=0)

        # draw start and end squares
        sr = self.startCell // self.dims[1]
        sc = self.startCell % self.dims[1]
        er = self.endCell // self.dims[1]
        ec = self.endCell % self.dims[1]
        canvas.create_rectangle(margin + (sc*cell_w),
                                margin + (sr*cell_h),
                                margin + ((1+sc)*cell_w),
                                margin + ((1+sr)*cell_h),
                                fill='#85f781',
                                width=0)
        canvas.create_rectangle(margin + (ec*cell_w),
                                margin + (er*cell_h),
                                margin + ((1+ec)*cell_w),
                                margin + ((1+er)*cell_h),
                                fill='#81f7eb',
                                width=0)
        if sr == 0:
            canvas.create_text(margin + ((sc + 0.5)*cell_w),
                               (2 * margin // 3),
                               anchor='center',
                               text='START',
                               font=('Courier %d bold' % (cell_w // 4)),
                               fill='#5db85a')
        elif sr == self.dims[0] - 1:
            canvas.create_text(margin + ((sc + 0.5)*cell_w),
                               h - (2 * margin // 3),
                               anchor='center',
                               text='START',
                               font=('Courier %d bold' % (cell_w // 4)),
                               fill='#5db85a')
        else:
            word = 'START'
            for i in range(5):
                canvas.create_text(2 * margin // 3,
                                   margin + ((sr + 0.25*i)*cell_h),
                                   anchor='center',
                                   text=word[i],
                                   font='Courier %d bold' % (cell_h // 4),
                                   fill='#5db85a')

        if er == 0:
            canvas.create_text(margin + ((ec + 0.5)*cell_w),
                               (2 * margin // 3),
                               anchor='center',
                               text='END',
                               font=('Courier %d bold' % (cell_w // 4)),
                               fill='#5cb5ac')
        elif er == self.dims[0] - 1:
            canvas.create_text(margin + ((ec + 0.5)*cell_w),
                               h - (2 * margin // 3),
                               anchor='center',
                               text='END',
                               font=('Courier %d bold' % (cell_w // 4)),
                               fill='#5cb5ac')
        else:
            word = 'END'
            for i in range(3):
                canvas.create_text(2 * margin // 3,
                                   margin + ((er + 0.25*(i+1))*cell_h),
                                   anchor='center',
                                   text=word[i],
                                   font='Courier %d bold' % (cell_h // 4),
                                   fill='#5cb5ac')

    def drawBoundaries(self, canvas, margin, w, h, cell_w, cell_h):
        canvas.create_line(margin, margin, w - margin, margin,
                           width=7, capstyle='round')
        canvas.create_line(margin, margin, margin, h - margin,
                           width=7, capstyle='round')
        canvas.create_line(margin, h - margin, w - margin, h - margin,
                           width=7, capstyle='round')
        canvas.create_line(w - margin, margin, w - margin, h - margin,
                           width=7, capstyle='round')

        for boundary in self.boundaries:
            b = abs(boundary)
            if b < self.dims[0] * self.dims[1]:
                r = b // self.dims[1]
                c = b % self.dims[1]
                if boundary > 0:
                    canvas.create_line(margin + (cell_w * c),
                                       margin + (cell_h * r),
                                       margin + (cell_w * (c+1)),
                                       margin + (cell_h * r),
                                       width=5, capstyle='round',
                                       tags=('b',))
                else:
                    canvas.create_line(margin + (cell_w * c),
                                       margin + (cell_h * r),
                                       margin + (cell_w * c),
                                       margin + (cell_h * (r+1)),
                                       width=5, capstyle='round',
                                       tags=('b',))

    # draws maze onto the canvas based on data + white background
    def drawMaze(self, canvas, w, h):
        canvas.create_rectangle(0, 0, w, h, fill='white')
        margin = min(w, h) / 10
        cell_w = (w - (2*margin)) / self.dims[1]
        cell_h = (h - (2*margin)) / self.dims[0]
        self.drawCellColors(canvas, margin, w, h, cell_w, cell_h)
        self.drawBoundaries(canvas, margin, w, h, cell_w, cell_h)
        


    def updateRows(self, rs, canvas, w, h):
        # update start/end cells if they're on the bottom row
        if (self.startCell >= self.dims[1]*(self.dims[0]-1)):
            self.startCell = (int(rs.get())-1) * self.dims[1] + \
                             self.startCell % self.dims[1]
        if (self.endCell >= self.dims[1]*(self.dims[0]-1)):
            self.endCell = (int(rs.get())-1) * self.dims[1] + \
                           self.endCell % self.dims[1]

        self.dims = (int(rs.get()), self.dims[1])

        self.drawMaze(canvas, w, h)
    
    def updateCols(self, cs, canvas, w, h):
        # update start/end cells if they're on the right
        if (self.startCell % self.dims[1] == self.dims[1] - 1):
            self.startCell = (self.startCell // self.dims[1] + 1) * \
                             int(cs.get()) - 1
        if (self.endCell % self.dims[1] == self.dims[1] - 1):
            self.endCell = (self.endCell // self.dims[1] + 1) * \
                           int(cs.get()) - 1
        
        self.dims = (self.dims[0], int(cs.get()))

        self.drawMaze(canvas, w, h)
    
    def updateStartEndCells(self):
        pass
        # ??? don't know if i'll need this
        # want changing location of start and end cells feature to be disabled
        # when:
        # an animation is running
        # when we're in generate mode, and there's a human-drawn solution still
        # there
        # MAKE IT SO THEY JUST CAN'T BE PUT ON THE SAME SQUARE (text would overlap)
        
    def clearMaze(self, stateData, canvas, w, h):
        if (stateData.mode == 'sol'):
            self.boundaries = set()
        else:
            pass
        self.drawMaze(canvas, w, h)  
        # to be called when Clear Maze button is pressed
        # updates MazeData object, clearing boundaries/solve line,
        # depending on what mode it's in

        # TODO only mode necessary for this, not whole stateData object