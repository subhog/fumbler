import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart
from ...utils import Anchor

def make_cylinder(
  self,
  r,
  h,
  name = "Cylinder",
  anchor = Anchor.Face,
):
  v = self.doc.addObject("Part::Cylinder", name)
  v.Radius = r
  v.Height = h
  part = WrappedPart(self, v)
  if anchor.value == Anchor.Volume.value:
    part = part.move((0, 0, -h / 2))
  return part
