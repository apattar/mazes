from tkinter import *
from tkinter import ttk

def rgbString(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)


class ApplicationStateData(object):
    solveAlgorithms = ['dfs', 'bfs', 'astar']   # dijkstra?
    genAlgorithms = ['ec', 'vc']    # possibly more?

    def __init__(self):
        self.mode = StringVar()
        self.setSolveMode()
        self.animationRunning = False  # bool
        self.currentAlgorithm = StringVar(value='dfs')
        # don't need to store some of these things twice - can just access them directly from the widget
    
    def setSolveMode(self):
        self.mode.set('Solve')
        # extend!!!
        # updates state to solve mode
        # also deals with mode button appearance
        # set algorithm
    
    def setGenerateMode(self):
        self.mode.set('Generate')
        # updates state to generate mode
        # also deals with mode button appearance
    
    def animate(self):
        pass
        # to be called when solve/generate button is clicked
        # use animationSpeedSlider.get() (widget) and algorithm.get() (a StringVar)
        # disable stuff that needs to be disabled; maybe set an 'animating' mode?
        # handles calling the step function when animation not in step mode - if in step mode, just do one step
    
    def stepAnimation(self):
        pass
        # advances animation, and redraws stuff
    
    def configAnimButtonPushed(self):
        pass

    def configAlgButtonPushed(self):
        pass

class MazeData(object):
    def __init__(self, dims, boundaries, startCell, endCell):
        # dims must be a 2-tuple with form (rows, cols)
        # there will be rows*cols cells in the maze, indexed 0 to rows*cols
        # boundaries is a set of integers; the absolute value of the integer
        # represents a cell, positive values represent a boundary to the right,
        # and negative values represent a boundary below
        self.dims = dims
        self.numCells = dims[0] * dims[1]
        self.startCell = startCell
        self.endCell = endCell
        self.boundaries = boundaries
    
    def drawMaze(self, canvas):
        pass
        # draws maze onto the canvas.
        # Things to remember:
        # checkered cells, with light grey
        # start and end squares light blue and green, respectively

    def updateRows(self):
        pass
        # updates the dims for the main maze and calls the redraw function.
        # to be called when dimensions are changed by the user
        # maybe combine this and updateCols into one updateDims?
    
    def updateCols(self):
        pass
    
    def updateStartEndCells(self):
        pass
        # ??? don't know if i'll need this
        # want changing location of start and end cells feature to be disabled
        # when:
        # an animation is running
        # when we're in generate mode, and there's a human-drawn solution still
        # there
        
    def clearMaze(self):
        pass
        # to be called when Clear Maze button is pressed
        # updates MazeData object, clearing boundaries/solve line,
        # depending on what mode it's in

class CanvasData(object):
    def __init__(self, resizeRedrawDelay):
        self.resizeRedrawDelay = resizeRedrawDelay  # prevent resize redraw lagging
        self.resizeTracker = 0

    def redrawCanvas(self, canvas, mazeData):
        # to be called whenever the screen is resized.
        # mazeData is a MazeData object that should be passed in
        # canvas.update_idletasks()
        self.resizeTracker += 1
        if self.resizeTracker == self.resizeRedrawDelay:
            w = canvas.winfo_width() + self.resizeRedrawDelay
            h = canvas.winfo_height() + self.resizeRedrawDelay
            # canvas['width'] = w - 4
            # canvas['height'] = h - 4
            canvas.create_rectangle(0, 0, w, h, fill='white')
            mazeData.drawMaze(canvas)
            self.resizeTracker = 0



if __name__ == '__main__':
    print('starting...')
    root = Tk()
    root.title('Mazes')

    # create the object instances that will store all the data
    mData = MazeData((6,6), set(), 0, 35)  # magic numbers - have defaultDims, etc.
    stateData = ApplicationStateData()
    cData = CanvasData(10)

    # initialize algorithm options, and set value of algorithm StringVar
    # initialize animation options, and set display accordingly


    # create widgets
    mainframe = ttk.Frame(root, relief='ridge', borderwidth=10)

    modeButtonsFrame = ttk.Frame(mainframe, relief='sunken', borderwidth=5)
    solveModeButton = ttk.Button(modeButtonsFrame, text='Solve Mode', width=30,
                                command=stateData.setSolveMode)
    genModeButton = ttk.Button(modeButtonsFrame, text='Generate Mode', width=30,
                            command=stateData.setGenerateMode)

    genControlsFrame = ttk.Frame(mainframe, relief='sunken', borderwidth=5)
    clearButton = ttk.Button(genControlsFrame, text='Clear Maze',
                            command=mData.clearMaze)
    rowsLabel = ttk.Label(genControlsFrame, text='Rows: ')
    rowsSpinbox = ttk.Spinbox(genControlsFrame, from_=1.0, to=30.0,
                            command=lambda: mData.updateRows())    # TODO disable when there's user-inputted stuff on the maze, or an animation running
    colsLabel = ttk.Label(genControlsFrame, text='Columns: ')
    colsSpinbox = ttk.Spinbox(genControlsFrame, from_=1.0, to=30.0,
                            command=lambda: mData.updateCols())    # TODO disable when there's user-inputted stuff on the maze, or an animation running
    # use rowsSpinbox.get() to get the value in the spinbox

    algDisplayFrame = ttk.Frame(mainframe, relief='sunken', borderwidth=5)
    algSupLabel = ttk.Label(algDisplayFrame, text='Algorithm:')
    algMainLabel = ttk.Label(algDisplayFrame, textvariable=stateData.currentAlgorithm,
                            anchor='center', relief='ridge', borderwidth=10)  # TODO more decoration?
    configAlgButton = ttk.Button(algDisplayFrame,
                                 text='Configure\nAlgorithm Options',
                                 command=stateData.configAlgButtonPushed)
    animationSpeedLabel = ttk.Label(algDisplayFrame, text='Animation Speed:')
    animationSpeedSlider = ttk.Scale(algDisplayFrame, orient=HORIZONTAL, length=30,
                                    from_=1.0, to=30.0)
    # use animationSpeedSlider.get()
    # PUT STEP OR SPEED THING BELOW algMainLabel
    animationStepButton = ttk.Button(algDisplayFrame, text='Step Animation',
                                     command=stateData.stepAnimation)   # grid only when in step mode
    configAnimButton = ttk.Button(algDisplayFrame,
                                  text='Configure\nAnimation Options',
                                  command=stateData.configAnimButtonPushed)


    solgenButton = ttk.Button(mainframe, textvariable=stateData.mode, command=stateData.animate)

    canvas = Canvas(mainframe, width=500, height=370)


















    # geometry management
    mainframe.grid(sticky='nsew', padx=10, pady=10)

    modeButtonsFrame.grid(row=0, columnspan=2, sticky='nsew', padx=5, pady=5)
    solveModeButton.grid(row=0, column=0, sticky='nse', padx=5, pady=5)
    genModeButton.grid(row=0, column=1, sticky='nsw', padx=5, pady=5)

    genControlsFrame.grid(row=1, column=0, sticky='new', padx=5, pady=5)
    clearButton.grid(row=0, column=0, columnspan=2, sticky='new', padx=5, pady=5)
    rowsLabel.grid(row=1, column=0, sticky='new', padx=5, pady=(10,5))
    rowsSpinbox.grid(row=1, column=1, sticky='new', padx=5, pady=(10,5))
    colsLabel.grid(row=2, column=0, sticky='new', padx=5, pady=(5,10))
    colsSpinbox.grid(row=2, column=1, sticky='new', padx=5, pady=(5,10))

    algDisplayFrame.grid(row=2, column=0, sticky='new', padx=5, pady=5)
    algSupLabel.grid(row=0, column=0, sticky='nsw', padx=5, pady=5)
    algMainLabel.grid(row=1, column=0, sticky='nsew', padx=5, pady=(5,10))
    configAlgButton.grid(row=0, rowspan=2, column=1, sticky='nsew', padx=5, pady=5)
    animationSpeedLabel.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
    animationSpeedSlider.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
    configAnimButton.grid(row=2, rowspan=2, column=1, sticky='nsew', padx=5, pady=5)

    solgenButton.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)

    canvas.grid(row=1, column=1, rowspan=3, sticky='nsew', padx=5, pady=5)


    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    mainframe.rowconfigure(1, weight=50)
    mainframe.rowconfigure(2, weight=50)
    mainframe.rowconfigure(3, weight=50)
    mainframe.columnconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=50)
    modeButtonsFrame.rowconfigure(0, weight=1)
    modeButtonsFrame.columnconfigure(0, weight=1)
    modeButtonsFrame.columnconfigure(1, weight=1)
    genControlsFrame.rowconfigure(0, weight=1)
    genControlsFrame.rowconfigure(1, weight=1)
    genControlsFrame.rowconfigure(2, weight=1)
    genControlsFrame.columnconfigure(0, weight=1)
    genControlsFrame.columnconfigure(1, weight=1)
    algDisplayFrame.rowconfigure(0, weight=1)
    algDisplayFrame.rowconfigure(1, weight=1)
    algDisplayFrame.columnconfigure(0, weight=1)
    algDisplayFrame.columnconfigure(1, weight=1)


    # Put this next block into function to initialize everything



    # put algorithm StringVar into AnimationStateData object

    rowsSpinbox.state(['readonly'])
    colsSpinbox.state(['readonly'])
    rowsSpinbox.set(6)
    colsSpinbox.set(6)
    animationSpeedSlider.set(15)

    # then draw the data onto the canvas
    # initially draw the canvas and maze
    canvas.create_rectangle(0, 0, 304, 304, fill='white')
    mData.drawMaze(canvas)
    # add event binding to handle canvas resizing
    root.bind('<Configure>', lambda e: cData.redrawCanvas(canvas, mData))

    root.mainloop()
    print('done')


# things might not exist on a global scope anymore,
# so that might potentially cause problems




# Add configure buttons for the animation and algorithm,
# which will create new windows to set those properties
# then commit