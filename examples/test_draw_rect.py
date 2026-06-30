############################################################
import math, re
import FreeCAD, FreeCADGui, Part, Draft
import os, sys

# Load fumbler dynamically
sys.path.append(os.path.join(
  os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
  "src"
))
import fumbler
fumbler.reload()
############################################################


A = fumbler.create_wrapped_document("TestDrawRect")

plain = A.draw_rect(15, 10).move((5, 5, 0))
chamfer = A.draw_rect(15, 10, ch=3).move((25, 5, 0))
fillet = A.draw_rect(15, 10, fi=3).move((45, 5, 0))
override = A.draw_rect(15, 10, fi=3, ftl=0, ftr=6, cbr=3).move((65, 5, 0))

A.draft_text("draw_rect", 5, 20, font_size=6)

A.draft_label(plain, "plain", 5 + 7.5, 5, 0, 5 + 7.5, -10, 0, font_size=3, point_size=0.25)
# A.draft_label(chamfer, "chamfer", 25 + 7.5, 5, 0, 25 + 7.5, -15, 0, font_size=3, point_size=0.25)
# A.draft_label(fillet, "fillet", 45 + 7.5, 5, 0, 45 + 7.5, -20, 0, font_size=3, point_size=0.25)
# A.draft_label(override, "override", 65 + 7.5, 5, 0, 65 + 7.5, -25, 0, font_size=3, point_size=0.25)

# # Bottom-left chamfer edge of the second rectangle (vertices 6 and 7)
# A.draft_linear_dimension(0, 0, 0, 0, 26.5, 3, part=chamfer, i1=6, i2=7)
A.draft_linear_label("ch",
  25, 5, 0,
  25 + 3, 5, 0,
  3,
  font_size=3, point_size=0.5
)
A.draft_linear_label("fi",
  45, 5, 0,
  45 + 3, 5, 0,
  1,
  font_size=3, point_size=0.25
)

# # Bottom-right fillet arc of the third rectangle (edge 8)
# A.draft_radial_dimension(fillet, edge=8, dim_x=57, dim_y=7)

# # Sharp top-left corner of the fourth rectangle
# A.draft_angular_dimension(65, 15, 270, 360, 67, 17)

A.flush()
