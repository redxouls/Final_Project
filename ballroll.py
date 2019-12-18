from anastruct import SystemElements
import matplotlib.pyplot as plt
import numpy as np
x = np.arange(1, 10) * np.pi
y = np.cos(x)
y -= y.min()
cnt=0
cd=x[1]
dt=0.1
Fy=-3
ltop=(len(x[1:-1][::2]))*2*np.pi
#print(ltop)
while cd<ltop:
    #print(cd)
    ss = SystemElements()
    element_type = 'truss'

        # create triangles
    ss.add_element_grid(x, y, element_type=element_type)

    # add top girder
    ss.add_element_grid(x[1:-1][::2], y[1:-1][::2], element_type=element_type)

    # add bottom girder
    ss.add_element_grid(x[::2], y[::2], element_type=element_type)
    # supports
    ss.add_support_hinged(1)
    ss.add_support_roll(-1, 2)
    lni=2*int(cd//(2*np.pi))
    rni=int(lni+2)
    #print('gee',lni,rni)
    fl=Fy*(x[rni-1]-cd)/(2*np.pi)
    fr=Fy-fl
    #print(fl,fr)
    # loads
    ss.point_load(lni, Fy=fl)
    ss.point_load(rni, Fy=fr)
    ss.solve()
    ss.show_structure()
    dispalcement = ss.get_node_displacements()

    plt.plot(x,y)
    for k in range(len(dispalcement)):
        x[k]+= dispalcement[k][3]
        y[k]+= dispalcement[k][2]
    cd+=dt*np.pi
    ss.remove_loads(False)
#plt.show()