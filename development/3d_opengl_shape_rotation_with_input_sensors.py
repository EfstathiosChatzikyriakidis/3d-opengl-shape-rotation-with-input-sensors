#!/usr/bin/env pythonw
# -*- coding: utf-8 -*-

#    3D OpenGL Shape Rotation With Input Sensors.
#
#    Copyright (C) 2010 Efstathios Chatzikyriakidis <stathis.chatzikyriakidis@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# try to import the necessary modules.
try:
    import sys

    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *

    from serial import Serial
except ImportError:
    # exit with abnormal error code.
    sys.exit(2)


## objects imported when `from <module> import *' is used
__all__ = ['main']


# establish serial line cummunication.
serLine = Serial('/dev/ttyUSB0', 9600)

# better escape key code.
ESCAPE_KEY = '\033'

# separator character between angles.
SEPARATOR = ':'

# window title message.
WINDOW_TITLE = "Controllable 3D OpenGL Shape Rotation Via Serial Communication"

# window size (height and width).
WINDOW_HEIGHT = 200
WINDOW_WIDTH = 200

# new and old angle values of the 3D object.
newXPosValue = 0.0
newYPosValue = 0.0
oldXPosValue = 0.0
oldYPosValue = 0.0


# this function is called right after our OpenGL window is created.
def initGL(width, height):
    glClearColor(0.0, 0.0, 0.0, 0.0)      # clear the background color to black.
    glClearDepth(1.0)                     # enable clearing of the depth buffer.
    glDepthFunc(GL_LESS)                  # type of depth test to do.
    glEnable(GL_DEPTH_TEST)               # enable depth testing.
    glShadeModel(GL_SMOOTH)               # enable smooth color shading.
    glMatrixMode(GL_PROJECTION)           # specify current matrix.
    glLoadIdentity()                      # replace the current matrix with the identity matrix.

    # calculate the aspect ratio of the window.
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)

    # specify current matrix.
    glMatrixMode(GL_MODELVIEW)


# call this function when the window is resized.
def resizeGLScene(width, height):
    # prevent a divide by zero if the window is too small.
    if height == 0: height = 1

    glViewport(0, 0, width, height)   # reset the current viewport.
    glMatrixMode(GL_PROJECTION)       # specify current matrix.
    glLoadIdentity()                  # replace the current matrix with the identity matrix.

    # calculate the aspect ratio of the window.
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)

    # specify current matrix.
    glMatrixMode(GL_MODELVIEW)


# the main drawing function.
def drawGLScene():
    # clear the screen and the depth buffer.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()                             # replace the current matrix with the identity matrix.
    glTranslatef(0.0, 0.0, -5.0)                 # move center into the screen.
    glRotatef(newXPosValue, 1.0, 0.0, 0.0)       # rotate the cube on X.
    glRotatef(newYPosValue, 0.0, 1.0, 0.0)       # rotate the cube on Y.

    glBegin(GL_QUADS)                   # start drawing the shape.

    glColor3f(0.0, 1.0, 0.0)            # set the color to green.
    glVertex3f( 1.0, 1.0, -1.0)         # top right of the quad (top).
    glVertex3f(-1.0, 1.0, -1.0)         # top left of the quad (top).
    glVertex3f(-1.0, 1.0,  1.0)         # bottom left of the quad (top).
    glVertex3f( 1.0, 1.0,  1.0)         # bottom right of the quad (top).

    glColor3f(1.0, 0.5, 0.0)            # set the color to orange.
    glVertex3f( 1.0, -1.0,  1.0)        # top right of the quad (bottom).
    glVertex3f(-1.0, -1.0,  1.0)        # top left of the quad (bottom).
    glVertex3f(-1.0, -1.0, -1.0)        # bottom left of the quad (bottom).
    glVertex3f( 1.0, -1.0, -1.0)        # bottom right of the quad (bottom).

    glColor3f(1.0, 0.0, 0.0)            # set the color to red.
    glVertex3f( 1.0,  1.0, 1.0)         # top right of the quad (front).
    glVertex3f(-1.0,  1.0, 1.0)         # top left of the quad (front).
    glVertex3f(-1.0, -1.0, 1.0)         # bottom left of the quad (front).
    glVertex3f( 1.0, -1.0, 1.0)         # bottom right of the quad (front).

    glColor3f(1.0, 1.0, 0.0)            # set the color to yellow.
    glVertex3f( 1.0, -1.0, -1.0)        # top right of the quad (back).
    glVertex3f(-1.0, -1.0, -1.0)        # top left of the quad (back).
    glVertex3f(-1.0,  1.0, -1.0)        # bottom left of the quad (back).
    glVertex3f( 1.0,  1.0, -1.0)        # bottom right of the quad (back).

    glColor3f(0.0, 0.0, 1.0)            # set the color to blue.
    glVertex3f(-1.0,  1.0,  1.0)        # top right of the quad (left).
    glVertex3f(-1.0,  1.0, -1.0)        # top left of the quad (left).
    glVertex3f(-1.0, -1.0, -1.0)        # bottom left of the quad (left).
    glVertex3f(-1.0, -1.0,  1.0)        # bottom right of the quad (left).

    glColor3f(1.0, 0.0, 1.0)            # set the color to violet.
    glVertex3f(1.0,  1.0, -1.0)         # top right of the quad (right).
    glVertex3f(1.0,  1.0,  1.0)         # top left of the quad (right).
    glVertex3f(1.0, -1.0,  1.0)         # bottom left of the quad (right).
    glVertex3f(1.0, -1.0, -1.0)         # bottom right of the quad (right).

    glEnd()                             # done drawing the shape.

    glutSwapBuffers()


# call this function whenever a key is pressed.
def keyPressed(key, x, y):
    # exit the program if escape key pressed.
    if key == ESCAPE_KEY: sys.exit()


# call this function whenever there is an idle moment.
def idleMoment():
    global oldXPosValue, oldYPosValue
    global newXPosValue, newYPosValue

    # get a line from the serial.
    line = serLine.readline().strip()

    # if the line is not empty try to handle it.
    if line != "":
        # try to get the dimension angles.
        [x, s, y] = line.partition(SEPARATOR)

        # if the message is correct handle its values.
        if x != "" and s != "" and y != "":
            # get the new angle values.
            newXPosValue = float(x)
            newYPosValue = float(y)

            # redisplay the scene only if there was a change in angles.
            if (newXPosValue != oldXPosValue or
                newYPosValue != oldYPosValue):
                # store previous angles' values.
                oldXPosValue = newXPosValue
                oldYPosValue = newYPosValue

                # print newXPosValue
                # print newYPosValue

                # set flag for redisplay the scene.
                glutPostRedisplay()


# call this function to start the application
def main():

    # initialize the GLUT library.
    glutInit(sys.argv)

    # select display mode:
    #   bit mask to select an RGBA mode window.
    #   bit mask to select a double buffered window.
    #   bit mask to request a window with a depth buffer.
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a window size.
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    # the window starts at the upper left corner of the screen.
    glutInitWindowPosition(0, 0)

    # create a window and set its title.
    glutCreateWindow(WINDOW_TITLE)

    # register the drawing function with glut.
    glutDisplayFunc(drawGLScene)

    # when we are doing nothing, try to redraw the scene.
    glutIdleFunc(idleMoment)

    # register the function called when the window is resized.
    glutReshapeFunc(resizeGLScene)
    
    # register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)
    
    # initialize our window.
    initGL(WINDOW_WIDTH, WINDOW_HEIGHT)

    # start event processing engine.
    glutMainLoop()


# run the script if executed
if __name__ == '__main__':
    main()
