class FumblerConfigurationError(Exception):
  """Raised when a method is called with incompatible parameters."""

def assert_exclusive_non_zero(paramsLists, values):
  """Assert that only one of the given parameters is non-zero."""
  for params, value in zip(paramsLists, values):
    if value != 0:
      for param in params:
        if param in value:
          raise FumblerConfigurationError(
            f"Only one of {', '.join(params)} may be set, "
            f"got {value}"
          )