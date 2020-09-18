import pygame
from numpy import matrix
import sys

# colors used in the game Format: RGB
color_yellow = (255,255,0)
color_red = (255,51,0)
color_green = (0,255,0)
color_white = (255,255,255)
color_black = (0,0,0)

class Board:
	Grid = []
	x_points = [0,60,120,180,240,300,360,420,480]
	y_points = [0,60,120,180,240,300,360,420,480]
	def __init__(self,screen,filename):
		self.screen = screen
		self.filename = filename
		self.open_file()
		self.print_grid()
		self.print_numbers()
		self.fnt = pygame.font.SysFont("comicsans",45)
	
	# Print the grid Lines of the Board
	def print_grid(self):
		
		for i in range(0,541,60):
			thicc = 1
			if i % 180 == 0:
				thicc = 4
			pygame.draw.line(self.screen,color_white,(0,i),(540,i),thicc)
			pygame.draw.line(self.screen,color_white,(i,0),(i,540),thicc)

	# Printing the given numbers of the puzzle
	def print_numbers(self):
		fnt = pygame.font.SysFont("comicsans",45)

		for i in range(9):
			for j in range(9):
				if Board.Grid[i][j] != 0:
					text = fnt.render(str(Board.Grid[i][j]),1,color_white)
					self.screen.blit(text,(Board.x_points[j] + (30 - text.get_width()/2),Board.y_points[i] + (30 - text.get_height()/2)))

		text = fnt.render("Press ENTER to solve",1,(210,210,13))
		self.screen.blit(text,(0 + (272 - text.get_width()/2),544 + (28 - text.get_height()/2 )))


	# Opening the puzzle file provided as text file
	def open_file(self):
		with open(self.filename) as file:
			for line in file:
				values = line.split()
				x = list()
				for e in values:
					x.append(int(e))
				Board.Grid.append(x)

	# Solving the Sudoku
	def sudoku_solver(self):
		pygame.draw.rect(self.screen,color_black,[0,544,544,600])
		text = self.fnt.render("Solving...",1,(253,187,45))
		self.screen.blit(text,(0 + (272 - text.get_width()/2),544 + (28 - text.get_height()/2 )))

		for i in range(9):
			for j in range(9):
				if Board.Grid[i][j] == 0:
					self.update_grid(color_yellow,Board.x_points[j],Board.y_points[i],0)
					for val in range(1,10):
						if self.check(i,j,val):
							Board.Grid[i][j] = val
							self.update_grid(color_green,Board.x_points[j],Board.y_points[i],val)
							result = self.sudoku_solver()
							if result:
								return True
							Board.Grid[i][j] = 0
							self.update_grid(color_red,Board.x_points[j],Board.y_points[i],0)

					self.update_grid(color_red,Board.x_points[j],Board.y_points[i],0)
					return False

		return True

	# Priting a valid input for the game 
	def update_grid(self,color,point_x,point_y,val):
		fnt = pygame.font.SysFont("comicsans",45)
		if val == 0:
			pygame.draw.rect(self.screen,color_black,[point_x,point_y,60,60])
		else:
			txt = fnt.render(str(val),1,color_white)
			self.screen.blit(txt,(point_x + (30 - txt.get_width()/2),point_y + (30 - txt.get_height()/2)))
		pygame.draw.rect(self.screen,color,[point_x,point_y,60,60],2)
		pygame.display.update()
		pygame.time.wait(80)


	# Checking the validity of a number to be filled in the grid
	def check(self,x,y,val):
		for i in range(9):
			if Board.Grid[x][i] == val:
				return False
			if Board.Grid[i][y] == val:
				return False
			
		x0 = (x//3) * 3
		y0 = (y//3) * 3

		for i in range(0,3):
			for j in range(0,3):
				if Board.Grid[x0+i][y0+j] == val:
					return False

		return True

# initializing the pygame window
def main(filename):
	pygame.init()
	screen = pygame.display.set_mode((544,600))
	pygame.display.set_caption("Sudoku Solver")
	screen.fill(color_black)

	board = Board(screen,filename)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					board.sudoku_solver()
					pygame.draw.rect(board.screen,color_black,[0,544,544,600])
					text = board.fnt.render("Solved",1,(121,255,86))
					board.screen.blit(text,(0 + (272 - text.get_width()/2),544 + (28 - text.get_height()/2 )))
		
		pygame.display.update()


if __name__ == "__main__":
	# Checking if puzzle file is provided as a argument or not
	if len(sys.argv) != 1:
		main(sys.argv[1])

	print("Give a file as input")
