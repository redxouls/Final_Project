def analyze(self):
        try:
            if len(self.nodes)<1:
                return None
            nodes = self.nodes
            trusses = self.trusses
            ss = SystemElements(EA=15000, EI=5000)
            for i in trusses:
                ta=[i.nodeA.cod[0],i.nodeA.cod[1]]
                tb=[i.nodeB.cod[0],i.nodeB.cod[1]]
                ss.add_element(location=[ta,tb])
            ends = self.two_end()
            ss.add_support_hinged(ends[0]+1)
            ss.add_support_hinged(ends[1]+1)
            #ss.add_support_roll(1,2)
            #ss.add_support_roll(1,2)
            self.loadid = 3+int(self.t)*2
            ss.point_load(self.loadid,Fy=50)
            ss.solve()
            #ss.show_structure()
            #ss.show_axial_force()
            forces = ss.get_node_results_system()
            axial_forces = ss.get_element_result_range('axial')
            #print([(round(i[0],3),round(i[2],3)) for i in forces])
            #print([round(i,3) for i in axial_forces])
            #ss.show_displacement()
            dispalcements = ss.get_node_displacements()
            ####################
            print('forces',len(forces),forces,'fuck')
            print('displacements',dispalcements)
            print(len(nodes),'nodes fuck')
            for k in range(len(nodes)):
                node_forces_scalar = (forces[k][1]**2+forces[k][2]**2)**0.5
                dispalcement_scalar = (dispalcements[k][0]**2+dispalcements[k][1]**2)**0.5
                if nodes[k].displacing(node_forces_scalar) and dispalcement_scalar > 1000:
                    newcod = [nodes[k].cod[0]+dispalcements[k][1]*0.00001,nodes[k].cod[1]+dispalcements[k][2]*0.00001]
                    nodes[k].change_cod(newcod)
            ###################
            '''
            discon = []
            for i in range(len(axial_forces)):
                force = axial_forces[i]
                tpoint = nodes.index(trusses[i].nodeA), nodes.index(trusses[i].nodeB)
                if nodes[tpoint[0]].damaged(force) or nodes[tpoint[1]].damaged(force):
                    discon.append((i,nodes[tpoint[0]].damaged(force),nodes[tpoint[1]].damaged(force)))
            '''
            ###############################
            
            broken_trusses = []
            for j in range(len(axial_forces)):
                if  trusses[j].damaged(abs(axial_forces[j])):
                    broken_trusses.append(j)
            #print('broken_trusses are',broken_trusses)
            #print('they\'re axial_forces are ',axial_forces)
            
            for i in broken_trusses:
                trusses[i] = 0
            for i in range(len(broken_trusses)):
                trusses.remove(0)
            #print('after_delete_trusses',trusses) 
            
            ###############


            self.t+=0.05
            return "success"
        except (KeyError):
            print('fuck')
        except (FEMException):
            print('FEMException')
            #main_structure.game_collapse()

    def displacement_limit():
        print('forces',len(forces),forces,'fuck')
        print('displacements',dispalcements)
        print(len(nodes),'nodes fuck')
        for k in range(len(nodes)):
            node_forces_scalar = (forces[k][1]**2+forces[k][2]**2)**0.5
            dispalcement_scalar = (dispalcements[k][0]**2+dispalcements[k][1]**2)**0.5
            if nodes[k].displacing(node_forces_scalar) and dispalcement_scalar > 1000:
                newcod = [nodes[k].cod[0]+dispalcements[k][1]*0.00001,nodes[k].cod[1]+dispalcements[k][2]*0.00001]
                nodes[k].change_cod(newcod)
    
    def broken():
        broken_trusses = []
        for j in range(len(axial_forces)):
            if  trusses[j].damaged(abs(axial_forces[j])):
                broken_trusses.append(j)
        #print('broken_trusses are',broken_trusses)
        #print('they\'re axial_forces are ',axial_forces)
        
        for i in broken_trusses:
            trusses[i] = 0
        for i in range(len(broken_trusses)):
            trusses.remove(0)
        #print('after_delete_trusses',trusses) 

    Eexception :
    except (FEMException):
        print('FEMException')
        #main_structure.game_collapse()