from package_tutorial.src.math_package_tamar import basic_math


def test_add():
  assert basic_math.add(1, 2) == 3
  assert basic_math.subtract(1, 2) == -1