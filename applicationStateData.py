from tkinter import StringVar

class ApplicationStateData(object):
    solveAlgorithms = ['dfs', 'bfs', 'astar']   # dijkstra?
    genAlgorithms = ['ec', 'vc']    # possibly more?

    def __init__(self):
        self.solgenButtonText = StringVar()
        self.setSolveMode()     # initializes self.mode
        self.animationRunning = False  # bool
        self.currentAlgorithm = StringVar(value='dfs')
        # don't need to store some of these things twice - can just access them directly from the widget
    
    def setSolveMode(self):
        self.solgenButtonText.set('Solve')
        self.mode = 'sol'
        # extend!!!
        # updates state to solve mode
        # also deals with mode button appearance
        # set algorithm
    
    def setGenerateMode(self):
        self.solgenButtonText.set('Generate')
        self.mode = 'gen'
        # updates state to generate mode
        # also deals with mode button appearance
    
    def startAnimateMode(self, solgenButton, *args):
        # args are widgets to be disabled in animate mode
        self.animationRunning = True
        self.solgenButtonText.set('Stop Animation')     # change this later
        solgenButton.configure(command=lambda: self.stopAnimateMode(
                               solgenButton, *args))       # textvariable vs text??
        

        # disable ui widgets
        for item in args:
            item.state(['disabled'])

        print('startAnimateMode called')
        # call animate function, or just start the animation

    def stopAnimateMode(self, solgenButton, *args):
        self.animationRunning = False
        if self.mode == 'sol':
            self.solgenButtonText.set('Solve')
        else:
            self.solgenButtonText.set('Generate')
        solgenButton.configure(command=
            lambda: self.startAnimateMode(solgenButton, *args))

        # enable all widgets
        for item in args:
            item.state(['!disabled'])
        
        print('stopAnimateMode called')

    def animate(self, solgenButton, *args):
        pass
        # self.startAnimateMode(solgenButton, *args)
        # to be called when solve/generate button is clicked
        # once this button is clicked, put into animate mode -- includes
        # disabling sol/gen button, rows and cols spinboxes,
        # use animationSpeedSlider.get() (widget) and
        # algorithm.get() (a StringVar)
        # disable stuff that needs to be disabled;
        # maybe set an 'animating' mode?
        # handles calling the step function when animation 
        # not in step mode - if in step mode, just do one step
    
    def stepAnimation(self):
        pass
        # advances animation, and redraws stuff
        # stuff should probably be drawn within drawMaze. Hear me out:
        # will handle resizing and everything
        # is sort of a different case than the hovering

        # when drawing lines representing solving the maze,
        # check out the Tk line options (joinstyle, smooth, etc.)
    
    def configAnimButtonPushed(self):
        pass

    def configAlgButtonPushed(self):
        pass