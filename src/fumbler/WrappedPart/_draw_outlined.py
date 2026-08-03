import FreeCAD, FreeCADGui, Part
import re
import math

def draw_outlined(self, thickness):
  if thickness <= 0:
    raise ValueError("thickness must be greater than zero")

  wire = self.part.Shape
  if not wire.isClosed():
    raise ValueError("draw_outlined requires a closed wire")

  half_thickness = thickness / 2
  offset_a = wire.makeOffset2D(half_thickness, 0, True, False, False)
  offset_b = wire.makeOffset2D(-half_thickness, 0, True, False, False)

  outer, inner = sorted(
    (offset_a, offset_b),
    key=lambda shape: shape.Area,
    reverse=True,
  )
  outline = outer.cut(inner)
  if outline.ShapeType != "Face" and len(outline.Faces) == 1:
    outline = outline.Faces[0]
  part = Part.show(outline, self.part.Label + " Outline")

  self.doc.recompute()
  return type(self)(self.doc, part)
