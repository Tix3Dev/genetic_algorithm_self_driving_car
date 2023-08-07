import pygame

from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    max_fps = 60

    game = Game(screen)
    
    game_running = True
    while game_running:
        clock.tick(max_fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        game.gameloop()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
