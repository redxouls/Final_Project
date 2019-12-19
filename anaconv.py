import structure
from anastruct import SystemElements
import matplotlib.pyplot as plt

def visualize(structure,nodes,trusses):
    ss = SystemElements(EA=15000, EI=5000)
    for i in trusses:
        ta=[i.nodeA.cod[0],i.nodeA.cod[1]]
        tb=[i.nodeB.cod[0],i.nodeB.cod[1]]
        ss.add_element(location=[ta,tb])
    print(structure.two_end())
    ss.add_support_hinged(1)
    ss.add_support_roll(-1, 2)
    ss.point_load(2, Fy=100)
    ss.point_load(4, Fy=100)
    ss.solve()
    dispalcement = ss.get_node_displacements()
    print(dispalcement)
    x = [i.cod[0] for i in structure.nodes]
    y = [i.cod[1] for i in structure.nodes]
    plt.plot(x,y)
    for k in range(len(dispalcement)):
        x[k]+= dispalcement[k][3]
        y[k]+= dispalcement[k][2]
    plt.plot(x,y)
    plt.show()
    ss.show_structure()
    return trusses