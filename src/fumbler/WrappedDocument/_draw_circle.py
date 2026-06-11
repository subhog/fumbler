import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart



def draw_circle(
  self,
  r,
  name = "Circle"
):
  """
    Draws a flat circle on z=0 plane,
    with center in (0, 0, 0) and given radius.

    Parameters:
    r (float): Radius of the circle
    name (string): Name of the drawing

    Returns:
    WrappedPart<Part.Face>: 
  """
  arc = self.doc.addObject("Part::Circle")
  arc.Radius = r

  wire = Part.Wire([arc.Shape])
  face = Part.show(Part.Face(wire), name)

  self.remove_and_clean(arc)
  self.recompute()
  return WrappedPart(self, face)
