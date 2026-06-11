from time import sleep
import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def draw_pillow(
  self,
  r,
  scale = 0.75,
  name = "Pillow"
):
  s = r * scale

  a = Part.BezierCurve()
  b = Part.BezierCurve()
  c = Part.BezierCurve()
  d = Part.BezierCurve()


  a.setPoles([
    FreeCAD.Vector(r, 0, 0),
    FreeCAD.Vector(r, s, 0),
    FreeCAD.Vector(s, r, 0),
    FreeCAD.Vector(0, r, 0),
  ])

  b.setPoles([
    FreeCAD.Vector(0, r, 0),
    FreeCAD.Vector(-s, r, 0),
    FreeCAD.Vector(-r, s, 0),
    FreeCAD.Vector(-r, 0, 0),
  ])

  c.setPoles([
    FreeCAD.Vector(-r, 0, 0),
    FreeCAD.Vector(-r, -s, 0),
    FreeCAD.Vector(-s, -r, 0),
    FreeCAD.Vector(0, -r, 0),
  ])

  d.setPoles([
    FreeCAD.Vector(0, -r, 0),
    FreeCAD.Vector(s, -r, 0),
    FreeCAD.Vector(r, -s, 0),
    FreeCAD.Vector(r, 0, 0),
  ])
  
  beziers = [
    a.toShape(),
    b.toShape(),
    c.toShape(),
    d.toShape(),
  ]

  wire = Part.Wire(beziers)
  face = Part.show(Part.Face(wire), name)

  # for b in beziers:
    # self.remove_and_clean(b)
  self.recompute()
  return WrappedPart(self, face)
