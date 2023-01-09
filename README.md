# Mazes

This is a small application that can be used to randomly generate and solve mazes using various graph algorithms. It shows animations to help visualize how the algorithms are working. The app is written in Python using the `tkinter` library.

## Usage

The app has two modes, Solve Mode and Generate Mode, for solving and generating mazes respectively. You can toggle between modes using the buttons at the top of the window. To run the animations, click "Solve" or "Generate" (depending on what mode you're in). Check the options to change how the animations run, or to remove them altogether.

Note that in Solve Mode, you can add or remove boundaries in the maze by clicking. You can also change the number of rows and columns in the maze, using the options at the left of the window.

## Running the App

To run the app from within this repository, make sure you have Python 3 installed, and run the following shell command (use `python3` on Mac if necessary):

```
$ python mazes.pyw
```

You can also use the following commands to build a standalone executable file for your operating system which runs the app. You need to have Python installed to build the executable file, but once you have it, it can be run without a Python installation.

```
$ pip install -r requirements.txt
$ source build.sh
```

Once these commands have been run, you can access the executable file in the `dist/` directory.