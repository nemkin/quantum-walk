def is_power_of_2(x):
  return (x & (x-1)) == 0 and x != 0
