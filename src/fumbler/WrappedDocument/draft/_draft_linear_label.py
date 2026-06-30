import FreeCAD, FreeCADGui, Part, Draft
import re
import math


def _unit_perpendicular(ab):
  z_axis = FreeCAD.Vector(0, 0, 1)
  perp = ab.cross(z_axis)
  if perp.Length < 1e-9:
    perp = FreeCAD.Vector(0, 1, 0)
  perp.normalize()
  return perp


def _default_point_size():
  try:
    import draftutils.params as params
    return params.get_param("arrowsizestart")
  except ImportError:
    return 1


def _marker_sphere(center, point_size):
  diameter = point_size if point_size is not None else _default_point_size()
  return Part.makeSphere(diameter / 2, center)


def _apply_flat_black(view_object):
  black = (0.0, 0.0, 0.0)
  view_object.ShapeColor = black
  view_object.LineColor = black
  if hasattr(view_object, "SpecularColor"):
    view_object.SpecularColor = black
  if hasattr(view_object, "ShapeAppearance"):
    try:
      view_object.ShapeAppearance = (FreeCAD.Material(
        DiffuseColor=black,
        AmbientColor=black,
        SpecularColor=black,
        EmissiveColor=black,
        Shininess=0.0,
        Transparency=0.0,
      ),)
    except (AttributeError, TypeError):
      pass
  if FreeCAD.GuiUp:
    try:
      import pivy.coin as coin
      material = coin.SoMaterial()
      material.lightingModel = coin.SoMaterial.BASE_COLOR
      material.diffuseColor.setValue(0, 0, 0)
      view_object.RootNode.insertChild(material, 0)
    except (ImportError, AttributeError):
      pass


def draft_linear_label(
  self,
  text,
  ax,
  ay,
  az,
  bx,
  by,
  bz,
  distance,
  font_size = None,
  point_size = None,
):
  """
  Adds a linear dimension-style label with custom text between two points.

  Draws a C-shaped annotation: markers at A and B, short legs perpendicular
  to the AB line, a connecting line offset by distance, and text centered
  on that connecting line.

  Parameters:
  text (str): Label text
  ax (float): X coordinate of point A
  ay (float): Y coordinate of point A
  az (float): Z coordinate of point A
  bx (float): X coordinate of point B
  by (float): Y coordinate of point B
  bz (float): Z coordinate of point B
  distance (float): Perpendicular offset of the connecting line from AB.
    Positive values offset to the left of the A→B direction in the XY plane.

  Keyword arguments:
  font_size (float): Text height. Default uses Draft preferences.
  point_size (float): Marker diameter at A and B in mm. Default uses Draft
    arrow size preference (same scale as draft_label point_size).

  Returns:
  App::FeaturePython: The created Draft text object
  """
  FreeCAD.setActiveDocument(self.doc.Name)
  # print("--------------------------------")

  a = FreeCAD.Vector(ax, ay, az)
  b = FreeCAD.Vector(bx, by, bz)
  ab = b.sub(a)
  unit_perp = _unit_perpendicular(ab)
  # print("unit_perp", unit_perp)
  offset = _unit_perpendicular(ab).multiply(distance)
  a_leg = a.add(offset)
  b_leg = b.add(offset)

  Part.show(Part.Compound([
    Part.makeLine(a, a_leg),
    Part.makeLine(b, b_leg),
    Part.makeLine(a_leg, b_leg),
  ]), "LinearLabel")

  markers = Part.show(Part.Compound([
    _marker_sphere(a, point_size),
    _marker_sphere(b, point_size),
  ]), "LinearLabelMarker")
  _apply_flat_black(markers.ViewObject)

  mid = a_leg.add(b_leg).multiply(0.5)
  # print("mid", mid)
  # print("unit_perp", unit_perp)
  text_gap = (font_size if font_size is not None else 1)
  # text_gap = 1
  text_pos = mid.add(unit_perp.multiply(text_gap))
  angle = math.degrees(math.atan2(ab.y, ab.x))
  # print("angle", angle)
  placement = FreeCAD.Placement(
    text_pos,
    FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), angle),
  )

  label = Draft.make_text(text, placement=placement)
  label.ViewObject.FontName = "Helvetica,Arial,sans"
  label.ViewObject.Justification = "Center"
  if font_size is not None:
    label.ViewObject.FontSize = font_size

  self.recompute()
  return label
