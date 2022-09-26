import pygame
from fighter import Fighter
from pygame import mixer

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
intro_count= 0
last_count_update= pygame.time.get_ticks()
score= [0, 0] #player score [p1, p2]
round_over= False
ROUND_OVER_COOLDOWN= 2000

#define fighter variables
# WARRIOR_SIZE= [162, 162] #old
# WIZARD_SIZE= [250, 250]  #old

WARRIOR_SIZE= [64, 44]  #new
WIZARD_SIZE= [231, 190]	  #new

# WARRIOR_SCALE= 4
# WIZARD_SCALE= 3
WARRIOR_SCALE= 4.9
WIZARD_SCALE= 2.3

# WARRIOR_OFFSET= [72, 56]
# WIZARD_OFFSET= [112, 107]
WARRIOR_OFFSET= [15, 7]
WIZARD_OFFSET= [112, 63]

WARRIOR_DATA= [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_DATA= [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load music and sound
pygame.mixer.music.load("assets/audio/lop13.mp3")
pygame.mixer.music.set_volume(0) #20
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx= pygame.mixer.Sound("assets/muontam/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx= pygame.mixer.Sound("assets/muontam/audio/magic.wav")
magic_fx.set_volume(0.75)



#load background image (chay phong nen)
#bg_image= pygame.image.load("assets/Flat Night 2 BG/Flat Night 2 BG.png").convert_alpha() old
bg_image= pygame.image.load("assets/Background/Demo.png").convert_alpha()

#load spritesheets
# warrior_sheet= pygame.image.load("assets/muontam/images/warrior/Sprites/warrior.png").convert_alpha() old
# wizard_sheet= pygame.image.load("assets/muontam/images/wizard/Sprites/wizard.png").convert_alpha() old
warrior_sheet= pygame.image.load("assets/Warrior-V1.3/aaa.png").convert_alpha() 
wizard_sheet= pygame.image.load("assets/Wizard Pack/aa.png").convert_alpha() 

#load victory image
victory_img= pygame.image.load("assets/muontam/images/icons/victory.png").convert_alpha()

#define number of steps in each animations
# WARRIOR_ANIMATION_STEPS= [10, 8, 1, 7 ,7, 3, 7] old
# WIZARD_ANIMATION_STEPS= [8, 8, 1, 8, 8, 3, 7]	old
WARRIOR_ANIMATION_STEPS= [6, 8, 3, 12 ,10, 4, 10]
WIZARD_ANIMATION_STEPS= [6, 8, 2, 8, 8, 4, 7]	

#define font
count_font= pygame.font.Font("assets/muontam/fonts/turok.ttf", 80)
score_font= pygame.font.Font("assets/muontam/fonts/turok.ttf", 30)

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
fighter_1 = Fighter(1, 200, 340, False, WARRIOR_DATA,warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 340, True, WIZARD_DATA,wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


#game loop (tao vong lap cho game, tat ca moi thu se dien ra tai day)
run= True
while run:

	clock.tick(FPS)

	#draw beackground (ve nen trong nay)
	draw_bg()

	#show health bars
	draw_health_bar(fighter_1.health, 20, 20)
	draw_health_bar(fighter_2.health, 580, 20)
	draw_text("P1: "+ str(score[0]), score_font, RED, 20, 60)
	draw_text("P2: "+ str(score[1]), score_font, RED, 580, 60)

	#update countdown
	if intro_count<= 0:
		#move fighters (goi thang nay ra de di chuyen)
		fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
		fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
	else:
		#display count timer
		draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH/ 2- 30, SCREEN_HEIGHT/ 2)
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


	#check for player defeated
	if round_over== False:
		if fighter_1.alive== False:
			score[1]+= 1
			round_over= True
			round_over_time= pygame.time.get_ticks()
		elif fighter_2.alive== False:
			score[0]+= 1
			round_over= True
			round_over_time= pygame.time.get_ticks()
	else:
		#display victory img
		screen.blit(victory_img, (360, 150))
		if pygame.time.get_ticks()- round_over_time> ROUND_OVER_COOLDOWN:
			round_over= False
			intro_count= 3
			#create 2 instance of fighters (chac chan se co 2 thang tren man hinh, nen ta tao 2 tk)
			fighter_1 = Fighter(1, 200, 340, False, WARRIOR_DATA,warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
			fighter_2 = Fighter(2, 700, 340, True, WIZARD_DATA,wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

	#event handler (xu li de thoat game, ko de cho vong lap vo tan)
	for event in pygame.event.get():
		if event.type== pygame.QUIT:
			run= False

	#update display(nom na la trong vong loop co rat nhieu thay doi, sau moi vong lap, ta phai cap nhat nen lai ngay lap tuc)
	pygame.display.update()


#exit pygame (thoat khoi tat ca)
pygame.quit()