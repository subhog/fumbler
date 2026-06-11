"""
Fumbler – Thin wrapper for fumbling things together in FreeCAD
"""


import FreeCAD, FreeCADGui, Part
import re
import math
import importlib
import sys

from .WrappedDocument import WrappedDocument

from .utils import TeethInset, TeethSide, CircleCap

epsilon = 0.0001
"""
An imperceptibly small distance,
useful for decoupling elements before boolean operations.
"""

def create_wrapped_document(name):
  return WrappedDocument(name)

def close_all():
  [FreeCAD.closeDocument(d) for d in FreeCAD.listDocuments()]

def reload():
  """
  Reload all loaded fumbler submodules so library edits take effect
  without restarting FreeCAD.

  Submodules must reload deepest-first: WrappedDocument binds methods via
  `from .draw._draw_rect import draw_rect` at class definition time, so
  _draw_rect must be refreshed before WrappedDocument is reloaded.

  The changes may not take effect until the second time the script is run.
  """
  names = sorted(
    (name for name in list(sys.modules) if name.startswith("fumbler")),
    key=lambda name: name.count("."),
    reverse=True,
  )
  for name in names:
    module = sys.modules.get(name)
    if module is None:
      continue
    try:
      importlib.reload(module)
    except ModuleNotFoundError:
      del sys.modules[name]
