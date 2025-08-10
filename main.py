import pygame
from note import Note

# CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS=60

CIRCLE_RADIUS = 26
CIRCLE_OFFSET = 25
FLASH_WIDTH, FLASH_HEIGHT = 100, 550
FLASH_DURATION = 80
LANE_START_X = 675
LANE_GAP = 137.5
LANE_COUNT = 4
HIT_Y = 612.5
MISS_MARGIN = 40
VERTICAL_HIT_RANGE = 300

# POINTS
PERFECT = 200
GOOD = 100
OKAY = 50
BAD = -50
MISS = -100

# THRESHOLDS FOR POINTS
PERFECT_THRESHOLD = 25
GOOD_THRESHOLD = 40
OKAY_THRESHOLD = 70

# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW  = (255, 255, 0)
GREEN = (0, 255, 0)
SEMI_BLACK = (0, 0, 0, 51)
FLASH_COLOUR = (128, 128, 128, 100)

# Key-to-lane mapping
KEY_TO_LANE = {
    pygame.K_a: 0,
    pygame.K_s: 1,
    pygame.K_k: 2,
    pygame.K_l: 3
}

def drawArea(surface, x, y, width, height, colour):
    screen_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, colour, screen_rect)

def draw_lanes(surface, lanes, pos):
    for lane_x in lanes:
        pygame.draw.circle(surface, BLACK, (int(lane_x + CIRCLE_OFFSET), int(pos)), CIRCLE_RADIUS, 2)

def showPoints(screen, points, colour):
    font = pygame.font.SysFont("Arial", 24)
    points_txt = font.render(f"Points: {points}", True, colour)
    screen.blit(points_txt, (10, 10))

def draw_flash(surface, flash_timers, lanes):
    for i, timer in enumerate(flash_timers):
        if timer > 0:
            flash_surf = pygame.Surface((FLASH_WIDTH, FLASH_HEIGHT), pygame.SRCALPHA)
            flash_surf.fill(FLASH_COLOUR)
            lane_center_x = lanes[i] + CIRCLE_OFFSET
            surface.blit(flash_surf, (int(lane_center_x - FLASH_WIDTH / 2), 0))

def update_notes(notes, dt, points):
    for note in notes[:]:
        note.fall(dt)
        if note.y > HIT_Y + MISS_MARGIN:
            points += MISS
            notes.remove(note)
    return points

def checkKeys(event, flash_timers, notes, lanes,  hitsounds, points):
    add_points = 0
    if event.type == pygame.KEYDOWN and event.key in KEY_TO_LANE:
        lane_index = KEY_TO_LANE[event.key]
        flash_timers[lane_index] = FLASH_DURATION # flash the lane
        hitsounds[lane_index].play()

        lane_x = lanes[lane_index]
        hit_note = None
        best_distance = float('inf')

        for note in notes:
            if abs(note.x - lane_x) < 50 and abs(note.y - HIT_Y) <= VERTICAL_HIT_RANGE:
                dist = abs(note.y - HIT_Y)
                if dist < best_distance:
                    best_distance = dist
                    hit_note = note

        if hit_note:
            if best_distance <= PERFECT_THRESHOLD: # add 200 points
                add_points = PERFECT
            elif best_distance <= GOOD_THRESHOLD: # add 100 points
                add_points = GOOD
            elif best_distance <= OKAY_THRESHOLD: # add 50 points
                add_points = OKAY
            else:
                add_points = BAD

            notes.remove(hit_note)
            
    
    points += add_points
    return flash_timers, points
            
def main():
    # Pygame init
    pygame.init()
    pygame.mixer.init()

    # setup screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Music Game")

    clock = pygame.time.Clock()

    # music
    music_file = "music/Lionheart.mp3"

    # sound effects
    sound1 = "sfx/kick.mp3"
    sound2 = "sfx/hi-hat.mp3"
    sound3 = "sfx/stick.mp3"
    sound4 = "sfx/ding.mp3"

    # load audio
    pygame.mixer.music.load(music_file)
    hitsounds = []
    hitsounds.append(pygame.mixer.Sound(sound1))
    hitsounds.append(pygame.mixer.Sound(sound2))
    hitsounds.append(pygame.mixer.Sound(sound3))
    hitsounds.append(pygame.mixer.Sound(sound4))
    hitsounds[1].set_volume(0.2)

    # play audio
    pygame.mixer.music.play()

    lanes = [LANE_START_X + i * LANE_GAP for i in range(LANE_COUNT)]
    circle_pos_y = HIT_Y

    # setup variables
    flash_timers = [0] * LANE_COUNT
    notes = []
    points = 0

    # Add some notes
    notes.append(Note(lanes[3], -100, 50, 50, (0, 0, 255)))

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            else:
                flash_timers, points = checkKeys(event, flash_timers, notes, lanes, hitsounds, points)

        points = update_notes(notes, dt, points)

        # update flash timers
        for i in range(len(flash_timers)):
            flash_timers[i] = max(0, flash_timers[i] - dt)

        # draw
        screen.fill(WHITE)
        drawArea(screen, 590, 0, 650, SCREEN_HEIGHT, SEMI_BLACK)
        drawArea(screen, 0, 580, SCREEN_WIDTH, 70, WHITE)

        draw_lanes(screen, lanes, circle_pos_y)

        draw_flash(screen, flash_timers, lanes)

        for note in notes:
            note.draw(screen)


        draw_flash(screen, flash_timers, lanes)
        showPoints(screen, points, BLACK)

        # Update display
        pygame.display.flip() 

    # quit
    pygame.quit()
    
if __name__ == "__main__":
    main()


