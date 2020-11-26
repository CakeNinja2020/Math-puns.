import math
def clamp_norm(v, n_max):
   vx, vy = v
   n = math.sqrt(vx**2 + vy**2)
   try:
        f = min(n, n_max) / n
   except:
       pass
   return [f * vx, f * vy]