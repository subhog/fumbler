import FreeCAD, FreeCADGui, Part
import re
import math


def _outline_straight_edge(edge, radius):
  start = edge.Vertexes[0].Point
  end = edge.Vertexes[-1].Point
  direction = end - start
  if direction.Length == 0:
    raise ValueError("draw_outlined requires a non-zero-length wire")

  normal = FreeCAD.Vector(-direction.y, direction.x, 0)
  normal = normal * (radius / normal.Length)
  tangent = direction * (radius / direction.Length)
  boundary = Part.Wire([
    Part.makeLine(start + normal, end + normal),
    Part.Arc(end + normal, end + tangent, end - normal).toShape(),
    Part.makeLine(end - normal, start - normal),
    Part.Arc(start - normal, start - tangent, start + normal).toShape(),
  ])
  return Part.Face(boundary)


def draw_outlined(self, thickness):
  if thickness <= 0:
    raise ValueError("thickness must be greater than zero")

  wire = self.part.Shape
  half_thickness = thickness / 2

  if wire.isClosed():
    outside = wire.makeOffset2D(half_thickness, 0, True, False, False)
    inside = wire.makeOffset2D(-half_thickness, 0, True, False, False)
    outline = outside.fuse(inside).removeSplitter()
  elif (
    len(wire.Edges) == 1
    and type(wire.Edges[0].Curve) in (Part.Line, Part.LineSegment)
  ):
    outline = _outline_straight_edge(wire.Edges[0], half_thickness)
  else:
    outline = wire.makeOffset2D(
      half_thickness,
      0,
      True,
      True,
      False,
    )

  if outline.ShapeType != "Face" and len(outline.Faces) == 1:
    outline = outline.Faces[0]
  part = Part.show(outline, self.part.Label + " Outline")

  self.doc.recompute()
  return type(self)(self.doc, part)
