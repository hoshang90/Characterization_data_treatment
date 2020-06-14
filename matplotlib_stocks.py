import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from py_pol import degrees, np
from py_pol.stokes import Stokes
from py_pol.mueller import Mueller
from py_pol.drawings import draw_poincare_sphere, draw_on_poincare

# s0=Stokes('s_0')
# s0.linear_light(angle=0, intensity=2)
# print(s0)
# s0.draw_poincare()
# plt.legend()

Stokes_points1=[]
s1=Stokes('s1')
s1.linear_light(angle=0, intensity=3)
print(s1)
angles=np.linspace(0,90*degrees,6)
for i, angle in enumerate(angles):
    s_rot=s1.rotate(angle=angle, keep=True, returns_matrix=False)
    Stokes_points1.append(s_rot)