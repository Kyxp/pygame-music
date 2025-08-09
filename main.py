import pygame
from note import Note

CIRCLE_RADIUS = 26
CIRCLE_OFFSET = 25
FLASH_WIDTH = 100
FLASH_HEIGHT = 550
FLASH_DURATION = 80
LANE_START_X = 675
LANE_GAP = 137.5
LANE_COUNT = 4
HIT_Y = 612.5
HIT_TOLERANCE = 20

# POINTS
PERFECT = 200
GOOD = 100
OKAY = 50
BAD = -50
MISS = -100

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
    flash_colour = (128, 128, 128, 100)

    # music
    music_file = "music/Lionheart.mp3"
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    
    # lane flashes
    flash_timers = [0, 0, 0, 0]  # initially no flash
    flash_duration = 80  # milliseconds

    # notes list
    notes = []

    # hit area
    HIT_TOLERANCE = 20

    # points
    points = 0

    # lane setup
    lane_count = 4
    lane_start_x = 675
    lane_gap = 137.5

    lanes = [lane_start_x + i * lane_gap for i in range(lane_count)]

    circle_centres = [x + 25 for x in lanes]

    # song to play
    playLionheart(notes, lanes, blue)

    # game loop
    running = True
    clock = pygame.time.Clock()
    pos = 612.5

    while running:
        dt = clock.tick(60) # 60fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # check keys
            flash_timers, add_points = checkKeys(event, flash_timers, flash_duration, notes, pos, HIT_TOLERANCE, lanes)
            points += add_points
            print(points)

        # falling notes
        for note in notes:
            note.fall(dt)

        # drawing ----------------------------------------------------------
        screen.fill(white) 

        # draw rectangular play area
        drawArea(screen, 590, 0, 650, screen_height, semi_black)

        # draw bottom part
        drawArea(screen, 0, 580, screen_width, 70, white)

        for cx in circle_centres: # draw circles
            pygame.draw.circle(screen, black, (cx, pos), 26, width=2)

        # draw lanes
        pass

        # draw notes
        for note in notes:
            if note.y > screen_height - (HIT_TOLERANCE / 2):
                notes.remove(note)
            else:
                note.draw(screen)


        # draw flash
        flash_width = 100
        flash_height = 550
        flash_left_edges = [int(cx - flash_width / 2) for cx in circle_centres]

        circle_centres = [x + 25 for x in lanes]

        for i in range(LANE_COUNT):
            if flash_timers[i] > 0:
                flash_surf = pygame.Surface((FLASH_WIDTH, FLASH_HEIGHT), pygame.SRCALPHA)
                flash_surf.fill(flash_colour)
                
                screen.blit(flash_surf, (int(circle_centres[i] - FLASH_WIDTH / 2), 0))

                flash_timers[i] = max(0, flash_timers[i] - dt) # refixes timer


        # show points
        showPoints(screen, points, black)

        # Update display
        pygame.display.flip() 

    # quit
    pygame.quit()

def drawArea(surface, x, y, width, height, colour):
    screen_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, colour, screen_rect)

def checkKeys(event, flash_timers, flash_duration, notes, hit_y, tolerance, lanes): # check keys pressed (controls)
    add_points = 0
    if event.type == pygame.KEYDOWN:
        key_to_lane = {
            pygame.K_a: 0,
            pygame.K_s: 1,
            pygame.K_k: 2,
            pygame.K_l: 3
        }
        if event.key in key_to_lane:
            lane_index = key_to_lane[event.key]
            flash_timers[lane_index] = flash_duration

            # check hit notesll
            lane_x = lanes[lane_index]
            hit_note = None
            for note in notes:
                if abs(note.x - lane_x) < 50:
                    if note.is_in_hit_area(hit_y, tolerance):
                        hit_note = note
                        break

            if hit_note:
                notes.remove(hit_note) # remove hit note
                add_points = GOOD


    return flash_timers, add_points

def showPoints(screen, points, colour):
    font = pygame.font.SysFont("Arial", 24)
    points_txt = font.render(f"Points: {points}", True, colour)
    screen.blit(points_txt, (10, 10))

def playLionheart(noteList, lanes, colour):
    # create notes
    noteList.append(Note(lanes[3], -100, 50, 50, colour))
    noteList.append(Note(lanes[2], -100, 50, 50, colour))
    noteList.append(Note(lanes[1], -100, 50, 50, colour))

    return noteList
    
if __name__ == "__main__":
    main()


