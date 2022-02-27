from tkinter import *
import random
import pyglet, os
import sys
import pygame


pyglet.font.add_file('mine-sweeper.ttf')

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

root = Tk()
root.title('Mine Sweeper - Difficult')

class Board():
	count = 0
	def __init__(self, num_bombs):
		self.root = root
		self.num_bombs = num_bombs
		self.total_bombs = -100
		self.tiles_left = 0
		self.game_over = False
		self.destroyed_tiles = 0

		self.main_frame = Frame(self.root, width = 560, height = 450, bd=4, bg = "#707070")
		self.main_frame.grid(row=0, pady=(80,0))
		root.config(bg="grey")
		score_header = Label(self.root, text='Mines Left', font=('mine-sweeper', 15), bg = "grey")
		score_header.place(height=50, width=270, anchor='center', x=125, y=15)
		self.score_num = Label(self.root, text=str(self.total_bombs), font=('mine-sweeper', 30), bg = "grey")
		self.score_num.place(height=45, width=200, anchor='center', x=125, y=55)
		self.time_num = Button(self.root, text='Mine Sweeper', font=('mine-sweeper', 40), bg = "grey", fg="#760000", command = restart)
		self.time_num.place(height=70, width=670, anchor='center', x=585, y=40)
			
board = Board(110)


class Tile:
	def __init__(self, row, col):
		self.root = root
		self.row = row
		self.col = col
		self.matrix_row = row + 1
		self.matrix_col = col + 1
		self.bomb = False
		self.adj = 0
		self.color = ""
		self.text = ""
		self.destroyed = False

		self.tile = Button(board.main_frame, width = 2, bd = 4, bg = "#D3D3D3", text = self.text)
		self.tile.bind("<Button-1>", self.remove)
		self.tile.bind("<Button-3>", self.alter)
		self.tile.grid(row=self.row, column=self.col)

	def remove(self, event):
		total_removed = 0	
		if board.game_over == True:
			pass
		elif Board.count == 0:
			adj_list = []
			if self.adj == 0:
				Board.count += 1
				dxs = [-1,0,1]
				dys = [-1,0,1]
				for dx in dxs:
					for dy in dys:
						if self.matrix_row + dx in list(range(1,19)) and self.matrix_col + dy in list(range(1,34)):
							adj_list.append(matrix2.matrix[self.matrix_row + dx][self.matrix_col + dy])
							matrix2.matrix[self.matrix_row + dx][self.matrix_col + dy].destroyed = True
							
			for item in adj_list:
				item.destroys()
		elif self.bomb == True:
			Board.count += 1
			self.tile.destroy()
			self.reveal = Label(board.main_frame, text = '*', font = ('mine-sweeper', 11, 'bold'), fg = 'black', bg = "red")
			self.reveal.grid(row = self.row, column = self.col)
			board.game_over = True
			lose_frame = Frame(root, width = 230, height = 100)
			lose_frame.grid(row=0, column=0)
			lose_screen = Label(lose_frame, text = "You Lose", font = ('mine-sweeper', 20), fg = "black", bg = "red", relief = 'solid', padx = 5)
			lose_screen.grid(row=0, column=0)
			board.total_bombs = '000'
			board.score_num.config(text=board.total_bombs)

			for i in range(1,19):
				for j in range(1,34):
					if matrix2.matrix[i][j].bomb == True:
						matrix2.matrix[i][j].destroys()
		
		else:
			Board.count += 1
			if self.adj == 0:
				dxs = [-1,0,1]
				dys = [-1,0,1]
				for dx in dxs:
					for dy in dys:
						if self.matrix_row + dx in list(range(1,19)) and self.matrix_col + dy in list(range(1,34)):
							matrix2.matrix[self.matrix_row + dx][self.matrix_col + dy].destroys()
							matrix2.matrix[self.matrix_row + dx][self.matrix_col + dy].destroyed = True
							if matrix2.matrix[self.matrix_row + dx][self.matrix_col + dy].adj == 0:
								for d2 in dxs:
									for d2 in dys:
										if self.matrix_row + dx + d2 in list(range(1,19)) and self.matrix_col + dy + d2 in list(range(1,34)):
											matrix2.matrix[self.matrix_row + dx + d2][self.matrix_col + dy + d2].destroys()
											matrix2.matrix[self.matrix_row + dx + d2][self.matrix_col + dy + d2].destroyed = True



			else:
				self.tile.destroy()
				self.destroyed = True
				self.reveal = Label(board.main_frame, text = str(self.adj), font = ('mine-sweeper', 12, 'bold'), fg = self.color, bg = "#707070")
				self.reveal.grid(row = self.row, column = self.col)
		for i in range(1,19):
			for j in range(1,34):
				if matrix2.matrix[i][j].destroyed == True:
					total_removed += 1
		board.destroyed_tiles = total_removed
		print(board.destroyed_tiles)
		if board.tiles_left == board.destroyed_tiles:
			board.game_over = True
			#board.main_frame.wm_attributes('-alpha', 0.0)
			win_frame = Frame(root, width = 200, height = 100)
			win_frame.grid(row=0, column=0)
			win_screen = Label(win_frame, text = "You Won!", font = ('mine-sweeper', 20), fg = "black", bg = "green")
			win_screen.grid(row=0, column=0)	


	def alter(self, event):	
			if board.game_over == True:
				pass
			else:
				if self.text == '':
					self.text = "*"
					board.total_bombs -= 1
					board.score_num.config(text=str(board.total_bombs - 130))
					self.tile.config(text = self.text, font = ('mine-sweeper', 8, 'bold'), width=1, height=1)
				elif self.text == '*':
					self.text = "?"
					board.total_bombs += 1
					board.score_num.config(text=str(board.total_bombs - 130))
					self.tile.config(text = self.text, font = ('mine-sweeper', 8, 'bold'), width=1, height=1)
				elif self.text == '?':
					self.text = ""
					self.tile.config(text = self.text, font = ('mine-sweeper', 8, 'bold'), width=1, height=1)
	def destroys(self):
		if self.bomb == True:
			self.tile.destroy()
			self.reveal = Label(board.main_frame, text = '*', font = ('mine-sweeper', 11, 'bold'), fg = 'black', bg = "red")
			self.reveal.grid(row = self.row, column = self.col)

		else:
			self.tile.destroy()
			self.reveal = Label(board.main_frame, text = str(self.adj), font = ('mine-sweeper', 12, 'bold'), fg = self.color, bg = "#707070")
			self.reveal.grid(row = self.row, column = self.col)

			

class BlankTile:
	def __init__(self):
		self.root = root
		self.bomb = False
		self.adj = 0

class Matrix:
	def __init__(self):
		self.root = root
		
		self.matrix = []
		for i in range(18):
			self.col = []
			for j in range(33):
				tile = Tile(i,j)
				self.col.append(tile)
			self.matrix.append(self.col)
		for i in self.matrix:
			i.insert(0,BlankTile())
			i.append(BlankTile())
		self.matrix.insert(0,[BlankTile() for k in range(35)])
		self.matrix.append([BlankTile() for p in range(35)])

		for bomb in range(board.num_bombs):			
			i = random.randint(2,18)
			j = random.randint(2,33)
			if self.matrix[i][j].bomb == False:
				self.matrix[i][j].bomb = True
		
		while board.total_bombs < board.num_bombs + 30:
			next_path = [random.randint(0,7) for i in range(2)]
			for p in range(1,2):
				if 0 in next_path:
					go_path = random.randint(0,2)
					if go_path == 1 and i+p in range(1,19):            
						self.matrix[i+p][j].bomb = True
						board.total_bombs += 1
				if 1 in next_path:
					go_path = random.randint(0,2)
					if go_path == 1 and i-p in range(1,19):            
						self.matrix[i-p][j].bomb = True
						board.total_bombs += 1
				if 2 in next_path:
					go_path = random.randint(0,2)
					if go_path == 1 and j+p in range(1,34):            
						self.matrix[i][j+p].bomb = True
						board.total_bombs += 1
				if 3 in next_path:
					go_path = random.randint(0,2)
					if go_path == 1 and j-p in range(1,34):            
						self.matrix[i][j-p].bomb = True
						board.total_bombs += 1
				if 4 in next_path:
					go_path = random.randint(0,2)
					if go_path == 1 and j+p in range(1,34) and i+p in range(1,19):            
						self.matrix[i+p][j+p].bomb = True
						board.total_bombs += 1
				if 5 in next_path:
					go_path = random.randint(0,2)
					if go_path == 1 and j+p in range(1,34) and i-p in range(1,19):            
						self.matrix[i-p][j+p].bomb = True
						board.total_bombs += 1
				if 6 in next_path:
					go_path = random.randint(0,2)
					if go_path == 1 and j-p in range(1,34) and i-p in range(1,19):            
						self.matrix[i-p][j-p].bomb = True
						board.total_bombs += 1
				if 7 in next_path:
					go_path = random.randint(0,2)
					if go_path == 1 and j-p in range(1,34) and i+p in range(1,19):            
						self.matrix[i+p][j-p].bomb = True
						board.total_bombs += 1
		board.score_num.config(text=str(board.total_bombs))

		for i in range(1,19):
			for j in range(1,34):
				if self.matrix[i][j].bomb == True:
					self.matrix[i][j].adj = 20
				elif self.matrix[i][j].bomb == False:
					if self.matrix[i+1][j].bomb == True:
						self.matrix[i][j].adj += 1
					if self.matrix[i-1][j].bomb == True:
						self.matrix[i][j].adj += 1
					if self.matrix[i][j+1].bomb == True:
						self.matrix[i][j].adj += 1
					if self.matrix[i][j-1].bomb == True:
						self.matrix[i][j].adj += 1
					if self.matrix[i+1][j+1].bomb == True:
						self.matrix[i][j].adj += 1
					if self.matrix[i-1][j+1].bomb == True:
						self.matrix[i][j].adj += 1
					if self.matrix[i-1][j-1].bomb == True:
						self.matrix[i][j].adj += 1
					if self.matrix[i+1][j-1].bomb == True:
						self.matrix[i][j].adj += 1
				if self.matrix[i][j].adj == 0:
					self.matrix[i][j].color = "#707070"
				elif self.matrix[i][j].adj == 1:
					self.matrix[i][j].color = "blue"
				elif self.matrix[i][j].adj == 2:
					self.matrix[i][j].color = "#008900"
				elif self.matrix[i][j].adj == 3:
					self.matrix[i][j].color = "#ff0000"
				elif self.matrix[i][j].adj == 4:
					self.matrix[i][j].color = "#000080"
				elif self.matrix[i][j].adj == 5:
					self.matrix[i][j].color = "#760000"
				elif self.matrix[i][j].adj == 6:
					self.matrix[i][j].color = "#388E8E"
				elif self.matrix[i][j].adj == 7:
					self.matrix[i][j].color = "black"
				elif self.matrix[i][j].adj == 8:
					self.matrix[i][j].color = "#A9A9A9"

matrix2 = Matrix()



for i in range(1,19):
	for j in range(1,34):
		if matrix2.matrix[i][j].bomb == True:
			board.total_bombs += 1
		elif matrix2.matrix[i][j].bomb == False:
			board.tiles_left += 1
board.score_num.config(text=str(board.total_bombs - 130))




root.mainloop()