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
  
  from ._flush import flush
  from ._recompute import recompute
  from ._remove_and_clean import remove_and_clean
  from ._plot_line import plot_line
  from ._plot_arc import plot_arc
  from ._plot_helix import plot_helix
  from ._draw_polygon import draw_polygon
  from ._draw_cubic import draw_cubic
  from ._draw_flat_cubic import draw_flat_cubic
  from ._draw_svg import draw_svg
  from ._draw_pillow import draw_pillow
  from ._draw_pillow_2 import draw_pillow_2
  from ._draw_rounded_shape import draw_rounded_shape
  from ._draw_rounded_n_gon import draw_rounded_n_gon
  from ._draw_roller import draw_roller
  from ._draw_n_gon import draw_n_gon
  from ._draw_hex import draw_hex
  from ._draw_rect import draw_rect
  from ._draw_rounded_rect import draw_rounded_rect
  from ._draw_chamfered_rect import draw_chamfered_rect
  from ._draw_circle import draw_circle
  from ._draw_capped_circle import draw_capped_circle
  from ._draw_pointy_circle import draw_pointy_circle
  from ._draw_right_pointy_circle import draw_right_pointy_circle
  from ._draw_left_pointy_circle import draw_left_pointy_circle
  from ._make_from import make_from
  from ._make_cube import make_cube
  from ._make_cylinder import make_cylinder
  from ._make_capped_cylinder import make_capped_cylinder
  from ._make_extruded import make_extruded
  from ._make_loft import make_loft
  from ._make_polyhedron import make_polyhedron
  from ._make_sweep import make_sweep
  from ._make_plot import make_plot
  from ._make_fuse import make_fuse
  from ._make_teeth import make_teeth
  from ._make_screw_thread import make_screw_thread
  from ._make_trapeze_thread import make_trapeze_thread
  from ._make_square_spiral import make_square_spiral





