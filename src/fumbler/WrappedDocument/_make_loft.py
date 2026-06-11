import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def make_loft(
  self,
  sections,
  name = "Loft",
):
  v = self.doc.addObject("Part::Loft", name)
  v.Sections = [section.part for section in sections]
  v.Solid = True    # Make sure it's a solid
  v.Ruled = True    # Set to True if you want straight sections
  v.Closed = False  # Closed loft makes a solid (if shapes are closed and profiles are compatible)

  for section in sections:
    section.part.Visibility = False

  self.recompute()
  return WrappedPart(self, v)
