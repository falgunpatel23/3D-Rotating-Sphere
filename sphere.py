
import numpy as np
import pygame
import math

from fpvector import FPDecPoint3
from fpvector import FPDecVec3
from fpmatrix import FPDecMtx44
from fpquaternion import FPQuaternion

def Init():
    global _verts
    global _surfaces
    global _colors

    y_stp = -0.1
    rotstp = 72
    a_stp = math.pi / (rotstp/2)
    h_stp = int(-2 / y_stp - 2)

    _verts = [FPDecPoint3( 0, 1, 0)]
    for y in np.arange(1 + y_stp, -1, y_stp):
        for a in np.arange(0, 2 * math.pi, a_stp):
            # Exercise #2
            # The goal is to create a 3D object out of surfaces shaped to look like a sphere
            # Modify the code in this section to create the vertices for the sphere (set the correct values for x, y, z)
            # The radius of the sphere must be 1
            # The code for making the surfaces and colors is already provided
            # NOTE: When you run this code it will be laggy because it is trying to do too much. That is fine. You don't have to fix that.
            # You may not import any module except the ones imported above
            # You may not use any code copied from the internet (write your own code so you become a better programmer)
            # You may not modify any code outside of this section
            
            # BEGIN section
            
            # Your code her
            # Looping over y-values, moving from the top to the bottom of the unit sphere.
            # 'theta' is the polar angle measured from the vertical (y-axis) down to the point on the sphere's surface.
            theta = math.acos(y)  # Compute polar angle from the y-value using inverse cosine
            
            # Using spherical coordinate formulas to determine the 3D position:
            # x = sin(theta) * cos(phi)
            # y = cos(theta)
            # z = sin(theta) * sin(phi)
            x = math.sin(theta) * math.cos(a)  # Derive x-position based on angle 'a' and polar angle
            y = math.cos(theta)                # y-position corresponds to the vertical component
            z = math.sin(theta) * math.sin(a)  # Compute z-position using angle 'a' and theta

            
            # END section

            _verts.append(FPDecPoint3(x, y, z))
    _verts.append(FPDecPoint3( 0, -1, 0))

    # Create the surfaces and set the colors
    _surfaces = []
    _colors = []
    last = len(_verts) - 1
    for b in range(rotstp):
        # Create the top triangles
        bb = b + 1
        _surfaces.append((0, bb % rotstp + 1, bb))
        _colors.append((  0,   0, 128))

        # Create the mid quads
        for y in range(h_stp):
            i1 = 1 + b + y * rotstp
            i2 = 1 + (b + 1) % rotstp + y * rotstp
            _surfaces.append((i1, i2, i2 + rotstp, i1 + rotstp))
            _colors.append((int(128 * (y+1) / (h_stp+2)), 0, int(128 * (1 - (y+1) / (h_stp+2)))))

        # Create the bottom triangles
        _surfaces.append((last - (rotstp - b) % rotstp - 1, last - (rotstp - b), last))
        _colors.append((  128,   0,   0))

class Sphere:
    def __init__(self):
        self.axis = np.asarray([3.0,1.0,1.0])
        self.axis /= np.linalg.norm(self.axis)
        self.apply = FPQuaternion()
        self.rot = FPQuaternion()

    def ProcessEvent(self, event):
        return False

    def Update(self, deltaTime):
        if deltaTime:
            self.apply.Assign(0.5 * deltaTime, self.axis, _normalized = True)
            self.rot *= self.apply

    def Render(self, modelview, camVec, screen):
        global _verts
        global _surfaces
        global _colors

        m = modelview * self.rot.GetMatrix()

        for i in range(len(_surfaces)):
            # Apply the new position to each vertex of this face of the cube
            fppoints = []
            for vert in _surfaces[i]:
                v = _verts[vert] * m
                fppoints.append(v)

            # This code determines if this side of the cube is facing the camera so we can cull sides that are not facing the camera
            v1 = fppoints[1] - fppoints[0]
            v2 = fppoints[2] - fppoints[1]
            vc = FPDecVec3.Cross(v1, v2)
            if FPDecVec3.Dot(vc, camVec) <= 0:
                continue

            # Draw this face of the sphere (to do that we first convert our fixed-point numbers to regular integers which pygame.draw requires)
            points = []
            for j in range(len(fppoints)):
                points.append([int(fppoints[j][d]) for d in range(2)])
            pygame.draw.polygon(screen, _colors[i], points)
