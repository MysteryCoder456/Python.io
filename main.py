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
		self.player = Snake(width / 2, height / 2, 20, (255, 0, 0), 2)
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
		turn_speed = math.pi / 80

		if left:
			self.player.head.angle -= turn_speed
		if right:
			self.player.head.angle += turn_speed

		# Boost if "up" arrow key is held
		if up:
			if len(self.player.tail) > 7:
				# Chance of player losing a segment of tail if they boost
				chance = 5000
				if randint(0, 100000) < chance:
					self.player.tail.pop()

				self.player.speed = 4
		else:
			self.player.speed = 2

		# dx = mouse_x - self.seg.x
		# dy = mouse_y - self.seg.y
		# new_angle = math.atan2(dy, dx)
		# self.seg.angle = new_angle
		# self.seg.speed = 5
		# self.seg.update()

		# Make the snake follow the mouse
		# dx = mouse_x - self.player.head.x
		# dy = mouse_y - self.player.head.y
		# new_angle = math.atan2(dy, dx)
		# self.player.head.angle = new_angle
		self.player.head.speed = self.player.speed

		# Slithering effect
		for i in range(len(self.player.tail)):
			if i == 0:
				dx = self.player.head.x - self.player.tail[i].x
				dy = self.player.head.y - self.player.tail[i].y
			else:
				dx = self.player.tail[i-1].x - self.player.tail[i].x
				dy = self.player.tail[i-1].y - self.player.tail[i].y

			new_angle = math.atan2(dy, dx)
			self.player.tail[i].angle = new_angle
			self.player.tail[i].speed = self.player.speed

		# Stop game if player touches edges
		if self.collision_edges(self.player.head.x, self.player.head.y, self.player.head.size):
			self.running = False

		# Add a segment to player's tail if the player touches food
		for food in self.food:
			if self.collision_circle(
									food.x, food.y, food.size,
									self.player.head.x, self.player.head.y, self.player.head.size
									):
				seg = Segment(
								self.player.tail[len(self.player.tail)-1].x,
								self.player.tail[len(self.player.tail)-1].y,
								self.player.seg_size,
								self.player.color
							)
				self.player.tail.append(seg)
				self.food.remove(food)

		# Stop snake if it touches the mouse
		# if self.collision_circle(
		# 							mouse_x, mouse_y, -5,
		# 							self.player.head.x, self.player.head.y, self.player.head.size
		# 						):
		# 	self.player.head.speed = 0

		# 	for seg in self.player.tail:
		# 		seg.speed = 0

		# Limit distance between each tail segment
		for i in range(len(self.player.tail)):
			tail = self.player.tail
			limit = 12
			if i == 0:
				x1 = self.player.head.x
				y1 = self.player.head.y
				r1 = self.player.head.size - limit
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

		# Update player's variables
		self.player.update()
		
		self.frame_count += 1
		
	def render(self):
		# self.seg.render()

		for food in self.food:
			food.render()

		self.player.render()



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
