from tkinter import *
from tkinter import ttk
from objects import *

def rgbString(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)

def configAnimButtonPushed():
    pass
    # creates new toplevel window; will need root and
    # data objects to be passed into this function
    # as arguments, so the new toplevel window can
    # have the root as a parent

def configAlgButtonPushed():
    pass

if __name__ == '__main__':
    print('starting...')
    root = Tk()
    root.title('Mazes')

    defaultDims = (7,10)
    defaultSpeed = 15   # from 1 to 30
    defaultCanvasWidth = 504
    defaultCanvasHeight = 354
    redrawDelay = 1

    # create the object instances that will store all the data
    mData = MazeData(defaultDims, 
                      set([-6, -7]), 0, defaultDims[0]*defaultDims[1] - 1)
    stateData = ApplicationStateData()
    cData = CanvasData(redrawDelay)

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
                            command=lambda: mData.clearMaze(stateData,
                                            canvas,
                                            canvas.winfo_width(),
                                            canvas.winfo_height()))
    rowsLabel = ttk.Label(genControlsFrame, text='Rows: ')
    rowsSpinbox = ttk.Spinbox(genControlsFrame, from_=2.0, to=30.0,
                            command=lambda: mData.updateRows(rowsSpinbox,
                                            canvas,
                                            canvas.winfo_width(),
                                            canvas.winfo_height()))    # TODO disable when there's user-inputted stuff on the maze, or an animation running
    colsLabel = ttk.Label(genControlsFrame, text='Columns: ')
    colsSpinbox = ttk.Spinbox(genControlsFrame, from_=2.0, to=30.0,
                            command=lambda: mData.updateCols(colsSpinbox,
                                            canvas,
                                            canvas.winfo_width(),
                                            canvas.winfo_height()))    # TODO disable when there's user-inputted stuff on the maze, or an animation running
    # use rowsSpinbox.get() to get the value in the spinbox

    algDisplayFrame = ttk.Frame(mainframe, relief='sunken', borderwidth=5)
    algSupLabel = ttk.Label(algDisplayFrame, text='Algorithm:')
    algMainLabel = ttk.Label(algDisplayFrame, textvariable=stateData.currentAlgorithm,
                            anchor='center', relief='ridge', borderwidth=10)  # TODO more decoration?
    configAlgButton = ttk.Button(algDisplayFrame,
                                 text='Configure\nAlgorithm Options',
                                 command=configAlgButtonPushed)
    animationSpeedLabel = ttk.Label(algDisplayFrame, text='Animation Speed:')
    animationSpeedSlider = ttk.Scale(algDisplayFrame, orient=HORIZONTAL, length=30,
                                    from_=1.0, to=30.0)
    # use animationSpeedSlider.get()
    # PUT STEP OR SPEED THING BELOW algMainLabel
    animationStepButton = ttk.Button(algDisplayFrame, text='Step Animation',
                                     command=stateData.stepAnimation)   # grid only when in step mode
    configAnimButton = ttk.Button(algDisplayFrame,
                                  text='Configure\nAnimation Options',
                                  command=configAnimButtonPushed)


    solgenButton = ttk.Button(mainframe, textvariable=stateData.mode, command=stateData.animate)

    canvas = Canvas(mainframe, width=defaultCanvasWidth,
                    height=defaultCanvasHeight)


















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

    algDisplayFrame.grid(row=2, column=0, sticky='ews', padx=5, pady=5)
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
    mainframe.rowconfigure(3, weight=5)
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
    rowsSpinbox.set(defaultDims[0])
    colsSpinbox.set(defaultDims[1])
    animationSpeedSlider.set(defaultSpeed)

    # then draw the data onto the canvas
    # initially draw the canvas and maze
    canvas.create_rectangle(0, 0, defaultCanvasWidth,
                            defaultCanvasHeight, fill='white')
    mData.drawMaze(canvas, defaultCanvasWidth, defaultCanvasHeight)
    # add event binding to handle canvas resizing
    canvas.bind('<Configure>', lambda e: cData.resizeCanvas(canvas, mData))
    canvas.bind('<Motion>', lambda e: cData.mouseHovering(canvas, e,
                                                          stateData.mode.get(),
                                                          mData))
    canvas.bind('<B1-Motion>', lambda e: cData.mouseDragging(canvas, e,
                            stateData.mode.get(),
                            mData,
                            canvas.winfo_width(),
                            canvas.winfo_height()))
    canvas.bind('<ButtonPress-1>', lambda e: cData.mouseClicked(canvas, e,
                            stateData.mode.get(),
                            mData,
                            canvas.winfo_width(),
                            canvas.winfo_height()))

    root.mainloop()
    print('done')


# things might not exist on a global scope anymore,
# so that might potentially cause problems

# maybe should have stored things like root, mainframe, buttons, etc. in an object instead of in variables, so you can pass the object around easily?


# maybe use activefill and activewidth attributes for lines??
# probably not





# figure out event bindings for the canvas - hovering, and
# adding boundaries
# bindings go just above here, functions that are called
# might go in canvasData? Maybe they can draw the hover lines
# on top of the maze, and then they can update the mData object
# and call drawMaze with a mData object that's passed in?