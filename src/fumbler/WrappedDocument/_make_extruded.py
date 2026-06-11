import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def make_extruded(
  self,
  shape,
  height,
  name = "Extruded",
):
  v = self.doc.addObject("Part::Loft", name)
  v.Sections = [shape.part, shape.make_copy().elevate(height).part]
  v.Solid = True    # Make sure it's a solid
  v.Ruled = True    # Set to True if you want straight sections
  v.Closed = False  # Closed loft makes a solid (if shapes are closed and profiles are compatible)

  shape.part.Visibility = False

  self.recompute()
  return WrappedPart(self, v)
