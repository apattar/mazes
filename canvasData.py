class CanvasData(object):
    def __init__(self, resizeRedrawDelay):
        self.resizeRedrawDelay = resizeRedrawDelay  # prevent resize redraw lagging
        self.resizeTracker = 0

    def resizeCanvas(self, canvas, mazeData):
        # to be called whenever the screen is resized.
        # mazeData is a MazeData object that should be passed in
        # canvas.update_idletasks()
        self.resizeTracker += 1
        if self.resizeTracker == self.resizeRedrawDelay:
            mazeData.drawMaze(canvas, canvas.winfo_width(),
                              canvas.winfo_height())
            self.resizeTracker = 0
    
    def mouseHovering(self, canvas, e, mode, mazeData, animating):
        # mode is a string with either 'sol' or 'gen'

        if animating: return

        w = canvas.winfo_width()
        h = canvas.winfo_height()
        margin = min(w, h) / 10
        cell_w = (w - (2*margin)) / mazeData.dims[1]
        cell_h = (h - (2*margin)) / mazeData.dims[0]
        r = (e.y - margin) // cell_h
        c = (e.x - margin) // cell_w
        if (mode == 'sol'):
            canvas.delete(*canvas.find_withtag('hoverBound'))
            if (margin < e.x < w - margin) and \
               (margin < e.y < h - margin):
                local_x = (e.x - margin) % cell_w
                local_y = (e.y - margin) % cell_h
                if (local_x > local_y) and (local_x > (cell_h - local_y)):
                    # draw boundary to right
                    canvas.create_line(margin + ((1+c)*cell_w),
                                       margin + (r*cell_h),
                                       margin + ((1+c)*cell_w),
                                       margin + ((1+r)*cell_h),
                                       stipple='gray50',
                                       width=5, capstyle='round',
                                       tags=('hoverBound'))         # TODO mazeData.boundaryWidth - replace everywhere
                elif (local_x > local_y):
                    # draw boundary up
                    canvas.create_line(margin + (c*cell_w),
                                       margin + (r*cell_h),
                                       margin + ((1+c)*cell_w),
                                       margin + (r*cell_h),
                                       stipple='gray50',
                                       width=5, capstyle='round',
                                       tags=('hoverBound'))
                elif (local_x > (cell_h - local_y)):
                    # draw boundary down
                    canvas.create_line(margin + (c*cell_w),
                                       margin + ((1+r)*cell_h),
                                       margin + ((1+c)*cell_w),
                                       margin + ((1+r)*cell_h),
                                       stipple='gray50',
                                       width=5, capstyle='round',
                                       tags=('hoverBound'))
                else:
                    # draw boundary to left
                    canvas.create_line(margin + (c*cell_w),
                                       margin + (r*cell_h),
                                       margin + (c*cell_w),
                                       margin + ((1+r)*cell_h),
                                       stipple='gray50',
                                       width=5, capstyle='round',
                                       tags=('hoverBound'))
        else:
            canvas.delete(*canvas.find_withtag('hoverNode'))
            # only want something to happen if in start square,
            # or current active square
            # if (margin < e.x < w - margin) and \
            #    (margin < e.y < h - margin):
            #     diameter = min(cell_w, cell_h) / 4
            #     canvas.create_oval()

        # what to do depends on mode
        # eventual support for changing start and end squares
        
        # lift and lower methods for canvas items allow
        # you to change the stacking order

        # if only need dims, no need to pass whole mazeData object

    def mouseClicked(self, canvas, e, mode, mazeData, w, h, animating):
        if animating: return
        
        print(mazeData.boundaries)  # TODO remove later
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        margin = min(w, h) / 10
        cell_w = (w - (2*margin)) / mazeData.dims[1]
        cell_h = (h - (2*margin)) / mazeData.dims[0]
        c = (e.x - margin) // cell_w
        r = (e.y - margin) // cell_h
        if (mode == 'sol'):
            if (margin < e.x < w - margin) and \
               (margin < e.y < h - margin):
                local_x = (e.x - margin) % cell_w
                local_y = (e.y - margin) % cell_h
                if (local_x > local_y) and (local_x > (cell_h - local_y)):
                    # add boundary to right
                    if (c != mazeData.dims[1] - 1):
                        boundary = int(-1 * (r*mazeData.dims[1] + c + 1))
                        if boundary in mazeData.boundaries:
                            mazeData.boundaries.remove(boundary)
                        else:
                            mazeData.boundaries.add(boundary)
                elif (local_x > local_y):
                    # add boundary up
                    if (r != 0):
                        boundary = int(r*mazeData.dims[1] + c)
                        if boundary in mazeData.boundaries:
                            mazeData.boundaries.remove(boundary)
                        else:
                            mazeData.boundaries.add(boundary)
                elif (local_x > (cell_h - local_y)):
                    # add boundary down
                    if (r != mazeData.dims[0] - 1):
                        boundary = int((r+1)*mazeData.dims[1] + c)
                        if boundary in mazeData.boundaries:
                            mazeData.boundaries.remove(boundary)
                        else:
                            mazeData.boundaries.add(boundary)
                else:
                    # add boundary to left
                    boundary = int(-1 * (r*mazeData.dims[1] + c))
                    if boundary in mazeData.boundaries:
                        mazeData.boundaries.remove(boundary)
                    else:
                        mazeData.boundaries.add(boundary)
            canvas.delete(*canvas.find_withtag('b'))
            mazeData.drawBoundaries(canvas, min(w, h) / 10, w, h,
                                    (w - (2*margin)) / mazeData.dims[1],
                                    (h - (2*margin)) / mazeData.dims[0])
            self.mouseHovering(canvas, e, mode, mazeData, False)
        else:
            pass

    def mouseDragging(self, canvas, e, mode, mazeData, w, h, animating):
        if animating: return
        
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        margin = min(w, h) / 10
        cell_w = (w - (2*margin)) / mazeData.dims[1]
        cell_h = (h - (2*margin)) / mazeData.dims[0]
        c = (e.x - margin) // cell_w
        r = (e.y - margin) // cell_h
        if (mode == 'sol'):
            if (margin < e.x < w - margin) and \
               (margin < e.y < h - margin):
                local_x = (e.x - margin) % cell_w
                local_y = (e.y - margin) % cell_h
                if (local_x > local_y) and (local_x > (cell_h - local_y)):
                    # add boundary to right
                    if (c != mazeData.dims[1] - 1):
                        boundary = int(-1 * (r*mazeData.dims[1] + c + 1))
                        if boundary not in mazeData.boundaries:
                            mazeData.boundaries.add(boundary)
                elif (local_x > local_y):
                    # add boundary up
                    if (r != 0):
                        boundary = int(r*mazeData.dims[1] + c)
                        if boundary not in mazeData.boundaries:
                            mazeData.boundaries.add(boundary)
                elif (local_x > (cell_h - local_y)):
                    # add boundary down
                    if (r != mazeData.dims[0] - 1):
                        boundary = int((r+1)*mazeData.dims[1] + c)
                        if boundary not in mazeData.boundaries:
                            mazeData.boundaries.add(boundary)
                else:
                    # add boundary to left
                    boundary = int(-1 * (r*mazeData.dims[1] + c))
                    if boundary not in mazeData.boundaries:
                        mazeData.boundaries.add(boundary)
            canvas.delete(*canvas.find_withtag('b'))
            mazeData.drawBoundaries(canvas, min(w, h) / 10, w, h,
                                    (w - (2*margin)) / mazeData.dims[1],
                                    (h - (2*margin)) / mazeData.dims[0]) 
        else:
            pass