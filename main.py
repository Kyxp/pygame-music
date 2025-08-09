import pygame
from note import Note

def main():
    # Pygame init
    pygame.init()
    pygame.mixer.init()

    # setup screen
    screen_width, screen_height = 1280, 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Music Game")

    # icon change
    pass

    # colours
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow  = (255, 255, 0)
    green = (0, 255, 0)
    semi_black = (0, 0, 0, 51)

    # music
    music_file = "music/Lionheart.mp3"
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

    # notes list
    notes = []

    # test notes
    lane1, lane2, lane3, lane4 = 675, 812.5, 937.5, 1075

    # song to play
    playLionheart(notes, lane1, lane2, lane3, lane4, blue)

    # game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(60) # 60fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # check keys
            checkKeys(event)

        # falling notes
        for note in notes:
            note.fall(dt)

        # drawing ----------------------------------------------------------
        screen.fill(white) 

        # draw rectangular play area
        pos = 612.5
        drawArea(screen, 590, 0, pos, screen_height, semi_black)

        # draw bottom part
        drawArea(screen, 0, 580, screen_width, 70, white)
        pygame.draw.circle(screen, black, (lane1+25, pos), 26, width=2) # Lane1
        pygame.draw.circle(screen, black, (lane2+24, pos), 26, width=2) # Lane2
        pygame.draw.circle(screen, black, (lane3+25, pos), 26, width=2) # Lane3
        pygame.draw.circle(screen, black, (lane4+25, pos), 26, width=2) # Lane4

        # draw lanes
        pass

        # draw notes
        for note in notes:
            note.draw(screen)



        # Update display
        pygame.display.flip() 

    # quit
    pygame.quit()

def drawLaneLine(surface, x, y, width, height):
    pass

def drawArea(surface, x, y, width, height, colour):
    screen_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, colour, screen_rect)

def checkKeys(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            print("hi")

def playLionheart(noteList, lane1, lane2, lane3, lane4, colour):
    # create notes
    #noteList.append(Note(lane4, -100, 50, 50, colour))

    return noteList
    
if __name__ == "__main__":
    main()


