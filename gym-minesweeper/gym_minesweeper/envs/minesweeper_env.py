import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.spaces import Discrete,Tuple,Box,MultiDiscrete
import numpy as np
import random
import sys

class Minesweeper(gym.Env):
	metadata = {'render.modes': ['human']}
	UNKNOWN = -1
	MINE = -99999

	def __init__(self, rows=10, cols=10, mines=10):
		
		self.action_space = Tuple((Discrete(rows),Discrete(cols)))
		self.observation_space = Box(low= -1, high=8, shape=(rows, cols), dtype=np.uint8)
		self.rows = rows
		self.cols = cols
		self.mines = mines
		self.nonMines = rows*cols - mines
		self.clickedCoords = set()
		self.letter_Axis = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19']
		self.chosenCoords = []
		self.state = np.full([self.rows, self.cols], Minesweeper.UNKNOWN)
		self.neighboring_mines = 0
		self.reward = 0
		self.info = dict()
		self.coordcount = dict()

	def conCoord(self, userInput):
		# rows x cols
		self.cc = userInput
		firstVal = self.letter_Axis[self.cc[0]]
		x = str(firstVal)
		y = str(self.cc[1])
		xy = x + y
		return xy

	def checkDigit(self,coord):
		n = coord % 10
		return n == coord


	def step(self, coord ):
		done = False
		
		if self.checkDigit(coord):
			self.coord = (0,coord)
		else:
			coord = str(coord)
			self.coord = (int(coord[0]),int(coord[1]))

		if self.reward < -100 :
			done = True
			self.reward = -9999

		if self.coord in self.clickedCoords:
		    self.reward -=  1

		elif self.coord in self.mine_coords:
		    # Clicked on a mine!
		    self.state[self.coord] = Minesweeper.MINE
		    self.reward = Minesweeper.MINE # -99
		    self.clickedCoords.add(self.coord)
		    done = True
		else:
		    self.neighboring_mines = 0
		    for r in range(self.coord[0]-1, self.coord[0]+2):
		        for c in range(self.coord[1]-1, self.coord[1]+2):
		            if r >= 0 and c >= 0:
		                if (r,c) in self.mine_coords:
		                    self.neighboring_mines += 1
		    self.state[self.coord] = self.neighboring_mines
		    self.neighboring_mines = 0
		    self.coords_to_clear -= 1
		    if self.coords_to_clear == 0:
		        self.reward += 500     # Yay you won.
		        done = True
		    else:
		        self.reward += 4
		        self.clickedCoords.add(self.coord)
		
		return (self.state, self.reward, done, self.info)

	def reset(self):
		# Internal state: where are all the mines?
		self.mine_coords = set()
		mines_to_place = self.mines
		while mines_to_place > 0:
		    r = random.randrange(self.rows)
		    c = random.randrange(self.cols)
		    if (r, c) not in self.mine_coords:  # new coord
		        self.mine_coords.add((r, c))
		        mines_to_place -= 1
		print("SECRET locations:", self.mine_coords)
		self.state = np.full([self.rows, self.cols], Minesweeper.UNKNOWN)
		self.coords_to_clear = self.rows * self.cols - self.mines
		self.reward = 0
		return self.state

	def render(self):
		for x in range(self.rows):
		    sys.stdout.write(self.letter_Axis[x])
		    for y in range(self.cols):
		        if self.state[x][y] == -99:                  
		            sys.stdout.write(' x')
		        elif self.state[x][y] == -1:                  
		            sys.stdout.write(' .')
		        elif self.state[x][y] != -1:
		            sys.stdout.write(' %s' % int(self.state[x][y]))
		        if y != self.cols-1:
		            sys.stdout.write(' ')
		            if y == (self.cols - 1):
		                sys.stdout.write('\n')
		    sys.stdout.write('\n')
		sys.stdout.write(' ')
		for k in range(self.cols):
		    sys.stdout.write(' %s ' % k)
		print ("")
