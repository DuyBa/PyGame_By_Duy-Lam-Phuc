import pygame

class Fighter():
	def __init__(self, x, y):

		#x, y la vi tri dung trong khung hinh, cai nay se luon thay doi, con 80, 180 la chieu rong chieu cao cua nhan vat
		#x tinh 0 tu trai sang
		#y tinh 0 tu tren xuong, maybe :v
		#thang nay la tu goi hinh chu nhat,con phai tao ham ve nua
		self.rect= pygame.Rect((x, y, 80, 180))
		#thang nay de tinh toan xem nhay len cao bao nhieu :v
		self.vel_y= 0
		#thang nay giup kiem soat chi nhay 1 lan, ko bi cong don nhay vi vong lap
		self.jump= False

	#tao ra ham di chuyen cho nhan vat
	def move(self, screen_width, screen_height):
		SPEED= 10
		GRAVITY= 2
		dx= 0
		dy= 0 

		#get keypresses (lay nhap tu ban phim, vi du nhu w, a, s, d)
		key= pygame.key.get_pressed()


		#movement (thang nay se dinh huong di chuyen)
		if key[pygame.K_a]:
			dx= - SPEED 
		if key[pygame.K_d]:
			dx= SPEED
		#jump (nhay, nut w)
		if key[pygame.K_w] and self.jump== False:
			self.vel_y= -30
			self.jump= True

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


		#update position (cap nhat vi tri cua nhan vat)
		self.rect.x+= dx
		self.rect.y+= dy

	#day la ham ve ra hinh chu nhat
	def draw(self, surface):
		pygame.draw.rect(surface, (255, 0, 0), self.rect)