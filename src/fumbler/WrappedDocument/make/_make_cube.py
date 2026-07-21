import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart
from ...utils import Anchor

def make_cube(
  self,
  x,
  y,
  z,
  name = "Cube",
  anchor = Anchor.Corner,
):
  cube = self.doc.addObject("Part::Box", name)
  cube.Length = x
  cube.Width = y
  cube.Height = z
  part = WrappedPart(self, cube)
  if anchor.value == Anchor.Edge.value:
    part = part.move((-x / 2, 0, 0))
  elif anchor.value == Anchor.Face.value:
    part = part.move((-x / 2, -y / 2, 0))
  elif anchor.value == Anchor.Volume.value:
    part = part.move((-x / 2, -y / 2, -z / 2))
  return part
