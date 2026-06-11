from time import sleep
import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def draw_pillow_2(
  self,
  r,
  xshift = 0.75,
  yshift = 0.25,
  # rshift = 0.5,
  rshift = 0.0625,
  name = "Pillow"
):
  s = r * xshift
  t = r * (1 + yshift)

  rp = r * (1 + rshift)
  rm = r * (1 - rshift)

  a0 = Part.BezierCurve()
  a1 = Part.BezierCurve()
  b0 = Part.BezierCurve()
  b1 = Part.BezierCurve()
  c0 = Part.BezierCurve()
  c1 = Part.BezierCurve()
  d0 = Part.BezierCurve()
  d1 = Part.BezierCurve()

  a0.setPoles([
    FreeCAD.Vector(-r, -r, 0),
    FreeCAD.Vector(-rm, -rp, 0),
    FreeCAD.Vector(-s, -t, 0),
    FreeCAD.Vector(0, -t, 0),
  ])
  a1.setPoles([
    FreeCAD.Vector(0, -t, 0),
    FreeCAD.Vector(s, -t, 0),
    FreeCAD.Vector(rm, -rp, 0),
    FreeCAD.Vector(r, -r, 0),
  ])

  b0.setPoles([
    FreeCAD.Vector(r, -r, 0),
    FreeCAD.Vector(rp, -rm, 0),
    FreeCAD.Vector(t, -s, 0),
    FreeCAD.Vector(t, 0, 0),
  ])
  b1.setPoles([
    FreeCAD.Vector(t, 0, 0),
    FreeCAD.Vector(t, s, 0),
    FreeCAD.Vector(rp, rm, 0),
    FreeCAD.Vector(r, r, 0),
  ])

  c0.setPoles([
    FreeCAD.Vector(r, r, 0),
    FreeCAD.Vector(rm, rp, 0),
    FreeCAD.Vector(s, t, 0),
    FreeCAD.Vector(0, t, 0),
  ])
  c1.setPoles([
    FreeCAD.Vector(0, t, 0),
    FreeCAD.Vector(-s, t, 0),
    FreeCAD.Vector(-rm, rp, 0),
    FreeCAD.Vector(-r, r, 0),
  ])

  d0.setPoles([
    FreeCAD.Vector(-r, r, 0),
    FreeCAD.Vector(-rp, rm, 0),
    FreeCAD.Vector(-t, s, 0),
    FreeCAD.Vector(-t, 0, 0),
  ])
  d1.setPoles([
    FreeCAD.Vector(-t, 0, 0),
    FreeCAD.Vector(-t, -s, 0),
    FreeCAD.Vector(-rp, -rm, 0),
    FreeCAD.Vector(-r, -r, 0),
  ])
  
  beziers = [
    a0.toShape(),
    a1.toShape(),
    b0.toShape(),
    b1.toShape(),
    c0.toShape(),
    c1.toShape(),
    d0.toShape(),
    d1.toShape(),
  ]

  wire = Part.Wire(beziers)
  face = Part.show(Part.Face(wire), name)

  # for b in beziers:
    # self.remove_and_clean(b)
  self.recompute()
  return WrappedPart(self, face)
