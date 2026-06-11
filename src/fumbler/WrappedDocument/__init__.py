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
  
  from .draw._draw_capped_circle import draw_capped_circle
  from .draw._draw_circle import draw_circle
  from .draw._draw_cubic import draw_cubic
  from .draw._draw_flat_cubic import draw_flat_cubic
  from .draw._draw_hex import draw_hex
  from .draw._draw_left_pointy_circle import draw_left_pointy_circle
  from .draw._draw_n_gon import draw_n_gon
  from .draw._draw_pillow import draw_pillow
  from .draw._draw_pillow_2 import draw_pillow_2
  from .draw._draw_pointy_circle import draw_pointy_circle
  from .draw._draw_polygon import draw_polygon
  from .draw._draw_rect import draw_rect
  from .draw._draw_right_pointy_circle import draw_right_pointy_circle
  from .draw._draw_roller import draw_roller
  from .draw._draw_rounded_n_gon import draw_rounded_n_gon
  from .draw._draw_rounded_shape import draw_rounded_shape
  from .draw._draw_svg import draw_svg
  from .make._make_capped_cylinder import make_capped_cylinder
  from .make._make_cube import make_cube
  from .make._make_cylinder import make_cylinder
  from .make._make_extruded import make_extruded
  from .make._make_from import make_from
  from .make._make_fuse import make_fuse
  from .make._make_loft import make_loft
  from .make._make_plot import make_plot
  from .make._make_polyhedron import make_polyhedron
  from .make._make_sweep import make_sweep
  from .make._make_teeth import make_teeth
  from .plot._plot_arc import plot_arc
  from .plot._plot_helix import plot_helix
  from .plot._plot_line import plot_line
  from .draft._draft_text import draft_text
  from .draft._draft_label import draft_label
  from .draft._draft_linear_dimension import draft_linear_dimension
  from .draft._draft_radial_dimension import draft_radial_dimension
  from .draft._draft_angular_dimension import draft_angular_dimension
  from .utils._flush import flush
  from .utils._recompute import recompute
  from .utils._remove_and_clean import remove_and_clean
  from .create._make_screw_thread import make_screw_thread
  from .create._make_trapeze_thread import make_trapeze_thread
  from .create._make_square_spiral import make_square_spiral





