import pygame

class Fighter():
	def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
		self.player= player
		#self.size= data[0]
		self.sizex= data[0][0]
		self.sizey= data[0][1]
		self.image_scale= data[1]
		self.offset= data[2]
		self.flip= flip
		self.animation_list= self.load_images(sprite_sheet, animation_steps)
		self.action= 0 #0: idle #1: run #2: jump #3: attack1 #4: attack2 #5:hit #6:death
		self.frame_index= 0
		self.image= self.animation_list[self.action][self.frame_index]
		self.update_time= pygame.time.get_ticks()
		#x, y la vi tri dung trong khung hinh, cai nay se luon thay doi, con 80, 180 la chieu rong chieu cao cua nhan vat
		#x tinh 0 tu trai sang
		#y tinh 0 tu tren xuong, maybe :v
		#thang nay la tu goi hinh chu nhat,con phai tao ham ve nua
		self.rect= pygame.Rect((x, y, 80, 180))
		#thang nay de tinh toan xem nhay len cao bao nhieu :v
		self.vel_y= 0
		self.running= False
		#thang nay giup kiem soat chi nhay 1 lan, ko bi cong don nhay vi vong lap
		self.jump= False
		self.attack_type= 0
		self.attack_cooldown= 0
		self.attack_sound= sound
		self.hit= False
		self.attacking= False
		self.alive= True
		self.health= 100
		
		
		
		
		
	def load_images(self, sprite_sheet, animation_steps):
		#extract images from sprtie_sheet
		animation_list= []
		for y, animation in enumerate(animation_steps):
			temp_img_list= []
			for x in range(animation):
				#temp_img= sprite_sheet.subsurface(x* self.size, y* self.size, self.size, self.size)
				temp_img= sprite_sheet.subsurface(x* self.sizex, y* self.sizey, self.sizex, self.sizey)
				temp_img_list.append(pygame.transform.scale(temp_img, (self.sizex* self.image_scale, self.sizey* self.image_scale)))	
			animation_list.append(temp_img_list)
		return animation_list			

	#tao ra ham di chuyen cho nhan vat
	def move(self, screen_width, screen_height, surface, target, round_over):
		SPEED= 10
		GRAVITY= 2
		dx= 0
		dy= 0 
		self.running= False
		self.attack_type= 0

		#get keypresses (lay nhap tu ban phim, vi du nhu w, a, s, d)
		key= pygame.key.get_pressed()

		#can only perform other actions if not currently attacking( chi di chuyen sang len xuong khi ma ko thuc hieen tan cong, mac du cai nay ko dung voi game ngoai doi :v)
		if self.attacking== False and self.alive== True and round_over== False:

			#check player 1 control:
			if self.player== 1:

				#movement (thang nay se dinh huong di chuyen)
				if key[pygame.K_a]:
					dx= - SPEED 
					self.running= True
				if key[pygame.K_d]:
					dx= SPEED
					self.running= True
				#jump (nhay, nut w)
				if key[pygame.K_w] and self.jump== False:
					self.vel_y= -30
					self.jump= True
				#attack
				if key[pygame.K_j] or key[pygame.K_k]:
					self.attack(target)
					#determine which kind of attack
					if key[pygame.K_j]:
						self.attack_type= 1
					if key[pygame.K_k]:
						self.attack_type= 2

			#check player 2 control:
			if self.player== 2:

				#movement (thang nay se dinh huong di chuyen)
				if key[pygame.K_LEFT]:
					dx= - SPEED 
					self.running= True
				if key[pygame.K_RIGHT]:
					dx= SPEED
					self.running= True
				#jump (nhay, nut w)
				if key[pygame.K_UP] and self.jump== False:
					self.vel_y= -30
					self.jump= True
				#attack
				if key[pygame.K_KP1] or key[pygame.K_KP2]:
					self.attack(target)
					#determine which kind of attack
					if key[pygame.K_KP1]:
						self.attack_type= 1
					if key[pygame.K_KP2]:
						self.attack_type= 2

		#apply gravity (them trong luc vao cho nhan vat, ban chat la neu chi co cai dong + them chieu y cho nhan vat, theo vong lap no se len mai neu ko dc dung, them dong trong luc vao thi no vua len vua xuong, tieo theo se xu li tiep)
		self.vel_y+= GRAVITY #thang di xuong nay thi always
		dy+= self.vel_y #thang di len nay thi chi khi nao bam W

		#ensure players are on screeen( thang nay se giup ta ghim 2 thang trong 1 man hinh maf ko bi di chuyen ra khoi man hinh) 
		if self.rect.left+ dx< 0:
			dx= - self.rect.left
		if self.rect.right+ dx> screen_width:
			dx= screen_width- self.rect.right
		if self.rect.bottom+ dy> screen_height- 80:
			self.vel_y= 0
			dy= screen_height- 80- self.rect.bottom
			self.jump= False

		#ensure players face each other
		if target.rect.centerx> self.rect.centerx:
			self.flip= False
		else: self.flip= True

		#apply attack cooldown
		if self.attack_cooldown> 0:
			self.attack_cooldown-= 1

		#update position (cap nhat vi tri cua nhan vat)
		self.rect.x+= dx
		self.rect.y+= dy

	#handle animation updates
	def update(self):

		#check what action the player is performing
		if self.health== 0:
			self.health= 0
			self.alive= False
			self.update_action(6)
		elif self.hit== True:
			self.update_action(5)
		elif self.attacking== True:
			if self.attack_type== 1:
				self.update_action(3)
			elif self.attack_type== 2:
				self.update_action(4)
		elif self.jump== True:
			self.update_action(2)
		elif self.running== True:
			self.update_action(1)
		else:
			self.update_action(0)

		animation_cooldown= 50
		#update image
		self.image= self.animation_list[self.action][self.frame_index]
		#check if enoygh time has passed since the last update
		if pygame.time.get_ticks()- self.update_time> animation_cooldown:
			self.frame_index+= 1
			self.update_time= pygame.time.get_ticks()
		#check if the animation has finished
		if self.frame_index >= len(self.animation_list[self.action]):
			#if the player is dead then and the animation
			if self.alive== False:
				self.frame_index= len(self.animation_list[self.action])- 1
			else:
				
				self.frame_index= 0
				#check if attack was executed
				if self.action== 3 or self.action== 4:
					self.attacking= False
					self.attack_cooldown= 20
				#cjecl if damage was taken
				if self.action== 5:
					self.hit= False
					#if the player was in the middle of an attack, then the attack is stopped
					self.attacking= False
					self.attack_cooldown= 20

	def attack(self, target):
		if self.attack_cooldown== 0:
			self.attacking= True
			self.attack_sound.play()
			attacking_rect= pygame.Rect(self.rect.centerx- (2* self.rect.width* self.flip), self.rect.y, self.rect.width* 2, self.rect.height)
			if attacking_rect.colliderect(target.rect):
				target.health-= 10
				target.hit= True
			#pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

	def update_action(self, new_action):
		#check if the new action is differnt to the previous one
		if new_action!= self.action:
			self.action= new_action
			#update the animation
			self.frame_index= 0
			self.update_time= pygame.time.get_ticks()

	#day la ham ve ra hinh chu nhat
	def draw(self, surface):
		img= pygame.transform.flip(self.image, self.flip, False)
		#pygame.draw.rect(surface, (255, 0, 0), self.rect)
		surface.blit(img, (self.rect.x- (self.offset[0]* self.image_scale), self.rect.y- (self.offset[1]* self.image_scale)))
