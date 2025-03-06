import os
import geometric_lib.circle as cr
import geometric_lib.square as sq

radius = int(os.environ.get("radius"))
len = int(os.environ.get("len"))

print(f"Площадь круга равна {cr.area(radius)}")
print(f"Площадь квадрата равна {sq.area(len)}")