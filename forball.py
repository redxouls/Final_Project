while ball.pos.x < 200: # simulate until x=200m
        rate(1000)
        
        for ele in new_truss:
            if ball.pos.x>=ele.nodeA.x and ball.pos.x<ele.nodeB.x:
                a=ele.nodeB.y-ele.nodeA.y
                b=-(ele.nodeA.y-ele.nodeA.y)
                c=-(a*ele.nodeA.x+b*ele.nodeA.y)
                break
        fsl=vector(a,b,0)#法向量
        tsl=vector(b,-a,0)
        if 0<abs(a*ball.pos.x+b*ball.pos.y+c)/sqrt(a**2+b**2)-size<0.005:
            ball.pos += ball.v*dt
            ball.a=(ifball-g*b/sqrt(a**2+b**2)*tsl)/ball.m
            ball.v+=ball.a*dt
        elif ball.pos.y <= size and ball.v.y < 0: # new: check if ball hits the ground
            ball.v.y = - ball.v.y # if so, reverse y component of velocity
        else:
            ball.pos+=ball.v*dt
            ball.v.y=-g*dt
