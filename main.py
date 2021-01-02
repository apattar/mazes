from tkinter import *
from tkinter import ttk

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

    def updateMazeDimensions():
        pass
        # updates the dims for the main maze and calls the redraw function.
        # to be called when dimensions are changed by the user
    
    def updateStartEndCells():
        pass
        # ??? don't know if i'll need this

def setSolveMode():
    pass
    # updates state to solve mode
    # also deals with mode button appearance

def setGenerateMode():
    pass
    # updates state to generate mode
    # also deals with mode button appearance

def redrawCanvas(canvas, mazeData, width, height):
    # to be called whenever the screen is resized.
    # mazeData is a MazeData object that should be passed in
    canvas.create_rectangle(0, 0, width+2, height+2, fill='white',
                            outline='black', width=10)
    mazeData.drawMaze(canvas)

def rgbString(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)

print('starting...')
root = Tk()
root.title('Mazes')

# create widgets
mainframe = ttk.Frame(root, relief='ridge', borderwidth=10)
modeButtonsFrame = ttk.Frame(mainframe, relief='sunken', borderwidth=5)
solveModeButton = ttk.Button(modeButtonsFrame, text='Solve Mode',
                             command=setSolveMode)
genModeButton = ttk.Button(modeButtonsFrame, text='Generate Mode',
                           command=setGenerateMode)
canvas = Canvas(mainframe, width=200, height=200)

# geometry management
mainframe.grid(sticky='nsew', padx=10, pady=10)

modeButtonsFrame.grid(row=0, columnspan=2, sticky='nsew', padx=5, pady=5)
solveModeButton.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
genModeButton.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

canvas.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)


root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=50)
mainframe.columnconfigure(1, weight=2)
modeButtonsFrame.rowconfigure(0, weight=1)
modeButtonsFrame.columnconfigure(0, weight=1)
modeButtonsFrame.columnconfigure(1, weight=1)


# Put this next block into function to initialize everything
setSolveMode()
# create the MazeData instance that will store all the data
# draw it all onto the canvas
mData = MazeData((6,6), set(), 0, 35)
redrawCanvas(canvas, mData, int(canvas['width']), int(canvas['height']))

root.mainloop()
print('done')