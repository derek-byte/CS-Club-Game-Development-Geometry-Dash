#Package Imports
import sys
import pygame
from pygame.locals import QUIT

from classes import *
from settings import*

#Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Geometry Dash')

#Initialize font
pygame.font.init()
game_font = pygame.font.SysFont(None, 32)

def main():

	running = True #If the game is running

	clock = pygame.time.Clock() #Used to get time
	dt = 0 # Delta-time, used for physics calcs

	gameobjects = [] #Array of all objects in scene

	#Create Player
	player = square(position=[0,0])
	gameobjects.append(player)

	#Level Initialization
	gameobjects.append(spike(position=[500,240]))
	gameobjects.append(block(position=[400, 240]))
	gameobjects.append(block(position=[800, 240]))
	
	gameobjects.append(spike(position=[860,240]))
	gameobjects.append(spike(position=[920,240]))

	gameobjects.append(block(position=[1200, 240]))
	gameobjects.append(spike(position=[1270,200]))
	gameobjects.append(block(position=[1350,160]))
	gameobjects.append(block(position=[1410,160]))
	gameobjects.append(block(position=[1470,160]))
	gameobjects.append(block(position=[1530,160]))

	#Game Loop
	while running:

		#Background
		screen.fill((0,0,0))

		#Exit with escape
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		#Delta time, to ensure movement is not bound to the framerate
		dt = clock.tick(60) / 1000

		#Stores all keys pressed at the current frame
		keys = pygame.key.get_pressed()

		#Reset game
		if keys[pygame.K_r]:
			main()

		#Handle Player
		if player.alive:
			#Jump
			if keys[pygame.K_SPACE]: # check if SPACE has been pressed
				player.jump(dt)
			player.check_collisions(gameobjects)

		#Draw Restart Text
		else:
			screen.blit(game_font.render('Press r to restart', True, (255, 255, 255), None), dest=(100,100))

		#Draw gameobjects in scene
		for obj in gameobjects:

			#Only Draw if object is in view (with a margin of 100 pixels)
			if obj.position[0] >= -100 and obj.position[0] < screen_width+100:
				#Draw the object
				obj.rect = pygame.Rect(obj.position[0], obj.position[1], obj.width * obj.scale, obj.height * obj.scale)
				screen.blit(obj.rendered_sprite, obj.rect)

				#Resize rect for collisions
				obj.rect = pygame.Rect(obj.position[0]-obj.collider_offset[0], obj.position[1]-obj.collider_offset[1], obj.width*obj.scale*obj.collider_size[0], obj.height*obj.scale*obj.collider_size[1])

				#Uncomment line bellow to see hitboxes in red
				#pygame.draw.rect(screen, (255, 0, 0), obj.rect, 5)

			#Move the level to the left
			if obj.tag != "Player":
				obj.velocity[0] = -level_speed*dt
				
			#Update movement
			if player.alive:
				obj.update_position(dt)

		#Update the screen
		pygame.display.update()

	#Quit the game if the game running is false
	pygame.quit()

#Initial main call
main()