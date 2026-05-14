import pygame#for the game
import os#for file path
import pyautogui#for getting the size of the monitor
import random
import math
import sys
import csv#for reading csv file

        
        

class World:#class for creating a game window and other related stuff
    screen = 0#just creates the variable
    def __init__(self,name):
        self.name = name
        self.width, self.height =  pyautogui.size()#gets the size of the monitor so then adjusts the size of the game window so it doesn't look weird
        self.width -= 200
        self.height -=200
        

    def InitWindow(self):#creates game window
        pygame.init()#initialises the game
        flags = pygame.OPENGL | pygame.FULLSCREEN#useless variable saved for never upcoming future
        World.screen = pygame.display.set_mode((self.width, self.height),pygame.RESIZABLE)#resizes the window
        pygame.display.set_caption(self.name)#sets the name of the game
        return World.screen
    def append(self, object,xy):
        return World.screen.blit(object,xy)#displays selected object

    def fill(self,other):
        return World.screen.fill(other)#fills the screen with the color
    
    def window_stats(self):
        #return self.width,self.height
        return World.screen.get_width(),World.screen.get_height()
    
    def events(self):#not used

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #SET FALSE TO QUIT
                pygame.quit()
    def rotation(self,item):#saved for later
        pass


    
class Image(World):
    def __init__(self,path=""):
        if len(path)>0:
            Image.multiple_load(self,path)#If path specified, imports all the images in the folder

    def load(self,folder,name,size = ""):#loads the image
        self.image = pygame.image.load(os.path.join(folder, name))
        if isinstance(size, tuple):#if size specified, resizes to that size
            Image.resize(self,size)
        return self.image
    def resize(self, size = ""):#resizes the image
        return pygame.transform.scale(self.image,size)
    def size(self):#gets size of the image
        return self.image.get_size()
    def multiple_load(self,path):#DONT MARK THIS MODULE, WAS TAKEN FROM OTHER SOURCE
        #path = 'path/to/directory/'
        filenames = [f for f in os.listdir(path) if f.endswith('.png')]
        images = {}
        for name in filenames:
            imagename = os.path.splitext(name)[0]
            images[imagename] = pygame.image.load(os.path.join(path, name)).convert_alpha()
        self.images = images
        return self.images
    def get_im(self,name):#returns image
        self.image = self.images[name]
        return self.images[name]

class Inputs(World):
    def __init__(self):
        pass
    def mouse_wheel(self,events):#saved for later, not currently used
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                # gets the mouse position as x y coordinates
                self.mouse_pos = pygame.mouse.get_pos()
                print("Mouse position:", self.mouse_pos)


            if event.type == pygame.MOUSEWHEEL:
                print("Mouse scroll:", event.x, event.y)
                self.eventx =event.x
                self.eventy =event.y
            if True in pygame.mouse.get_pressed():
                self.mouse_buttons = pygame.mouse.get_pressed()
                print("Mouse buttons:", self.mouse_buttons)
    

class Movement(Image):
    def __init__(self):
        self.start = 1
        self.num = 0
        self.dancestart = 1
        self.dancenum = 0
        self.rotated = 'right'
    def keys(self,scale,speed,facing,body,limit,s_width,s_height,name_run,name_still):
        x = 0
        y = 0
        
        keys = pygame.key.get_pressed()#detects the keyboard inputs
        if keys:
            if keys[pygame.K_LSHIFT]:#if shift pressed, speed increases
                speed *= 2
                limit /= 2
            if keys[pygame.K_w]:#forward
                y += speed*scale#scale is actually for the time when the game is zoomed in, but it's not actually works so far, so useless

            if keys[pygame.K_a]:#left
                x += speed*scale
                self.rotated = 'left'#marks that the player going left direction
            if keys[pygame.K_s]:#down
                y -= speed*scale
            
            if keys[pygame.K_d]:#right
                x -= speed*scale
                self.rotated = 'right'#marks that he's going right
            if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:#performs the rotation of the player
                if self.rotated == 'right':
                    facing = body.get_im(name_run+str(self.num))#gets right version of running image
                    #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                elif self.rotated == 'left':
                    facing = pygame.transform.flip(body.get_im(name_run+str(self.num)), True, False)#gets left version of running image
                self.start = (self.start+1)
                if self.start >=limit:#limit for time displayed for a specific frame
                    self.start = 1
                    self.num = (self.num+1)%3
            else:
                if self.rotated == 'left':
                    facing = pygame.transform.flip(body.get_im(name_still), True, False)#flips the image to the left if the player stands left direction
            return (x,y,facing)
        return True
    def interaction(self,building='',e=False,checksave=False,mousexy=False,savebutton='',checksaveinverse = False):
        if e==True:
            if pygame.key.get_pressed()[pygame.K_e]:#if e pressed, changes the invironment
                if building == 1:
                    return 'bank'
                if building == 2:
                    return 'gunshop'
                if building == 5:
                    return 'house'
                return 'a'
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                return 'world'
        if checksave == True:
            s_width,s_height = World.screen.get_size()
            
            saverect = pygame.Rect(s_width-100,0,100,100)#rect of save button
            
            if checksaveinverse and saverect.colliderect(mousexy+(1,1)):
                return False
            elif saverect.colliderect(mousexy+(1,1)):
                return True
    def dance(self, F,stickmandanceinit,dancelimit):
        if F:
            facing = stickmandanceinit.get_im('stickman_dance'+str(self.dancenum))#performs the animation
            
            self.dancestart +=1
            if self.dancestart>=dancelimit:#limits the time each frame gets displayed
                self.dancenum+=1
                self.dancestart=1
            if self.dancenum>36:#if goes beyound, means the animation is done
                self.dancenum=0
                return False
            return facing
    def action(self,slotnum,inventory,game,s_width,s_height,angle,stickmanhead,glockhold):
        slotnum+=1
        
        try:#prevents the errors
            if angle >90 or angle <-90:#if angle beyond that, it means he faces leftwards, so this if prevents glitches
                angle *=-1

            weapon = inventory[slotnum][1].copy()#copies the image, so it avoids an error
            
            rot_image = Movement.round_rotation(stickmanhead,angle)#does rotation

            

            weapon = Movement.round_rotation(weapon,angle)#does rotation
            #stickmanhead = pygame.transform.rotate(stickmanhead,angle)
            
            if angle >90 or angle <-90:#rotates the images differently if faced left
                            rot_image = pygame.transform.flip(rot_image, False, True)
                            weapon= pygame.transform.flip(weapon, False, True)
            #if inventory[slotnum][-1] == 'glock':
            
            game.append(weapon,(s_width/2-50,s_height/2-50))#displays result
            game.append(rot_image,(s_width/2-19,s_height/2-34))
            print(inventory[slotnum][-1])
            #return inventory[slotnum][1], True
        except:
            pass

    def round_rotation(image,angle):#taken from another source
        orig_rect = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = orig_rect.copy()
        rotated_rect.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rect).copy()

        return rotated_image




class FileSave:
    def __init__(self):
        self.saves = []
    def readcsv(self):
        
        
        with open('saves.csv') as csvfile:
            reader = csv.reader(csvfile)#reads csv file
            for row in reader:
                #print(','.join(row))
                self.saves.append(row)
            return self.saves
    def writecsv(self,stickman,x,y,money,health,inventory_slot2,inventory_slot3,inventory_slot4,inventory_slot5,inventory_slot6,inventory_slot7,inventory_slot8,condition):
        with open('saves.csv', 'a',newline='') as csvfile:
            self.j = []
            spamwriter = csv.writer(csvfile)#writes data in csv file
            
            spamwriter.writerow([stickman,x,y,money,health,inventory_slot2,inventory_slot3,inventory_slot4,inventory_slot5,inventory_slot6,inventory_slot7,inventory_slot8,condition])

    def picksave(self,num):
        return self.saves[num]
    def displaysave(self,savenum,game,x,y,reader):
        save = reader[savenum]
        font = pygame.font.Font(os.path.join("Assets\\gui\\font","Mansalva-Regular.ttf"), 24)#picks custom font
        text = font.render("Money: "+save[3], True, (0,0,0)) #displays money
        game.append(text, (x, y))
        text = font.render("Health: "+save[4], True, (0,0,0)) #displays health
        game.append(text, (x, y+24))
        guns=[]
        for indx,item in enumerate(save[5:-2]):#appends the items from inventory
            if item=='1':
                pass
            else:
                guns.append(item)
            '''if indx==len(save[5:-2])-1:
                guns=guns[:-2]'''
            
        if len(guns)>3:#if items too much, divides in half, otherwise prints as it is
                text = font.render("Inventory: "+', '.join(guns[:3]), True, (0,0,0)) 
                game.append(text, (x, y+48))
                text = font.render(', '.join(guns[3:]), True, (0,0,0)) 
                game.append(text, (x, y+72))
        else:
            text = font.render("Inventory: "+', '.join(guns), True, (0,0,0)) 
            game.append(text, (x, y+48))
            

        text = font.render(save[-1], True, (0,0,0)) #date
        game.append(text, (x+220, y))
        
        
