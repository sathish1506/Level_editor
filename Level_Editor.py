import pygame
import csv
import pickle


pygame.init()


clock = pygame.time.Clock()
FPS = 60 

#game window
Screen_width = 800
Screen_height = 640
Lower_margin = 70
Side_margin = 300

screen = pygame.display.set_mode((Screen_width + Side_margin , Screen_height + Lower_margin))
pygame.display.set_caption('Level Editor')

#define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = Screen_height // ROWS
TILE_TYPES = 21
level = 0
current_tile = 0 
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1



#load images 
pine1_img = pygame.image.load('Level/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('Level/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('Level/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('Level/Background/sky_cloud.png').convert_alpha()

#store tiles in a list 
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Level/Tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('Level/save_btn.png').convert_alpha()
load_img = pygame.image.load('Level/load_btn.png').convert_alpha()

#define colors
Green = (144, 201, 120)
White = (255, 255 ,255)
Red = (200, 25, 25)
Black = (0, 0, 0)
Maroon = (128, 0, 0)

#define font
font = pygame.font.SysFont('futura', 25)
font2 = pygame.font.SysFont('futura', 25)


#CREATE empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)
    
#create ground 
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1 ][tile] = 0
    
#function for outputting text onto screen 
def draw_text(text,font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))
    

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
                
#create function for drawing background
def draw_bg():
    screen.fill(Green)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img, ((x *width ) - scroll * 0.5, 0))
        screen.blit(mountain_img, ((x *width ) - scroll * 0.6, Screen_height - mountain_img.get_height()-300))
        screen.blit(pine1_img, ((x * width) - scroll * 0.8, Screen_height - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x *width ) - scroll * 0.9, Screen_height - pine2_img.get_height()))

#draw grid
def draw_grid():
    #vertical lines 
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, White, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, Screen_height))
    #horizontal lines 
    for c in range(ROWS + 1):
        pygame.draw.line(screen, White, (0, c * TILE_SIZE), (Screen_width, c * TILE_SIZE))

#function for drawing world tiles
def draw_world():
     for y, row in enumerate(world_data):
         for x, tile in enumerate(row):
             if tile>=0:
                 screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))                 
                 

#create buttons
save_button = Button(Screen_width // 2, Screen_height + Lower_margin - 50, save_img, 1)
load_button = Button(Screen_width // 2+ 200 , Screen_height + Lower_margin - 50, load_img, 1)

#make buttons list
button_list = []
button_col = 0
button_row = 0

for i in range(len(img_list)):
    tile_button = Button(Screen_width + (75 * button_col) + 50,75 * button_row + 50,img_list[i],1)
    
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

run = True
while run :
    
    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()
    
    draw_text(f'Level: {level}',font , Black, 10, Screen_height + Lower_margin - 61) #pos of the the level text
    draw_text(f'Press UP or DOWN to change level', font2, Maroon , 10, Screen_height + Lower_margin - 40) 
    
    
    #SAVE AND LOAD DATA 
    if save_button.draw(screen):
        #save level data
        with open(f'level{level}_data.csv', 'w', newline= '')as csvfile:
            writer = csv.writer(csvfile, delimiter =',') #delimiter for seprates the value using ,
            for row in world_data:
                writer.writerow(row) 
        #alternative pickle method
		#pickle_out = open(f'level{level}_data', 'wb')
		#pickle.dump(world_data, pickle_out)
		#pickle_out.close()        
        
    if load_button.draw(screen):
        #load in level data
        #reset scroll back to the start of te levl 
        scroll = 0
        #with open(f'level{level}_data.csv', newline= '')as csvfile:
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter =',')
            for x, row in enumerate(reader):
                for y , tile in enumerate(row):
                    world_data[x][y] = int(tile)
        #alternative pickle method
		#world_data = []
		#pickle_in = open(f'level{level}_data', 'rb')
		#world_data = pickle.load(pickle_in)
                
    
    #draw tile panel and tiles
    pygame.draw.rect(screen, Green, (Screen_width, 0, Side_margin, Screen_height)) 
    
    
    #choose a tile
    for i, button in enumerate(button_list):
        button.draw(screen)
        if button.clicked:
            current_tile = i
            
    #highlight the selected tile
    pygame.draw.rect(screen, Red, button_list[current_tile].rect, 3)
    
  
     #scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed 
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - Screen_width :
        scroll += 5 * scroll_speed
      
    #add new tile to the screen 
    #get mouse position 
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE
    
    #check that coordinates within the tile area
    if pos[0] < Screen_width and pos[1] < Screen_height:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:     #to create the tile 
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        
        if pygame.mouse.get_pressed()[2] == 1:   # to erase the tile  which have been created in world
            world_data[y][x] = -1
            
         
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
                
        #keyboard presses 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                 level += 1
            if event.key == pygame.K_DOWN and level > 0:
                 level -= 1     
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
        
        #keyboard release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1
    
    
    
    
    pygame.display.update()
            
pygame.quit()
