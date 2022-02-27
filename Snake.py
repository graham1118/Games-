from tkinter import *
import random
import pyglet, os
import sys
import time
import threading

pyglet.font.add_file('mine-sweeper.ttf')

def restart():
	python = sys.executable
	os.execl(python, python, * sys.argv)

root = Tk()



class Board:
	def __init__(self):
		self.root = root
		self.value = 0
		self.num = "000"
		

		self.root.config(bg = "#282828")
		self.frame = Frame(self.root, width=560, height=450,bd = 4,bg="black")
		self.frame.grid(row=0, pady = (80,0))
		title = Label(self.root, text = "Snake", font = ("mine-sweeper", 40, "bold"), fg = "white", bg = "#282828")
		title.place(anchor = "center",x=600,y=40, width = 300, height = 80)
		score_header = Label(self.root, text = "Score", font = ("mine-sweeper", 20, "bold"), fg = "white", bg = "#282828")
		score_header.place(anchor = 'center', x=100,y=18,width=150, height=25)
		self.score = Label(self.root, text = self.num, font = ("mine-sweeper", 30, "bold"), fg = "white", bg = "#282828")
		self.score.place(anchor = 'center', x=100,y=55,width=150, height=45)
		self.restart = Button(self.root, text = 'GG', font = ("mine-sweeper", 20, "bold"),bg = "white", fg = "#282828", command = restart)
		self.restart.place(anchor = 'center', x = 315, y = 40, height = 45, width = 73)
board = Board()


class Tile:
	def __init__(self, i, j):
		self.snake = False
		self.root = root
		self.i = i
		self.j = j
		self.tile = Label(board.frame, bg = 'black', padx = 8)
		self.tile.grid(row = self.i, column = self.j, padx = 1, pady = 1)
	

class Matrix:
	def __init__(self):
		self.root = root
		self.matrix = []
		for x in range(20):
			self.row = []
			for y in range(34):
				tile = Tile(x, y)
				self.row.append(tile)
			self.matrix.append(self.row)

matrix = Matrix()

class Game:
	def __init__(self):
		self.root = root
		self.dx = 0
		self.dy = 0
		self.food_row = 0
		self.food_col = 0
		self.snake_tiles = []


		rows_w = range(20)
		cols_w = range(34)
		self.head_row = random.choice(rows_w)
		self.head_col = random.choice(cols_w)
		self.tail_row = random.choice(rows_w)
		self.tail_col = random.choice(cols_w)
		matrix.matrix[self.head_row][self.head_col].tile.config(bg = 'white')
		self.snake_tiles.append([self.head_row, self.head_col])
		#self.snake_tiles.append([self.tail_row, self.tail_col])
		
		self.movement()
		self.new_food()

	def none(self, e):
		None
		
	def left(self, e):
		if self.dx != 1: 
			self.dx = -1
			self.dy = 0

	def right(self, e):
		if self.dx != -1:
			self.dx = 1
			self.dy = 0

	def up(self, e):
		if self.dy != 1:
			self.dx = 0
			self.dy = -1

	def down(self, e):
		if self.dy != -1:
			self.dx = 0
			self.dy = 1
	
	def new_food(self):
		possible_x = []
		possible_y = []
		for i in range(20):
			for j in range(34):
				if matrix.matrix[i][j].snake == False:
					possible_x.append(i)
					possible_y.append(j)

		self.food_row = random.choice(possible_x)
		self.food_col = random.choice(possible_y)
		matrix.matrix[self.food_row][self.food_col].tile.config(bg = 'red')
	
	def add_point(self):
		board.value += 1
		if board.value < 10:
			board.num = "00{}".format(board.value)
		elif board.value < 100:
			board.num = "0{}".format(board.value)
		else:
			board.num = str(board.value)
		board.score.config(text = board.num)
	
	def game_over(self):
		self.dx = 0
		self.dy = 0
		self.root.bind("<Left>", self.none)
		self.root.bind("<Right>", self.none)
		self.root.bind("<Up>", self.none)
		self.root.bind("<Down>", self.none)
		self.lose_frame = Frame(self.root, width = 150, height = 50, bg = 'red')
		self.lose_frame.place(x = 245, y = 260)
		lose_label = Label(self.lose_frame, text = 'You Lose', font = ("mine-sweeper", 20, "bold"),fg = 'black',bg = 'red', bd = 4, padx = 5, pady = 5)
		lose_label.pack(padx = 10, pady = 10)
		
	def movement(self):
		self.root.bind("<Left>", self.left)
		self.root.bind("<Right>", self.right)
		self.root.bind("<Up>", self.up)
		self.root.bind("<Down>", self.down)
		
		if self.head_row + self.dy < 0 or self.head_row + self.dy > 19 or self.head_col + self.dx < 0 or self.head_col + self.dx > 33:
			self.game_over()
		else:
			if self.head_row == self.food_row and self.head_col == self.food_col:
				self.new_food()
				self.add_point()
				
				matrix.matrix[self.head_row + self.dy][self.head_col + self.dx].tile.config(bg = "white")
				matrix.matrix[self.head_row + self.dy][self.head_col + self.dx].snake = True
				if [self.head_row + self.dy, self.head_col + self.dx] in self.snake_tiles:
					self.game_over()
				else:
					self.snake_tiles.insert(0, [self.head_row + self.dy, self.head_col + self.dx])
					
					self.head_row += self.dy
					self.head_col += self.dx

			else:
				matrix.matrix[self.tail_row][self.tail_col].tile.config(bg = "black")
				matrix.matrix[self.tail_row][self.tail_col].snake = False
				self.snake_tiles.pop(-1)
				
				matrix.matrix[self.head_row + self.dy][self.head_col + self.dx].tile.config(bg = "white")
				matrix.matrix[self.head_row + self.dy][self.head_col + self.dx].snake = True
				if [self.head_row + self.dy, self.head_col + self.dx] in self.snake_tiles:
					self.game_over()
				else:
					self.snake_tiles.insert(0, [self.head_row + self.dy, self.head_col + self.dx])
					
					self.head_row += self.dy
					self.head_col += self.dx


					self.tail_row = self.snake_tiles[-1][0]
					self.tail_col = self.snake_tiles[-1][1]
			board.frame.after(100,self.movement)
			
		

game = Game()

root.mainloop()