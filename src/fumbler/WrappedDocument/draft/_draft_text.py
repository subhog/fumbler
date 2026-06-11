import FreeCAD, FreeCADGui, Part, Draft
import re
import math


def draft_text(
  self,
  text,
  x,
  y,
  z = 0,
  screen = False,
  font_size = None,
):
  """
  Adds a Draft text annotation at the given point.

  Parameters:
  text (str): Text to display
  x (float): X coordinate
  y (float): Y coordinate

  Keyword arguments:
  z (float): Z coordinate. Default is 0.
  screen (bool): If True, text always faces the camera. Default is True.
  font_size (float): Text height. Default uses Draft preferences.

  Returns:
  App::FeaturePython: The created Draft text object
  """
  FreeCAD.setActiveDocument(self.doc.Name)
  obj = Draft.make_text(text, placement=FreeCAD.Vector(x, y, z), screen=screen)
  obj.ViewObject.FontName = "Helvetica,Arial,sans"
  if font_size is not None:
    obj.ViewObject.FontSize = font_size
  self.recompute()
  return obj
