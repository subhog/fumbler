import FreeCAD, FreeCADGui, Part, Draft
import re
import math
from ...WrappedPart import WrappedPart


def draft_radial_dimension(
  self,
  part,
  edge = 1,
  mode = "radius",
  dim_x = None,
  dim_y = None,
  z = 0,
):
  """
  Adds a Draft radial or diameter dimension on a circular edge of a part.

  Parameters:
  part (WrappedPart): Part containing the circular edge

  Keyword arguments:
  edge (int): Edge index (1-based). Default is 1.
  mode (str): "radius" or "diameter". Default is "radius".
  dim_x (float): X coordinate the dimension line passes through. Default is auto.
  dim_y (float): Y coordinate the dimension line passes through. Default is auto.
  z (float): Z coordinate. Default is 0.

  Returns:
  App::FeaturePython: The created Draft dimension object
  """
  FreeCAD.setActiveDocument(self.doc.Name)
  dim_line = None
  if dim_x is not None and dim_y is not None:
    dim_line = FreeCAD.Vector(dim_x, dim_y, z)
  obj = Draft.make_radial_dimension_obj(part.part, index=edge, mode=mode, dim_line=dim_line)
  self.recompute()
  return obj
