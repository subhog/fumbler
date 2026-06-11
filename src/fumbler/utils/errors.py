class FumblerConfigurationError(Exception):
  """Raised when a method is called with incompatible parameters."""

def assert_exclusive_non_zero(paramsLists, values):
  """Assert that only one of the given parameters is non-zero."""
  for params in paramsLists:
    non_zero = [p for p in params if values[p] != 0 and values[p] is not None and values[p] is not False]
    if len(non_zero) > 1:
      raise FumblerConfigurationError(
        f"Only one of {', '.join(params)} may be set, "
        f"got {', '.join(non_zero)}"
      )
    # if value != 0:
    #   for param in params:
    #     if param in value:
    #       raise FumblerConfigurationError(
    #         f"Only one of {', '.join(params)} may be set, "
    #         f"got {value}"
    #       )


  # global_corner_params = ["round", "fi", "chamfer", "ch"]
  # global_corner_set = [p for p in global_corner_params if p in kwargs]
  # if len(global_corner_set) > 1:
  #   raise FumblerConfigurationError(
  #     f"Only one of {', '.join(global_corner_params)} may be set, "
  #     f"got {', '.join(global_corner_set)}"
  #   )

  # corner_pairs = [
    
  # ]
  # for fillet_param, chamfer_param in corner_pairs:
  #   if fillet_param in kwargs and chamfer_param in kwargs:
  #     raise FumblerConfigurationError(
  #       f"Only one of {fillet_param} and {chamfer_param} may be set for a single corner"
  #     )
