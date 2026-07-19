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
  print("ANCHOR IS", anchor)
  if anchor.value == Anchor.Edge.value:
    print("EDGE")
    part = part.move((-x / 2, 0, 0))
  elif anchor.value == Anchor.Face.value:
    print("FACE")
    part = part.move((-x / 2, -y / 2, 0))
  elif anchor.value == Anchor.Volume.value:
    print("VOLUME")
    part = part.move((-x / 2, -y / 2, -z / 2))
  return part
