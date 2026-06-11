import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

def draw_cubic(
  self,
  points,
  name = "Cubic"
):
  beziers = []
  for i in range(len(points)):
    j = (i + 1) % len(points)
    p0 = points[i][0]
    p1 = points[i][1]
    p2 = points[i][2]
    p3 = points[j][0]

    bezier = Part.BezierCurve()
    # bezier.increaseDegree(3)
    bezier.setPoles([
      FreeCAD.Vector(p0[0], p0[1], p0[2]),
      FreeCAD.Vector(p1[0], p1[1], p1[2]),
      FreeCAD.Vector(p2[0], p2[1], p2[2]),
      FreeCAD.Vector(p3[0], p3[1], p3[2]),
    ])
    beziers.append(bezier.toShape())

  wire = Part.Wire(beziers)
  face = Part.show(Part.Face(wire), name)

  # for b in beziers:
    # self.remove_and_clean(b)
  self.recompute()
  return WrappedPart(self, face)
