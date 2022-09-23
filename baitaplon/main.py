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

#define color
RED= (255, 0, 0)
YELLOW= (255, 255, 0) 
WHITE= (255, 255, 255)

#define game variables
intro_count= 3
last_count_update= pygame.time.get_ticks()

#define fighter variables
WARRIOR_SIZE= 162
WIZARD_SIZE= 250

WARRIOR_SCALE= 4
WIZARD_SCALE= 3

WARRIOR_OFFSET= [72, 56]
WIZARD_OFFSET= [112, 107]

WARRIOR_DATA= [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_DATA= [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load background image (chay phong nen)
bg_image= pygame.image.load("assets/Flat Night 2 BG/Flat Night 2 BG.png").convert_alpha()

#load spritesheets
warrior_sheet= pygame.image.load("assets/muontam/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet= pygame.image.load("assets/muontam/images/wizard/Sprites/wizard.png").convert_alpha()

#define number of steps in each animations
WARRIOR_ANIMATION_STEPS= [10, 8, 1, 7 ,7, 3, 7]
WIZARD_ANIMATION_STEPS= [8, 8, 1, 8, 8, 3, 7]

#define font
cont_font= pygame.font.Font("assets/muontam/fonts/turok.ttf", 80)

#funtion for drawing tect
def draw_text(text, font, text_col, x, y):
	img= font.render(text, True, text_col)
	screen.blit(img, (x, y))


#function for drawing background (thang bg_img chi la 1 bien khoi tao, chung ta phai tao ham de goi no, xong no se luu vao bo nho memory va ta se cho chay trong vong lap)
def draw_bg():
	#vi bg cua chung ta ko fit size nen chung ta se resize lai, ok
	scaled_bg= pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
	screen.blit(scaled_bg, (0, 0))

#function for drawing fight health bars
def draw_health_bar(health, x, y):
	ratio= health/  100
	pygame.draw.rect(screen, RED, (x, y, 400, 30))
	pygame.draw.rect(screen, YELLOW, (x, y, 400* ratio, 30))


#create 2 instance of fighters (chac chan se co 2 thang tren man hinh, nen ta tao 2 tk)
fighter_1 = Fighter(1, 200, 340, False, WARRIOR_DATA,warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Fighter(2, 700, 340, True, WIZARD_DATA,wizard_sheet, WIZARD_ANIMATION_STEPS)


#game loop (tao vong lap cho game, tat ca moi thu se dien ra tai day)
run= True
while run:

	clock.tick(FPS)

	#draw beackground (ve nen trong nay)
	draw_bg()

	#show health bars
	draw_health_bar(fighter_1.health, 20, 20)
	draw_health_bar(fighter_2.health, 580, 20)


	#update countdown
	if intro_count<= 0:
		#move fighters (goi thang nay ra de di chuyen)
		fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
		fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
	else:
		#display count timer
		draw_text(str(intro_count), cont_font, RED, SCREEN_WIDTH/ 2- 30, SCREEN_HEIGHT/ 2)
		#update count timer
		if(pygame.time.get_ticks()- last_count_update) >= 1000:
			intro_count-= 1
			last_count_update= pygame.time.get_ticks()
			#print(intro_count)



	#update fighters
	fighter_1.update()
	fighter_2.update()

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