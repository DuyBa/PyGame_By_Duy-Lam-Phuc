import pygame
from fighter import Fighter

pygame.init()

# create game window (tạo khung cho game)
SCREEN_WIDTH= 1000
SCREEN_HEIGHT= 600

screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("countervailing game")

#set framerate (vi fps qua cao, no di chuyen nhanh va muot, nen theo li ma noi, ta lai phari giam FPS xuong, dm di nguoc lai voi tu nhien :v)
clock= pygame.time.Clock()
FPS= 60

#load background image (chay phong nen)
bg_image= pygame.image.load("assets/Flat Night 2 BG/Flat Night 2 BG.png").convert_alpha()

#function for drawing background (thang bg_img chi la 1 bien khoi tao, chung ta phai tao ham de goi no, xong no se luu vao bo nho memory va ta se cho chay trong vong lap)
def draw_bg():
	#vi bg cua chung ta ko fit size nen chung ta se resize lai, ok
	scaled_bg= pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
	screen.blit(scaled_bg, (0, 0))

#create 2 instance of fighters (chac chan se co 2 thang tren man hinh, nen ta tao 2 tk)
fighter_1 = Fighter(200, 340)
fighter_2 = Fighter(700, 340)


#game loop (tao vong lap cho game, tat ca moi thu se dien ra tai day)
run= True
while run:

	clock.tick(FPS)

	#draw beackground (ve nen trong nay)
	draw_bg()

	#move fighters (goi thang nay ra de di chuyen)
	fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT)
	#fighter_2.move()

	#draw fighters (ve 2 thang o day)
	fighter_1.draw(screen)
	fighter_2.draw(screen)


	#event handler (xu li de thoat game, ko de cho vong lap vo tan)
	for event in pygame.event.get():
		if event.type== pygame.QUIT:
			run= False

	#update display(nom na la trong vong loop co rat nhieu thay doi, sau moi vong lap, ta phai cap nhat nen lai ngay lap tuc)
	pygame.display.update()


#exit pygame (thoat khoi tat ca)
pygame.quit()