from tkinter import *
import random
import pyglet, os
import sys
import time
import threading
from PIL import Image
pyglet.font.add_file('mine-sweeper.ttf')
global root 
root = Tk()
root.geometry = "800x800"

class Board:
	def __init__(self):
		root.config(bg="#2F4F4F")
		self.mainframe = Frame(root,width=350, height=700, bd=4, bg="black")
		self.mainframe.grid(row=0,column=0,pady=(40,0))
		self.next_shape = Frame(root,width=100,height=100,bd=4,bg="#C0C0C0")
		self.next_shape.grid(row=0,column=1) 
		self.next_shape_header = Label(root,text = "Next\nShape:",font = ("mine-sweeper", 10,'bold'), bg = "#2F4F4F")
		self.next_shape_header.place(anchor='nw',x=250,y=150)
		self.score_header = Label(root, text = "Score:", font = ("mine-sweeper", 8,'bold'), bg="#2F4F4F")
		self.score_header.place(anchor = 'center',x=72,y=21,height=20,width=100)
		self.score_value = Label(root, text='000', font=("mine-sweeper", 17,'bold'), bg="#2F4F4F")
		self.score_value.place(anchor = 'center',x=164,y=20,height=25,width=100)
		self.restart = Button(text = "Start\nOver",bg = "#C0C0C0", bd = 1, font =("mine-sweeper", 10,'bold'),command=self.restart)
		self.restart.place(anchor = 'nw',x=250,y=50)
		self.line = [[0,-1],[0,0],[0,+1],[0,+2],PhotoImage(file='LB.png')]
		self.left_Z = [[-1,-1],[-1,0],[0,0],[0,+1],PhotoImage(file='Red.png')]
		self.right_Z = [[0,-1], [0,0],[-1,0],[-1,+1],PhotoImage(file='Green.png')]
		self.left_L = [[-1,-1],[0,-1],[0,0],[0,+1],PhotoImage(file='DB.png')]
		self.right_L = [[0,-1],[0,0],[0,+1],[-1,+1],PhotoImage(file='Orange.png')]
		self.square = [[0,0],[0,+1],[-1,0],[-1,+1],PhotoImage(file='Yellow.png')]
		self.upsidedown_T = [[0,-1],[0,0],[0,+1],[-1,0],PhotoImage(file='Purple.png')]
		self.shapes = [self.line,self.left_Z,self.right_Z,self.left_L,self.right_L,self.square,self.upsidedown_T]	
	def restart(self):
		python = sys.executable
		os.execl(python,python,* sys.argv)
board = Board()

class Tile:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.out_of_play = False
		self.color = 0
		self.tile = Label(board.mainframe,bg='black', padx=10,pady=3,borderwidth=0, highlightthickness=0, state='normal',compound='center')
		self.tile.grid(row=x,column=y)
class nextTile(Tile):
	def __init__(self,x,y):
		self.tile = Label(board.next_shape,bg="black",bd = 1,padx=9,pady=2)
		self.tile.grid(row=x,column=y)
class Matrix:
	def __init__(self):
		self.img = PhotoImage(file = 'Grey1.png')
		self.matrix = []
		
		for i in range(22):
			self.rows = []
			for j in range(12):
				tile = Tile(i,j)
				self.rows.append(tile)
			self.matrix.append(self.rows)
		for i in range(4):
			for j in range(4):
				tile = nextTile(i,j)
		for i in range(22):
			self.matrix[i][0].tile.config(image=self.img)
			self.matrix[i][-1].tile.config(image=self.img)
			self.matrix[i][0].out_of_play = True
			self.matrix[i][-1].out_of_play = True
		for j in range(12):
			self.matrix[0][j].tile.config(image=self.img)
			self.matrix[-1][j].tile.config(image=self.img)
			self.matrix[0][j].out_of_play = True
			self.matrix[-1][j].out_of_play = True
matrix = Matrix()

class Game():
	def __init__(self):
		root.bind("<Left>",lambda event, arg=-1: self.side(event, arg))
		root.bind("<Down>",self.harddown)
		root.bind("<Right>",lambda event, arg=1: self.side(event, arg))
		root.bind("<Up>", self.rotate)
		self.origin = [2,5]
		self.origin2 = [0,0]
		self.index = random.randint(0,6)
		self.shape = board.shapes[self.index]
		self.stop = False
		self.place(self.origin)
		self.down()
		for i in range(0,4):
			matrix.matrix[self.origin[0] + self.shape[i][0]][self.origin[1] + self.shape[i][1]].color = self.shape[4]
		#Assign shape attribute to matrix tiles here in order to assign each tile a shape with a color which can be accesssed below
	def delete(self):
		self.project_delete()
		for i in range(0,4):
			matrix.matrix[self.origin[0] + self.shape[i][0]][self.origin[1] + self.shape[i][1]].tile.config(image = '')
	def place(self,ref):
		self.project()
		for i in range(0,4):
			matrix.matrix[ref[0] + self.shape[i][0]][ref[1] + self.shape[i][1]].tile.config(image = self.shape[4])
	def finish(self):
		for i in range(0,4):
			matrix.matrix[self.origin[0] + self.shape[i][0]][self.origin[1] + self.shape[i][1]].out_of_play = True
		newgame = Game()
		#for i in range(1,21):
		#	self.complete = 0
		#	for item in range(12):
		#		if matrix.matrix[i][item].out_of_play == True:
		#			self.complete += 1
		#	if self.complete == 12:
		#		for item in range(12):
		#			matrix.matrix[i][item].tile.config(image = "")
		#			matrix.matrix[i][item].tile.config(bg = "white")
		#			time.sleep(0.1)
		#			matrix.matrix[i][item].tile.config(bg = "black")
		#	for m in range(1,i):
		#		for n in range(12):
		#			matrix.matrix[m+1][n].tile.config(image = matrix.matrix[m][n].color[4])
	def down(self):
		if matrix.matrix[self.origin[0] + self.shape[0][0]+1][self.origin[1] + self.shape[0][1]].out_of_play == True or self.stop == True:
			self.finish()
		elif matrix.matrix[self.origin[0] + self.shape[1][0]+1][self.origin[1] + self.shape[1][1]].out_of_play == True or self.stop == True:
			self.finish()
		elif matrix.matrix[self.origin[0] + self.shape[2][0]+1][self.origin[1] + self.shape[2][1]].out_of_play == True or self.stop == True:
			self.finish()
		elif matrix.matrix[self.origin[0] + self.shape[3][0]+1][self.origin[1] + self.shape[3][1]].out_of_play == True or self.stop == True:
			self.finish()	
		else:
			self.delete()
			self.origin[0] += 1
			self.place(self.origin)
			board.mainframe.after(500,self.down)
	def side(self, e, x):
		if self.origin[1] + self.shape[0][1] == 1 or self.origin[1] + self.shape[1][1] == 1 or self.origin[1] + self.shape[2][1] == 1 or self.origin[1] + self.shape[3][1] == 1:
			None
		elif self.origin[0] + self.shape[0][0] == 20 or self.origin[0] + self.shape[1][0] == 20 or self.origin[0] + self.shape[2][0] == 20 or self.origin[0] + self.shape[3][0] == 20:
			None
		else:
			self.delete()
			self.origin[1] += x
			self.place(self.origin)
	def rotate(self,e):
		self.delete()
		for i in range(4):
			zero = self.shape[i][0]
			one = self.shape[i][1]
			self.shape[i][0] = one*-1
			self.shape[i][1] = zero + 1
			matrix.matrix[self.origin[0] + self.shape[i][0]][self.origin[1] + self.shape[i][1]].tile.config(image = self.shape[4])
		self.project()
	def harddown(self,e):
		self.delete()
		self.stop = True
		for i in range(0,4):
			matrix.matrix[self.origin2[0] + self.shape[i][0]][self.origin2[1] + self.shape[i][1]].tile.config(image = self.shape[4])
			matrix.matrix[self.origin2[0] + self.shape[i][0]][self.origin2[1] + self.shape[i][1]].out_of_play = True
	def project(self):
		self.distances = []
		for i in range(4):
			x = 1
			while matrix.matrix[x+1][self.origin[1] + self.shape[i][1]].out_of_play == False:
				x += 1
			self.distances.append(x)
		self.origin2 = [min(self.distances),self.origin[1]]
		for i in range(0,4):
			matrix.matrix[self.origin2[0] + self.shape[i][0]][self.origin2[1] + self.shape[i][1]].tile.config(bg = "#303030")
	def project_delete(self):
		for i in range(0,4):
			matrix.matrix[self.origin2[0] + self.shape[i][0]][self.origin2[1] + self.shape[i][1]].tile.config(bg = "black")
game = Game()
root.mainloop()