############################################################
import os, sys

# Load fumbler dynamically
sys.path.append(os.path.join(
  os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
  "src"
))
import fumbler
fumbler.reload()
############################################################


A = fumbler.create_wrapped_document("TestDrawOutlined")

wire = A.plot_cubic([
  ((0, 0, 0), (3, 0, 0), (7, 0, 0)),
  ((10, 0, 0), (10, 3, 0), (10, 7, 0)),
  ((10, 10, 0), (7, 10, 0), (3, 10, 0)),
  ((0, 10, 0), (0, 7, 0), (0, 3, 0)),
])
outlined = wire.draw_outlined(2)

assert wire.part.Shape.ShapeType == "Wire"
assert outlined.part.Shape.ShapeType == "Face"
assert len(outlined.part.Shape.Faces) == 1
assert outlined.part.Shape.Area > 0
