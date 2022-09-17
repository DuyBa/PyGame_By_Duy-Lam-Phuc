import pygame

class Fighter():
	def __init__(self, x, y):

		#x, y la vi tri dung trong khung hinh, cai nay se luon thay doi, con 80, 180 la chieu rong chieu cao cua nhan vat
		#x tinh 0 tu trai sang
		#y tinh 0 tu tren xuong, maybe :v
		#thang nay la tu goi hinh chu nhat,con phai tao ham ve nua
		self.rect= pygame.Rect((x, y, 80, 180))

	#tao ra ham di chuyen cho nhan vat
	def move(self):
		SPEED= 10
		dx= 0
		dy= 0 

		#get keypresses (lay nhap tu ban phim, vi du nhu w, a, s, d)
		key= pygame.key.get_pressed()


		#movement (thang nay se dinh huong di chuyen)
		if key[pygame.K_a]:
			dx= - SPEED 
		if key[pygame.K_d]:
			dx= SPEED 

		#update position (cap nhat vi tri cua nhan vat)
		self.rect.x+= dx
		self.rect.y+= dy

	#day la ham ve ra hinh chu nhat
	def draw(self, surface):
		pygame.draw.rect(surface, (255, 0, 0), self.rect)