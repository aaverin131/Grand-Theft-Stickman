'''
MADE BY ALEXANDER AVERIN
COPYRIGHT LAW ETC. ETC.
TO RUN THIS GAME PROPERTLY PLEASE INSTALL PYGAME, OS AND SYS USING PIP
'''


from gameclass1 import * #imports the classes from gameclass.py
#import pygame


game = World("Grand Theft Stickman") #initialises the game
screen = game.InitWindow() #creates the game window
s_width = game.window_stats()[0] #gets the width of the game window
s_height = game.window_stats()[1] #gets the height of the game window

pygame.mixer.init() #initialises sound for the game (playing songs etc.)

#2 lines of code below set the icon for the game(top left corner)
#it uses os.path.join to navigate to the file that is in a folder and it uses convert_alpha() to optimise the image so it loads faster and the game makes more FPS. Applicable to all the images used.
img = pygame.image.load(os.path.join("Assets","icon2.png")).convert_alpha()
# Set image as icon 
pygame.display.set_icon(img) 

movement = Movement()#initialises the movement for the player
filesave = FileSave()

stickmaninit = Image("Assets\\stickman")#gets the set of the images for the stickman located at assets/stickman 
print(stickmaninit)
stickman = stickmaninit.get_im('stickman_still2') #sets the starting image of the player once the game starts
stickman_rect = stickman.get_rect() #gets it rect to make it able to interact with another objects
playerxy = [300,100] #starting position

#4 lines of code below are for the shooting part of the game. 
#It gets the image of the head of the stickman to be able to look 
#where he aims, and it also loads the body without the hands to make it 
#look more realistic when he interact with the weapon
stickmanheadinit = Image() 
stickmanhead = stickmanheadinit.load("Assets\\stickman\\weapon","head.png").convert_alpha()
stickmanweaponinit = Image("Assets\\stickman\\weapon")
stickmanweapon = stickmanweaponinit.get_im('stickman_weapon_still')

stickmandanceinit = Image("Assets\\stickman\\fortnite dance") #gets the set of the images for the dance

ak47 = 1


#3 lines below are basically the same as for stickman but this time for background. 
#Main difference is that it loads only one image since no animation needed
backgroundinit = Image()
background = backgroundinit.load("Assets\\background","mapbg.png").convert_alpha()
background_rect = background.get_rect()
print(background_rect, stickman_rect)

#4 lines below are the same as for background but this time is for the bank
bankinit = Image()
bank = bankinit.load("Assets\\bank","bank2.png").convert_alpha()
#bank = bankinit.resize((bankinit.size()[0]*2,bankinit.size()[1]*2)).convert_alpha()
bankinsideinit = Image()
bankinside = bankinsideinit.load("Assets\\bank","bankinside.png").convert_alpha()


#4 lines below are the same as bank, but this time for the gun shop
gunshopinit = Image()
gunshop = gunshopinit.load("Assets\\gunshop","gun_shop.png").convert_alpha()
gunshopinsideinit = Image()
gunshopinside = gunshopinsideinit.load("Assets\\gunshop","gunshopinside.png").convert_alpha()

#2 lines below are the same as for the bank but now it's for playground obj.
#it also doesn't use the rect line because it doesn't need to interact with the player
playgroundinit = Image()
playground = playgroundinit.load("Assets\\background","playground2.png").convert_alpha()

#2 lines below are the same as for the playground but now it's for the forest obj.
forestinit = Image()
forest = forestinit.load("Assets\\background","forest2.png").convert_alpha()

#4 lines below are.. you get the idea
houseinit = Image()
house = houseinit.load("Assets\\house","hous.png").convert_alpha()
houseinsideinit = Image()
houseinside = houseinsideinit.load("Assets\\house","housinside.png").convert_alpha()


#loads the button for interaction in the game(for doors, picking up the items, etc.)
ebuttoninit = Image()
ebutton = ebuttoninit.load("Assets\\gui","ebutton.png").convert_alpha()

#loads the bar with the slots for the items and also the frame so highlight selected item
toolbarinit = Image()
toolbar = toolbarinit.load("Assets\\gui","toolbar.png").convert_alpha()
toolbarframeinit = Image()
toolbarframe = toolbarframeinit.load("Assets\\gui","toolbarframe.png").convert_alpha()

#loads save list
savelistpnginit = Image()
savelistpng = savelistpnginit.load("Assets\\gui\\saveoption","savelistempty.png")
saveslotpnginit = Image()
saveslotpng = saveslotpnginit.load("Assets\\gui\\saveoption","saveslot.png")
savebuttonpnginit = Image()
savebuttonpng = savebuttonpnginit.load("Assets\\gui\\saveoption","savebutton.png")

#loads first weapon for the player - punch attack
#punchaction is for the active state, so like when you click, it does animation
punchinit = Image()
punch = punchinit.load("Assets\\stickman\\weapon\\punch","punchstill.png").convert_alpha()
punchaction = Image("Assets\\stickman\\weapon\\punch\\punch animation")

#same as punch, but also loads the image for the toolbar
glockinit = Image()
glock = glockinit.load("Assets\\gui","glock.png").convert_alpha()
glockholdinit = Image()
glockhold = glockholdinit.load("Assets\\stickman\\weapon\\glock","glockhold.png").convert_alpha()
glockfireinit = Image()
glockfire = glockfireinit.load("Assets\\stickman\\weapon\\glock","glockfire.png").convert_alpha()

condition = 'world' #sets the spawnpoint 
money = 10
limit = 15
dancelimit = 15 #limits the time each frame gets displayed on the screen for the dance
f = False #this is for dance. If clicked it is true, so it plays the animation. Otherwise not.
speed = 5
bulletspeed = 10
FPS = 70        #YOU CAN ADJUST THIS PARAMETER FOR YOUR DEVICE SPECIFICATIONS. 
if FPS!=72: #it adjusts the player speed and dance seed accordingly to 
    #fps so animations and player speed doesn't get too quick or too slow
    #72 because it was the initial fps it was programmed on
    dancelimit = int(FPS/4.8)
    limit = int(FPS/4.8)
    speed = int(FPS/14.4)
clock = pygame.time.Clock() #initialises clock for limiting fps
run = True#SET TRUE TO RUN GAME
scale = 1
last_scale = scale
slotnum=0
use = False #it's for the event when the player wants to shoot or punch, it turns True to make it possible to do the action
right_mbutton = False #it's used in the pair with use but if this variable is true, it allows to turn use to True
#right_mbutton and use are separate because it allows the player to click right mouse to reveal/unreveal the weapon from the inventory 
#and make it aim and variable use is for when the player clicks the left mouse he performs the action with the weapon(shoots or punches).

savelistbool = False


#variables below that start with the objects_ are for the different locations of the game
#uses 2d list to have the list of each object and contains its x & y, image itialise and its image
objects_world = [[background,-playerxy[0],  -playerxy[1],  backgroundinit],
           [bank,playerxy[0]+984,  playerxy[1]-190,  bankinit],
           [gunshop,playerxy[0]+372,  playerxy[1]-370,  gunshopinit],
            [playground,playerxy[0]-250,  playerxy[1]+625,  playgroundinit],
            [forest,playerxy[0]-400,  playerxy[1]+770,  forestinit],
            [house,playerxy[0]-512,  playerxy[1]-140,  houseinit],
            #[ebutton,playerxy[0],  playerxy[1],  ebuttoninit],
           [stickman,s_width/2,s_height/2,stickmaninit]]

objects_bank = [[bankinside,playerxy[0],  playerxy[1],  bankinsideinit],
                [stickman,s_width/2,s_height/2,stickmaninit]]

objects_gunshop = [[gunshopinside,playerxy[0],  playerxy[1],  gunshopinsideinit],
    [stickman,s_width/2,s_height/2,stickmaninit]]

objects_house = [[houseinside,playerxy[0],  playerxy[1],  houseinsideinit],
    [stickman,s_width/2,s_height/2,stickmaninit]]

objects_basement = [
    [stickman,s_width/2,s_height/2,stickmaninit]]


font = pygame.font.SysFont("Arial", 32) # creates a font object
#pygame.display.set_mode(vsync=1)

#creates dectionary inventory for the player
#contains the animation, images and its name at a given slot
inventory = {1:[punch,punch,punchaction,'punch'], 2:[glock,glockhold,glockfire,'glock'],3:0 , 4:0 , 5:0 , 6:0 , 7:0 , 8:0}
inventoryobjects=0


#air 0
#player 1
#grass 2
#road 3
#road horizontal 3.1
#road intersection 4 +
#road turn 5 ⌜(5.1:⌝ ; 5.2:⌟ ; 5.3: ⌞)
#bank 6
#gun shop 7
#home 8
#road triple 9 ⊥ (9.1: ⊢ ; 9.2: ⊤ ; 9.3: ⊣ )
#forest 10

#playground 11


'''matrix = [[0,   8,   0,   0,   0,   7,   0,   0,   0,   0,   ],
          [0,   3,   2,   0,   0,   3,   0,   6,   0,   0,   ],
          [0,   5, 3.1, 9.2, 3.1,   4, 3.1, 5.2,   0,   0,   ],
          [0,   0,   0,  11,   0,   3,   0,   0,   0,   0,   ],
          [0,   0,   0,   0,   0,  10,   0,   0,   0,   0,   ],
          [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   ]]'''
'''orig_scale = []
for i in range(len(objects)):
    orig_scale.append(objects[i][-1].size())'''












allowed = False

while run:#GAME LOOP
    clock.tick(FPS)
    if condition == 'world':
        game.fill((120,214,60))#fills the screen with the green color
        objects = objects_world#sets the objects used for 'world'
        #other if elif uses the same strategy
    else:
        game.fill((0,0,0)) #fills with black color
    if condition == 'bank':
        objects = objects_bank
    elif condition == 'gunshop':
        objects = objects_gunshop
    elif condition == 'house':
        objects = objects_house
    elif condition == 'basement':
        objects = objects_basement
    
    #if right mouse clicked, performs aim and changes the image of the player, otherwise gets back
    if right_mbutton:
        name_run = 'stickman_weapon_run'
        name_still = 'stickman_weapon_still'
        body = stickmanweaponinit
    else:
        name_run = 'stickman_run'
        name_still = 'stickman_still2'
        body = stickmaninit

    #events = game.events()
    mouse_pos = pygame.mouse.get_pos() #gets x & y of the mouse for aim
    #print(mouse_pos)
    text = font.render(str(clock), True, (0,0,0)) #displays the fps on the screen
    game.append(text, (10,   10)) #also used to display that text
    
    #gets the information of wasd and other keys that matter for player movement
    keys = movement.keys(scale,speed,stickman,body,limit,s_width,s_height,name_run,name_still)
    newxy = keys[0:2]#slicing the list to get new x&y
    if right_mbutton:#if true changes the player object to weapon
        objects[-1][-1] = stickmanweaponinit
    else:
        objects[-1][-1] = stickmaninit
    objects[-1][0] = keys[2] #sets the the image of the player(runs right image if he moves right etc.)
    #print(keys[2].get_bounding_rect())
    for event in pygame.event.get(): #gets inputs like mouse or exit button
        #print(event)
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        elif event.type == pygame.MOUSEWHEEL:#used for changing the used inventory slot
            print("Mouse scroll:", event.x, event.y)
            '''scale+=event.y
            if scale<1:
                scale = 1
            elif scale>=2:
                scale = 2'''
            slotnum = (slotnum+event.y)%8
        elif event.type == pygame.MOUSEBUTTONDOWN:#gets the pressed mouse input and the number of the button(left,right,middle)
            print(event)
            if event.button == 3:#right mouse button
                print('real')
                right_mbutton = not right_mbutton#changes to true if pressed
                print(right_mbutton)
            if event.button == 1:#left mouse button
                if right_mbutton:
                    print("left one")
                    use = True
                if savelistbool == False:
                    #checks if mouse clicked on the area where save button is placed
                    check = movement.interaction(checksave=True,mousexy = mouse_pos,savebutton=savebuttonpng)
                    if check == True:
                        savelistbool = check
                        check = 0
                else:
                    #checks if mouse clicked on the area where save button is placed
                    check = movement.interaction(checksave=True,mousexy = mouse_pos,savebutton=savebuttonpng,checksaveinverse=True)
                    if check == False:
                        savelistbool = check
                        check = 0
                '''d=pygame.font.get_fonts()
                for i in d:
                    print(i)'''
        elif event.type == pygame.MOUSEBUTTONUP:#same thing as previous elif but this time if it released
            #print(event)
            #print(event)
            if right_mbutton:
                if event.button == 1:
                    print("left one")
                    use = False#changes to false so it works like as long as button is being held, he shoots
        elif event.type == pygame.MOUSEMOTION:#used to detect xy of the mouse
            
            try:
                angle = math.atan2((event.pos[1]-s_height/2),(event.pos[0]-s_width/2))#calculates the elevation angle for the head to look right into the mouse
                angle = -1*math.degrees(angle)
                #print(angle)
            except ZeroDivisionError:
                pass

            #stickman = pygame.transform.scale(stickman,(stickmaninit.size()[0]*scale,stickmaninit.size()[1]*scale))
            """for i in range(len(objects)):

                if last_scale<scale:
                    last_scale = scale
                    objects[i][1] -= objects[i][-1].size()[0]/2
                    objects[i][2] -= objects[i][-1].size()[1]/2
                elif last_scale>scale:
                    last_scale = scale
                    objects[i][1] += objects[i][-1].size()[0]/2
                    objects[i][2] += objects[i][-1].size()[1]/2
                    #print(orig_scale)
                    '''objects[i][1] += orig_scale[i][0]/2
                    objects[i][2] += orig_scale[i][1]/2'''
                '''if scale == 2:
                    last_scale = scale
                    objects'''
                
                objects[i][0] = pygame.transform.scale(objects[i][0],(objects[i][-1].size()[0]*scale, objects[i][-1].size()[1]*scale))
                """
            '''if i!=len(objects)-1:
                    objects[i][1] = s_width/2 - (s_width/2 - objects[i][1]) * scale - objects[i][-1].size()[0] / 2
                    objects[i][2] = s_height/2 - (s_height/2 - objects[i][2]) * scale - objects[i][-1].size()[1] / 2'''
            """"""
    
    
    '''try:
        if right_mbutton and isinstance(inventory[slotnum+1],list):
            objects[-1][0],objects[-1][-1]= stickmanweapon,stickmanweaponinit
    except KeyError:
        pass'''
    if pygame.key.get_pressed()[pygame.K_f]:#if key f pressed, plays fortnite dance
        f = True#tru as long as dance played
        pygame.mixer.music.load(os.path.join("Assets\\stickman\\fortnite dance","fortnitedance.mp3"))
        pygame.mixer.music.play()#plays sound
        last_slotnum = slotnum#stores the las slot equipped by the user
    if f:
        objects[-1][0] = movement.dance(f,stickmandanceinit,dancelimit)#replaces the image for dance animation
        
        slotnum = 0#makes slot default for time of animation
        if right_mbutton:
            allowed = True#it's for changing back to the selected slot if equipped
        right_mbutton = False#changes to false so the equipped items doesn't get displayed
        if isinstance(objects[-1][0], bool):#if animation is done, it returns bool, so then rhis if returns everything to state it was before the dance
            if allowed:
                right_mbutton = True
                slotnum = last_slotnum
            f = False
            allowed = False
            objects[-1][0] = stickman
    

    for i in range(0,  len(objects)-1):#changes the coordinates for the objects except for the player if the player presses movement keys
        objects[i][1] += newxy[0]
        objects[i][2] += newxy[1]
        #print(objects[i][1],objects[i][2],objects[i][-1].size()[0]*scale,objects[i][-1].size()[0]*scale)
        #game.append(objects[i][0],(objects[i][1],objects[i][2]))
    

    for indx,obj in enumerate(objects):#loop for displaying each object on the screen
        if indx==len(objects)-1:#player position(centered)
            '''# Create a mask from the image
            mask = pygame.mask.from_surface (objects[1][0])
            # Get a list of rects that cover the non-transparent areas
            rects = mask.get_bounding_rects()
            # Loop through the rects and draw them on the screen
            for rect in rects:
                pygame.draw.rect (stickman, (255, 0,   0), rect) # draw a red outline'''
            game.append(obj[0], (s_width/2-obj[-1].size()[0]*scale/2, s_height/2-obj[-1].size()[0]*scale/2))
        else:
            game.append(obj[0], (obj[1], obj[2]))#displaying at its x and y
            
            
    #game.matrix(matrix,game,objects,scale)
    #game.append(stickman,(s_width/2-stickmaninit.size()[0]*scale/2,s_height/2-stickmaninit.size()[1]*scale/2))
    
    #mouse = pygame.mouse.get_pressed(num_buttons=5)
    #print(mouse)
    
    
    
    building = []
    obj_rects = []
    for index,item in enumerate(objects):#for loop to detect each rect of the object
        if item[0] in [background,forest,playground]:
            pass
        else:
            #mask = pygame.mask.from_surface()
            obj_rects.append(item[0].get_bounding_rect())#appends the rect of an object
            building.append(index)
            for i in range(4):#sets up the coordinates of each object propertly
                if i ==0:
                    obj_rects[-1][i]+=item[1]
                elif i == 1:
                    obj_rects[-1][i]+=item[2]
    obj_rects[-1][0]-=50#these lines of code are to set up the coordinates of the player's rect
    obj_rects[-1][1]-=50#and a little rect at a position nearby his foot
    obj_rects.append(stickman.get_bounding_rect())
    obj_rects[-1][0]+=objects[-1][1]-47
    obj_rects[-1][1]+=objects[-1][2]+10
    obj_rects[-1][3]-=55

    for i in range(len(obj_rects)-2):#this loop is for preventing the player getting over the objects, so like he can't walk on the wall
        outline_color = (255, 0, 0)
        if obj_rects[i].colliderect(obj_rects[-2]):#if player's foot touches the wall it prevents from walking further
            
            

            # Draws the rectangles with an outline
            pygame.draw.rect(screen, outline_color, obj_rects[i], 2)
            pygame.draw.rect(screen, outline_color, obj_rects[-2], 2)
            game.append(ebutton,(obj_rects[i][0]+obj_rects[i][2]/2-14,obj_rects[i][1]+obj_rects[i][3]/2-11))
            test = movement.interaction(building[i],e=True)#tests if the button e is pressed if the player is nearby the building
            if test in ('bank','gunshop','house','basement','world'):
                condition = test#changes the environment
                test = 0

        if condition == 'world':#if it is then it prevents to walking over the buildings
            if obj_rects[i].colliderect(obj_rects[-1]):
                pygame.draw.rect(screen, outline_color, obj_rects[-1], 2)
                #print(len(obj_rects))
                for i in range(0,  len(objects)-1):
                    objects[i][1] -= newxy[0]
                    objects[i][2] -= newxy[1]
    if right_mbutton:
        a = movement.action(slotnum,inventory,game,s_width,s_height,angle,stickmanhead,glockhold)#performs the rotation of the objects(head, item)
        #print("YEEEEAH")

    

    #game.append(objects[1][0], (s_width/2-objects[1][-1].size()[0]*scale/2, s_height/2-objects[1][-1].size()[0]*scale/2))
    
    # fill the screen with black color
    #screen.fill((0,   0,   0))
    # loop through the objects and scale them according to the scaling factor
    '''for obj in objects:
            # get the original size of the object
            width, height = obj.get_size()
            # calculate the new size by multiplying the original size by the scaling factor
            new_width = int(width * scale)
            new_height = int(height * scale)
            # scale the object to the new size
            scaled_obj = pygame.transform.scale(obj, (new_width, new_height))
            # draw the scaled object on the screen
            game.append(scaled_obj, (0,   0)) # you can change the position as you like'''
    '''a = []
    for rect in objects:
        a.append(rect[0].get_rect())'''
    
    game.append(toolbar,(s_width/2-410.5,s_height-120))#displays bar for items
    for index,item in enumerate(inventory):
        if isinstance(inventory[item],list) and index!=0:
            game.append(inventory[item][0],(s_width/2-407.5+103*(int(item)-1),s_height-117))#displays items
        '''else:
            #print(item)
            game.append(inventory[item][0],(s_width/2-407.5+103*(int(item)-1),s_height-117))'''
        
    
    game.append(toolbarframe,(s_width/2-413.5+103*slotnum,s_height-123))#displays highlighted frame for the selected item
    






    game.append(savebuttonpng,(s_width-100,0))#displays save button
    if savelistbool == True:#if save button pressed, displays this window below
        game.append(savelistpng,(s_width/2-250,s_height/2-250))
        reader = filesave.readcsv()
        for i in range(4):
            if i==0:
                game.append(saveslotpng,(s_width/2-241,s_height/2-119*2-3))
                filesave.displaysave(1,game,s_width/2-238,s_height/2-119*2,reader)
                
            elif i==1:
                game.append(saveslotpng,(s_width/2-241,s_height/2-119-1))
                filesave.displaysave(2,game,s_width/2-238,s_height/2-119+2,reader)
            elif i==2:
                game.append(saveslotpng,(s_width/2-241,s_height/2+1))
            elif i==3:
                game.append(saveslotpng,(s_width/2-241,s_height/2+119+3))
    

    pygame.display.update()#updates the display