import tkinter as tk
import time
import queue

#Create Grid
def create_grid(event=None):
    w = Frame.winfo_width() # Get current width of canvas
    h = Frame.winfo_height() # Get current height of canvas
    Frame.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, w, N):
        Frame.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, N):
        Frame.create_line([(0, i), (w, i)], tag='grid_line')
#Create Shape
def CreateShape(x,y,Time,color):
	time.sleep(Time)
	distx = N*x;disty = N*y
	Frame.create_rectangle(5+distx, 5+disty, N-5 +distx, N-5 +disty, outline='white', fill=color)
	Frame.update()
#Event Origin
def dragOrigin(eventorigin):
      x = eventorigin.x
      y = eventorigin.y
      x = int(x/N)
      y = int(y/N)
      if(x == RunCell[0] and y == RunCell[1]):
      	return 0
      elif(x == Start[0] and y == Start[1]):
      	return 0
      elif(x == End[0] and y == End[1]):
      	return 0
      else:
      	Block[x][y] = 1
      	CreateShape(x,y,0,"pink")
#startBFS
def getorigin(eventorigin):
	x = eventorigin.x
	y = eventorigin.y
	x = int(x/N)
	y = int(y/N)

	if(Start[0]!= -1):
		if(End[0]!=-1):
			if(x == RunCell[0] and y == RunCell[1]):
				flag = a_star_search(Start,End)
				print(flag)
				if(flag == True):
					traceBack()
					#print(dist[End[0]][End[1]])
			elif(x == Start[0] and y == Start[1]):
				CreateShape(Start[0],Start[1],0,"white")
				Start[0] = -1
				Start[1] = -1
			elif(x == End[0] and y == End[1]):
				CreateShape(End[0],End[1],0,"white")
				End[0] = -1
				End[1] = -1
		elif(x != Start[0] or y != Start[1]):
			End[0] = x
			End[1] = y
			CreateShape(x,y,0,"Orange")
	elif(x != End[0] or y != End[1]):
		Start[0] = x
		Start[1] = y
		CreateShape(x,y,0,"Red")	

#Init Grid
def InitMatrix():
	#Gobal varaiable
	global Frame,N,root,Start,End,sizeX,sizeY,Block
	root = tk.Tk()
	sizeX = 50
	sizeY = 50
	Block = [ [0 for i in range(sizeX+10)] for i in range(sizeY+10)]
	N = 30
	Frame = tk.Canvas(root, height=1500, width=1500, bg='white')
	Frame.pack(fill=tk.BOTH, expand=True)
	Frame.bind('<Configure>', create_grid)
	# Frame.bind("<Button 1>",getorigin)
	Frame.bind("<Button 1>",getorigin)
	Frame.bind("<B1-Motion>",dragOrigin)
	#Start Cell: color Red
	Start = ([5,6])
	CreateShape(Start[0],Start[1],0,"Red")
	#End Cell: color Orange
	End = ([30,20])
	CreateShape(End[0],End[1],0,"Orange")
	#Run Cell: color Red
	global RunCell
	RunCell = ([20,0])
	CreateShape(RunCell[0],RunCell[1],0,"Red")
#printTrack
def traceBack():
	x = End[0]
	y = End[1]
	a = path[x][y][0]
	b = path[x][y][1]
	while(a!=-1 and b!=-1):
		if(x != End[0] or y != End[1]):
			CreateShape(x,y,0,"Purple")
		x = a
		y = b
		a = path[x][y][0]
		b = path[x][y][1]
#A Start Search
def heuristic(a,b):
	(x1,y1) = a
	(x2,y2) = b
	return abs(x1-x2)+abs(y1-y2)
def Astar_ValidNode(Node):
	if(Node[0]>=0 and Node[0]<=sizeX and Node[1]>=0 and Node[1]<=sizeY and Block[Node[0]][Node[1]] == 0):
		return True
	return False
def a_star_search(start,goal):
	global path,dist
	path = [[([]) for i in range(sizeX+10)] for i in range(sizeY+10)]
	start = (start[0],start[1])
	goal = (goal[0],goal[1])
	path[Start[0]][Start[1]] = ([-1,-1])
	#Base Time
	BaseTime = 0
	#Direction
	dx = [0,1,0,-1]
	dy = [-1,0,1,0]
	#Queue
	frontier = queue.PriorityQueue()
	Cell = (0,start)
	frontier.put((0,start))
	cost_so_far = {start: 0}
	while not frontier.empty():
		current = frontier.get()[1]
		#Reach Goal
		if(current == goal):
			CreateShape(Start[0],Start[1],BaseTime,"Red")
			CreateShape(End[0],End[1],BaseTime,"Green2")
			return True
		#Draw Blue spot
		if(current != start):
			CreateShape(current[0],current[1],BaseTime,"yellow")
			CreateShape(current[0],current[1],BaseTime,"blue")
		#Scout 4 directions
		for i in range(4):
			Next = (current[0]+dx[i],current[1]+dy[i])
			if(not Astar_ValidNode(Next)):
				continue
			new_cost = cost_so_far[current]+1
			if(Next not in cost_so_far or new_cost < cost_so_far[Next]):
				cost_so_far[Next] = new_cost
				priority = new_cost+heuristic(goal,Next)
				frontier.put((priority,Next))
				path[Next[0]][Next[1]] = ([current[0],current[1]])
	return False		
#Main
InitMatrix()
#loop
root.mainloop()