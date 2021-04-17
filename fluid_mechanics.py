import numpy
import matplotlib
from matplotlib import pyplot

def linear_convection():
    # density
    # dt - czas
    # u - prędkość w kierunku x

    x = 2
    nodes = 101
    dx = x / (nodes - 1)
    timesteps = 700
    dt = 0.001
    c = 4 # wave speed

    u = numpy.ones(nodes)
    u[int(0.5/dx):int(1/dx+1)] = 2
    print(u

    pyplot.plot(numpy.linspace(0, 2, nodes), u)

    for k in range(0,1):
        un = numpy.ones(nodes)

        for i in range(timesteps): 
            un = u.copy()
            for i in range(0, nodes): ## you can try commenting this line and...
            #for i in range(nodes): ## ... uncommenting this line and see what happens!
                u[i] = un[i] - c * dt / dx * (un[i] - un[i-1])

        return pyplot.plot(numpy.linspace(0, 2, nodes), u);

def Navier_stokes_1D():
	nx = 51
	dx = 3 / (nx - 1)
	nt = 40    #nt is the number of timesteps we want to calculate
	dt = .01  #dt is the amount of time each timestep covers (delta t)

	u = numpy.ones(nx)      #as before, we initialize u with every value equal to 1.
	u[int(.5 / dx) : int(1 / dx + 1)] = 2  #then set u = 2 between 0.5 and 1 as per our I.C.s

	un = numpy.ones(nx)
	for k in range(10):
    for n in range(nt):  #iterate through time
        un = u.copy() ##copy the existing values of u into un
        for i in range(1, nx):  ##now we'll iterate through the u array

         ###This is the line from Step 1, copied exactly.  Edit it for our new equation.
         ###then uncomment it and run the cell to evaluate Step 2   

               u[i] = un[i] - un[i] * dt / dx * (un[i] - un[i-1]) 


    pyplot.plot(numpy.linspace(0, 3, nx), u) ##Plot the results
		  
	nx = 51
	dx = 3 / (nx - 1)
	nt = 40    #nt is the number of timesteps we want to calculate
	dt = .01  #dt is the amount of time each timestep covers (delta t)

	u = numpy.ones(nx)      #as before, we initialize u with every value equal to 1.
	u[int(.5 / dx) : int(1 / dx + 1)] = 2  #then set u = 2 between 0.5 and 1 as per our I.C.s

	un = numpy.ones(nx)

	for k in range(10):
		for n in range(nt):  #iterate through time
			un = u.copy() ##copy the existing values of u into un
			for i in range(1, nx):  ##now we'll iterate through the u array

			 ###This is the line from Step 1, copied exactly.  Edit it for our new equation.
			 ###then uncomment it and run the cell to evaluate Step 2   

				   u[i] = un[i] - 1 * dt / dx * (un[i] - un[i-1]) 


		pyplot.plot(numpy.linspace(0, 3, nx), u) ##Plot the results
		  
		  
def Navier_stokes_2D():
	from matplotlib import cm
	from mpl_toolkits.mplot3d import Axes3D    ##New Library required for projected 3d plots
	nodes = 100
	x = numpy.linspace(0,2,nodes)
	y = numpy.linspace(0,2,nodes)
	dx = 2 / (nodes - 1)
	dy = 2 / (nodes - 1)
	timesteps = 100
	dt = 0.2*dx
	c = 1 # wave speed
	#warunki brzegowe
	u = numpy.ones((nodes,nodes))
	u[int(1/dy):int(1.2/dy+1),int(1/dx):int(1.2/dx+1)] = 2
	u[int(1.1/dy):int(1.15/dy+1),int(1.1/dx):int(1.15/dx+1)] = 3

	fig = pyplot.figure(figsize=(11, 7), dpi=100)
	ax = fig.gca(projection='3d')                      
	X, Y = numpy.meshgrid(x, y)                            
	surf = ax.plot_surface(X, Y, u[:], cmap=cm.viridis)
	
	un = numpy.ones((nodes,nodes))

	for i in range(timesteps): 
		un = u.copy()
		for j in range(0, nodes): ## you can try commenting this line and...
			for i in range(0, nodes): ## you can try commenting this line and...
				u[i][j] = (un[i][j] - un[i][j] * dt / dx * (un[i][j] - un[i][j-1]) -
									  un[i][j] * dt / dy * (un[i][j] - un[i-1][j]))
				u[0, :] = 1
				u[-1, :] = 1
				u[:, 0] = 1
				u[:, -1] = 1             
	from mpl_toolkits.mplot3d import Axes3D    ##New Library required for projected 3d plots

	fig = pyplot.figure(figsize=(11, 7), dpi=100)
	ax = fig.gca(projection='3d')                      
	X, Y = numpy.meshgrid(x, y)                            
	surf = ax.plot_surface(X, Y, u[:], cmap=cm.viridis)
