import pygame
pygame.init()

win = pygame.display.set_mode((500,500))

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.png')
char = pygame.image.load('standing.png')

pygame.display.set_caption('test')
win.blit(bg, (0,0))               #used to put images on window
pygame.display.update()

clock = pygame.time.Clock()

class player():
	def __init__(self ,x, y, height, width):
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.vel = 5
		self.isJump = False
		self.jumpCount = 10
		self.right = False
		self.left = False
		self.walkCount = 0
		self.standing = True
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)
		
	def redraw(self ,win):
		if self.walkCount + 1 >= 27:
			self.walkCount = 0
		if not(self.standing):
			if self.left:
				win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
			elif self.right:
				win.blit(walkRight[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
		else:
			if self.right:
				win.blit(walkRight[0], (self.x,self.y))
			else:
				win.blit(walkLeft[0], (self.x,self.y))
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)
		#pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
				
				
class projectile():
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y		
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 8 * facing
		
	def draw(self ,win):
		pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
	
	

class enemy():
	walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
	walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
	
	def __init__(self, x, y, width ,height ,end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.end = end
		self.walkCount = 0
		self.vel = 3
		self.path = [self.x, self.y]
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)
		
	def draw(self, win):
		self.move()
		if self.walkCount + 1 >= 33:
			self.walkCount = 0
			
		if self.vel > 0:
			win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
			self.walkCount += 1
		else:
			win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
			self.walkCount += 1		
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)
		#pygame.draw.rect(win ,(255,0,0), self.hitbox, 2)
	
	def move(self):
		if self.vel > 0:
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
		else:
			if self.x - self.vel > self.path[0]:
				self.x += self.vel
			else:
				self.vel =  self.vel * -1
	
	def hit(self):
		print('hit')
			
		
		
def redrawGameWin():
	win.blit(bg, (0,0))
	box.redraw(win)
	goblin.draw(win)
	for bullet in bullets:
		bullet.draw(win)
		
	pygame.display.update()


box = player(0, 350, 64, 64)	
goblin = enemy(100, 350, 64, 64, 450)

bullets = []
shootLoop = 0

run = True
while run :

	if shootLoop > 0:
		shootLoop += 1
	if shootLoop == 4:
		shootLoop = 0

	clock.tick(27)

	for event in pygame.event.get() :
		if event.type == pygame.QUIT:
			run = False
			
	for bullet in bullets:
		if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
			if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
				goblin.hit()
				bullets.pop(bullets.index(bullet))
		if bullet.x >= 0  and bullet.x <500:
			bullet.x += bullet.vel
		else:
			bullets.pop(bullets.index(bullet))
		
	keys = pygame.key.get_pressed()    #returns dictionary
	
	if keys[pygame.K_SPACE] and shootLoop == 0:
		if box.left:
			facing = -1
		else:
			facing = 1
		
		if len(bullets) < 5:		
			bullets.append(projectile(round(box.x + box.width//2), round(box.y + box.height//2), 6, (255,0,0), facing))
		
		shootLoop = 1
		
	
	if keys[pygame.K_RIGHT] and box.x < 500 - box.width - box.vel:
		box.x += box.vel
		box.right = True
		box.left = False
		box.standing = False
	elif keys[pygame.K_LEFT] and box.x > box.vel :
		box.x -= box.vel	
		box.right = False
		box.left = True
		box.standing = False
	else:
		box .standing = True
		box.walkCount = 0
		
	if not(box.isJump) :
		if keys[pygame.K_UP] :
			box.isJump = True
	else :
		if box.jumpCount >= -10:
			neg = 1
			if box.jumpCount < 0 :
				neg = -1
			box.y -= (box.jumpCount ** 2) * 0.5 * neg
			box.jumpCount -= 1
		else:
			box.isJump = False
			box.jumpCount = 10
		
		
	
	redrawGameWin()
			
pygame.quit()