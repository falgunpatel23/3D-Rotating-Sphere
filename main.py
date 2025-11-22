
import numpy as np
import pygame

import sphere
from sphere import Sphere

from fpvector import FPDecVec3
from fpmatrix import FPDecMtx44

pygame.init()
_size = 640, 480
_screen = pygame.display.set_mode(_size)

# Set screen scale (length of 1 spans 160 pixels) (y-positive is up)
_modelView = FPDecMtx44.GetScaleMtx(160, -160, 1)

# set camera position (make 0,0 center of the screen) (set camera back 5 which doesn't do anything because this is an orthographic view)
_modelView = FPDecMtx44.GetTranslateMtx(_size[0]//2, _size[1]//2, -5) * _modelView

sphere.Init()
_sphere = Sphere()

def Update(deltaTime):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if _sphere.ProcessEvent(event):
            continue

    _sphere.Update(deltaTime)

    return True

def Render():
    _screen.fill((0,0,0))

    # Get the vector that is pointing in the direction of the camera
    c = FPDecMtx44(_modelView)
    cam = FPDecVec3(0, 0, -1) * c
    cam.Normalize()

    _sphere.Render(_modelView, cam, _screen)

    pygame.display.flip()

_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
    Render()
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0
    _gTickLastFrame = t