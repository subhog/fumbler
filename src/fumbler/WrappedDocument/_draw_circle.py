import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart



def draw_circle(
  self,
  r,
  name = "Circle"
):
  arc = self.doc.addObject("Part::Circle")
  arc.Radius = r

  wire = Part.Wire([arc.Shape])
  face = Part.show(Part.Face(wire), name)

  self.remove_and_clean(arc)
  self.recompute()
  return WrappedPart(self, face)



def draw_capped_circle(
  self,
  r,
  angle = 60,
  name = "Circle",
):
  a0_deg = (90 - angle) % 360
  a1_deg = (360 - (90 - angle)) % 360
  ang_rad = math.radians(angle % 360)
  a0_rad = math.radians(a0_deg)
  a1_rad = math.radians(a1_deg)


  arc = self.doc.addObject("Part::Circle")
  arc.Radius = r
  arc.Angle1 = a0_deg
  arc.Angle2 = a1_deg

  dx = r * (1 - math.cos(a0_rad))
  dy = dx * math.tan(ang_rad)

  p0 = FreeCAD.Vector(
    r * math.cos(a0_rad),
    r * math.sin(a0_rad),
    0,
  )
  p1 = FreeCAD.Vector(
    r,
    r * math.sin(a0_rad) - dy,
    0,
  )
  p2 = FreeCAD.Vector(
    r,
    r * math.sin(a1_rad) + dy,
    0,
  )
  p3 = FreeCAD.Vector(
    r * math.cos(a1_rad),
    r * math.sin(a1_rad),
    0,
  )

  line0 = Part.makeLine(p3, p2)
  line1 = Part.makeLine(p2, p1)
  line2 = Part.makeLine(p1, p0)
  line0_obj = self.doc.addObject("Part::Feature")
  line1_obj = self.doc.addObject("Part::Feature")
  line2_obj = self.doc.addObject("Part::Feature")
  line0_obj.Shape = line0
  line1_obj.Shape = line1
  line2_obj.Shape = line2

  self.recompute()

  lines = [arc, line0_obj, line1_obj, line2_obj]
  wire = Part.Wire([line.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line)

  self.recompute()
  return WrappedPart(self, face)


def draw_pointy_circle(
  self,
  r,
  angle = 60,
  name = "Circle",
):
  a0_deg = (90 - angle) % 360
  a1_deg = (360 - (90 - angle)) % 360
  ang_rad = math.radians(angle % 360)
  a0_rad = math.radians(a0_deg)
  a1_rad = math.radians(a1_deg)


  arc = self.doc.addObject("Part::Circle")
  arc.Radius = r
  arc.Angle1 = a0_deg
  arc.Angle2 = a1_deg

  # dx = r * (1 - math.cos(a0_rad))
  # dy = dx * math.tan(ang_rad)

  p0 = FreeCAD.Vector(
    r * math.cos(a0_rad),
    r * math.sin(a0_rad),
    0,
  )
  p1 = FreeCAD.Vector(
    r / math.sin(ang_rad),
    0,
    0,
  )
  # p1 = FreeCAD.Vector(
  #   r,
  #   r * math.sin(a0_rad) - dy,
  #   0,
  # )
  # p2 = FreeCAD.Vector(
  #   r,
  #   r * math.sin(a1_rad) + dy,
  #   0,
  # )
  p3 = FreeCAD.Vector(
    r * math.cos(a1_rad),
    r * math.sin(a1_rad),
    0,
  )

  line0 = Part.makeLine(p3, p1)
  # line1 = Part.makeLine(p2, p1)
  line2 = Part.makeLine(p1, p0)
  line0_obj = self.doc.addObject("Part::Feature")
  # line1_obj = self.doc.addObject("Part::Feature")
  line2_obj = self.doc.addObject("Part::Feature")
  line0_obj.Shape = line0
  # line1_obj.Shape = line1
  line2_obj.Shape = line2

  self.recompute()

  lines = [arc, line0_obj, line2_obj]
  wire = Part.Wire([line.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line)

  self.recompute()
  return WrappedPart(self, face)


def draw_left_pointy_circle(
  self,
  r,
  angle = 60,
  name = "Circle",
):
  a0_deg = 90
  a1_deg = (360 - (90 - angle)) % 360
  ang_rad = math.radians(angle % 360)
  a0_rad = math.radians(a0_deg)
  a1_rad = math.radians(a1_deg)


  arc = self.doc.addObject("Part::Circle")
  arc.Radius = r
  arc.Angle1 = a0_deg
  arc.Angle2 = a1_deg

  p0 = FreeCAD.Vector(
    r * math.cos(a0_rad),
    r * math.sin(a0_rad),
    0,
  )
  p1 = FreeCAD.Vector(
    r / math.sin(ang_rad) + r / math.tan(ang_rad),
    r,
    0,
  )
  p3 = FreeCAD.Vector(
    r * math.cos(a1_rad),
    r * math.sin(a1_rad),
    0,
  )

  line0 = Part.makeLine(p3, p1)
  line2 = Part.makeLine(p1, p0)
  line0_obj = self.doc.addObject("Part::Feature")
  line2_obj = self.doc.addObject("Part::Feature")
  line0_obj.Shape = line0
  line2_obj.Shape = line2

  self.recompute()

  lines = [arc, line0_obj, line2_obj]
  wire = Part.Wire([line.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line)

  self.recompute()
  return WrappedPart(self, face)


def draw_right_pointy_circle(
  self,
  r,
  angle = 60,
  name = "Circle",
):
  a0_deg = (90 - angle) % 360
  a1_deg = 270
  ang_rad = math.radians(angle % 360)
  a0_rad = math.radians(a0_deg)
  a1_rad = math.radians(a1_deg)


  arc = self.doc.addObject("Part::Circle")
  arc.Radius = r
  arc.Angle1 = a0_deg
  arc.Angle2 = a1_deg

  p0 = FreeCAD.Vector(
    r * math.cos(a0_rad),
    r * math.sin(a0_rad),
    0,
  )
  p1 = FreeCAD.Vector(
    r / math.sin(ang_rad) + r / math.tan(ang_rad),
    -r,
    0,
  )
  p3 = FreeCAD.Vector(
    r * math.cos(a1_rad),
    r * math.sin(a1_rad),
    0,
  )

  line0 = Part.makeLine(p3, p1)
  line2 = Part.makeLine(p1, p0)
  line0_obj = self.doc.addObject("Part::Feature")
  line2_obj = self.doc.addObject("Part::Feature")
  line0_obj.Shape = line0
  line2_obj.Shape = line2

  self.recompute()

  lines = [arc, line0_obj, line2_obj]
  wire = Part.Wire([line.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line)

  self.recompute()
  return WrappedPart(self, face)

