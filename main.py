from tkinter import *
from tkinter import ttk
# from applicationStateData import *
# from mazeData import *
# from canvasData import *

def rgbString(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)

class SimpleSearchAnimationData(object):
    dfsOrder = ['Up', 'Down', 'Right', 'Left']      # TODO for later

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
    solveAlgorithms = ['dfs', 'bfs', 'as']   # dijkstra?
    genAlgorithms = ['ec', 'vc']    # possibly more?

    def __init__(self):
        self.solgenButtonText = StringVar()
        # self.mode = 'sol'
        self.setSolveMode()     # ***initializes self.mode***
        self.animationRunning = BooleanVar(value=False)
        self.animStepModeOn = False
        self.currentAlgorithm = StringVar(value='as')
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
    



    def startAnimateMode(self):
        # TODO could just put all of this in mData.animate... maybe not
        # for the sake of modularity?
        self.animationRunning.set(True)
        solgenButton.grid_remove()
        pausePlayButton.config(image=pauseImage, command=self.pauseAnimation)
        pausePlayButton.grid()
        stopButton.grid()

        # disable ui widgets
        solveModeButton.state(['disabled'])
        genModeButton.state(['disabled'])
        clearButton.state(['disabled'])
        rowsSpinbox.state(['disabled'])
        colsSpinbox.state(['disabled'])
        # animationSpeedSlider.state(['disabled'])
        configAlgButton.state(['disabled'])
        configAnimButton.state(['disabled'])

        # TODO change appearance of frames and such?

        # animationSpeedSlider.get() -- use when programming in

        print('startAnimateMode called')
        print('starting the animation...')

        mData.animate()

    def pauseAnimation(self):
        # called when the pausePlayButton is pressed while animation is playing
        self.animationRunning.set(False)
        pausePlayButton.config(image=playImage, command=self.playAnimation)

    def playAnimation(self):
        # called when the pausePlayButton is pressed while animation is paused
        self.animationRunning.set(True)
        pausePlayButton.config(image=pauseImage, command=self.pauseAnimation)

    def stopAnimateMode(self):
        # called when the stopButton is pressed
        MazeData.ad = None
        self.animationRunning.set(True)
        self.animationRunning.set(False)
        pausePlayButton.grid_remove()
        stopButton.grid_remove()
        solgenButton.grid()

        # enable all widgets
        solveModeButton.state(['!disabled'])
        genModeButton.state(['!disabled'])
        clearButton.state(['!disabled'])
        rowsSpinbox.state(['!disabled'])
        colsSpinbox.state(['!disabled'])
        # animationSpeedSlider.state(['!disabled'])
        configAlgButton.state(['!disabled'])
        configAnimButton.state(['!disabled'])
        
        # clear animation
        canvas.delete(*canvas.find_withtag('d'))

        print('stopAnimateMode called')
    
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
            if stateData.currentAlgorithm.get() == 'dfs' or \
               stateData.currentAlgorithm.get() == 'bfs':
                mData.drawSimpleSearchAnimation()
            else:
                mData.drawAsAnimation()

    
    def animate(self):
        if stateData.currentAlgorithm.get() == 'dfs':
            MazeData.ad = SimpleSearchAnimationData(self.startCell)
            self.drawSimpleSearchAnimation()
            root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                   lambda: self.stepDfs())
            # TODO configure step button here to have stepDfs
            # as its callback, & same for the other cases
        elif stateData.currentAlgorithm.get() == 'bfs':
            MazeData.ad = SimpleSearchAnimationData(self.startCell)
            self.drawSimpleSearchAnimation()
            root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                   lambda: self.stepBfs())
        elif stateData.currentAlgorithm.get() == 'as':
            MazeData.ad = asAnimationData(self.startCell)
            self.drawAsAnimation()
            root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                   lambda: self.stepAs())
        else:
            print('There was a problem... algorithm not valid')
            stateData.stopAnimateMode()

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
            print('maze solved!')
            self.drawSimpleSearchAnimation()
            # TODO update ui elements
            return

        # collect neighbors; if unmarked, push them into worklist
        upper = curr - self.cols
        lower = curr + self.cols
        left = curr - 1
        right = curr + 1
        noValidNeighbors = True

        # TODO maybe you could put all of these code blocks into
        # individual functions, passing in data that is updated,
        # and have the globally stored information be a list of
        # functions to determine the priority order for dfs

        # check upper neighbor if exists
        if (upper not in MazeData.ad.seen and \
            curr not in self.boundaries and \
            upper >= 0):
            MazeData.ad.seen.add(upper)
            MazeData.ad.worklistWithParents.append((upper, curr))
            noValidNeighbors = False

        # check lower neighbor if exists
        if (lower not in MazeData.ad.seen and \
            lower not in self.boundaries and \
            lower < self.rows*self.cols):
            MazeData.ad.seen.add(lower)
            MazeData.ad.worklistWithParents.append((lower, curr))
            noValidNeighbors = False

        # check neighbor to left if exists
        if (left not in MazeData.ad.seen and \
            -curr not in self.boundaries and \
            curr % self.cols != 0):
            MazeData.ad.seen.add(left)
            MazeData.ad.worklistWithParents.append((left, curr))
            noValidNeighbors = False

        # check neighbor to right if exists
        if (right not in MazeData.ad.seen and \
            -right not in self.boundaries and \
            (curr+1) % self.cols != 0):
            MazeData.ad.seen.add(right)
            MazeData.ad.worklistWithParents.append((right, curr))
            noValidNeighbors = False

        if noValidNeighbors:
            MazeData.ad.black.append(curr)
        
        self.drawSimpleSearchAnimation()
        
        if len(MazeData.ad.worklistWithParents) == 0:     # stack empty; maze unsolvable
            print('maze unsolvable')
            return
            # TODO update ui state label

        root.update()
        root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                   lambda: self.stepDfs())
        # TODO if animation is in step mode, don't do this

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
            print('maze solved!')
            self.drawSimpleSearchAnimation()
            # TODO update ui elements
            return

        # collect neighbors; if unmarked, push them into worklist
        upper = curr - self.cols
        lower = curr + self.cols
        left = curr - 1
        right = curr + 1
        noValidNeighbors = True

        # TODO maybe you could put all of these code blocks into
        # individual functions, passing in data that is updated,
        # and have the globally stored information be a list of
        # functions to determine the priority order for dfs

        # check upper neighbor if exists
        if (upper not in MazeData.ad.seen and \
            curr not in self.boundaries and \
            upper >= 0):
            MazeData.ad.seen.add(upper)
            MazeData.ad.worklistWithParents.append((upper, curr))
            noValidNeighbors = False

        # check lower neighbor if exists
        if (lower not in MazeData.ad.seen and \
            lower not in self.boundaries and \
            lower < self.rows*self.cols):
            MazeData.ad.seen.add(lower)
            MazeData.ad.worklistWithParents.append((lower, curr))
            noValidNeighbors = False

        # check neighbor to left if exists
        if (left not in MazeData.ad.seen and \
            -curr not in self.boundaries and \
            curr % self.cols != 0):
            MazeData.ad.seen.add(left)
            MazeData.ad.worklistWithParents.append((left, curr))
            noValidNeighbors = False

        # check neighbor to right if exists
        if (right not in MazeData.ad.seen and \
            -right not in self.boundaries and \
            (curr+1) % self.cols != 0):
            MazeData.ad.seen.add(right)
            MazeData.ad.worklistWithParents.append((right, curr))
            noValidNeighbors = False

        if noValidNeighbors:
            MazeData.ad.black.append(curr)
        
        self.drawSimpleSearchAnimation()
        
        if len(MazeData.ad.worklistWithParents) == 0:     # worklist empty; maze unsolvable
            print('maze unsolvable')
            return
            # TODO update ui state label

        root.update()
        root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                   lambda: self.stepBfs())
        # TODO if animation is in step mode, don't do this

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
            print('maze unsolvable')
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
                print('maze solved!')
                self.drawAsAnimation()
                # TODO update ui elements
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
                print('maze solved!')
                self.drawAsAnimation()
                # TODO update ui elements
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
                print('maze solved!')
                self.drawAsAnimation()
                # TODO update ui elements
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
                print('maze solved!')
                self.drawAsAnimation()
                # TODO update ui elements
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
        self.drawAsAnimation() 

        root.update()   # TODO necessary?
        root.after(int(animationSpeedSlider.get()) * 1000 // 30, 
                   lambda: self.stepAs())
        # TODO if animation is in step mode, don't do this

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
                               width=7, fill='red', capstyle='round',
                               tags=('d'))
            canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - 10,
                               cData.margin + ((sr+0.5)*cData.cell_h) - 10,
                               cData.margin + ((sc+0.5)*cData.cell_w) + 10,
                               cData.margin + ((sr+0.5)*cData.cell_h) + 10,
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
                               width=7, fill='blue', capstyle='round',
                               tags=('d'))
            canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - 10,
                               cData.margin + ((sr+0.5)*cData.cell_h) - 10,
                               cData.margin + ((sc+0.5)*cData.cell_w) + 10,
                               cData.margin + ((sr+0.5)*cData.cell_h) + 10,
                               width=0, fill='blue', tags=('d'))

        # draw black dots
        for vtx in MazeData.ad.black:
            r = vtx // self.cols
            c = vtx % self.cols
            canvas.create_oval(cData.margin + ((c+0.5)*cData.cell_w) - 16,
                                cData.margin + ((r+0.5)*cData.cell_h) - 16,
                                cData.margin + ((c+0.5)*cData.cell_w) + 16,
                                cData.margin + ((r+0.5)*cData.cell_h) + 16,
                                width=0, fill='black', tags=('d'))

        # if finished, draw the solution line
        if MazeData.ad.solution:
            currColor = 'darkgreen'

            # either use a queue to not have to calculate rows & columns
            # twice for each vertex, or TODO update to reflect new
            # indexing scheme
            for i in range(len(MazeData.ad.solution) - 1):
                sr = MazeData.ad.solution[i] // self.cols
                sc = MazeData.ad.solution[i] % self.cols
                er = MazeData.ad.solution[i+1] // self.cols
                ec = MazeData.ad.solution[i+1] % self.cols
                canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - 10,
                                cData.margin + ((sr+0.5)*cData.cell_h) - 10,
                                cData.margin + ((sc+0.5)*cData.cell_w) + 10,
                                cData.margin + ((sr+0.5)*cData.cell_h) + 10,
                                width=0, fill=rgbString(56, 176, 14),
                                tags=('d'))
                canvas.create_line(cData.margin + ((sc+0.5)*cData.cell_w),
                               cData.margin + ((sr+0.5)*cData.cell_h),
                               cData.margin + ((ec+0.5)*cData.cell_w),
                               cData.margin + ((er+0.5)*cData.cell_h),
                               width=7, fill=rgbString(56, 176, 14),
                               capstyle='round', tags=('d'))

        else:
            currColor = 'purple'

        # draw curr dot
        canvas.create_oval(cData.margin + ((curr_c+0.5)*cData.cell_w) - 16,
                            cData.margin + ((curr_r+0.5)*cData.cell_h) - 16,
                            cData.margin + ((curr_c+0.5)*cData.cell_w) + 16,
                            cData.margin + ((curr_r+0.5)*cData.cell_h) + 16,
                            width=0, fill=currColor, tags=('d'))

        print(f'curr: {MazeData.ad.currWithParent}\nseen: {MazeData.ad.seen}\ntraversalLog: {MazeData.ad.traversalLog}\nworklist: {MazeData.ad.worklistWithParents}\nblack: {MazeData.ad.black}\n') # TODO remove

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
                                width=7, fill=color, capstyle='round',
                                tags=('d'))
                canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - 10,
                                cData.margin + ((sr+0.5)*cData.cell_h) - 10,
                                cData.margin + ((sc+0.5)*cData.cell_w) + 10,
                                cData.margin + ((sr+0.5)*cData.cell_h) + 10,
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
                                width=7, fill=color, capstyle='round',
                                tags=('d'))
                canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - 10,
                                cData.margin + ((sr+0.5)*cData.cell_h) - 10,
                                cData.margin + ((sc+0.5)*cData.cell_w) + 10,
                                cData.margin + ((sr+0.5)*cData.cell_h) + 10,
                                width=0, fill=color, tags=('d'))

        # if finished, draw the solution line
        if MazeData.ad.solution:
            curr = mData.endCell
            currColor = 'darkgreen'

            # either use a queue to not have to calculate rows & columns
            # twice for each vertex, or TODO update to reflect new
            # indexing scheme
            for i in range(len(MazeData.ad.solution) - 1):
                sr = MazeData.ad.solution[i] // self.cols
                sc = MazeData.ad.solution[i] % self.cols
                er = MazeData.ad.solution[i+1] // self.cols
                ec = MazeData.ad.solution[i+1] % self.cols
                canvas.create_oval(cData.margin + ((sc+0.5)*cData.cell_w) - 10,
                                cData.margin + ((sr+0.5)*cData.cell_h) - 10,
                                cData.margin + ((sc+0.5)*cData.cell_w) + 10,
                                cData.margin + ((sr+0.5)*cData.cell_h) + 10,
                                width=0, fill=rgbString(56, 176, 14),
                                tags=('d'))
                canvas.create_line(cData.margin + ((sc+0.5)*cData.cell_w),
                               cData.margin + ((sr+0.5)*cData.cell_h),
                               cData.margin + ((ec+0.5)*cData.cell_w),
                               cData.margin + ((er+0.5)*cData.cell_h),
                               width=7, fill=rgbString(56, 176, 14),
                               capstyle='round', tags=('d'))
        else:
            currColor = 'purple'

        # draw curr dot
        if curr:
            curr_r = curr // self.cols
            curr_c = curr % self.cols
            canvas.create_oval(cData.margin + ((curr_c+0.5)*cData.cell_w) - 16,
                                cData.margin + ((curr_r+0.5)*cData.cell_h) - 16,
                                cData.margin + ((curr_c+0.5)*cData.cell_w) + 16,
                                cData.margin + ((curr_r+0.5)*cData.cell_h) + 16,
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

            mData.drawMaze()
            # TODO if an animation is running, redraw that too
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
pauseImage = pauseImage.subsample(5, 5)
playImage = playImage.subsample(5, 5)
stopImage = stopImage.subsample(5, 5)

# create the object instances that will store all the data
mData = MazeData(defaultRows, defaultCols, defaultBounds,
                 0, defaultRows*defaultCols - 1)
stateData = ApplicationStateData()
cData = CanvasData(redrawDelay, defaultCanvasWidth, defaultCanvasHeight)

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
                        command=lambda: mData.clearMaze())
rowsLabel = ttk.Label(genControlsFrame, text='Rows: ')
rowsSpinbox = ttk.Spinbox(genControlsFrame, from_=2.0, to=30.0,
                        command=lambda: mData.updateRows())    # TODO disable when there's user-inputted stuff on the maze, or an animation running
colsLabel = ttk.Label(genControlsFrame, text='Columns: ')
colsSpinbox = ttk.Spinbox(genControlsFrame, from_=2.0, to=30.0,
                        command=lambda: mData.updateCols())    # TODO disable when there's user-inputted stuff on the maze, or an animation running
# use rowsSpinbox.get() to get the value in the spinbox

algDisplayFrame = ttk.Frame(mainframe, relief='sunken', borderwidth=5)
algSupLabel = ttk.Label(algDisplayFrame, text='Algorithm:', width=30)
algMainLabel = ttk.Label(algDisplayFrame, textvariable=stateData.currentAlgorithm,
                        anchor='center', relief='ridge', borderwidth=10)  # TODO more decoration?
configAlgButton = ttk.Button(algDisplayFrame,
                                text='Configure\nAlgorithm\nOptions',
                                command=stateData.configAlgButtonPushed)
animationSpeedLabel = ttk.Label(algDisplayFrame, text='Animation Speed:')
animationSpeedSlider = ttk.Scale(algDisplayFrame, orient=HORIZONTAL, length=40,
                                from_=30.0, to=1.0)
# use animationSpeedSlider.get()
# PUT STEP OR SPEED THING BELOW algMainLabel
animationStepButton = ttk.Button(algDisplayFrame, text='Step Animation',
                                    command=stateData.stepAnimation)   # grid only when in step mode
configAnimButton = ttk.Button(algDisplayFrame,
                                text='Configure\nAnimation\nOptions',
                                command=stateData.configAnimButtonPushed)

solgenFrame = ttk.Frame(mainframe)
solgenButton = ttk.Button(solgenFrame, 
                            textvariable=stateData.solgenButtonText,
                            command=stateData.startAnimateMode,
                            default='active')
pausePlayButton = ttk.Button(solgenFrame, image=pauseImage,
                             command=stateData.pauseAnimation)    # TODO add command callback
stopButton = ttk.Button(solgenFrame, image=stopImage,
                        command=stateData.stopAnimateMode)         # TODO add command callback

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
pausePlayButton.grid(row=0, column=0, sticky='nse', padx=(0,5))
stopButton.grid(row=0, column=1, sticky='nsw')
pausePlayButton.grid_remove()
stopButton.grid_remove()

algDisplayFrame.grid(row=3, column=0, sticky='ews', padx=5, pady=5)
algSupLabel.grid(row=0, column=0, sticky='nsw', padx=5, pady=5)
algMainLabel.grid(row=1, column=0, sticky='nsew', padx=5, pady=(5,10))
configAlgButton.grid(row=0, rowspan=2, column=1, sticky='nsew', padx=5, pady=5)
animationSpeedLabel.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
animationSpeedSlider.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
configAnimButton.grid(row=2, rowspan=2, column=1, sticky='nsew', padx=5, pady=5)

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
solgenFrame.rowconfigure(0, weight=1)
solgenFrame.columnconfigure(0, weight=1)
solgenFrame.columnconfigure(1, weight=1)
algDisplayFrame.rowconfigure(0, weight=1)
algDisplayFrame.rowconfigure(1, weight=1)
algDisplayFrame.columnconfigure(0, weight=1)
algDisplayFrame.columnconfigure(1, weight=1)
























# Put this next block into function to initialize everything



# put algorithm StringVar into AnimationStateData object

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
# add event binding to handle canvas resizing
canvas.bind('<Configure>', lambda e: cData.resizeCanvas())
canvas.bind('<Motion>', cData.mouseHovering)
canvas.bind('<B1-Motion>', cData.mouseDragging)
canvas.bind('<ButtonPress-1>', cData.mouseClicked)

root.mainloop()
print('done')


# to do:

# find solve line function - use traversalLog to just trace back,
# since every node is stored only once

# mData now has mData.animData class-wide attribute that stores animation
# data when animate mode is on
# - can phase out mData.animateModeOn, since we know the mode is on
# when animData is not None