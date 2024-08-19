############################################################
import math
import FreeCAD, FreeCADGui, Part, Draft
import os, sys
sys.path.append(os.path.join(
  os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
  "fumbler/src"
))
import fumbler
import importlib
importlib.reload(fumbler)
############################################################


A = fumbler.create_wrapped_document("Fillet")


(
  A.make_cube(20, 20, 20)
)

(
  A.make_cube(20, 20, 20)
  .fillet([1, 2, 3, 4], 5)
  .move((40, 0, 0))
)

(
  A.make_cube(20, 20, 20)
  .fillet([
    (1, 5, 5),
    (2, 5, 5),
    (3, 5, 5),
    (4, 10, 10),
  ])
  .move((80, 0, 0))
)


