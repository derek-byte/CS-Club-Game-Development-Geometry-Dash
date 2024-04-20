import pygame
from settings import*

class gameobject():

	def __init__(self,
				position, width, height,
				image_path,
				tag="",
				scale=1,
				transparent=False,
				collider_offset=[0,0], collider_size=[1,1],):

		self.position = position
		self.velocity = [0,0]
	
		#Dimensions of the sprite
		self.width = width
		self.height = height
	
		self.collider_offset = collider_offset
		self.collider_size = collider_size
	
		#Get the object tag from image path (ex."Sprites/Player"-->"Player")
		self.tag = image_path[image_path.find("/")+1:]
	
		self.scale = scale
	
		#If the image has transparency in it
		self.transparent = transparent
	
		self.rect = pygame.Rect(0, 0, 0, 0)
	
		self.sprite = pygame.image.load(image_path + ".png").convert()
	
		#Create the object sprite
		self.rendered_sprite = pygame.Surface((self.width, self.height)).convert_alpha()
		self.rendered_sprite.blit(self.sprite, (0,0), (0, 0, self.width, self.height))
		self.rendered_sprite = pygame.transform.scale(self.rendered_sprite, (self.width*self.scale, self.height*self.scale))
		if transparent:
			self.rendered_sprite.set_colorkey((0,0,0))
	
	def update_position(self, delta):
	
		self.position[0] += self.velocity[0] * delta
		self.position[1] += self.velocity[1] * delta
	
class square(gameobject):

	def __init__(self,position):

		#Call the gameobject constructor
		super().__init__(position, image_path="Sprites/Player", width=121, height=120, scale = 0.5)

		self.alive = True
		
		#If object is on ground
		self.grounded = False
		
	def update_position(self, delta):
	
		# Prevent player from falling off the screen
		self.position[1] = min(self.position[1], screen_height-(self.height*self.scale))	
		if self.rect.bottom >= screen_height:
				self.grounded = True
			
		# Add Gravity
		if self.grounded == False:
				self.velocity[1] += gravity*delta

		super().update_position(delta)

	def jump(self, delta):

		#Only jump if on ground
		if self.grounded:
				self.velocity[1] = -player_jump*delta
				self.grounded = False

	def check_collisions(self, gameobjects):

		self.grounded = False

		#Itterate through all objects in the sccene to check collisions
		for obj in gameobjects:

			if obj != self and pygame.Rect.colliderect(self.rect, obj.rect):

				#If we are on top of a block
				if obj.tag == "Block" and abs(obj.rect.top - self.rect.bottom) <= collision_margin:

					#Only stop ourself if we are coming down from a jump
					if self.velocity[1] >= 0:
						self.grounded = True
						self.velocity[1] = 0

				#Die if we touch a spike or a block from the side
				else:
						self.alive = False

class spike(gameobject):
	def __init__(self,position):
		super().__init__(position, image_path="Sprites/Spike", width=122, height=122, scale = 0.5, transparent=True, collider_size=[0.5,0.9], collider_offset=[-15,-10])

class block(gameobject):
	def __init__(self,position):
		super().__init__(position, image_path="Sprites/Block", width=122, height=122, scale = 0.5)