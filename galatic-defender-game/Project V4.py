import pygame, sys, math, random, time, datetime
from pygame.locals import *

# important setup

pygame.mixer.pre_init(frequency=22050,size=-16,channels=256,buffer=8)
pygame.init()

screenWidth = pygame.display.Info().current_w # game adjusts for monitor resolution, might have issues on very small or very high resolutions but works fine on 1080p
screenHeight = pygame.display.Info().current_h
screenWidthCentre = screenWidth / 2
screenHeightCentre = screenHeight / 2

screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN )
pygame.display.set_caption('Galactic Defender')
clock = pygame.time.Clock()

# load pictures

if screenWidth > 1920 or screenHeight > 1080:
	Background = pygame.image.load('Sprites/Background2.jpg').convert()
else:
	Background = pygame.image.load('Sprites/Background1.jpg').convert()

Explosion_IMGS = []
for x in range(1,11):
	Explosion_IMGS.append(pygame.image.load('Sprites/Explosion' + str(x) + '.png'))

# load sounds

pygame.mixer.init()
pygame.mixer.set_num_channels(256)

pygame.mixer.music.load('Music/Music1.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

explosionSound1 = pygame.mixer.Sound("Sounds/SmallBoom1.wav")
explosionSound2 = pygame.mixer.Sound("Sounds/SmallBoom2.wav")
explosionSound3 = pygame.mixer.Sound("Sounds/SmallBoom3.wav")
explosionSound4 = pygame.mixer.Sound("Sounds/SmallBoom4.wav")
explosionSoundBig = pygame.mixer.Sound("Sounds/BigBoom.wav")
explosionSoundSmall = pygame.mixer.Sound("Sounds/TinyBoom.wav")
alienShootingSound1 = pygame.mixer.Sound("Sounds/AlienAttack1.wav")
alienShootingSound2 = pygame.mixer.Sound("Sounds/AlienAttack2.wav")
alienShootingSound3 = pygame.mixer.Sound("Sounds/AlienAttack3.wav")
gunSound = pygame.mixer.Sound("Sounds/Gunshot.wav")
missileSound = pygame.mixer.Sound("Sounds/MissileLaunch.wav")
ammoSound = pygame.mixer.Sound("Sounds/Reload.wav")
healSound = pygame.mixer.Sound("Sounds/Heal.wav")

# set volume of sounds

explosionSoundBig.set_volume(0.6)
explosionSoundSmall.set_volume(0.3)
alienShootingSound1.set_volume(0.15)
alienShootingSound2.set_volume(0.15)
alienShootingSound3.set_volume(0.15)
gunSound.set_volume(0.05)
missileSound.set_volume(0.4)
ammoSound.set_volume(0.6)
healSound.set_volume(0.7)

# colours

black = (0,0,0)
white = (255,255,255)
green = (0,240,0)
yellow = (240,240,0)
red = (240,0,0)
lightgray = (210, 210, 210)
darkgray = (50, 50, 50)
gray = (150, 150, 150)

# menu and UI functions

largeFont = pygame.font.Font('freesansbold.ttf', 115)
medFont = pygame.font.Font('freesansbold.ttf', 50)
smallFont = pygame.font.Font('freesansbold.ttf', 30)
tinyFont = pygame.font.Font('freesansbold.ttf', 15)

def title(text, font, color, offsetX, offsetY): # main titles for menu
    
    textContent = font.render(text, True, color)
    textRect = textContent.get_rect()  
    textRect.center = ((screenWidth / 2 + offsetX),(screenHeight / 2 + offsetY))
    screen.blit(textContent,textRect)

def button(text, x, y, width, height, color1, color2, font, textColor, action=None): # buttons for menu
	
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	if x+width > mouse[0] > x and y+height > mouse[1] > y:
		pygame.draw.rect(screen, color2, (x,y,width,height))
		
		if click[0] == 1: # button actions
			if action == "quit":
				pygame.quit()
				quit()
				
			elif action == "play":
				game_loop()	
				
			elif action == "controls":
				controls()
				
			elif action == "back":
				global runControls
				runControls = False
				
			elif action == "resume":
				global runGame
				runGame = True
				pygame.mouse.set_visible(False)
				
			elif action == "restart":
				global timeSurvived
				global timePaused
				timeSurvived = 0
				timePaused = 0
				
				for Powerup in Powerups:
					Powerups.remove(Powerup)
				for Asteroid in Asteroids:
					Asteroids.remove(Asteroid)
				for Alien in Aliens:
					Aliens.remove(Alien)
				for Bullet in AlienShots:
					AlienShots.remove(Bullet)
				for Bullet in PlayerShots:
					PlayerShots.remove(Bullet)
				for Bullet in PlayerMissiles:
					PlayerShots.remove(Bullet)
				for Explosion in Explosions:
					Explosion.remove(Explosion)
				
				Player1.image = pygame.image.load('Sprites/Fighter48px.png')
				Player1.health = 100
				Player1.ammo = 3
				Player1.x = screenWidthCentre
				Player1.y = screenHeightCentre
				
				explosionSound1.set_volume(1)
				explosionSound2.set_volume(1)
				explosionSound3.set_volume(1)
				explosionSound4.set_volume(1)
				explosionSoundSmall.set_volume(0.3)
				alienShootingSound1.set_volume(0.15)
				alienShootingSound2.set_volume(0.15)
				alienShootingSound3.set_volume(0.15)
				gunSound.set_volume(0.05)
				missileSound.set_volume(0.4)
				ammoSound.set_volume(0.6)
				healSound.set_volume(0.7)
				
				pygame.mixer.music.stop()
				pygame.mixer.music.load('Music/Music1.mp3')
				pygame.mixer.music.play(-1)
				game_loop()
	
	else:
		pygame.draw.rect(screen, color1, (x,y,width,height))
		
	textContent = font.render(text, True, textColor)
	textRect = textContent.get_rect()  
	textRect.center = ((x + (width/2)),(y + (height/2)))
	screen.blit(textContent,textRect)

def label(text, font, color, x, y): # text labels
    
    textContent = font.render(text, True, color)
    screen.blit(textContent, (x, y))
 
def healthbar(health, x, y): # player healthbar
	
	pygame.draw.rect(screen, black, (x+55, y-5, 310, 40))
	label('HP:', smallFont, white, x, y)
	
	if health > 66:
		pygame.draw.rect(screen, green, (x+60, y, health*3, 30))
	elif health > 33:
		pygame.draw.rect(screen, yellow, (x+60, y, health*3, 30))
	else:
		pygame.draw.rect(screen, red, (x+60, y, health*3, 30))

# gameplay functions

def distance(obj1, obj2): # finds distance between 2 objects
	return math.sqrt(math.pow((obj1.nextx - obj2.nextx), 2) + math.pow((obj1.nexty - obj2.nexty), 2))
	
def update_player(): # runs all the player functions
	
	Player1.move()
	Player1.crosshair()
	Player1.shoot()	
	Player1.update()
	Player1.edge()
	
	if Player1.health <= 0:
		game_over()

def update_asteroids(): # runs all the asteroid functions and collisions
				
	Asteroids.update()
	
	for Asteroid in pygame.sprite.spritecollide(Player1, Asteroids, False, pygame.sprite.collide_mask):
		if Asteroid.size == 64:
			Player1.health -= 50
			Asteroid.health -= 200
		else:
			Player1.health -= 100
	
	for Asteroid in Asteroids:
		if Asteroid.edge() == True:
			Asteroids.remove(Asteroid)
		
		if Asteroid.health <= 0:
			if Asteroid.size == 64:
				blast_size = 200
			elif Asteroid.size == 128:
				blast_size = 400
			elif Asteroid.size == 256:
				blast_size = 800
				
			explosion_sound("medium")
			Explosions.add(Explosion(Asteroid.x, Asteroid.y, blast_size))
			Asteroids.remove(Asteroid)
		
def update_aliens(): # runs all the alien functions and collisions
	
	Aliens.update(Player1)	
	
	for Alien in Aliens:
		Alien.shoot(Player1)
		Alien.edge()
		
		if Alien.health <= 0:
			explosion_sound("medium")
			Explosions.add(Explosion(Alien.x, Alien.y, 200))
			rng = random.randint(1,8)
			
			if rng == 8:
				Powerups.add(Powerup(Alien.speed, Alien.direction, Alien.x, Alien.y, random.randint(1,2)))
			
			Aliens.remove(Alien)
		
	for Alien in pygame.sprite.groupcollide(Aliens, Asteroids, False, False, pygame.sprite.collide_mask): # alien crashes into asteroid
		Alien.health -= 200
		
	for Alien in pygame.sprite.spritecollide(Player1, Aliens, False, pygame.sprite.collide_mask): # alien crashes into player
		Alien.health -= 200
		Player1.health -= 40
	
def update_projectiles(): # updates projectiles and removes them if they go offscreen
	
	AlienShots.update()
	PlayerShots.update()
	PlayerMissiles.update()
	
	for Bullet in AlienShots:
		if Bullet.edge() == True:
			AlienShots.remove(Bullet)	
	
	for Bullet in PlayerShots:
		if Bullet.edge() == True:
			PlayerShots.remove(Bullet)
			
	for Bullet in PlayerMissiles:
		if Bullet.edge() == True:
			PlayerMissiles.remove(Bullet)

def update_powerups(): # updates health and ammo drops
	
	Powerups.update()
	
	for Powerup in Powerups:
		if Powerup.edge == True:
			Powerups.remove(Powerup)

def update_interactions(): # updates all the projectile collisions
	
	for Bullet in pygame.sprite.groupcollide(AlienShots, PlayerMissiles, True, False, pygame.sprite.collide_mask): # player missiles and enemy bullets collide
		explosion_sound("small")
		Explosions.add(Explosion(Bullet.x, Bullet.y, 80))
	
	for Bullet in pygame.sprite.groupcollide(AlienShots, PlayerShots, True, True, pygame.sprite.collide_mask): # player bullets and enemy bullets collide
		explosion_sound("small")
		Explosions.add(Explosion(Bullet.x, Bullet.y, 80))
	
	for Alien in pygame.sprite.groupcollide(Aliens, PlayerMissiles, False, False, pygame.sprite.collide_mask): # player missile shoots enemy
		Alien.health -= 200
		for Bullet in pygame.sprite.groupcollide(PlayerMissiles, Aliens, False, False, pygame.sprite.collide_mask):
			Explosions.add(Explosion(Bullet.x, Bullet.y, 200))
		
	for Alien in pygame.sprite.groupcollide(Aliens, PlayerShots, False, False, pygame.sprite.collide_mask): # player shoots enemy
		explosion_sound("small")
		Alien.health -= 20
		for Bullet in pygame.sprite.groupcollide(PlayerShots, Aliens, False, False, pygame.sprite.collide_mask):
			Explosions.add(Explosion(Bullet.x, Bullet.y, 80))
			PlayerShots.remove(Bullet)
	
	for Asteroid in pygame.sprite.groupcollide(Asteroids, PlayerMissiles, False, False, pygame.sprite.collide_mask): # player missile shoots asteroid
		explosion_sound("medium")
		Asteroid.health -= 200
		for Bullet in pygame.sprite.groupcollide(PlayerMissiles, Asteroids, False, False, pygame.sprite.collide_mask):
			Explosions.add(Explosion(Bullet.x, Bullet.y, 200))
			PlayerMissiles.remove(Bullet)
		
	for Asteroid in pygame.sprite.groupcollide(Asteroids, PlayerShots, False, False, pygame.sprite.collide_mask): # player shoots asteroid
		explosion_sound("small")
		Asteroid.health -= 20
		for Bullet in pygame.sprite.groupcollide(PlayerShots, Asteroids, False, False, pygame.sprite.collide_mask):
			Explosions.add(Explosion(Bullet.x, Bullet.y, 80))
			PlayerShots.remove(Bullet)
		
	for Asteroid in pygame.sprite.groupcollide(Asteroids, AlienShots, False, False, pygame.sprite.collide_mask): # enemy shoots asteroid
		explosion_sound("small")
		Asteroid.health -= 20
		for Bullet in pygame.sprite.groupcollide(AlienShots, Asteroids, False, False, pygame.sprite.collide_mask):
			Explosions.add(Explosion(Bullet.x, Bullet.y, 80))
			AlienShots.remove(Bullet)
	
	for Bullet in pygame.sprite.spritecollide(Player1, AlienShots, True, pygame.sprite.collide_mask): # enemy shoots player
		explosion_sound("small")
		Explosions.add(Explosion(Player1.x, Player1.y, 150))
		Player1.health -= 20
		
	for Powerup in pygame.sprite.spritecollide(Player1, Powerups, False, pygame.sprite.collide_mask): # enemy shoots player
		#explosion_sound("small")
		Player1.pickup(Powerup.type)
		Powerups.remove(Powerup)
	
	Explosions.update()
	
def explosion_sound(size): # plays randomized explosion sound
	
	channel = pygame.mixer.find_channel(True)
	
	if size == "small":
		channel.queue(explosionSoundSmall)
	elif size == "medium":
		rng = random.randint(1,4)
		if rng == 1:
			channel.queue(explosionSound1)
		elif rng == 2:
			channel.queue(explosionSound2)
		elif rng == 3:
			channel.queue(explosionSound3)
		elif rng == 4:
			channel.queue(explosionSound4)
	elif size == "large":
		channel.queue(explosionSoundBig)
	
# sprite classes

class Player(pygame.sprite.Sprite): # the player
	def __init__(self):
		
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Sprites/Fighter48px.png')
		self.x = screenWidthCentre
		self.y = screenHeightCentre
		self.size = 48
		self.speed = 0
		self.direction = 180
		self.nextx, self.nexty = 0,0
		self.health = 100
		self.ammo = 3
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.last = pygame.time.get_ticks()     
	
	def move(self): # finds player direction relative to mouse
		
		keys = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pos()
		
		if keys[pygame.K_w]:	
			if self.speed < 8:
				self.speed += 0.4
		elif keys[pygame.K_s]:
			if self.speed > -2:
				self.speed -= 0.4
		else:
			if self.speed > 0.3:
				self.speed -= 0.4
			elif self.speed < -0.3:
				self.speed += 0.4
			else:
				self.speed = 0

		mouse_rad = math.atan2(-(self.y - mouse[1]), (self.x - mouse[0]))
		self.direction = math.degrees(mouse_rad % (2 * math.pi)) - 90
		
	def update(self): # updates movement
		
		mouse = pygame.mouse.get_pos()
		distance = math.sqrt(math.pow((self.y - mouse[1]), 2) + math.pow((self.x - mouse[0]), 2))
		rad = self.direction * math.pi/180
		
		if distance > 9:	
			self.x += self.speed*math.sin(rad)
			self.y += self.speed*math.cos(rad)
		
		self.nextx = self.x + self.speed*math.sin(rad)
		self.nexty = self.y + self.speed*math.cos(rad)
		self.render()
		
	def render(self): # renders onto screen
	
		scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
		rotated_image = pygame.transform.rotate(scaled_image, self.direction)
		self.rect = rotated_image.get_rect()
		self.rect.center = self.x, self.y
		screen.blit(rotated_image, self.rect)
		
		self.mask = pygame.mask.from_surface(rotated_image)
		
	def edge(self): # prevents player from moving offscreen
				
		rad = self.direction * math.pi/180
		if self.x < 15 or self.x > (screenWidth - 15):
			self.x -= self.speed*math.sin(rad)
		if self.y < 15 or self.y > (screenHeight - 15):
			self.y -= self.speed*math.cos(rad)
	
	def shoot(self): # attacking
		
		rad = self.direction * math.pi/180
		rng = random.randint(0,1)
		click = pygame.mouse.get_pressed()
	
		if click[0] == 1:
			now = pygame.time.get_ticks()
			if now - self.last >= 100:
				self.last = now
				PlayerShots.add(Bullet(Player, 1, self.speed, 15, self.direction, self.x, self.y))
				channel = pygame.mixer.find_channel(True)
				channel.queue(gunSound)
		elif click[2] == 1:
			now = pygame.time.get_ticks()
			if now - self.last >= 300:
				if self.ammo > 0:
					self.last = now
					PlayerMissiles.add(Bullet(Player, 2, self.speed, 10, self.direction, self.x, self.y))
					self.ammo -= 1
					channel = pygame.mixer.find_channel(True)
					channel.queue(missileSound)
	
	def crosshair(self): # renders crosshair for aiming
		
		mouse = pygame.mouse.get_pos()
		pygame.draw.line(screen, gray, (mouse[0],mouse[1]), (self.x,self.y), 1)
		
		crosshair = pygame.image.load('Sprites/Crosshair2.png')
		scaled_image = pygame.transform.scale(crosshair, (32, 32))
		self.rect = scaled_image.get_rect()
		self.rect.center = mouse[0], mouse[1]
		screen.blit(scaled_image, self.rect)
		
	def pickup(self, type): # when player reaches health or ammo pickup
		
		channel = pygame.mixer.find_channel(True)
		
		if type == 1:
			self.health += 50
			channel.queue(healSound)
			if self.health > 100:
				self.health = 100
				
		if type == 2:
			self.ammo += 3
			channel.queue(ammoSound)
			
class Asteroid(pygame.sprite.Sprite): # destroyable obstacles, does heavy damage if crashed into
	def __init__(self, size, target):
		
		pygame.sprite.Sprite.__init__(self)
		
		if size == 1:
			self.image = pygame.image.load('Sprites/Asteroid64px.png')
			self.size = 64
			self.rotation_speed = random.randint(-4,4)
			self.health = 200
		elif size == 2:
			self.image = pygame.image.load('Sprites/Asteroid128px.png')
			self.size = 128
			self.rotation_speed = random.randint(-3,3)
			self.health = 400
		elif size == 3:
			self.image = pygame.image.load('Sprites/Asteroid256px.png')
			self.size = 256
			self.rotation_speed = random.randint(-1,1)
			self.health = 800
		
		self.speed = random.randint(2,4)
		self.rotation = random.randint(0,360)
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		
		entry_side = random.randint(1,4)
		
		if entry_side == 1:
			self.x = -200
			self.y = random.randint(0,screenHeight)
			self.direction = random.randint(60,120)
		elif entry_side == 2:
			self.x = screenWidth + 200
			self.y = random.randint(0,screenHeight)
			self.direction = random.randint(240,300)
		elif entry_side == 3:
			self.x = random.randint(0,screenWidth)
			self.y = -200
			self.direction = random.randint(-30,30)
		elif entry_side == 4:
			self.x = random.randint(0,screenWidth)
			self.y = screenHeight + 200
			self.direction = random.randint(150,210)
		
		if target != None:
			self.angle = math.atan2(-(self.y - target.nexty), (self.x - target.nextx))
			self.direction = math.degrees(self.angle % (2 * math.pi)) - 90
		
		self.nextx, self.nexty = 0,0
		
	def update(self): # updates location
		
		self.rotation += self.rotation_speed
		rad = self.direction * math.pi/180
		
		self.x += self.speed*math.sin(rad)
		self.y += self.speed*math.cos(rad)
		self.nextx = self.x + self.speed*math.sin(rad)
		self.nexty = self.y + self.speed*math.cos(rad)
		self.render()
	
	def render(self): # renders onto screen
	
		scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
		rotated_image = pygame.transform.rotate(scaled_image, self.rotation)
		self.rect = rotated_image.get_rect()
		self.rect.center = self.x, self.y
		screen.blit(rotated_image, self.rect)
		
		self.mask = pygame.mask.from_surface(rotated_image)

	def edge(self): # finds if asteroid is offscreen
		
		if self.x < -210 or self.x > (screenWidth + 210) or self.y < -210 or self.y > (screenHeight + 210):
			return True

class Alien(pygame.sprite.Sprite): # enemies, 4 different variations
	def __init__(self, attack_pattern):
		
		pygame.sprite.Sprite.__init__(self)
		self.attack_pattern = attack_pattern
		
		if self.attack_pattern == 1: # standard, follows player and shoots
			self.image = pygame.image.load('Sprites/AlienBlue64px.png')
			self.health = 100
			self.speed = random.uniform(1,2)
			self.bullet_speed = 4
			self.chase_distance = random.randint(200,350) 
			self.cooldown = 1500
			 
		elif self.attack_pattern == 2: # chaser, weak ranged attack but fast movement and high hp
			self.image = pygame.image.load('Sprites/AlienRed64px.png')
			self.health = 200
			self.speed = random.uniform(3,4)
			self.bullet_speed = 4
			self.chase_distance = 0
			self.cooldown = 2000
			
		elif self.attack_pattern == 3: # sniper, fast shooting but low hp
			self.image = pygame.image.load('Sprites/AlienBlack64px.png')
			self.health = 60
			self.speed = random.uniform(1,2)
			self.bullet_speed = 10
			self.chase_distance = random.randint(400,600) 
			self.cooldown = 1000
			
		elif self.attack_pattern == 4: # rapid fire
			self.image = pygame.image.load('Sprites/AlienGreen64px.png')
			self.health = 100
			self.speed = random.uniform(2,3)
			self.bullet_speed = 4
			self.chase_distance = 0
			self.cooldown = 700
		
		self.size = 64
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.nextx, self.nexty = 0,0
		self.last = pygame.time.get_ticks() 
		self.entry = False
		
		entry_side = random.randint(1,4)
		
		if entry_side == 1:
			self.x = -200
			self.y = random.randint(0,screenHeight)
			self.direction = random.randint(60,120)
		elif entry_side == 2:
			self.x = screenWidth + 200
			self.y = random.randint(0,screenHeight)
			self.direction = random.randint(240,300)
		elif entry_side == 3:
			self.x = random.randint(0,screenWidth)
			self.y = -200
			self.direction = random.randint(-30,30)
		elif entry_side == 4:
			self.x = random.randint(0,screenWidth)
			self.y = screenHeight + 200
			self.direction = random.randint(150,210)
		
	def update(self, target): # updates movement depending on attack pattern
		
		self.angle = math.atan2(-(self.nexty - target.nexty), (self.nextx - target.nextx))
		self.direction = math.degrees(self.angle % (2 * math.pi)) - 90
		
		if self.attack_pattern == 1: # standard
			if distance(self,target) < self.chase_distance:
				rad = (self.direction + 90) * math.pi/180
			else:
				rad = self.direction * math.pi/180
		
		elif self.attack_pattern == 2: # chaser
			rad = self.direction * math.pi/180
		
		elif self.attack_pattern == 3: # sniper
			if distance(self,target) < self.chase_distance:
				rad = (self.direction - 90) * math.pi/180
			else:
				rad = self.direction * math.pi/180
			
		elif self.attack_pattern == 4: # rapid fire
			rad = self.direction * math.pi/180
		
		self.x += self.speed*math.sin(rad)
		self.y += self.speed*math.cos(rad)
		
		self.nextx = self.x + self.speed*math.sin(rad)
		self.nexty = self.y + self.speed*math.cos(rad)
		self.render()
	
	def render(self): # renders onto screen
	
		scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
		self.rect = scaled_image.get_rect()
		self.rect.center = self.x, self.y
		screen.blit(scaled_image, self.rect)
		
		self.mask = pygame.mask.from_surface(scaled_image)
		
	def edge(self): # detects if alien has entered the screen
		
		if self.x > 15 and self.x < (screenWidth - 15) and self.y > 15 and self.y < (screenHeight - 15):
			self.entry = True
		
	def shoot(self, target): # shoots based on attack pattern
		
		if self.entry == True:
			
			if self.attack_pattern == 3: # sniper leads shots
				travel_time = distance(self,target) / self.bullet_speed
				target_rad = target.direction * math.pi/180
		
				target_x = target.x + travel_time * target.speed * math.sin(target_rad)
				target_y = target.y + travel_time * target.speed * math.cos(target_rad)
		
				attack_angle = math.atan2(-(self.nexty - target_y), (self.nextx - target_x))
				attack_direction = math.degrees(attack_angle % (2 * math.pi)) - 90
			else: # the rest attack directly towards player
				attack_direction = self.direction
		
			now = pygame.time.get_ticks()
			if now - self.last >= self.cooldown:
				self.last = now
				AlienShots.add(Bullet(Alien, 0, self.speed, self.bullet_speed, attack_direction, self.x, self.y))
		
				rng = random.randint(1,3)
				channel = pygame.mixer.find_channel(True)
			
				if rng == 1:
					channel.queue(alienShootingSound1)
				elif rng == 2:
					channel.queue(alienShootingSound2)
				elif rng == 3:
					channel.queue(alienShootingSound3)
		
class Bullet(pygame.sprite.Sprite): # projectiles
	def __init__(self, shooter, projectile, shooter_speed, speed, direction, x, y):
		
		pygame.sprite.Sprite.__init__(self)
		
		if shooter == Player:
			if projectile == 1: # player gun
				self.image = pygame.image.load('Sprites/Orb16px.png')
				self.size = 8
			if projectile == 2: # player missile
				self.image = pygame.image.load('Sprites/Missile24px.png')
				self.size = 24
		else: # alien gun
			self.image = pygame.image.load('Sprites/Orb16px.png')
			self.size = 16

		self.x = x
		self.y = y
		self.direction = direction
		self.shooter = shooter
		self.speed = speed + shooter_speed
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		
	def update(self): # updates movement
		
		rad = self.direction * math.pi/180
	
		self.x += self.speed*math.sin(rad)
		self.y += self.speed*math.cos(rad)
		
		self.nextx = self.x + self.speed*math.sin(rad)
		self.nexty = self.y + self.speed*math.cos(rad)
		self.render()
		
	def render(self): # renders onto screen
		
		scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
		rotated_image = pygame.transform.rotate(scaled_image, self.direction)
		self.rect = rotated_image.get_rect()
		self.rect.center = self.x, self.y
		screen.blit(rotated_image, self.rect)
		
		self.mask = pygame.mask.from_surface(rotated_image)
		
	def edge(self): # detects if offscreen
		
		if self.x < -210 or self.x > (screenWidth + 210) or self.y < -210 or self.y > (screenHeight + 210):
			return True

class Explosion(pygame.sprite.Sprite): # boom animation
	def __init__(self, x, y, size):
	
		pygame.sprite.Sprite.__init__(self)
	
		self.x = x
		self.y = y
		self.size = size
		self.frame = 3
	
	def update(self): # plays through frames
		
		if self.frame >= 27:
			self.kill()
	
		self.image = Explosion_IMGS[self.frame/3]
		self.frame += 1
		self.render()
		
	def render(self): # renders onto screen
		
		scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
		self.rect = scaled_image.get_rect()
		self.rect.center = self.x, self.y
		screen.blit(scaled_image, self.rect)

class Powerup(pygame.sprite.Sprite): # dropped by aliens, can be heal or missile ammo
	def __init__(self, speed, direction, x, y, type):
		
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.speed = speed / 2
		self.direction = direction
		self.type = type
		
		if self.type == 1: # hp restore
			self.image = pygame.image.load('Sprites/Health24px.png')
			self.size = 24
		if self.type == 2: # missile ammo
			self.image = pygame.image.load('Sprites/Ammo48px.png')
			self.size = 24
			
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		
	def update(self): # updates movement
		
		rad = self.direction * math.pi/180
			
		self.x += self.speed*math.sin(rad)
		self.y += self.speed*math.cos(rad)
		self.render()
	
	def render(self): # renders onto screen
	
		scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
		self.rect = scaled_image.get_rect()
		self.rect.center = self.x, self.y
		screen.blit(scaled_image, self.rect)
		
		self.mask = pygame.mask.from_surface(scaled_image)
		
	def edge(self): # detects if offscreen
		
		if self.x < -210 or self.x > (screenWidth + 210) or self.y < -210 or self.y > (screenHeight + 210):
			return True

# important variables

runGame = False
runControls = False
paused = False
timeSurvived = 0
timePaused = 0

Player1 = Player()
Asteroids = pygame.sprite.Group()
Aliens = pygame.sprite.Group()
AlienShots = pygame.sprite.Group()
PlayerShots = pygame.sprite.Group()
PlayerMissiles = pygame.sprite.Group()
Explosions = pygame.sprite.Group()
Powerups = pygame.sprite.Group()

# main game loops

def game_intro(): # introductory screen
	
	global runGame
	
	while not runGame:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		
		screen.blit(Background,(0,0))
		
		title('GALACTIC DEFENDER', largeFont, white, 0, -150)
		button('START', screenWidthCentre -200, screenHeightCentre - 30, 400, 80, darkgray, lightgray, medFont, white, 'play')
		button('HELP', screenWidthCentre - 200, screenHeightCentre + 70, 400, 80, darkgray, lightgray, medFont, white, 'controls')
		button('QUIT', screenWidthCentre - 200, screenHeightCentre + 170, 400, 80, darkgray, lightgray, medFont, white, 'quit')
		
		#label('PROGRAMMING 12', tinyFont, white, screenWidth - 150, screenHeight - 60)
		#label('FINAL PROJECT', tinyFont, white, screenWidth - 150, screenHeight - 40)
		#label('BY JORDAN FANG', tinyFont, white, screenWidth - 150, screenHeight - 20)
		
		pygame.display.update()
		clock.tick(60)

def controls(): # controls and help screen
	
	global runControls
	runControls = True
	
	while runControls:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				runControls = False
		
		screen.blit(Background,(0,0))
		
		global paused
		if paused == True:
			for Powerup in Powerups:
				Powerup.render()
			for Asteroid in Asteroids:
				Asteroid.render()
			for Alien in Aliens:
				Alien.render()
			for Bullet in AlienShots:
				Bullet.render()
			for Bullet in PlayerShots:
				Bullet.render()
			for Bullet in PlayerMissiles:
				Bullet.render()
			for Explosion in Explosions:
				Explosion.render()
			
			Player1.render()
			healthbar(Player1.health, 10, 20)
			label('MISSILES: ' + str(Player1.ammo), smallFont, white, 10, 70)
			label('TIME: ' + timeSurvived, smallFont, white, screenWidth - 210, 20)
			
			white_screen = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
			white_screen.fill((200, 200, 200, 100))  
			screen.blit(white_screen, (0,0))
		
		pygame.draw.rect(screen, darkgray, (screenWidthCentre - 650, screenHeightCentre - 230, 600, 450))
		title('CONTROLS:', medFont, white, -350, -150)
		title('DIRECTION: MOUSE', smallFont, white, -350, -50)
		title('MOVEMENT: W/S KEYS', smallFont, white, -350, 0)
		title('FIRE GUNS: HOLD LEFT CLICK', smallFont, white, -350, 50)
		title('FIRE MISSILES: RIGHT CLICK', smallFont, white, -350, 100)
		title('PAUSE GAME: ESC', smallFont, white, -350, 150)
		
		pygame.draw.rect(screen, darkgray, (screenWidthCentre + 50, screenHeightCentre - 230, 600, 450))
		title('TIPS:', medFont, white, 350, -150)
		title('GUNS HAVE INFINITE AMMO', smallFont, white, 350, -50)
		title('USE MISSILES ON TOUGH ENEMIES', smallFont, white, 350, 0)
		title('ASTEROIDS CAN BE GOOD COVER', smallFont, white, 350, 50)
		title("DON'T CRASH INTO THINGS", smallFont, white, 350, 100)
		
		button('BACK', screenWidthCentre - 200, screenHeightCentre + 270, 400, 80, darkgray, lightgray, medFont, white, 'back')
		
		pygame.display.update()
		clock.tick(60)

def pause_game(): # pause screen
	
	global runGame
	global paused
	global timePaused
	runGame = False
	paused = True
	pygame.mouse.set_visible(True)
	start_time = pygame.time.get_ticks() - timePaused * 1000
	
	while not runGame:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				runGame = True
				paused = False
				pygame.mouse.set_visible(False)
	
		timePaused = (pygame.time.get_ticks() - start_time) / 1000
		
		screen.blit(Background,(0,0))
		
		for Powerup in Powerups:
			Powerup.render()
		for Asteroid in Asteroids:
			Asteroid.render()
		for Alien in Aliens:
			Alien.render()
		for Bullet in AlienShots:
			Bullet.render()
		for Bullet in PlayerShots:
			Bullet.render()
		for Bullet in PlayerMissiles:
			Bullet.render()
		for Explosion in Explosions:
			Explosion.render()
		
		Player1.render()
		healthbar(Player1.health, 10, 20)
		label('MISSILES: ' + str(Player1.ammo), smallFont, white, 10, 70)
		label('TIME: ' + timeSurvived, smallFont, white, screenWidth - 210, 20)
		
		white_screen = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
		white_screen.fill((200, 200, 200, 100))  
		screen.blit(white_screen, (0,0))
		
		title('GALACTIC DEFENDER', largeFont, black, 0, -150)
		button('RESUME', screenWidthCentre -200, screenHeightCentre - 30, 400, 80, darkgray, lightgray, medFont, white, 'resume')
		button('HELP', screenWidthCentre - 200, screenHeightCentre + 70, 400, 80, darkgray, lightgray, medFont, white, 'controls')
		button('QUIT', screenWidthCentre - 200, screenHeightCentre + 170, 400, 80, darkgray, lightgray, medFont, white, 'quit')
		
		pygame.display.update()
		clock.tick(60)

def game_over(): # game over animation and final screen

	global runGame
	runGame = False
	pygame.mouse.set_visible(True)
	
	explosion_sound("large")
	Explosions.add(Explosion(Player1.x, Player1.y, 800))
	Player1.image = pygame.image.load('Sprites/Blank.png')
	
	pygame.mixer.music.stop()
	explosionSound1.set_volume(0)
	explosionSound2.set_volume(0)
	explosionSound3.set_volume(0)
	explosionSound4.set_volume(0)
	explosionSoundSmall.set_volume(0)
	alienShootingSound1.set_volume(0)
	alienShootingSound2.set_volume(0)
	alienShootingSound3.set_volume(0)
	gunSound.set_volume(0)
	
	darkness = 0
	black_screen = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
	
	while not runGame:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		
		Player1.speed = 0
		screen.blit(Background,(0,0))
		
		update_projectiles()
		update_asteroids()
		update_aliens()
		Player1.update()
		update_interactions()
		
		black_screen.fill((0, 0, 0, darkness))  
		screen.blit(black_screen, (0,0))
		
		if darkness < 255:
			darkness += 1
		else:
			title('GAME OVER', largeFont, white, 0, -150)
			title('YOU SURVIVED: ' + timeSurvived, medFont, white, 0, 0)	
			button('RESTART', screenWidthCentre - 410, screenHeightCentre + 220, 400, 80, darkgray, lightgray, medFont, white, 'restart')
			button('EXIT', screenWidthCentre + 10, screenHeightCentre + 220, 400, 80, darkgray, lightgray, medFont, white, 'quit')
		
		if darkness == 200:
			pygame.mixer.music.load('Music/Music2.ogg')
			pygame.mixer.music.play(-1)		
			
		pygame.display.update()
		clock.tick(60)

def game_loop(): # main game loop
	
	global runGame
	runGame = True
	start_time = pygame.time.get_ticks()
	asteroid_timer = 1000
	alien_timer = 2000
	last_moved = 0
	pygame.mouse.set_visible(False)
	displayFPS = False
	
	while runGame:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pause_game()
			elif event.type == pygame.KEYDOWN: # cheat codes for enemy spawns
				if event.key == pygame.K_1:
					Aliens.add(Alien(1))
				elif event.key == pygame.K_2:
					Aliens.add(Alien(2))
				elif event.key == pygame.K_3:
					Aliens.add(Alien(3))
				elif event.key == pygame.K_4:
					Aliens.add(Alien(4))
				elif event.key == pygame.K_5: 
					Asteroids.add(Asteroid(random.randint(1,3), None))
				elif event.key == pygame.K_0: 
					if displayFPS == False:
						displayFPS = True
					else:
						displayFPS = False
	
		timer = (pygame.time.get_ticks() - start_time) / 1000
		global timeSurvived
		global timePaused
		timeSurvived = str(datetime.timedelta(seconds=(timer-timePaused)))
		
		# enemy spawn times
		
		if timer < 30:
			asteroid_spawn_cooldown = 3500
			alien_spawn_cooldown = 5000
		elif timer < 60:
			asteroid_spawn_cooldown = 3500
			alien_spawn_cooldown = 4500
		elif timer < 120:
			asteroid_spawn_cooldown = 3000
			alien_spawn_cooldown = 4000
		elif timer < 180:
			asteroid_spawn_cooldown = 3000
			alien_spawn_cooldown = 3500
		elif timer < 240:
			asteroid_spawn_cooldown = 2500
			alien_spawn_cooldown = 3000
		elif timer < 300:
			asteroid_spawn_cooldown = 2500
			alien_spawn_cooldown = 2500
		elif timer < 360:
			asteroid_spawn_cooldown = 2000
			alien_spawn_cooldown = 2000
		elif timer < 420:
			asteroid_spawn_cooldown = 2000
			alien_spawn_cooldown = 1500
		else:
			asteroid_spawn_cooldown = 2000
			alien_spawn_cooldown = 1250
		
		# enemy spawn clock
		
		now = pygame.time.get_ticks()
		
		if now - asteroid_timer >= asteroid_spawn_cooldown:
			asteroid_timer = now
			Asteroids.add(Asteroid(random.randint(1,3), None))
		
		if now - alien_timer >= alien_spawn_cooldown:
			alien_timer = now 
			if timer < 30:
				Aliens.add(Alien(1))
			else:
				Aliens.add(Alien(random.randint(1,4)))
		
		# spawns asteroids if player is camping for too long
		
		if Player1.speed != 0: 
			last_moved = now
			
		if now - last_moved >= 5000:
			Asteroids.add(Asteroid(random.randint(2,3), Player1))
			last_moved = now
		
		# updates everything
		
		screen.blit(Background,(0,0))
		update_projectiles()
		update_powerups()
		update_asteroids()
		update_aliens()
		update_interactions()
		update_player()
		
		healthbar(Player1.health, 10, 20)
		label('MISSILES: ' + str(Player1.ammo), smallFont, white, 10, 70)
		label('TIME: ' + timeSurvived, smallFont, white, screenWidth - 210, 20)
		
		if displayFPS == True:
			label('FPS: ' + str(int(clock.get_fps())), smallFont, white, screenWidth - 120, 50)
		
		pygame.display.update()
		clock.tick(60)

game_intro()
pygame.quit()
	
	
	
	
	
	
	
	
