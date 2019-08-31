# Python.io Game
# Made by MysteryCoder456 / Rehatbir Singh
# GNU GENERAL PUBLIC LICENSE in LICENSE file

from snake import Snake
from segment import Segment
from food import Food
from menu import Menu
from uni_vars import *
from random import randint
import pygame
import math


#========================================================================================================#
#=========================================== Game Starts Here ===========================================#
#========================================================================================================#


class Game:
	def start(self):
		# self.seg = Segment(100, 100, 20, (140, 0, 0))
		self.p1 = Snake(width/4, height / 2, 20, (255, 0, 0), 2)
		self.p2 = Snake(width/4*3, height / 2, 20, (0, 255, 0), 2)
		self.food = []
		self.min_food_count = 25
		self.frame_count = 0

		for i in range(50):
			x = randint(0, width - 10) + 5
			y = randint(0, height - 10) + 5
			r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
			f = Food(x, y, (r, b, g))
			self.food.append(f)

	def logic(self):
		# for seg in self.p2.tail:
		# 	seg.color = (0, 255, 0)

		if self.frame_count % 1000 == 0:
			for i in range(randint(self.min_food_count * 2, self.min_food_count * 5)):
				if len(self.food) < self.min_food_count:
					x = randint(0, width - 10) + 5
					y = randint(0, height - 10) + 5
					r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
					f = Food(x, y, (r, b, g))
					self.food.append(f)

		# mouse_x = pygame.mouse.get_pos()[0]
		# mouse_y = pygame.mouse.get_pos()[1]

		keys = pygame.key.get_pressed()
		left = keys[pygame.K_LEFT]
		right = keys[pygame.K_RIGHT]
		up = keys[pygame.K_UP]
		w = keys[pygame.K_w]
		a = keys[pygame.K_a]
		d = keys[pygame.K_d]
		turn_speed = math.pi / 80

		if a:
			self.p1.head.angle -= turn_speed
		if d:
			self.p1.head.angle += turn_speed

		if left:
			self.p2.head.angle -= turn_speed
		if right:
			self.p2.head.angle += turn_speed

		# Boost if "up" arrow key or "w" key is held
		chance = 5000

		if up:
			if len(self.p1.tail) > 7:
				# Chance of p1 losing a segment of tail if they boost
				if randint(0, 100000) < chance:
					self.p1.tail.pop()

				self.p1.speed = 4
		else:
			self.p1.speed = 2

		if w:
			if len(self.p2.tail) > 7:
				# Chance of p2 losing a segment of tail if they boost
				if randint(0, 100000) < chance:
					self.p2.tail.pop()

				self.p2.speed = 4
		else:
			self.p2.speed = 2

		# dx = mouse_x - self.seg.x
		# dy = mouse_y - self.seg.y
		# new_angle = math.atan2(dy, dx)
		# self.seg.angle = new_angle
		# self.seg.speed = 5
		# self.seg.update()

		# Make the snake follow the mouse
		# dx = mouse_x - self.p1.head.x
		# dy = mouse_y - self.p1.head.y
		# new_angle = math.atan2(dy, dx)
		# self.p1.head.angle = new_angle
		self.p1.head.speed = self.p1.speed
		self.p2.head.speed = self.p2.speed

		# Slithering effect
		for i in range(len(self.p1.tail)):
			if i == 0:
				dx = self.p1.head.x - self.p1.tail[i].x
				dy = self.p1.head.y - self.p1.tail[i].y
			else:
				dx = self.p1.tail[i-1].x - self.p1.tail[i].x
				dy = self.p1.tail[i-1].y - self.p1.tail[i].y

			new_angle = math.atan2(dy, dx)
			self.p1.tail[i].angle = new_angle
			self.p1.tail[i].speed = self.p1.speed

		for i in range(len(self.p2.tail)):
			if i == 0:
				dx = self.p2.head.x - self.p2.tail[i].x
				dy = self.p2.head.y - self.p2.tail[i].y
			else:
				dx = self.p2.tail[i-1].x - self.p2.tail[i].x
				dy = self.p2.tail[i-1].y - self.p2.tail[i].y

			new_angle = math.atan2(dy, dx)
			self.p2.tail[i].angle = new_angle
			self.p2.tail[i].speed = self.p2.speed

		# Stop game if a snake touches edges
		global running
		if self.collision_edges(self.p1.head.x, self.p1.head.y, self.p1.head.size):
			running = False
			print("GREEN WINS!")

		if self.collision_edges(self.p2.head.x, self.p2.head.y, self.p2.head.size):
			running = False
			print("RED WINS!")

		# Add a segment to a snake's tail if the it touches food
		for food in self.food:
			food_eaten = False

			if self.collision_circle(
									food.x, food.y, food.size,
									self.p1.head.x, self.p1.head.y, self.p1.head.size
									):
				seg = Segment(
								self.p1.tail[len(self.p1.tail)-1].x,
								self.p1.tail[len(self.p1.tail)-1].y,
								self.p1.seg_size,
								self.p1.color
							)
				self.p1.tail.append(seg)
				food_eaten = True

			if self.collision_circle(
									food.x, food.y, food.size,
									self.p2.head.x, self.p2.head.y, self.p2.head.size
									):
				seg = Segment(
								self.p2.tail[len(self.p2.tail)-1].x,
								self.p2.tail[len(self.p2.tail)-1].y,
								self.p2.seg_size,
								self.p2.color
							)
				self.p2.tail.append(seg)
				food_eaten = True

			if food_eaten:
				self.food.remove(food)

		# Stop snake if it touches the mouse
		# if self.collision_circle(
		# 							mouse_x, mouse_y, -5,
		# 							self.p1.head.x, self.p1.head.y, self.p1.head.size
		# 						):
		# 	self.p1.head.speed = 0

		# 	for seg in self.p1.tail:
		# 		seg.speed = 0

		# Limit distance between each tail segment
		limit = 12

		for i in range(len(self.p1.tail)):
			tail = self.p1.tail
			if i == 0:
				x1 = self.p1.head.x
				y1 = self.p1.head.y
				r1 = self.p1.head.size - limit
				x2 = tail[i].x
				y2 = tail[i].y
				r2 = tail[i].size - limit
			else:
				x1 = tail[i-1].x
				y1 = tail[i-1].y
				r1 = tail[i-1].size - limit
				x2 = tail[i].x
				y2 = tail[i].y
				r2 = tail[i].size - limit

			if self.collision_circle(x1, y1, r1, x2, y2, r2):
				tail[i].speed = 0

		for i in range(len(self.p2.tail)):
			tail = self.p2.tail
			if i == 0:
				x1 = self.p2.head.x
				y1 = self.p2.head.y
				r1 = self.p2.head.size - limit
				x2 = tail[i].x
				y2 = tail[i].y
				r2 = tail[i].size - limit
			else:
				x1 = tail[i-1].x
				y1 = tail[i-1].y
				r1 = tail[i-1].size - limit
				x2 = tail[i].x
				y2 = tail[i].y
				r2 = tail[i].size - limit

			if self.collision_circle(x1, y1, r1, x2, y2, r2):
				tail[i].speed = 0

		# Update p1's variables
		self.p1.update()

		# Update p2's variables
		self.p2.update()
		
		self.frame_count += 1
		
	def render(self):
		# self.seg.render()

		for food in self.food:
			food.render()

		self.p1.render()
		self.p2.render()



	#========================================================================================================#
	#========================================== Gameplay Functions ==========================================#
	#========================================================================================================#



	def dist(self, x1, y1, x2, y2):
		# Pythagorean Theorem: a^2 + b^2 = c^2
		a = x1 - x2
		b = y1 - y2
		c = math.sqrt(math.pow(a, 2) + math.pow(b, 2))
		return c

	def collision_circle(self, x1, y1, r1, x2, y2, r2):
		# find the distance between seg1 and seg2 and tell if they collide
		d = self.dist(x1, y1, x2, y2)

		if d <= r1 + r2:
			return True

	def collision_edges(self, x, y, r):
		if x - r < 0:
			return True
		if x + r > width:
			return True
		
		if y - r < 0:
			return True
		if y + r > height:
			return True



		
	
































# !!! - DO NOT MODIFY THE BELOW CODE IN ANYWAY - !!! #


def menu():
	main_menu = Menu()

	while main_menu.running:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				global running
				main_menu.running = False
				running = False

		main_menu.logic()
		win.fill(background)
		main_menu.render()
		pygame.display.update()



def main():
	global running

	game = Game()

	game.start()
	
	while running:
		# clock.tick() takes parameter than specifies the fps that you game should run at
		clock.tick(60)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				
		game.logic()
		win.fill(background)
		game.render()
		pygame.display.update()
		
		
if __name__ == "__main__":
	menu()
	main()
	pygame.quit()
	quit()
