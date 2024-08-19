import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart



def draw_polygon(
  self,
  points,
  name = "Polygon"
):
  lines = []
  for idx in range(0, len(points)):
    a = points[idx]
    b = points[(idx + 1) % len(points)]
    lines.append(self.plot_line(a[0], a[1], b[0], b[1]))

  wire = Part.Wire([line.part.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line.part)
  self.recompute()
  return WrappedPart(self, face)


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

def draw_flat_cubic(
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
      FreeCAD.Vector(p0[0], p0[1], 0),
      FreeCAD.Vector(p1[0], p1[1], 0),
      FreeCAD.Vector(p2[0], p2[1], 0),
      FreeCAD.Vector(p3[0], p3[1], 0),
    ])
    beziers.append(bezier.toShape())

  wire = Part.Wire(beziers)
  face = Part.show(Part.Face(wire), name)

  # for b in beziers:
    # self.remove_and_clean(b)
  self.recompute()
  return WrappedPart(self, face)


def draw_roller(
  self,
  n,
  long_arc,
  short_arc,
  name = "Roller"
):
  VERTICES_X_DIFFERENCE = math.sin(math.pi / n)
  VERTICES_Y_DIFFERENCE = 1 + math.cos(math.pi / n)
  VERTICES_DIAGONAL = math.sqrt(VERTICES_X_DIFFERENCE * VERTICES_X_DIFFERENCE + VERTICES_Y_DIFFERENCE * VERTICES_Y_DIFFERENCE)
  EPICIRCLE_RADIUS = (long_arc - short_arc) / VERTICES_DIAGONAL
  ANGLE_DOUBLE_RAD = math.pi * 2 / n
  ANGLE_DOUBLE_DEG = 360 / n
  ANGLE_SINGLE_DEG = 180 / n
  ANGLE_HALF_DEG = 90 / n


  arcs = []
  for i in range(n):
    j = (i + math.ceil(n / 2)) % n
    center_i = FreeCAD.Vector(
      EPICIRCLE_RADIUS * math.cos(ANGLE_DOUBLE_RAD * i),
      EPICIRCLE_RADIUS * math.sin(ANGLE_DOUBLE_RAD * i),
      0
    )
    center_j = FreeCAD.Vector(
      EPICIRCLE_RADIUS * math.cos(ANGLE_DOUBLE_RAD * j),
      EPICIRCLE_RADIUS * math.sin(ANGLE_DOUBLE_RAD * j),
      0
    )

    arc = self.doc.addObject("Part::Circle", f"___LONG {i}")
    arc.Radius = long_arc
    arc.Angle1 = (180 + ANGLE_DOUBLE_DEG * i - ANGLE_HALF_DEG) % 360
    arc.Angle2 = (180 + ANGLE_DOUBLE_DEG * i + ANGLE_HALF_DEG) % 360
    arc.Placement = FreeCAD.Placement(center_i, FreeCAD.Rotation(0, 0, 0))
    arcs.append(arc)
    
    arc = self.doc.addObject("Part::Circle", f"___SHORT {i}")
    arc.Radius = short_arc
    arc.Angle1 = (ANGLE_DOUBLE_DEG * j - ANGLE_HALF_DEG) % 360
    arc.Angle2 = (ANGLE_DOUBLE_DEG * j + ANGLE_HALF_DEG) % 360
    arc.Placement = FreeCAD.Placement(center_j, FreeCAD.Rotation(0, 0, 0))
    arcs.append(arc)

  self.recompute()
  
  wire = Part.Wire([arc.Shape for arc in arcs])
  face = Part.show(Part.Face(wire), name)

  for part in arcs:
    self.remove_and_clean(part)

  self.recompute()
  return WrappedPart(self, face)
