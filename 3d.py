import zmq
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Define the vertices of the trapezoidal prism
vertices = (
    (1, -1, -1),   # 0 bottom back right
    (2, 1, -1),    # 1 bottom front right
    (-2, 1, -1),   # 2 bottom front left
    (-1, -1, -1),  # 3 bottom back left
    (0.5, -0.5, 1),# 4 top back right
    (1, 0.5, 1),   # 5 top front right
    (-1, 0.5, 1),  # 6 top front left
    (-0.5, -0.5, 1)# 7 top back left
)

# Define the faces of the trapezoidal prism, associating each face with vertex indices and colors
faces = (
    (0, 1, 5, 4, ((1, 0, 0), (1, 0.5, 0), (1, 0.5, 0.5), (1, 0, 0.5))),  # Right face with gradient red colors
    (2, 3, 7, 6, ((0, 1, 0), (0, 1, 0.5), (0, 0.5, 1), (0, 0.5, 0.5))),  # Left face with gradient green colors
    (1, 2, 6, 5, ((0, 0, 1), (0, 0.5, 1), (0, 0.5, 0.5), (0, 0, 0.5))),  # Front face with gradient blue colors
    (3, 0, 4, 7, ((1, 1, 0), (1, 1, 0.5), (1, 0.5, 1), (1, 0.5, 0.5))),  # Back face with gradient yellow colors
    (4, 5, 6, 7, ((1, 0, 1), (1, 0.5, 1), (0.5, 0, 1), (0.5, 0.5, 1))),  # Top face with gradient magenta colors
    (0, 1, 2, 3, ((0, 1, 1), (0.5, 1, 1), (0.5, 1, 0.5), (0, 1, 0.5)))   # Bottom face with gradient cyan colors
)

# Define the edges of the trapezoidal prism for drawing the lines
edges = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
)

# Render the trapezoidal prism by drawing its colored faces and white edges.
def TrapezoidalPrism():
    # Draw the faces with gradient colors
    glBegin(GL_QUADS)
    for face in faces:
        for i, vertex in enumerate(face[:4]):
            glColor3fv(face[4][i])  # Set color for each vertex
            glVertex3fv(vertices[vertex]) # Draw the vertex
    glEnd()

    # Draw the edges in white
    glColor3f(1, 1, 1)  # Set edge color to white
    glLineWidth(2)      # Set line width
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex]) # Draw the edge vertex
    glEnd()

# Initialize the graphics window, set up message receiving, and manage the rendering loop.
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_DEPTH_TEST)

    # Set up ZeroMQ subscriber
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555") # Connect to a local publisher
    subscriber.setsockopt_string(zmq.SUBSCRIBE, '') # Subscribe without any filter

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle window closure
                subscriber.close()
                context.term()
                pygame.quit()
                quit()

        # Try to receive the message, handling the case when no message arrives
        try:
            message = subscriber.recv_string(flags=zmq.NOBLOCK)  # Non-blocking receive
            xangle, yangle, scale_value = map(float, message.split(',')) # Parse received message
            print(f"Received angles: {xangle}, {yangle}, scale: {scale_value}")
        except zmq.Again:
            continue  # Continue the loop if no message is received

        # Calculate the zoom distance based on the scale value
        zoom_distance = np.interp(scale_value, [0, 10], [10, 2])  # Interpolate between specified zoom levels

        # Apply transformations for rotation and zoom based on received message
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the color and depth buffers
        glLoadIdentity()  # Reset the current matrix to the identity matrix
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)  # Reset the perspective
        glTranslatef(0.0, 0.0, -zoom_distance)  # Apply zoom based on scale
        glRotatef(xangle, 0, 1, 0)  # Rotate around the y-axis using xangle
        glRotatef(yangle, 1, 0, 0)  # Rotate around the x-axis using yangle

        # Draw the 3D trapezoidal prism
        TrapezoidalPrism()

        pygame.display.flip()  # Update the display
        pygame.time.wait(10)  # Wait a little before the next frame to limit speed

if __name__ == "__main__":
    main()

