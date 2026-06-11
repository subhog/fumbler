import FreeCAD, FreeCADGui, Part, Draft
import re
import math
from ...WrappedPart import WrappedPart


def draft_label(
  self,
  part,
  text,
  target_x,
  target_y,
  target_z,
  label_x,
  label_y,
  label_z,
  direction = "Horizontal",
  distance = 5,
  subelement = None,
  label_type = "Custom",
  font_size = None,
  point_size = None,
):
  """
  Adds a Draft label with a leader line pointing at a part.

  Parameters:
  part (WrappedPart): Part to attach the label to
  text (str): Label text (used when label_type is "Custom")
  target_x (float): X coordinate of the leader line target point
  target_y (float): Y coordinate of the leader line target point
  target_z (float): Z coordinate of the leader line target point
  label_x (float): X coordinate of the label text
  label_y (float): Y coordinate of the label text
  label_z (float): Z coordinate of the label text

  Keyword arguments:
  direction (str): Leader line direction ("Horizontal", "Vertical", or "Custom")
  distance (float): Length of the straight leader segment
  subelement (str): Optional subelement name ("Vertex1", "Edge2", "Face1", etc.)
  label_type (str): Label type ("Custom", "Length", "Area", etc.)
  font_size (float): Text height. Default uses Draft preferences.
  point_size (float): Target point marker size. Default uses Draft preferences.

  Returns:
  App::FeaturePython: The created Draft label object
  """
  FreeCAD.setActiveDocument(self.doc.Name)
  obj = Draft.make_label(
    target_point=FreeCAD.Vector(target_x, target_y, target_z),
    placement=FreeCAD.Vector(label_x, label_y, label_z),
    target_object=part.part,
    subelements=subelement,
    label_type=label_type,
    custom_text=text,
    direction=direction,
    distance=distance,
  )
  obj.ViewObject.FontName = "Helvetica,Arial,sans"
  if font_size is not None:
    obj.ViewObject.FontSize = font_size
  if point_size is not None:
    obj.ViewObject.ArrowSizeStart = point_size
  self.recompute()
  return obj
