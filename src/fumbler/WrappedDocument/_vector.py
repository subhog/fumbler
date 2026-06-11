import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def vector(point):
  return FreeCAD.Vector(point[0], point[1], 0)
