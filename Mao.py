####################\
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
            
            ###############


            self.t+=0.05
            return "success"
        except (KeyError):
            print('fuck')
        except (FEMException):
            print('FEMException')
            #main_structure.game_collapse()