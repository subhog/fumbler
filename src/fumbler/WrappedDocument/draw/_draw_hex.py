from time import sleep
import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

def draw_hex(
  self, R, name = "Hex"
):
  return self.draw_n_gon(6, R, name)
