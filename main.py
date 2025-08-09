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
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow  = (255, 255, 0)

    # music
    music_file = "music/Lionheart.mp3"
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

    # notes list
    notes = []

    # test note
    test_note = Note(400, -100, 30, 100, blue)
    notes.append(test_note)

    # game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(60) # 60fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # falling notes
        for note in notes:
            note.fall(dt)

        # drawing
        screen.fill(white) 
        for note in notes:
            note.draw(screen)

        # Update display
        pygame.display.flip() 

    # quit
    pygame.quit()

if __name__ == "__main__":
    main()


