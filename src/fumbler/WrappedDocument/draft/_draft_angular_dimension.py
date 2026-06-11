import FreeCAD, FreeCADGui, Part, Draft
import re
import math


def draft_angular_dimension(
  self,
  center_x,
  center_y,
  angle_start,
  angle_end,
  dim_x,
  dim_y,
  z = 0,
):
  """
  Adds a Draft angular dimension at the given center point.

  Parameters:
  center_x (float): X coordinate of the angle vertex
  center_y (float): Y coordinate of the angle vertex
  angle_start (float): Start angle in degrees (counter-clockwise from +X)
  angle_end (float): End angle in degrees
  dim_x (float): X coordinate the dimension arc passes through
  dim_y (float): Y coordinate the dimension arc passes through

  Keyword arguments:
  z (float): Z coordinate. Default is 0.

  Returns:
  App::FeaturePython: The created Draft dimension object
  """
  FreeCAD.setActiveDocument(self.doc.Name)
  obj = Draft.make_angular_dimension(
    center=FreeCAD.Vector(center_x, center_y, z),
    angles=[angle_start, angle_end],
    dim_line=FreeCAD.Vector(dim_x, dim_y, z),
  )
  self.recompute()
  return obj
