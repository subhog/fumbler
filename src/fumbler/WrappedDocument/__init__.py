import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart




class WrappedDocument:


  def __init__(self, name):
    self.doc = FreeCAD.newDocument()

    doc_names = [d.Label for (_, d) in FreeCAD.listDocuments().items()]
    doc_number_pattern = re.compile(r'v(\d+)$')
    doc_numbers = [int(match.group(1)) for s in doc_names if (match := doc_number_pattern.search(s))]
    self.doc.Label = name + " v" + str(1 + (max(doc_numbers) if doc_numbers else 0))
  
  from ._maintenance import flush, recompute, remove_and_clean
  from ._plot import plot_line, plot_arc
  from ._draw import draw_polygon, draw_cubic, draw_flat_cubic
  from ._draw_rectangle import draw_rect, draw_rounded_rect, draw_chamfered_rect
  from ._draw_circle import draw_circle, draw_capped_circle, draw_pointy_circle, draw_right_pointy_circle, draw_left_pointy_circle

  from ._make_primitives import make_cube, make_cylinder, make_capped_cylinder, make_loft, make_polyhedron
  from ._make_operations import make_fuse
  from ._make_parts import make_teeth, make_screw_thread, make_square_spiral





