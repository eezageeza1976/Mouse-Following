# sprite holder

import pygame as pg
from vector import *
from properties import *

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = Vector2D(WIDTH / 2, HEIGHT / 2)
        self.vel = Vector2D()
        self.acc = Vector2D()
        self.walk_direction = Vector2D()
        self.image = self.load_image()
        self.frames = self.image        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos.x, self.pos.y
        self.walking_dir = self.image
        self.walking = False
        self.running = False
        self.shooting = False
        self.current_frame = 0
        self.last_update = 0
    
    def get_image(self, x, y, width, height, scale = True):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        if scale:
            image = pg.transform.scale(image, (width // 2, height // 2))
        return image
    
    def load_image(self):
        self.spritesheet = pg.image.load('Graphics/cowboy_spritesheet.png').convert_alpha()        
        self.walk_frames_l = []
        self.walk_frames_r = []
        self.walk_frames_u = []
        self.walk_frames_d = []
        self.walk_frames_ur = []
        self.walk_frames_ul = []
        self.walk_frames_dr = []
        self.walk_frames_dl = []

        for i in range(SS_WALKING_FRAMES):
            x_start = 128
            image = self.get_image(x_start * i,  896, 128, 128, False)
            image = pg.transform.scale(image, (90, 90))
            self.walk_frames_l.append(image)            
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)
            
        for i in range(SS_WALKING_FRAMES):
            x_start = 128
            image = self.get_image(x_start * i,  384, 128, 128, False)
            image = pg.transform.scale(image, (90, 90))
            self.walk_frames_r.append(image)
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            
        for i in range(SS_WALKING_FRAMES):
            x_start = 128
            image = self.get_image(x_start * i,  640, 128, 128, False)
            image = pg.transform.scale(image, (90, 90))
            self.walk_frames_u.append(image)
        for frame in self.walk_frames_u:
            frame.set_colorkey(BLACK)
            
        for i in range(SS_WALKING_FRAMES):
            x_start = 128
            image = self.get_image(x_start * i,  1152, 128, 128, False)
            image = pg.transform.scale(image, (90, 90))
            self.walk_frames_d.append(image)
        for frame in self.walk_frames_d:
            frame.set_colorkey(BLACK)
            
        for i in range(SS_WALKING_FRAMES):
            x_start = 128
            image = self.get_image(x_start * i,  512, 128, 128, False)
            image = pg.transform.scale(image, (90, 90))
            self.walk_frames_ur.append(image)            
        for frame in self.walk_frames_ur:
            frame.set_colorkey(BLACK)
            
        for i in range(SS_WALKING_FRAMES):
            x_start = 128
            image = self.get_image(x_start * i,  768, 128, 128, False)
            image = pg.transform.scale(image, (90, 90))
            self.walk_frames_ul.append(image)
        for frame in self.walk_frames_ul:
            frame.set_colorkey(BLACK)
            
        for i in range(SS_WALKING_FRAMES):
            x_start = 128
            image = self.get_image(x_start * i,  256, 128, 128, False)
            image = pg.transform.scale(image, (90, 90))
            self.walk_frames_dr.append(image)
        for frame in self.walk_frames_dr:
            frame.set_colorkey(BLACK)
            
        for i in range(SS_WALKING_FRAMES):
            x_start = 128
            image = self.get_image(x_start * i,  1024, 128, 128, False)
            image = pg.transform.scale(image, (90, 90))
            self.walk_frames_dl.append(image)
        for frame in self.walk_frames_dl:
            frame.set_colorkey(BLACK)
            
        return self.walk_frames_l[0]
    
    def update(self):
        self.animate()
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.walking = True
            mouse_pos = Vector2D(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
            self.walk_direction = (mouse_pos - self.pos)
            self.walk_direction = normalize(self.walk_direction)
        if keys[pg.K_r]:
            self.running = True
    
    def animate(self):        
        # get the frames to use for walking direction
        self.working_frames = self.direction()
        
        if self.working_frames == None:
            self.working_frames = self.frames
        
        now = pg.time.get_ticks()

        if now - self.last_update > 120:
            if not self.walking and not self.shooting:
                self.image = self.working_frames[STILL]
                self.current_frame = 0
            elif self.walking:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % WALKING[2]
                self.image = self.working_frames[WALKING[0] + self.current_frame]
                self.game.tree.pos -= self.walk_direction * WALKING_SPEED
                self.walking = False
            elif self.shooting:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % SHOOTING[2]
                self.image = self.working_frames[SHOOTING[0] + self.current_frame]
        self.frames = self.working_frames   
            
    def angle_to_mouse(self):
        mouse_pos = Vector2D(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
        return rad_to_deg(angle_between(mouse_pos, self.pos))
        
    def direction(self):
        angle = self.angle_to_mouse()        
        if 67.5 < angle < 112.5:
            return self.walk_frames_d
        elif 22.5 < angle < 67.5:
            return self.walk_frames_dl
        elif 112.5 < angle < 157.5:
            return self.walk_frames_dr
        elif -22.5 > angle > -67.5:
            return self.walk_frames_ul
        elif -67.5 > angle > -112.5:
            return self.walk_frames_u
        elif -112.5 > angle > -157.5:
            return self.walk_frames_ur
        elif 0.1 < angle < 22.5 or -0.1 > angle > -22.5:
            return self.walk_frames_l
        else:
            return self.walk_frames_r
        
class Tree(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = Vector2D(WIDTH/4, HEIGHT/4)
        self.image = self.load_image()        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos.x, self.pos.y
        
    def load_image(self):
        image = pg.Surface((525, 716))
        sheet = pg.image.load('Graphics/_tree_09_00000.png').convert_alpha()
        image.blit(sheet, (0, 0))
           
        image = pg.transform.scale(image, (100, 120))
        image.set_colorkey(BLACK)
        return image
        
    def update(self):
        self.rect.center = self.pos.x, self.pos.y
        
        