import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def make_cylinder(
  self,
  r,
  h,
  name = "Cylinder",
):
  v = self.doc.addObject("Part::Cylinder", name)
  v.Radius = r
  v.Height = h
  return WrappedPart(self, v)
