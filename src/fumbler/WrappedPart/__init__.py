import FreeCAD, FreeCADGui, Part
import re
import math


class WrappedPart:


  def __init__(self, doc, part):
    self.doc = doc
    self.part = part


  def remove_and_clean(self):
    self.doc.remove_and_clean(self.part)

  def move(self, delta):
    self.part.Placement.Base = (
      self.part.Placement.Base[0] + delta[0],
      self.part.Placement.Base[1] + delta[1],
      self.part.Placement.Base[2] + delta[2],
    )
    return self
  


  def rename(self, name):
    self.part.Label = name
    return self

  def recolor(self, color, transparency):
    self.part.ViewObject.ShapeColor = color
    self.part.ViewObject.Transparency = int(100 * (1 - transparency))
    return self

  def elevate(self, dz):
    return self.move((0, 0, dz))

  def hide(self):
    self.part.ViewObject.Visibility = False
    return self

  def __rotate_deprecated(
    self,
    x, y, z,
    angle,
  ):
    rotation = FreeCAD.Rotation(FreeCAD.Vector(x, y, z), angle)
    self.part.Placement.Rotation = rotation.multiply(self.part.Placement.Rotation)
    return self


  def rotate(
    self,
    axis,
    angle,
  ):
    self.part.Placement.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(axis[0], axis[1], axis[2]), angle, True)
    return self


  def fillet(
    self,
    edges,
    radius,
    second_radius = None,
  ):
    label = self.part.Label
    result = self.doc.doc.addObject("Part::Fillet", "Fillet")
    result.Base = self.part
    r2 = second_radius if second_radius is not None else radius
    result.Edges = [(idx, radius, r2) for idx in edges];

    self.part.Label = label + " Raw"
    self.part.Visibility = False
    self.doc.recompute()
    self.part = result
    self.part.Label = label
    return self

  def fillet_all(
    self,
    edges_rounded,
  ):
    label = self.part.Label
    result = self.doc.doc.addObject("Part::Fillet", "Fillet")
    result.Base = self.part
    result.Edges = edges_rounded

    self.part.Label = label + " Raw"
    self.part.Visibility = False
    self.doc.recompute()
    self.part = result
    self.part.Label = label
    return self


  def chamfer(
    self,
    edges,
    radius,
    second_radius = None,
  ):
    label = self.part.Label
    result = self.doc.doc.addObject("Part::Chamfer", "Chamfer")
    result.Base = self.part
    r2 = second_radius if second_radius is not None else radius
    result.Edges = [(idx, radius, r2) for idx in edges];

    self.part.Label = label + " Raw"
    self.part.Visibility = False
    self.doc.recompute()
    self.part = result
    self.part.Label = label
    return self


  def fillet_exact(
    self,
    edges,
  ):
    label = self.part.Label
    result = self.doc.doc.addObject("Part::Fillet", "Fillet")
    result.Base = self.part
    result.Edges = edges;

    self.part.Label = label + " Raw"
    self.part.Visibility = False
    self.doc.recompute()
    self.part = result
    self.part.Label = label
    return self



  def fuse(self, gizmos):
    if type(gizmos) != list:
      gizmos = [gizmos]

    label = self.part.Label
    result = self.part

    for gizmo in gizmos:
      prev = result
      result = Part.show(prev.Shape.fuse(gizmo.part.Shape))
      self.doc.remove_and_clean(prev)
      self.doc.remove_and_clean(gizmo.part)
      self.doc.recompute()

    self.part = result
    self.part.Label = label
    return self


  def cut(self, gizmos):
    if type(gizmos) != list:
      gizmos = [gizmos]

    label = self.part.Label
    result = self.part
    for gizmo in gizmos:
      prev = result
      result = Part.show(prev.Shape.cut(gizmo.part.Shape))
      self.doc.remove_and_clean(prev)
      self.doc.remove_and_clean(gizmo.part)
      self.doc.recompute()

    self.part = result
    self.part.Label = label
    return self


  def intersect(self, gizmos):
    if type(gizmos) != list:
      gizmos = [gizmos]

    label = self.part.Label
    result = self.part
    for gizmo in gizmos:
      prev = result
      result = Part.show(prev.Shape.common(gizmo.part.Shape))
      self.doc.remove_and_clean(prev)
      self.doc.remove_and_clean(gizmo.part)
      self.doc.recompute()

    self.part = result
    self.part.Label = label
    return self


  def make_copy(self):
    return WrappedPart(self.doc, Part.show(self.part.Shape))


  def make_extruded(
    self,
    height,
    name = "Extruded",
  ):
    self.doc.recompute()

    shape = self.part.Shape.extrude(FreeCAD.Vector(0, 0, height))
    part = Part.show(shape, name)

    self.doc.remove_and_clean(self.part)
    self.doc.recompute()
    return WrappedPart(self.doc, part)

