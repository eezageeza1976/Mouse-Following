# practice for 8 way movement
import pygame as pg
from vector import *
from properties import *
from sprites import *

class Game:
    def __init__(self):
        # Initialise game window
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        
    def new(self):
        # Start a new game
        self.all_sprites = pg.sprite.Group()
        self.cowboy_sprite_group = pg.sprite.Group()
        self.tree_sprites = pg.sprite.Group()
        
        self.cb = Player(self)
        self.tree = Tree(self)
        self.all_sprites.add(self.cb)
        self.cowboy_sprite_group.add(self.cb)
        self.all_sprites.add(self.tree)
        self.tree_sprites.add(self.tree)
            
        self.run()
            
    def run(self):
        self.playing = True        
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        # update sprites
        self.all_sprites.update()
    
    def draw(self):        
        # fill screen black
        self.screen.fill(pg.Color('bisque4'))
        # draw all sprites
        self.all_sprites.draw(self.screen)
        # flip display after all drawing is done
        pg.display.flip()
    
    def events(self):
        for event in pg.event.get():
            # Check if window closed
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.cb.shooting = True
            elif event.type == pg.MOUSEBUTTONUP:
                self.cb.shooting = False
                
# Make a new Game object    
game = Game()

def main():
    while game.running:        
        game.new()

if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()





    
    
    
    
    