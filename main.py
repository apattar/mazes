from tkinter import *
from tkinter import ttk
from tkinter import font
from random import shuffle

def rgbString(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)


class vcAnimationData(object):
    def __init__(self):
        self.queue = [mData.startCell]
        # TODO continue

class ecAnimationData(object):
    def __init__(self):
        self.unionFind = [-1] * (mData.rows*mData.cols)
        self.unchecked = list(range(-1, -mData.cols, -1))
        for i in range(mData.cols, mData.rows*mData.cols, mData.cols):
            self.unchecked.append(i)
            for j in range(i+1, i+mData.cols):
                self.unchecked.append(j)
                self.unchecked.append(-j)
        mData.boundaries = set(self.unchecked.copy())
        shuffle(self.unchecked)
        self.done = False
    
    def __repr__(self):
        return f'unchecked: {self.unchecked}\nunion find: {self.unionFind}\nbounds: {mData.boundaries}'
        # TODO remove


class SimpleSearchAnimationData(object):
    dfsNeighborFuncs = []   # stored in order of execution
                            # which, since stack, means
                            # neighbors examined in reverse
    bfsNeighborFuncs = []   # stored in order of execution
                            # which, since queue, means
                            # neighbors examined in order

    def __init__(self, start):
        self.currWithParent = (start, start)
        self.seen = set([start])
        self.traversalLog = []
        self.worklistWithParents = [(start, start)]
        self.black = []
        self.solution = []      # from end to start
    
    def calculateSolution(self):
        self.solution = [mData.endCell]
        unused = dict()

        # loop backwards through traversalLog (including first (0,0) element)
        for i in range(len(self.traversalLog)-1, -1, -1):
            curr = self.solution[-1]
            if curr == self.traversalLog[i][0]:
                self.solution.append(self.traversalLog[i][1])
            else:
                if curr in unused:
                    self.solution.append(unused[curr])
                    del unused[curr]
                unused[self.traversalLog[i][0]] = self.traversalLog[i][1]

    @staticmethod
    def initDfsBfsFuncs():
        # check upper neighbor if exists
        def checkUpper(curr):
            upper = curr - mData.cols
            if (upper not in MazeData.ad.seen and \
                curr not in mData.boundaries and \
                upper >= 0):
                MazeData.ad.seen.add(upper)
                MazeData.ad.worklistWithParents.append((upper, curr))
        
        # check lower neighbor if exists
        def checkLower(curr):
            lower = curr + mData.cols
            if (lower not in MazeData.ad.seen and \
                lower not in mData.boundaries and \
                lower < mData.rows*mData.cols):
                MazeData.ad.seen.add(lower)
                MazeData.ad.worklistWithParents.append((lower, curr))

        # check neighbor to left if exists
        def checkLeft(curr):
            left = curr - 1
            if (left not in MazeData.ad.seen and \
                -curr not in mData.boundaries and \
                curr % mData.cols != 0):
                MazeData.ad.seen.add(left)
                MazeData.ad.worklistWithParents.append((left, curr))

        # check neighbor to right if exists
        def checkRight(curr):
            right = curr + 1
            if (right not in MazeData.ad.seen and \
                -right not in mData.boundaries and \
                (curr+1) % mData.cols != 0):
                MazeData.ad.seen.add(right)
                MazeData.ad.worklistWithParents.append((right, curr))

        SimpleSearchAnimationData.dfsNeighborFuncs = [("Above", checkUpper),
                ("Left", checkLeft), ("Right", checkRight), ("Below", checkLower)]
        SimpleSearchAnimationData.bfsNeighborFuncs = [("Below", checkLower),
                ("Right", checkRight), ("Left", checkLeft), ("Above", checkUpper)]

class asVtx(object):
    def __init__(self, g, h, f, loc, parent):
        self.g = g
        self.h = h
        self.f = f
        self.loc = loc
        self.parent = parent

    # alternate initializer
    @staticmethod
    def new(selfLoc, parent, parentG):
        r = selfLoc // mData.cols
        c = selfLoc % mData.cols
        er = mData.endCell // mData.cols
        ec = mData.endCell % mData.cols

        # parentLoc is an integer cell index
        parent = parent
        g = parentG + 1
        h = abs(er - r) + abs(ec - c)
        f = g + h
        
        result = asVtx(g, h, f, selfLoc, parent)
        return result
    
    def __eq__(self, other):
        return self.loc == other.loc
    
    def __hash__(self):
        return hash(self.loc)
    
    def __repr__(self):
        return f'loc={self.loc};f={str(int(self.f))}'

class ClosedList(object):
    def __init__(self):
        self.list = []      # stores vertices from
                            # lowest to highest f-cost
    
    def push(self, vtx):
        # vtx is object of type asVtx
        for i in range(len(self.list)):
            if self.list[i].f > vtx.f:
                self.list.insert(i, vtx)
                return
        
        # list is empty
        # or entire list was traversed through
        self.list.append(vtx)
    
    def __repr__(self):
        return str(self.list)   # TODO remove once unnecessary

class OpenQueue(ClosedList):
    def __init__(self, startVtx):
        self.list = [startVtx]  # stores vertices from
                                # lowest to highest f-cost
    
    def pop(self):
        print(f'Popping {self.list[0]} from OpenQueue\n')
        result = self.list.pop(0)
        return result
    
    def getFofVtxWithLoc(self, loc):
        # requires that a vtx with the loc exists in list
        for vtx in self.list:
            if vtx.loc == loc:
                return vtx.f
        return 'error in getFofVtxWithLoc'     # TODO remove

class asAnimationData(object):
    def __init__(self, start):
        # both the openQueue and closedList contain asVtx objects
        self.openQueue = OpenQueue(asVtx(0, 0, 0, start, start))
        self.closedList = ClosedList()
        self.solution = []
    
    def calculateSolution(self):
        self.solution = [mData.endCell]
        unused = dict()

        # loop backwards through closedList
        for i in range(len(self.closedList.list)-1, -1, -1):
            curr = self.solution[-1]
            if curr == self.closedList.list[i].loc:
                self.solution.append(self.closedList.list[i].parent)
            else:
                if curr in unused:
                    self.solution.append(unused[curr])
                    del unused[curr]
                unused[self.closedList.list[i].loc] = \
                    self.closedList.list[i].parent
        
        print('Solution: ' + str(self.solution))

class ApplicationStateData(object):
    currSolAlg = 0  # holds index of current sol algorithm
    currGenAlg = 0  # holds index of current gen algorithm
    solveAlgorithms = ('DFS', 'BFS', 'A*')   # dijkstra?
    genAlgorithms = ('Edge-centric', 'Vertex-centric')    # possibly more?

    def __init__(self):
        self.solgenButtonText = StringVar(value='Solve')
        self.currentAlgorithm = StringVar(value='A*')
        self.mode = 'sol'
        self.animationRunning = BooleanVar(value=False)
        self.animMode = StringVar(value='default')
        # don't need to store some of these things twice - can just access them directly from the widget
    
    def setSolveMode(self):
        self.currentAlgorithm.set(
            stateData.solveAlgorithms[stateData.currSolAlg])
        algCombobox['values'] = stateData.solveAlgorithms
        self.solgenButtonText.set('Solve')
        self.mode = 'sol'
        # extend!!!
        # updates state to solve mode
        # also deals with mode button appearance
    
    def setGenerateMode(self):
        self.currentAlgorithm.set(
            stateData.genAlgorithms[stateData.currGenAlg])
        algCombobox['values'] = stateData.genAlgorithms
        self.solgenButtonText.set('Generate')
        self.mode = 'gen'
        # updates state to generate mode
        # also deals with mode button appearance

    def algorithmChanged(self, e):
        algCombobox.selection_clear()
        if self.mode == 'sol':
            stateData.currSolAlg = stateData.solveAlgorithms.index(
                stateData.currentAlgorithm.get())
        else:
            stateData.currGenAlg = stateData.genAlgorithms.index(
                stateData.currentAlgorithm.get())

    def startAnimateMode(self):
        # TODO could just put all of this in mData.animate... maybe not
        # for the sake of modularity?
        self.animationRunning.set(True)
        solgenButton.grid_remove()
        
        # add animation widgets to screen based on animation mode
        if self.animMode.get() == 'default':
            pausePlayButton.state(['!disabled'])
            pausePlayButton.config(image=pauseImage, command=self.pauseAnimation)
            pausePlayButton.grid()
            stopButton.grid(sticky='nse', columnspan=1)
        elif self.animMode.get() == 'step':
            arrowButton.state(['!disabled'])
            arrowButton.grid()
            stopButton.grid(sticky='nse', columnspan=1)
        else:
            print('running')
            stopButton.grid(sticky='', columnspan=2)

        # disable widgets
        solveModeButton.state(['disabled'])
        genModeButton.state(['disabled'])
        clearButton.state(['disabled'])
        rowsSpinbox.state(['disabled'])
        colsSpinbox.state(['disabled'])
        algCombobox.state(['disabled'])
        configAlgButton.state(['disabled'])
        configAnimButton.state(['disabled'])

        if self.mode == 'sol':
            infoLabelText.set('Solving...')
        else:
            infoLabelText.set('Generating...')

        print('startAnimateMode called')
        print('starting the animation...')

        mData.animate()

    # called when the pausePlayButton is pressed while animation is playing
    def pauseAnimation(self):
        self.animationRunning.set(False)
        pausePlayButton.config(image=playImage, command=self.playAnimation)
        infoLabelText.set('Animation paused.')

    # called when the pausePlayButton is pressed while animation is paused
    def playAnimation(self):
        self.animationRunning.set(True)
        pausePlayButton.config(image=pauseImage, command=self.pauseAnimation)
        infoLabelText.set('Solving...')

    # called when the stopButton is pressed
    def stopAnimateMode(self):
        MazeData.ad = None
        self.animationRunning.set(True)
        self.animationRunning.set(False)

        # remove animation widgets from screen based on animation mode
        stopButton.grid_remove()
        if self.animMode.get() == 'default':
            pausePlayButton.grid_remove()
        elif self.animMode.get() == 'step':
            arrowButton.grid_remove()
        solgenButton.grid()

        # enable all widgets
        solveModeButton.state(['!disabled'])
        genModeButton.state(['!disabled'])
        clearButton.state(['!disabled'])
        rowsSpinbox.state(['!disabled'])
        colsSpinbox.state(['!disabled'])
        algCombobox.state(['!disabled'])
        configAlgButton.state(['!disabled'])
        configAnimButton.state(['!disabled'])
        
        infoLabelText.set('Welcome!')
        
        # clear animation
        canvas.delete(*canvas.find_withtag('d'))
        canvas.delete(*canvas.find_withtag('b'))
        mData.drawMaze()

        print('stopAnimateMode called')

    def closeAuxWindow(self, window):
        print(f'closing {window}')
        root.deiconify()

        # position root in same location as window TODO center - simple!
        root.update_idletasks()
        rootGeom = root.geometry()
        a = rootGeom.find('+')
        b = rootGeom.find('-')
        if b == -1:
            rootGeom = rootGeom[:a]
        elif a == -1:
            rootGeom = rootGeom[:b]
        else:
            rootGeom = rootGeom[:a] if a < b else rootGeom[:b]
        windowGeom = window.geometry()
        a = windowGeom.find('+')
        b = windowGeom.find('-')
        if b == -1:
            windowGeom = windowGeom[a:]
        elif a == -1:
            windowGeom = windowGeom[b:]
        else:
            windowGeom = windowGeom[a:] if a < b else windowGeom[b:]
        root.geometry(rootGeom + windowGeom)

        window.destroy()

    def applyAlgSettings(self, window, tempAlgVal):
        stateData.currentAlgorithm.set(tempAlgVal)
        self.closeAuxWindow(window)

    def applyAnimSettings(self, window):
        if self.animMode.get() == 'default':
            animationSpeedSlider.state(['!disabled'])
            animationSpeedLabel.state(['!disabled'])
        else:
            animationSpeedSlider.state(['disabled'])
            animationSpeedLabel.state(['disabled'])
        self.closeAuxWindow(window)

    # configure text of info labels
    def resetAlgSettingsInterfaceLayout(self, cb, infoIntroLabel, infoLabel, alg, settingsFrame):
        cb.selection_clear()

        # clear the settings frame
        for widget in settingsFrame.winfo_children():
            widget.grid_forget()

        # make changes to widgets
        if alg == 'DFS':
            infoIntroLabel.config(text="""\
Depth-first search, or DFS, is a graph pathfinding algorithm that is not guaranteed to give an optimal solution.""")
            infoLabel.config(text="""\
Beginning at the start node, neighboring nodes are continually examined until the end node is reached, or until it is determined that no path exists. A stack is used to keep track of which nodes to visit next, which means that a path that stems from one neighbor of a node is followed as far as possible before a different neighbor is examined. Consult a search engine for a simpler or more in-depth explanation.

The nature of DFS is such that the order in which the neighbors of nodes are examined plays a large part in how long the algorithm takes to find a path. You can change the order that neighbors of nodes are examined below:""")

            # create settings UI
            ttk.Label(settingsFrame, text="Checked first:").grid(row=0, column=0, sticky="sew", padx=5, pady=5)
            ttk.Label(settingsFrame, text="Checked second:").grid(row=0, column=1, sticky="sew", padx=5, pady=5)
            ttk.Label(settingsFrame, text="Checked third:").grid(row=0, column=2, sticky="sew", padx=5, pady=5)
            ttk.Label(settingsFrame, text="Checked fourth:").grid(row=0, column=3, sticky="sew", padx=5, pady=5)

            dirs = [SimpleSearchAnimationData.dfsNeighborFuncs[i][0] for i in range(3, -1, -1)]
            cbs = []
            for i in range(4):
                newCb = ttk.Combobox(settingsFrame, textvariable=StringVar())
                newCb["values"] = tuple(dirs)
                newCb.set(dirs[i])
                newCb.state(["readonly"])
                newCb.grid(row=1, column=i, sticky="new", padx=5, pady=5)
                cbs.append(newCb)

            def createCBCallback(cb):
                def callback(_):
                    # find other combobox whose value has been switched to;
                    # set it to the value that was switched from
                    thisval = cb.get()
                    remaining = set(dirs)
                    for ocb in cbs:
                        otherval = ocb.get()
                        if otherval in remaining: remaining.remove(otherval)
                        if thisval == otherval and not cb is ocb:
                            theocb = ocb
                    if len(remaining) == 0: return  # there was no change made by selection
                    switchFrom = thisval
                    switchTo = remaining.pop()
                    theocb.set(switchTo)

                    # update SimpleSearchAnimationData.dfsNeighborFuncs with switch
                    for (i,el) in enumerate(SimpleSearchAnimationData.dfsNeighborFuncs):
                        if el[0] == switchFrom: s1 = i
                        elif el[0] == switchTo: s2 = i
                    lower, higher = (s1, s2) if s1 < s2 else (s2, s1)
                    popped = SimpleSearchAnimationData.dfsNeighborFuncs.pop(higher)
                    SimpleSearchAnimationData.dfsNeighborFuncs.insert(lower, popped)
                    popped = SimpleSearchAnimationData.dfsNeighborFuncs.pop(lower + 1)
                    SimpleSearchAnimationData.dfsNeighborFuncs.insert(higher, popped)
                return callback

            for cb in cbs: cb.bind("<<ComboboxSelected>>", createCBCallback(cb))

        elif alg == 'BFS':
            infoIntroLabel.config(text="""\
Breadth-first search, or BFS, is a graph pathfinding algorithm that is not guaranteed to give an optimal solution.""")
            infoLabel.config(text="""\
Beginning at the start node, neighboring nodes are continually examined until the end node is reached, or until it is determined that no path exists. A queue is used to keep track of which nodes to visit next, which means that all neighbors of a node are examined before any of the neighbors' neighbors are examined; in other words, the nodes of the graph are traversed 'level by level'. Consult a search engine for a simpler or more in-depth explanation.

In BFS, since all neighbors are examined at once, the order in which the neighbors of nodes are examined doesn't play a very large role in the algorithm's speed; however, it does have an effect. You can change the order that neighbors of nodes are examined below:""")
        
            # create settings UI
            ttk.Label(settingsFrame, text="Checked first:").grid(row=0, column=0, sticky="sew", padx=5, pady=5)
            ttk.Label(settingsFrame, text="Checked second:").grid(row=0, column=1, sticky="sew", padx=5, pady=5)
            ttk.Label(settingsFrame, text="Checked third:").grid(row=0, column=2, sticky="sew", padx=5, pady=5)
            ttk.Label(settingsFrame, text="Checked fourth:").grid(row=0, column=3, sticky="sew", padx=5, pady=5)

            dirs = [el[0] for el in SimpleSearchAnimationData.bfsNeighborFuncs]
            cbs = []
            for i in range(4):
                newCb = ttk.Combobox(settingsFrame, textvariable=StringVar())
                newCb["values"] = tuple(dirs)
                newCb.set(dirs[i])
                newCb.state(["readonly"])
                newCb.grid(row=1, column=i, sticky="new", padx=5, pady=5)
                cbs.append(newCb)

            def createCBCallback(cb):
                def callback(_):
                    # find other combobox whose value has been switched to;
                    # set it to the value that was switched from
                    thisval = cb.get()
                    remaining = set(dirs)
                    for ocb in cbs:
                        otherval = ocb.get()
                        if otherval in remaining: remaining.remove(otherval)
                        if thisval == otherval and not cb is ocb:
                            theocb = ocb
                    if len(remaining) == 0: return  # there was no change made by selection
                    switchFrom = thisval
                    switchTo = remaining.pop()
                    theocb.set(switchTo)

                    # update SimpleSearchAnimationData.bfsNeighborFuncs with switch
                    for (i,el) in enumerate(SimpleSearchAnimationData.bfsNeighborFuncs):
                        if el[0] == switchFrom: s1 = i
                        elif el[0] == switchTo: s2 = i
                    lower, higher = (s1, s2) if s1 < s2 else (s2, s1)
                    popped = SimpleSearchAnimationData.bfsNeighborFuncs.pop(higher)
                    SimpleSearchAnimationData.bfsNeighborFuncs.insert(lower, popped)
                    popped = SimpleSearchAnimationData.bfsNeighborFuncs.pop(lower + 1)
                    SimpleSearchAnimationData.bfsNeighborFuncs.insert(higher, popped)
                return callback

            for cb in cbs: cb.bind("<<ComboboxSelected>>", createCBCallback(cb))
        
        elif alg == 'A*':
            infoIntroLabel.config(text="""\
A* (pronounced 'ay-star') is a graph pathfinding algorithm that is always guaranteed to give an optimal solution.""")
            infoLabel.config(text="""\
Like in DFS and BFS, neighboring nodes are examined beginning with the start node until the end node is reached. As each node is examined, however, data that describes the path taken to get there from the start node is retained. Using this data, each node's 'f-cost' is calculated, which is the sum of the distance traveled to get there (the node's 'g-cost') and the distance from there to the end node (the node's 'h-cost'). The node with the lowest f-cost is always examined next, which always results in the shortest possible path from start to finish. Consult a search engine for a simpler or more in-depth explanation.

A* is guaranteed to be optimal, but it is not as memory-efficient as DFS or BFS, since lots of extra data must be stored for each node (its parent node, g-cost, h-cost, and f-cost). Despite this, a shortest possible path will always be found (there may be multiple). You can choose to display additional data about each node as the algorithm runs below:""")

            # add extra settings here for A*

        elif alg == 'Edge-centric':
            pass    # TODO generate stuff
        elif alg == 'Vertex-centric':
            pass

    def configAlgButtonPushed(self):
        print('opening configAlg window')
        root.withdraw()
        algRoot = Toplevel(root)
        algRoot.title('Algorithm Options')
        algRoot.protocol('WM_DELETE_WINDOW', lambda:
            self.closeAuxWindow(algRoot))

        # create widgets
        currAlgFrame = ttk.Frame(algRoot)
        currAlgLabel = ttk.Label(currAlgFrame, text='Algorithm:')
        tempAlg = StringVar(value=stateData.currentAlgorithm.get())
        localAlgCombobox = ttk.Combobox(currAlgFrame, textvariable=tempAlg)
        localAlgCombobox['values'] = stateData.solveAlgorithms \
            if stateData.mode == 'sol' else stateData.genAlgorithms
        localAlgCombobox.state(["readonly"])
        infoLabelFrame = ttk.Labelframe(algRoot, text='Info')
        infoIntroLabel = ttk.Label(infoLabelFrame, font=largerFont,
                                    style='InfoLabel.TLabel')
        infoLabel = ttk.Label(infoLabelFrame, style='InfoLabel.TLabel')
        settingsFrame = ttk.Frame(algRoot, relief='sunken')
        okayButton = ttk.Button(algRoot, text='Okay', command=lambda:
            self.applyAlgSettings(algRoot, tempAlg.get()))

        self.resetAlgSettingsInterfaceLayout(localAlgCombobox, infoIntroLabel,
            infoLabel, tempAlg.get(), settingsFrame)

        localAlgCombobox.bind('<<ComboboxSelected>>', lambda _:
            self.resetAlgSettingsInterfaceLayout(localAlgCombobox,
                                infoIntroLabel, infoLabel, tempAlg.get(),
                                settingsFrame))

        currAlgFrame.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
        currAlgLabel.grid(row=0, column=0, padx=5, pady=5)
        localAlgCombobox.grid(row=0, column=1, padx=5, pady=5)
        infoLabelFrame.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
        infoIntroLabel.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        infoLabel.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        settingsFrame.grid(row=2, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
        okayButton.grid(row=3, column=2, sticky='sw', padx=5, pady=10)

        algRoot.rowconfigure(0, weight=1)
        algRoot.rowconfigure(1, weight=100)
        algRoot.rowconfigure(2, weight=1)
        algRoot.rowconfigure(3, weight=1)
        algRoot.columnconfigure(0, weight=100)
        algRoot.columnconfigure(1, weight=1)
        algRoot.columnconfigure(2, weight=1)
        infoLabelFrame.rowconfigure(0, weight=1)
        infoLabelFrame.rowconfigure(1, weight=50)
        infoLabelFrame.columnconfigure(0, weight=1)

        # position in same location as root TODO center - simple!
        algRoot.update_idletasks()
        algGeom = algRoot.geometry()
        algGeom = algGeom[:algGeom.find('+')]
        rootGeom = root.geometry()
        a = rootGeom.find('+')
        b = rootGeom.find('-')
        if b == -1:
            rootGeom = rootGeom[a:]
        elif a == -1:
            rootGeom = rootGeom[b:]
        else:
            rootGeom = rootGeom[a:] if a < b else rootGeom[b:]
        algRoot.geometry(algGeom + rootGeom)
    
    def configAnimButtonPushed(self):
        print('opening configAlg window')
        root.withdraw()
        animRoot = Toplevel(root)
        animRoot.title('Animation Options')
        animRoot.protocol('WM_DELETE_WINDOW', lambda:
            self.applyAnimSettings(animRoot))

        # create widgets
        instrLabel = ttk.Label(animRoot, text='Choose an animation mode below.',
                                font=largerFont)
        defaultFrame = ttk.Frame(animRoot)
        defaultRadiobutton = ttk.Radiobutton(defaultFrame, text='Default Mode',
            variable=stateData.animMode, value='default')
        defaultDesc = ttk.Label(defaultFrame, text='''\
In this mode, animations run automatically upon clicking 'Solve' or 'Generate'. The speed that the animation runs can be controlled using the 'Animation Speed' slider, and the animations can be paused. When the button with a square is pressed, the animation is ended and the maze is cleared.''',
                            style='InfoLabel.TLabel')
        stepFrame = ttk.Frame(animRoot)
        stepRadiobutton = ttk.Radiobutton(stepFrame, text='Step Mode',
            variable=stateData.animMode, value='step')
        stepDesc = ttk.Label(stepFrame, text='''\
In this mode, only one step of the animation is performed at a time. Click the arrow button to advance to the next step.''',
                            style='InfoLabel.TLabel')
        jumpFrame = ttk.Frame(animRoot)
        jumpRadiobutton = ttk.Radiobutton(jumpFrame, text='Jump to End Mode',
            variable=stateData.animMode, value='jump')
        jumpDesc = ttk.Label(jumpFrame, text='''\
In this mode, the steps of the algorithm are not shown; the animation immediately jumps to the end, where the state of the auxiliary data for the algorithm as well as the green solution line is shown.''',
                            style='InfoLabel.TLabel')
        solutionFrame = ttk.Frame(animRoot)
        solutionRadiobutton = ttk.Radiobutton(solutionFrame, text='Solution Only Mode',
            variable=stateData.animMode, value='solution')
        solutionDesc = ttk.Label(solutionFrame, text='''\
In this mode, the steps of the algorithm are not shown; the animation immediately jumps to the end, and only the green solution line is shown. If there is no solution, the state of all the algorithm's auxiliary data is shown at the point where the algorithm failed.''',
                            style='InfoLabel.TLabel')
        okayButton = ttk.Button(animRoot, text='Okay', command=lambda:
            self.applyAnimSettings(animRoot))

        instrLabel.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        defaultFrame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        stepFrame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
        jumpFrame.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
        solutionFrame.grid(row=4, column=0, sticky='nsew', padx=5, pady=5)
        okayButton.grid(row=5, column=0, sticky='se', padx=10, pady=10)
        defaultRadiobutton.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        defaultDesc.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        stepRadiobutton.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        stepDesc.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        jumpRadiobutton.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        jumpDesc.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        solutionRadiobutton.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        solutionDesc.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

        animRoot.rowconfigure(0, weight=1)
        animRoot.rowconfigure(1, weight=1)
        animRoot.rowconfigure(2, weight=1)
        animRoot.rowconfigure(3, weight=1)
        animRoot.rowconfigure(4, weight=1)
        animRoot.rowconfigure(5, weight=1)
        animRoot.columnconfigure(0, weight=1)
        defaultFrame.rowconfigure(0, weight=1)
        defaultFrame.columnconfigure(0, weight=1)
        defaultFrame.columnconfigure(1, weight=1)
        stepFrame.rowconfigure(0, weight=1)
        stepFrame.columnconfigure(0, weight=1)
        stepFrame.columnconfigure(1, weight=1)
        jumpFrame.rowconfigure(0, weight=1)
        jumpFrame.columnconfigure(0, weight=1)
        jumpFrame.columnconfigure(1, weight=1)
        solutionFrame.rowconfigure(0, weight=1)
        solutionFrame.columnconfigure(0, weight=1)
        solutionFrame.columnconfigure(1, weight=1)

        # position in same location as root TODO center - simple!
        animRoot.update_idletasks()
        rootGeom = root.geometry()
        a = rootGeom.find('+')
        b = rootGeom.find('-')
        if b == -1:
            rootGeom = rootGeom[a:]
        elif a == -1:
            rootGeom = rootGeom[b:]
        else:
            rootGeom = rootGeom[a:] if a < b else rootGeom[b:]
        animRoot.geometry('600x650' + rootGeom)

class MazeData(object):
    ad = None

    def __init__(self, rows, cols, boundaries, startCell, endCell):
        # there will be rows*cols cells in the maze, indexed 0 to rows*cols
        # boundaries is a set of integers; the absolute value of the integer
        # represents a cell, positive values represent a boundary above,
        # and negative values represent a boundary to the left
        self.rows = rows
        self.cols = cols
        self.startCell = startCell
        self.endCell = endCell
        self.boundaries = boundaries
    
    # helper functions for drawMaze
    def drawCellColors(self):
        # draw checkerboard with grey squares
        for r in range(self.rows):
            for c in range(self.cols):
                if ((r % 2 == 0) and (c % 2 == 0)) or \
                    ((r % 2 != 0) and (c % 2 != 0)):
                    canvas.create_rectangle(cData.margin + (c*cData.cell_w),
                                            cData.margin + (r*cData.cell_h),
                                            cData.margin + ((1+c)*cData.cell_w),
                                            cData.margin + ((1+r)*cData.cell_h),
                                            fill='#e3e3e3',
                                            width=0)

        # draw start and end squares
        sr = self.startCell // self.cols
        sc = self.startCell % self.cols
        er = self.endCell // self.cols
        ec = self.endCell % self.cols
        canvas.create_rectangle(cData.margin + (sc*cData.cell_w),
                                cData.margin + (sr*cData.cell_h),
                                cData.margin + ((1+sc)*cData.cell_w),
                                cData.margin + ((1+sr)*cData.cell_h),
                                fill='#85f781',
                                width=0)
        canvas.create_rectangle(cData.margin + (ec*cData.cell_w),
                                cData.margin + (er*cData.cell_h),
                                cData.margin + ((1+ec)*cData.cell_w),
                                cData.margin + ((1+er)*cData.cell_h),
                                fill='#81f7eb',
                                width=0)
        if sr == 0:
            canvas.create_text(cData.margin + ((sc + 0.5)*cData.cell_w),
                               (2 * cData.margin // 3),
                               anchor='center',
                               text='START',
                               font=('Courier %d bold' % (cData.cell_w // 4)),
                               fill='#5db85a')
        elif sr == self.rows - 1:
            canvas.create_text(cData.margin + ((sc + 0.5)*cData.cell_w),
                               h - (2 * cData.margin // 3),
                               anchor='center',
                               text='START',
                               font=('Courier %d bold' % (cData.cell_w // 4)),
                               fill='#5db85a')
        else:
            word = 'START'
            for i in range(5):
                canvas.create_text(2 * cData.margin // 3,
                                   cData.margin + ((sr + 0.25*i)*cData.cell_h),
                                   anchor='center',
                                   text=word[i],
                                   font='Courier %d bold' % (cData.cell_h // 4),
                                   fill='#5db85a')

        if er == 0:
            canvas.create_text(cData.margin + ((ec + 0.5)*cData.cell_w),
                               (2 * cData.margin // 3),
                               anchor='center',
                               text='END',
                               font=('Courier %d bold' % (cData.cell_w // 4)),
                               fill='#5cb5ac')
        elif er == self.rows - 1:
            canvas.create_text(cData.margin + ((ec + 0.5)*cData.cell_w),
                               cData.h - (2 * cData.margin // 3),
                               anchor='center',
                               text='END',
                               font=('Courier %d bold' % (cData.cell_w // 4)),
                               fill='#5cb5ac')
        else:
            word = 'END'
            for i in range(3):
                canvas.create_text(2 * cData.margin // 3,
                                   cData.margin + ((er + 0.25*(i+1))*cData.cell_h),
                                   anchor='center',
                                   text=word[i],
                                   font='Courier %d bold' % (cData.cell_h // 4),
                                   fill='#5cb5ac')

    def drawBoundaries(self):
        canvas.create_line(cData.margin, cData.margin,
                           cData.w - cData.margin, cData.margin,
                           width=7, capstyle='round')
        canvas.create_line(cData.margin, cData.margin,
                           cData.margin, cData.h - cData.margin,
                           width=7, capstyle='round')
        canvas.create_line(cData.margin, cData.h - cData.margin,
                           cData.w - cData.margin, cData.h - cData.margin,
                           width=7, capstyle='round')
        canvas.create_line(cData.w - cData.margin, cData.margin,
                           cData.w - cData.margin, cData.h - cData.margin,
                           width=7, capstyle='round')

        for boundary in self.boundaries:
            b = abs(boundary)
            if b < self.rows * self.cols:
                r = b // self.cols
                c = b % self.cols
                if boundary > 0:
                    canvas.create_line(cData.margin + (cData.cell_w * c),
                                       cData.margin + (cData.cell_h * r),
                                       cData.margin + (cData.cell_w * (c+1)),
                                       cData.margin + (cData.cell_h * r),
                                       width=5, capstyle='round',
                                       tags=('b',))
                else:
                    canvas.create_line(cData.margin + (cData.cell_w * c),
                                       cData.margin + (cData.cell_h * r),
                                       cData.margin + (cData.cell_w * c),
                                       cData.margin + (cData.cell_h * (r+1)),
                                       width=5, capstyle='round',
                                       tags=('b',))

    # draws maze onto the canvas based on data + white background
    # maybe shouldn't have been a part of mazeData?
    # mazeData is model, this is view
    def drawMaze(self):
        canvas.create_rectangle(0, 0, cData.w, cData.h, fill='white')
        self.drawCellColors()
        self.drawBoundaries()
        if MazeData.ad:
            if stateData.currentAlgorithm.get() == 'DFS' or \
               stateData.currentAlgorithm.get() == 'BFS':
                self.drawSimpleSearchAnimation()
            elif stateData.currentAlgorithm.get() == 'A*':
                self.drawAsAnimation()
            elif stateData.currentAlgorithm.get() == 'Edge-centric':
                if not MazeData.ad.done:
                    self.drawEcAnimation()
            else:
                print('hi')

    
    def animate(self):
        if stateData.currentAlgorithm.get() == 'DFS':
            arrowButton.configure(command=mData.stepDfs)
            MazeData.ad = SimpleSearchAnimationData(self.startCell) # TODO start cell unnecessary here
            if stateData.animMode.get() == 'default':
                self.drawSimpleSearchAnimation()
                root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                    lambda: self.stepDfs())
            elif stateData.animMode.get() == 'step':
                self.drawSimpleSearchAnimation()
            else:
                self.stepDfs()
        elif stateData.currentAlgorithm.get() == 'BFS':
            arrowButton.configure(command=mData.stepBfs)
            MazeData.ad = SimpleSearchAnimationData(self.startCell)
            if stateData.animMode.get() == 'default':
                self.drawSimpleSearchAnimation()
                root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                    lambda: self.stepBfs())
            elif stateData.animMode.get() == 'step':
                self.drawSimpleSearchAnimation()
            else:
                self.stepBfs()
        elif stateData.currentAlgorithm.get() == 'A*':
            arrowButton.configure(command=mData.stepAs)
            MazeData.ad = asAnimationData(self.startCell)
            if stateData.animMode.get() == 'default':
                self.drawAsAnimation()
                root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                   lambda: self.stepAs())
            elif stateData.animMode.get() == 'step':
                self.drawAsAnimation()
            else:
                self.stepAs()
        elif stateData.currentAlgorithm.get() == 'Edge-centric':
            arrowButton.configure(command=mData.stepEc)
            MazeData.ad = ecAnimationData()
            if stateData.animMode.get() == 'default':
                self.drawEcAnimation()
                root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                   lambda: self.stepEc())
            elif stateData.animMode.get() == 'step':
                self.drawEcAnimation()
            else:
                self.stepEc()
        elif stateData.currentAlgorithm.get() == 'Vertex-centric':
            arrowButton.configure(command=mData.stepVc)
        else:
            print('There was a problem... algorithm not valid')
            stateData.stopAnimateMode()     # TODO remove

    def stepDfs(self):
        if not MazeData.ad: return
        if not stateData.animationRunning.get():
            print('paused')
            root.wait_variable(stateData.animationRunning)
            print('unpaused')
            if not MazeData.ad: return
        
        MazeData.ad.currWithParent = MazeData.ad.worklistWithParents.pop()
        curr = MazeData.ad.currWithParent[0]

        # add the traversal that just happened to the traversalLog
        MazeData.ad.traversalLog.append(MazeData.ad.currWithParent)

        # check if curr is the end cell
        if curr == self.endCell:    # maze solved
            MazeData.ad.calculateSolution()
            if stateData.animMode.get() == 'solution':
                self.drawSolution()
            else:
                self.drawSimpleSearchAnimation()
                pausePlayButton.state(['disabled'])
                arrowButton.state(['disabled'])
            infoLabelText.set('Solution found!')
            return

        initialSeenLen = len(MazeData.ad.seen)

        # check neighbors in set order; if unmarked, push to worklist
        for (_, func) in SimpleSearchAnimationData.dfsNeighborFuncs:
            func(curr)

        if len(MazeData.ad.seen) == initialSeenLen:
            # no valid neighbors
            MazeData.ad.black.append(curr)
        
        if stateData.animMode.get() == 'default' or \
            stateData.animMode.get() == 'step':
            self.drawSimpleSearchAnimation()
        
        if len(MazeData.ad.worklistWithParents) == 0:     # stack empty; maze unsolvable
            pausePlayButton.state(['disabled'])
            arrowButton.state(['disabled'])
            self.drawSimpleSearchAnimation()
            infoLabelText.set('Maze unsolvable.')
            return

        if stateData.animMode.get() == 'default':
            root.update_idletasks()
            root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                    lambda: self.stepDfs())
        elif stateData.animMode.get() != 'step':
            self.stepDfs()


    def stepBfs(self):
        if not MazeData.ad: return
        if not stateData.animationRunning.get():
            print('paused')
            root.wait_variable(stateData.animationRunning)
            print('unpaused')
            if not MazeData.ad: return
        
        MazeData.ad.currWithParent = MazeData.ad.worklistWithParents.pop(0)
        curr = MazeData.ad.currWithParent[0]

        # add the traversal that just happened to the traversalLog
        MazeData.ad.traversalLog.append(MazeData.ad.currWithParent)

        # check if curr is the end cell
        if curr == self.endCell:    # maze solved
            MazeData.ad.calculateSolution()
            if stateData.animMode.get() == 'solution':
                self.drawSolution()
            else:
                self.drawSimpleSearchAnimation()
                pausePlayButton.state(['disabled'])
                arrowButton.state(['disabled'])
            infoLabelText.set('Solution found!')
            return

        initialSeenLen = len(MazeData.ad.seen)

        for (_, func) in SimpleSearchAnimationData.bfsNeighborFuncs:
            func(curr)

        if len(MazeData.ad.seen) == initialSeenLen:
            MazeData.ad.black.append(curr)
        
        if stateData.animMode.get() == 'default' or \
            stateData.animMode.get() == 'step':
            self.drawSimpleSearchAnimation()
        
        if len(MazeData.ad.worklistWithParents) == 0:     # worklist empty; maze unsolvable
            pausePlayButton.state(['disabled'])
            arrowButton.state(['disabled'])
            self.drawSimpleSearchAnimation()
            infoLabelText.set('Maze unsolvable.')
            return

        if stateData.animMode.get() == 'default':
            root.update_idletasks()
            root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                    lambda: self.stepBfs())
        elif stateData.animMode.get() != 'step':
            self.stepBfs()

    def stepAs(self):
        if not MazeData.ad: return
        if not stateData.animationRunning.get():
            print('paused')
            root.wait_variable(stateData.animationRunning)
            print('unpaused')
            if not MazeData.ad: return
        
        # pop off of the open list
        if len(MazeData.ad.openQueue.list) != 0:
            curr = MazeData.ad.openQueue.pop()
        else:   # open queue empty; maze unsolvable
            pausePlayButton.state(['disabled'])
            arrowButton.state(['disabled'])
            self.drawAsAnimation()
            infoLabelText.set('Maze unsolvable.')
            return
        
        upper = curr.loc - self.cols
        lower = curr.loc + self.cols
        left = curr.loc - 1
        right = curr.loc + 1

        # check upper neighbor if exists
        if (curr.loc not in self.boundaries and \
            upper >= 0):
            newVtx = asVtx.new(upper, curr.loc, curr.g)
            if upper == self.endCell:
                MazeData.ad.closedList.push(curr)
                MazeData.ad.closedList.push(newVtx)
                MazeData.ad.calculateSolution()
                if stateData.animMode.get() == 'solution':
                    self.drawSolution()
                else:
                    self.drawAsAnimation()
                    pausePlayButton.state(['disabled'])
                    arrowButton.state(['disabled'])
                infoLabelText.set('Solution found!')
                return
            elif newVtx in MazeData.ad.openQueue.list:
                if newVtx.f < MazeData.ad.openQueue.getFofVtxWithLoc(upper):
                    MazeData.ad.openQueue.list.remove(newVtx)
                    MazeData.ad.openQueue.push(newVtx)
            elif newVtx in MazeData.ad.closedList.list:
                dup = MazeData.ad.closedList.list[
                    MazeData.ad.closedList.list.index(newVtx)]
                if newVtx.f < dup.f:
                    MazeData.ad.closedList.list.remove(dup)
                    MazeData.ad.openQueue.push(newVtx)
            else:
                MazeData.ad.openQueue.push(newVtx)

        # check lower neighbor if exists
        if (lower not in self.boundaries and \
            lower < self.rows*self.cols):
            newVtx = asVtx.new(lower, curr.loc, curr.g)
            if lower == self.endCell:
                MazeData.ad.closedList.push(curr)
                MazeData.ad.closedList.push(newVtx)
                MazeData.ad.calculateSolution()
                if stateData.animMode.get() == 'solution':
                    self.drawSolution()
                else:
                    self.drawAsAnimation()
                    pausePlayButton.state(['disabled'])
                    arrowButton.state(['disabled'])
                infoLabelText.set('Solution found!')
                return
            elif newVtx in MazeData.ad.openQueue.list:
                if newVtx.f < MazeData.ad.openQueue.getFofVtxWithLoc(lower):
                    MazeData.ad.openQueue.list.remove(newVtx)
                    MazeData.ad.openQueue.push(newVtx)
            elif newVtx in MazeData.ad.closedList.list:
                dup = MazeData.ad.closedList.list[
                    MazeData.ad.closedList.list.index(newVtx)]
                if newVtx.f < dup.f:
                    MazeData.ad.closedList.list.remove(dup)
                    MazeData.ad.openQueue.push(newVtx)
            else:
                MazeData.ad.openQueue.push(newVtx)

        # check neighbor to left if exists
        if (-curr.loc not in self.boundaries and \
            curr.loc % self.cols != 0):
            newVtx = asVtx.new(left, curr.loc, curr.g)
            if left == self.endCell:
                MazeData.ad.closedList.push(curr)
                MazeData.ad.closedList.push(newVtx)
                MazeData.ad.calculateSolution()
                if stateData.animMode.get() == 'solution':
                    self.drawSolution()
                else:
                    self.drawAsAnimation()
                    pausePlayButton.state(['disabled'])
                    arrowButton.state(['disabled'])
                infoLabelText.set('Solution found!')
                return
            elif newVtx in MazeData.ad.openQueue.list:
                if newVtx.f < MazeData.ad.openQueue.getFofVtxWithLoc(left):
                    MazeData.ad.openQueue.list.remove(newVtx)
                    MazeData.ad.openQueue.push(newVtx)
            elif newVtx in MazeData.ad.closedList.list:
                dup = MazeData.ad.closedList.list[
                    MazeData.ad.closedList.list.index(newVtx)]
                if newVtx.f < dup.f:
                    MazeData.ad.closedList.list.remove(dup)
                    MazeData.ad.openQueue.push(newVtx)
            else:
                MazeData.ad.openQueue.push(newVtx)

        # check neighbor to right if exists
        if (-right not in self.boundaries and \
            (curr.loc+1) % self.cols != 0):
            newVtx = asVtx.new(right, curr.loc, curr.g)
            if right == self.endCell:
                MazeData.ad.closedList.push(curr)
                MazeData.ad.closedList.push(newVtx)
                MazeData.ad.calculateSolution()
                if stateData.animMode.get() == 'solution':
                    self.drawSolution()
                else:
                    self.drawAsAnimation()
                    pausePlayButton.state(['disabled'])
                    arrowButton.state(['disabled'])
                infoLabelText.set('Solution found!')
                return
            elif newVtx in MazeData.ad.openQueue.list:
                if newVtx.f < MazeData.ad.openQueue.getFofVtxWithLoc(right):
                    MazeData.ad.openQueue.list.remove(newVtx)
                    MazeData.ad.openQueue.push(newVtx)
            elif newVtx in MazeData.ad.closedList.list:
                dup = MazeData.ad.closedList.list[
                    MazeData.ad.closedList.list.index(newVtx)]
                if newVtx.f < dup.f:
                    MazeData.ad.closedList.list.remove(dup)
                    MazeData.ad.openQueue.push(newVtx)
            else:
                MazeData.ad.openQueue.push(newVtx)
            
        MazeData.ad.closedList.push(curr)

        if stateData.animMode.get() == 'default' or \
            stateData.animMode.get() == 'step':
            self.drawAsAnimation() 

        if stateData.animMode.get() == 'default':
            root.update_idletasks()
            root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                    lambda: self.stepAs())
        elif stateData.animMode.get() != 'step':
            self.stepAs()

    def stepEc(self):
        if not MazeData.ad: return
        if not stateData.animationRunning.get():
            print('paused')
            root.wait_variable(stateData.animationRunning)
            print('unpaused')
            if not MazeData.ad: return
        
        if len(mData.boundaries) == \
                mData.rows*mData.cols - mData.rows - mData.cols + 1:
            pausePlayButton.state(['disabled'])
            arrowButton.state(['disabled'])
            canvas.delete(*canvas.find_withtag('b'))
            mData.drawBoundaries()
            MazeData.ad.done = True
            infoLabelText.set('Finished!')
            return
        
        curr = MazeData.ad.unchecked.pop(0)
        if curr > 0:
            other = curr - mData.cols
        else:
            other = -curr - 1
        
        currUfIndex = abs(curr)
        currUf = MazeData.ad.unionFind[currUfIndex]
        while currUf > 0:
            currUfIndex = currUf
            currUf = MazeData.ad.unionFind[currUfIndex]
        otherUfIndex = other
        otherUf = MazeData.ad.unionFind[otherUfIndex]
        while otherUf > 0:
            otherUfIndex = otherUf
            otherUf = MazeData.ad.unionFind[otherUfIndex]

        if currUfIndex != otherUfIndex:
            # cells are unconnected; it's okay to remove the boundary
            mData.boundaries.remove(curr)

            # update unionFind data structure
            if currUf < otherUf:
                MazeData.ad.unionFind[otherUfIndex] = currUfIndex
            elif otherUf < currUf:
                MazeData.ad.unionFind[currUfIndex] = otherUfIndex
            else:
                # currUf == otherUf
                # curr will become new root
                MazeData.ad.unionFind[currUfIndex] -= 1
                MazeData.ad.unionFind[otherUfIndex] = currUfIndex

        if stateData.animMode.get() == 'default' or \
            stateData.animMode.get() == 'step':
            self.drawEcAnimation()

        if stateData.animMode.get() == 'default':
            root.update_idletasks()
            root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                    lambda: self.stepEc())
        elif stateData.animMode.get() != 'step':
            self.stepEc()

    def drawEcAnimation(self):
        canvas.delete(*canvas.find_withtag('b'))
        mData.drawBoundaries()
        boundary = MazeData.ad.unchecked[0]
        b = abs(boundary)
        r = b // self.cols
        c = b % self.cols
        if boundary > 0:
            canvas.create_line(cData.margin + (cData.cell_w * c),
                                cData.margin + (cData.cell_h * r),
                                cData.margin + (cData.cell_w * (c+1)),
                                cData.margin + (cData.cell_h * r),
                                width=5, capstyle='round', fill='red',
                                tags=('b',))
        else:
            canvas.create_line(cData.margin + (cData.cell_w * c),
                                cData.margin + (cData.cell_h * r),
                                cData.margin + (cData.cell_w * c),
                                cData.margin + (cData.cell_h * (r+1)),
                                width=5, capstyle='round', fill='red',
                                tags=('b',))
        print(MazeData.ad)

    def drawSimpleSearchAnimation(self):
        curr = MazeData.ad.currWithParent[0]
        curr_r = curr // self.cols
        curr_c = curr % self.cols

        canvas.delete(*canvas.find_withtag('d'))

        # draw dots & lines from items in worklist to curr
        for vtx in MazeData.ad.worklistWithParents:
            sr = vtx[0] // self.cols
            sc = vtx[0] % self.cols
            er = vtx[1] // self.cols
            ec = vtx[1] % self.cols
            canvas.create_line(cData.margin + ((sc+0.5)*cData.cell_w),
                               cData.margin + ((sr+0.5)*cData.cell_h),
                               cData.margin + ((ec+0.5)*cData.cell_w),
                               cData.margin + ((er+0.5)*cData.cell_h),
                               width=cData.lineWidth, fill='red', capstyle='round',
                               tags=('d'))
            canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - cData.smallCircleRadius,
                               cData.margin + ((sr+0.5)*cData.cell_h) - cData.smallCircleRadius,
                               cData.margin + ((sc+0.5)*cData.cell_w) + cData.smallCircleRadius,
                               cData.margin + ((sr+0.5)*cData.cell_h) + cData.smallCircleRadius,
                               width=0, fill='red', tags=('d'))

        # draw dots & lines from traversalLog vertices to their parents
        for vtx in MazeData.ad.traversalLog:
            sr = vtx[0] // self.cols
            sc = vtx[0] % self.cols
            er = vtx[1] // self.cols
            ec = vtx[1] % self.cols
            canvas.create_line(cData.margin + ((sc+0.5)*cData.cell_w),
                               cData.margin + ((sr+0.5)*cData.cell_h),
                               cData.margin + ((ec+0.5)*cData.cell_w),
                               cData.margin + ((er+0.5)*cData.cell_h),
                               width=cData.lineWidth, fill='blue', capstyle='round',
                               tags=('d'))
            canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - cData.smallCircleRadius,
                               cData.margin + ((sr+0.5)*cData.cell_h) - cData.smallCircleRadius,
                               cData.margin + ((sc+0.5)*cData.cell_w) + cData.smallCircleRadius,
                               cData.margin + ((sr+0.5)*cData.cell_h) + cData.smallCircleRadius,
                               width=0, fill='blue', tags=('d'))

        # draw black dots
        for vtx in MazeData.ad.black:
            r = vtx // self.cols
            c = vtx % self.cols
            canvas.create_oval(cData.margin + ((c+0.5)*cData.cell_w) - cData.largeCircleRadius,
                                cData.margin + ((r+0.5)*cData.cell_h) - cData.largeCircleRadius,
                                cData.margin + ((c+0.5)*cData.cell_w) + cData.largeCircleRadius,
                                cData.margin + ((r+0.5)*cData.cell_h) + cData.largeCircleRadius,
                                width=0, fill='black', tags=('d'))

        # if finished, draw the solution line
        if MazeData.ad.solution:
            currColor = 'darkgreen'
            self.drawSolution()

        else:
            currColor = 'purple'

        # draw curr dot
        canvas.create_oval(cData.margin + ((curr_c+0.5)*cData.cell_w) - cData.largeCircleRadius,
                            cData.margin + ((curr_r+0.5)*cData.cell_h) - cData.largeCircleRadius,
                            cData.margin + ((curr_c+0.5)*cData.cell_w) + cData.largeCircleRadius,
                            cData.margin + ((curr_r+0.5)*cData.cell_h) + cData.largeCircleRadius,
                            width=0, fill=currColor, tags=('d'))

        print(f'curr: {MazeData.ad.currWithParent}\nseen: {MazeData.ad.seen}\ntraversalLog: {MazeData.ad.traversalLog}\nworklist: {MazeData.ad.worklistWithParents}\nblack: {MazeData.ad.black}\n') # TODO remove

    def drawSolution(self):
        # either use a queue to not have to calculate rows & columns
        # twice for each vertex, or TODO update to reflect new
        # indexing scheme
        for i in range(len(MazeData.ad.solution) - 1):
            sr = MazeData.ad.solution[i] // self.cols
            sc = MazeData.ad.solution[i] % self.cols
            er = MazeData.ad.solution[i+1] // self.cols
            ec = MazeData.ad.solution[i+1] % self.cols
            canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - cData.smallCircleRadius,
                            cData.margin + ((sr+0.5)*cData.cell_h) - cData.smallCircleRadius,
                            cData.margin + ((sc+0.5)*cData.cell_w) + cData.smallCircleRadius,
                            cData.margin + ((sr+0.5)*cData.cell_h) + cData.smallCircleRadius,
                            width=0, fill=rgbString(56, 176, 14),
                            tags=('d'))
            canvas.create_line(cData.margin + ((sc+0.5)*cData.cell_w),
                            cData.margin + ((sr+0.5)*cData.cell_h),
                            cData.margin + ((ec+0.5)*cData.cell_w),
                            cData.margin + ((er+0.5)*cData.cell_h),
                            width=cData.lineWidth, fill=rgbString(56, 176, 14),
                            capstyle='round', tags=('d'))


    def drawAsAnimation(self):
        curr = None
        canvas.delete(*canvas.find_withtag('d'))

        # draw open stuff with color gradient
        if len(MazeData.ad.openQueue.list) != 0:
            curr = MazeData.ad.openQueue.list[0].loc

            minColor = (10, 28, 10)
            maxColor = (89, 255, 89)
            buckets = MazeData.ad.openQueue.list[-1].f  # max f cost
            if buckets != 0:
                stepRed = abs(maxColor[0] - minColor[0]) // buckets
                stepGreen = abs(maxColor[1] - minColor[1]) // buckets
                stepBlue = abs(maxColor[2] - minColor[2]) // buckets
            else:
                stepRed, stepGreen, stepBlue = 0, 0, 0
            # TODO get rid of minColor and maxColor and just
            # put numbers in for lagging purposes?

            for vtx in MazeData.ad.openQueue.list:
                color = rgbString(minColor[0] + stepRed * vtx.f,
                                minColor[1] + stepGreen * vtx.f,
                                minColor[2] + stepBlue * vtx.f)
                sr = vtx.loc // self.cols
                sc = vtx.loc % self.cols
                er = vtx.parent // self.cols
                ec = vtx.parent % self.cols
                canvas.create_line(cData.margin + ((sc+0.5)*cData.cell_w),
                                cData.margin + ((sr+0.5)*cData.cell_h),
                                cData.margin + ((ec+0.5)*cData.cell_w),
                                cData.margin + ((er+0.5)*cData.cell_h),
                                width=cData.lineWidth, fill=color, capstyle='round',
                                tags=('d'))
                canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - cData.smallCircleRadius,
                                cData.margin + ((sr+0.5)*cData.cell_h) - cData.smallCircleRadius,
                                cData.margin + ((sc+0.5)*cData.cell_w) + cData.smallCircleRadius,
                                cData.margin + ((sr+0.5)*cData.cell_h) + cData.smallCircleRadius,
                                width=0, fill=color, tags=('d'))

        # draw closed stuff with color gradient
        if len(MazeData.ad.closedList.list) != 0:
            minColor = (135, 18, 21)
            maxColor = (255, 38, 44)
            buckets = MazeData.ad.closedList.list[-1].f  # max f cost
            if buckets != 0:
                stepRed = abs(maxColor[0] - minColor[0]) // buckets
                stepGreen = abs(maxColor[1] - minColor[1]) // buckets
                stepBlue = abs(maxColor[2] - minColor[2]) // buckets
            else:
                stepRed, stepGreen, stepBlue = 0, 0, 0
            # TODO get rid of minColor and maxColor and just
            # put numbers in for lagging purposes?

            for i in range(len(MazeData.ad.closedList.list)-1, -1, -1):
                vtx = MazeData.ad.closedList.list[i]
                color = rgbString(minColor[0] + stepRed * vtx.f,
                                minColor[1] + stepGreen * vtx.f,
                                minColor[2] + stepBlue * vtx.f)
                sr = vtx.loc // self.cols
                sc = vtx.loc % self.cols
                er = vtx.parent // self.cols
                ec = vtx.parent % self.cols
                canvas.create_line(cData.margin + ((sc+0.5)*cData.cell_w),
                                cData.margin + ((sr+0.5)*cData.cell_h),
                                cData.margin + ((ec+0.5)*cData.cell_w),
                                cData.margin + ((er+0.5)*cData.cell_h),
                                width=cData.lineWidth, fill=color, capstyle='round',
                                tags=('d'))
                canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - cData.smallCircleRadius,
                                cData.margin + ((sr+0.5)*cData.cell_h) - cData.smallCircleRadius,
                                cData.margin + ((sc+0.5)*cData.cell_w) + cData.smallCircleRadius,
                                cData.margin + ((sr+0.5)*cData.cell_h) + cData.smallCircleRadius,
                                width=0, fill=color, tags=('d'))

        # if finished, draw the solution line
        if MazeData.ad.solution:
            curr = mData.endCell
            currColor = 'darkgreen'
            self.drawSolution()
        else:
            currColor = 'purple'

        # draw curr dot
        if curr:
            curr_r = curr // self.cols
            curr_c = curr % self.cols
            canvas.create_oval(cData.margin + ((curr_c+0.5)*cData.cell_w) - cData.largeCircleRadius,
                                cData.margin + ((curr_r+0.5)*cData.cell_h) - cData.largeCircleRadius,
                                cData.margin + ((curr_c+0.5)*cData.cell_w) + cData.largeCircleRadius,
                                cData.margin + ((curr_r+0.5)*cData.cell_h) + cData.largeCircleRadius,
                                width=0, fill=currColor, tags=('d'))

        print(f'openQueue: {MazeData.ad.openQueue}\nclosedList: {MazeData.ad.closedList}\n')    # TODO remove

    def updateRows(self):
        # update start/end cells if they're on the bottom row
        if (self.startCell >= self.cols*(self.rows-1)):
            self.startCell = (int(rowsSpinbox.get())-1) * self.cols + \
                             self.startCell % self.cols
        if (self.endCell >= self.cols*(self.rows-1)):
            self.endCell = (int(rowsSpinbox.get())-1) * self.cols + \
                           self.endCell % self.cols

        self.rows = int(rowsSpinbox.get())

        # update canvas dimensions
        cData.cell_w = (cData.w - (2*cData.margin)) / self.cols
        cData.cell_h = (cData.h - (2*cData.margin)) / self.rows
        cData.lineWidth = min(cData.cell_w, cData.cell_h) // 6
        cData.smallCircleRadius = cData.lineWidth
        cData.largeCircleRadius = int(cData.smallCircleRadius * 1.5)
        self.drawMaze()
    
    def updateCols(self):
        # update start/end cells if they're on the right
        if (self.startCell % self.cols == self.cols - 1):
            self.startCell = (self.startCell // self.cols + 1) * \
                             int(colsSpinbox.get()) - 1
        if (self.endCell % self.cols == self.cols - 1):
            self.endCell = (self.endCell // self.cols + 1) * \
                           int(colsSpinbox.get()) - 1

        self.cols = int(colsSpinbox.get())

        # update canvas dimensions
        cData.cell_w = (cData.w - (2*cData.margin)) / self.cols
        cData.cell_h = (cData.h - (2*cData.margin)) / self.rows
        cData.lineWidth = min(cData.cell_w, cData.cell_h) // 6
        cData.smallCircleRadius = cData.lineWidth
        cData.largeCircleRadius = int(cData.smallCircleRadius * 1.5)
        self.drawMaze()
    
    def updateStartEndCells(self):
        pass
        # TODO ??? don't know if i'll need this
        # want changing location of start and end cells feature to be disabled
        # when:
        # an animation is running
        # when we're in generate mode, and there's a human-drawn solution still
        # there
        # MAKE IT SO THEY JUST CAN'T BE PUT ON THE SAME SQUARE (text would overlap)
        
    def clearMaze(self):
        if (stateData.mode == 'sol'):
            self.boundaries = set()
        else:
            pass
            # TODO add support for clearing solve line in generate mode
        self.drawMaze()  
        # to be called when Clear Maze button is pressed
        # updates MazeData object, clearing boundaries/solve line,
        # depending on what mode it's in

class CanvasData(object):
    def __init__(self, resizeRedrawDelay, startWidth, startHeight):
        self.resizeRedrawDelay = resizeRedrawDelay  # prevent resize redraw lagging
        self.resizeTracker = 0

        # initialize canvas dimension properties
        self.w = startWidth
        self.h = startHeight
        self.margin = min(self.w, self.h) / 10
        self.cell_w = (self.w - 2*self.margin) / mData.rows
        self.cell_h = (self.h - 2*self.margin) / mData.cols
        self.lineWidth = min(self.cell_w, self.cell_h) // 6
        self.smallCircleRadius = self.lineWidth
        self.largeCircleRadius = int(self.smallCircleRadius * 1.5)

    def resizeCanvas(self):
        # to be called whenever the screen is resized
        self.resizeTracker += 1
        # canvas.update_idletasks()
        if self.resizeTracker == self.resizeRedrawDelay:
            # update canvas dimension properties
            self.w = canvas.winfo_width()
            self.h = canvas.winfo_height()
            self.margin = min(self.w, self.h) / 10
            self.cell_w = (self.w - 2*self.margin) / mData.cols
            self.cell_h = (self.h - 2*self.margin) / mData.rows
            self.lineWidth = min(self.cell_w, self.cell_h) // 8
            self.smallCircleRadius = self.lineWidth
            self.largeCircleRadius = int(self.smallCircleRadius * 1.5)

            mData.drawMaze()
            self.resizeTracker = 0

        
    
    def mouseHovering(self, e):
        if MazeData.ad: return

        r = (e.y - cData.margin) // cData.cell_h
        c = (e.x - cData.margin) // cData.cell_w
        if (stateData.mode == 'sol'):
            canvas.delete(*canvas.find_withtag('hoverBound'))
            if (cData.margin < e.x < cData.w - cData.margin) and \
               (cData.margin < e.y < cData.h - cData.margin):
                local_x = (e.x - cData.margin) % cData.cell_w
                local_y = (e.y - cData.margin) % cData.cell_h
                if (local_x > local_y) and (local_x > (cData.cell_h - local_y)):
                    # draw boundary to right
                    canvas.create_line(cData.margin + ((1+c)*cData.cell_w),
                                       cData.margin + (r*cData.cell_h),
                                       cData.margin + ((1+c)*cData.cell_w),
                                       cData.margin + ((1+r)*cData.cell_h),
                                       stipple='gray50',
                                       width=5, capstyle='round',
                                       tags=('hoverBound'))         # TODO mData.boundaryWidth - replace everywhere
                elif (local_x > local_y):
                    # draw boundary up
                    canvas.create_line(cData.margin + (c*cData.cell_w),
                                       cData.margin + (r*cData.cell_h),
                                       cData.margin + ((1+c)*cData.cell_w),
                                       cData.margin + (r*cData.cell_h),
                                       stipple='gray50',
                                       width=5, capstyle='round',
                                       tags=('hoverBound'))
                elif (local_x > (cData.cell_h - local_y)):
                    # draw boundary down
                    canvas.create_line(cData.margin + (c*cData.cell_w),
                                       cData.margin + ((1+r)*cData.cell_h),
                                       cData.margin + ((1+c)*cData.cell_w),
                                       cData.margin + ((1+r)*cData.cell_h),
                                       stipple='gray50',
                                       width=5, capstyle='round',
                                       tags=('hoverBound'))
                else:
                    # draw boundary to left
                    canvas.create_line(cData.margin + (c*cData.cell_w),
                                       cData.margin + (r*cData.cell_h),
                                       cData.margin + (c*cData.cell_w),
                                       cData.margin + ((1+r)*cData.cell_h),
                                       stipple='gray50',
                                       width=5, capstyle='round',
                                       tags=('hoverBound'))
        else:
            canvas.delete(*canvas.find_withtag('hoverNode'))
            # TODO add stuff to do when mouse is hovering
            # while in generate mode
            # only want something to happen if in start square,
            # or current active square
            # if (margin < e.x < w - margin) and \
            #    (margin < e.y < h - margin):
            #     diameter = min(cell_w, cell_h) / 4
            #     canvas.create_oval()

        # TODO eventual support for changing start and end squares
        
        # lift and lower methods for canvas items allow
        # you to change the worklisting order

    def mouseClicked(self, e):
        if MazeData.ad: return
        
        print(mData.boundaries)  # TODO remove later
        c = (e.x - cData.margin) // cData.cell_w
        r = (e.y - cData.margin) // cData.cell_h
        if (stateData.mode == 'sol'):
            if (cData.margin < e.x < cData.w - cData.margin) and \
               (cData.margin < e.y < cData.h - cData.margin):
                local_x = (e.x - cData.margin) % cData.cell_w
                local_y = (e.y - cData.margin) % cData.cell_h
                if (local_x > local_y) and (local_x > (cData.cell_h - local_y)):
                    # add boundary to right
                    if (c != mData.cols - 1):
                        boundary = int(-1 * (r*mData.cols + c + 1))
                        if boundary in mData.boundaries:
                            mData.boundaries.remove(boundary)
                        else:
                            mData.boundaries.add(boundary)
                elif (local_x > local_y):
                    # add boundary up
                    if (r != 0):
                        boundary = int(r*mData.cols + c)
                        if boundary in mData.boundaries:
                            mData.boundaries.remove(boundary)
                        else:
                            mData.boundaries.add(boundary)
                elif (local_x > (cData.cell_h - local_y)):
                    # add boundary down
                    if (r != mData.rows - 1):
                        boundary = int((r+1)*mData.cols + c)
                        if boundary in mData.boundaries:
                            mData.boundaries.remove(boundary)
                        else:
                            mData.boundaries.add(boundary)
                else:
                    # add boundary to left
                    boundary = int(-1 * (r*mData.cols + c))
                    if boundary in mData.boundaries:
                        mData.boundaries.remove(boundary)
                    else:
                        mData.boundaries.add(boundary)
            canvas.delete(*canvas.find_withtag('b'))
            mData.drawBoundaries()
            self.mouseHovering(e)
        else:
            pass
            # TODO add stuff to do when mouse is clicked
            # in generate mode

    def mouseDragging(self, e):
        if MazeData.ad: return
        
        c = (e.x - cData.margin) // cData.cell_w
        r = (e.y - cData.margin) // cData.cell_h
        if (stateData.mode == 'sol'):
            if (cData.margin < e.x < cData.w - cData.margin) and \
               (cData.margin < e.y < cData.h - cData.margin):
                local_x = (e.x - cData.margin) % cData.cell_w
                local_y = (e.y - cData.margin) % cData.cell_h
                if (local_x > local_y) and (local_x > (cData.cell_h - local_y)):
                    # add boundary to right
                    if (c != mData.cols - 1):
                        boundary = int(-1 * (r*mData.cols + c + 1))
                        if boundary not in mData.boundaries:
                            mData.boundaries.add(boundary)
                elif (local_x > local_y):
                    # add boundary up
                    if (r != 0):
                        boundary = int(r*mData.cols + c)
                        if boundary not in mData.boundaries:
                            mData.boundaries.add(boundary)
                elif (local_x > (cData.cell_h - local_y)):
                    # add boundary down
                    if (r != mData.rows - 1):
                        boundary = int((r+1)*mData.cols + c)
                        if boundary not in mData.boundaries:
                            mData.boundaries.add(boundary)
                else:
                    # add boundary to left
                    boundary = int(-1 * (r*mData.cols + c))
                    if boundary not in mData.boundaries:
                        mData.boundaries.add(boundary)
            canvas.delete(*canvas.find_withtag('b'))
            mData.drawBoundaries() 
        else:
            pass
            # TODO add here the stuff to do when mouse is dragged
            # in generate mode


print('starting...')
root = Tk()
root.title('Mazes')

defaultRows = 4
defaultCols = 6
defaultSpeed = 5   # from 1 to 30; 30 is one second per step
defaultCanvasWidth = 504
defaultCanvasHeight = 354
defaultBounds = set([7, -22, -20, 14, 15, 16, -15,
                    -16, -13, -11, -9, -7, -6, -1])
redrawDelay = 1

pauseImage = PhotoImage(file='images/pause.png')
playImage = PhotoImage(file='images/start.png')
stopImage = PhotoImage(file='images/stop.png')
arrowImage = PhotoImage(file='images/arrow.png')
pauseImage = pauseImage.subsample(5, 5)
playImage = playImage.subsample(5, 5)
stopImage = stopImage.subsample(5, 5)
arrowImage = arrowImage.subsample(10, 10)

defFont = font.nametofont('TkDefaultFont')
defFont['size'] += 2
largerFont = font.Font(family=defFont['family'],
                        name='largerFont', size=(defFont['size']+5))

s = ttk.Style()
s.configure('OptionsButton.TButton', wraplength=80,
                justify='center', padding=5)
s.configure('InfoLabel.TLabel', wraplength=500)

# create the object instances that will store all the data
mData = MazeData(defaultRows, defaultCols, defaultBounds,
                 0, defaultRows*defaultCols - 1)
stateData = ApplicationStateData()
cData = CanvasData(redrawDelay, defaultCanvasWidth, defaultCanvasHeight)


# create widgets
mainframe = ttk.Frame(root, relief='ridge', borderwidth=10)

modeButtonsFrame = ttk.Frame(mainframe, relief='sunken', borderwidth=5)
solveModeButton = ttk.Button(modeButtonsFrame, text='Solve Mode', width=30,
                            command=stateData.setSolveMode)
genModeButton = ttk.Button(modeButtonsFrame, text='Generate Mode', width=30,
                        command=stateData.setGenerateMode)

genControlsFrame = ttk.Frame(mainframe, relief='sunken', borderwidth=5)
clearButton = ttk.Button(genControlsFrame, text='Clear Maze',
                        command=lambda: mData.clearMaze())
rowsLabel = ttk.Label(genControlsFrame, text='Rows: ')
rowsSpinbox = ttk.Spinbox(genControlsFrame, from_=2.0, to=30.0,
                        command=lambda: mData.updateRows())    # TODO disable when there's user-inputted stuff on the maze, or an animation running
colsLabel = ttk.Label(genControlsFrame, text='Columns: ')
colsSpinbox = ttk.Spinbox(genControlsFrame, from_=2.0, to=30.0,
                        command=lambda: mData.updateCols())    # TODO disable when there's user-inputted stuff on the maze, or an animation running
# use rowsSpinbox.get()

algDisplayFrame = ttk.Frame(mainframe, relief='sunken', borderwidth=5)
algSupLabel = ttk.Label(algDisplayFrame, text='Algorithm:', width=30)
algCombobox = ttk.Combobox(algDisplayFrame, textvariable=stateData.currentAlgorithm)
configAlgButton = ttk.Button(algDisplayFrame, style='OptionsButton.TButton',
                                text='Algorithm Info & Options',
                                command=stateData.configAlgButtonPushed)
animationSpeedLabel = ttk.Label(algDisplayFrame, text='Animation Speed:')
animationSpeedSlider = ttk.Scale(algDisplayFrame, orient=HORIZONTAL, length=40,
                                from_=30.0, to=1.0)         # use animationSpeedSlider.get()
animationStepButton = ttk.Button(algDisplayFrame, text='Step Animation') # grid only when in step mode;

configAnimButton = ttk.Button(algDisplayFrame, style='OptionsButton.TButton',
                                text='Animation Options',
                                command=stateData.configAnimButtonPushed)

solgenFrame = ttk.Frame(mainframe)
solgenButton = ttk.Button(solgenFrame, 
                            textvariable=stateData.solgenButtonText,
                            command=stateData.startAnimateMode,
                            default='active')
pausePlayButton = ttk.Button(solgenFrame, image=pauseImage,
                             command=stateData.pauseAnimation)
arrowButton = ttk.Button(solgenFrame, image=arrowImage)     # TODO set callback
stopButton = ttk.Button(solgenFrame, image=stopImage,
                        command=stateData.stopAnimateMode)

infoFrame = ttk.Frame(mainframe)
infoLabelText = StringVar(value='Welcome!')
infoLabel = ttk.Label(infoFrame, textvariable=infoLabelText, font=largerFont)

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

solgenFrame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
solgenButton.grid(sticky='nsew', columnspan=2)
pausePlayButton.grid(row=0, column=1, sticky='nsw', padx=(5, 0))
arrowButton.grid(row=0, column=1, sticky='nsw', padx=(5, 0))
stopButton.grid(row=0, column=0, sticky='nse')
arrowButton.grid_remove()
pausePlayButton.grid_remove()
stopButton.grid_remove()

algDisplayFrame.grid(row=3, column=0, sticky='ews', padx=5, pady=5)
algSupLabel.grid(row=0, column=0, sticky='nsw', padx=5, pady=5)
algCombobox.grid(row=1, column=0, sticky='nsew', padx=5, pady=(5,10))
configAlgButton.grid(row=0, rowspan=2, column=1, sticky='nsew', padx=5, pady=5)
animationSpeedLabel.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
animationSpeedSlider.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
configAnimButton.grid(row=2, rowspan=2, column=1, sticky='nsew', padx=5, pady=5)

infoFrame.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
infoLabel.grid(sticky='ns', padx=5, pady=10)

canvas.grid(row=1, column=1, rowspan=3, sticky='nsew', padx=5, pady=5)


root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=50)
mainframe.rowconfigure(2, weight=50)
mainframe.rowconfigure(3, weight=50)
mainframe.rowconfigure(4, weight=1)
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
solgenFrame.rowconfigure(0, weight=1)
solgenFrame.columnconfigure(0, weight=1)
solgenFrame.columnconfigure(1, weight=1)
algDisplayFrame.rowconfigure(0, weight=1)
algDisplayFrame.rowconfigure(1, weight=1)
algDisplayFrame.columnconfigure(0, weight=1)
algDisplayFrame.columnconfigure(1, weight=1)
infoFrame.rowconfigure(0, weight=1)
infoFrame.columnconfigure(0, weight=1)
























rowsSpinbox.state(['readonly'])
colsSpinbox.state(['readonly'])
rowsSpinbox.set(defaultRows)
colsSpinbox.set(defaultCols)
animationSpeedSlider.set(defaultSpeed)
# then draw the data onto the canvas
# initially draw the canvas and maze
canvas.create_rectangle(0, 0, defaultCanvasWidth,
                        defaultCanvasHeight, fill='white')
mData.drawMaze()
stateData.setSolveMode()
SimpleSearchAnimationData.initDfsBfsFuncs()

# add event binding to handle canvas resizing
canvas.bind('<Configure>', lambda e: cData.resizeCanvas())
canvas.bind('<Motion>', cData.mouseHovering)
canvas.bind('<B1-Motion>', cData.mouseDragging)
canvas.bind('<ButtonPress-1>', cData.mouseClicked)

root.bind('<<ComboboxSelected>>', stateData.algorithmChanged)
root.bind('<Control-w>', lambda e: root.destroy())

root.update_idletasks()
root.geometry('1000x600+200+200')

root.mainloop()
print('application closed')


# to do:

# find solve line function - use traversalLog to just trace back,
# since every node is stored only once

# mData now has mData.animData class-wide attribute that stores animation
# data when animate mode is on
# - can phase out mData.animateModeOn, since we know the mode is on
# when animData is not None

