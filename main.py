import pygame
from note import Note
import random

# CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS=60
STANDARD_TIME = 1000
SONG_DELAY = 200

CIRCLE_RADIUS = 26
CIRCLE_OFFSET = 25
FLASH_WIDTH, FLASH_HEIGHT = 100, 550
FLASH_DURATION = 80
LANE_START_X = 675
LANE_GAP = 137.5
LANE_COUNT = 4
HIT_Y = 612.5
MISS_MARGIN = 40
VERTICAL_HIT_RANGE = 400

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

# HIT COLOURS
HIT_COLOURS = {
    "PERFECT" : GREEN,
    "GOOD" : BLUE,
    "OKAY" : YELLOW,
    "BAD" : BLACK,
    "MISS" : RED
}
DISAPPEAR_TIME = 125

# Key-to-lane mapping
KEY_TO_LANE = {
    pygame.K_a: 0,
    pygame.K_s: 1,
    pygame.K_k: 2,
    pygame.K_l: 3
}

# MUSIC
lionHeart = [
    # Intro (kick + stick)
    (2000, 0),
    (2500, 1),
    (3000, 0),
    (3500, 1),

    # Dramatic transition: intro → verse 1 (chime)
    (3900, 3),

    # Verse 1 (kick + stick)
    (4000, 0),
    (4500, 1),
    (5000, 0),
    (5500, 1),
    (6000, 0),
    (6500, 1),

    # Verse 2 (kick2 + stick)
    (8500, 2),
    (9000, 1),
    (9500, 2),
    (10000, 1),
    (10500, 2),
    (11000, 1),

    # Dramatic transition: pre-chorus build-up (chime)
    (11500, 3),

    # Pre-chorus (kick only)
    (11500, 0),
    (12250, 0),
    (12750, 0),

    # Chorus (kick + stick + kick2)
    (13000, 0),
    (13500, 1),
    (14000, 2),
    (14500, 0),
    (15000, 1),
    (15500, 2),
    (16000, 0),
    (16500, 1),

    (17000, 2),
    (17500, 0),
    (18000, 1),
    (18500, 2),
    (19000, 0),
    (19500, 1),

    # Bridge (kick + stick + kick2)
    (20000, 0),
    (20500, 1),
    (21000, 2),

    # Dramatic transition: bridge → final chorus (chime)
    (21500, 3),

    # Final chorus (kick + stick + kick2)
    (21500, 0),
    (22000, 1),
    (22500, 2),
    (23000, 0),
    (23500, 1),
    (24000, 2),
    (24500, 0),
    (25000, 1),

    (25500, 2),
    (26000, 0),
    (26500, 1),
    (27000, 2),

    # Outro (kick + stick)
    (27500, 0),
    (28000, 1),

    # Gentle instrumental fade
    (28500, 1),   # stick
    (29000, 0),   # kick
    (29500, 1),   # stick

    # Sparse chime for subtle atmosphere
    (30000, 3),   # chime

    (30500, 0),   # kick
    (31000, 1),   # stick

    # Final soft chime for closure
    (31500, 3),

    # Last notes trailing off
    (32000, 0),   # kick
    (32500, 1),   # stick

    # End silence

    # Slow buildup after fade
    (33000, 1),   # stick
    (33500, 0),   # kick
    (34000, 1),   # stick

    # Dramatic chime moment
    (34500, 3),   # chime

    (35000, 2),   # kick2
    (35500, 0),   # kick
    (36000, 1),   # stick

    # Sparse chimes for tension
    (36500, 3),
    (37000, 3),

    (37500, 0),   # kick
    (38000, 1),   # stick

    # Another soft chime to close this phrase
    (38500, 3),

    (39000, 0),   # kick
    (39500, 1),   # stick
    (40000, 2),   # kick2
    (40500, 0),   # kick

    # Chime for dramatic shift
    (41000, 3),

    (41500, 1),   # stick
    (42000, 2),   # kick2
    (42500, 0),   # kick
    (43000, 1),   # stick

    # Sparse chimes to add tension
    (43500, 3),
    (44000, 3),

    (44500, 0),   # kick
    (45000, 2),   # kick2
    (45500, 1),   # stick

    # Dramatic chime again
    (46000, 3),

    (46500, 0),   # kick
    (47000, 1),   # stick
    (47500, 2),   # kick2
    (48000, 0),   # kick

    # Dramatic chime for transition
    (48500, 3),

    (49000, 1),   # stick
    (49500, 2),   # kick2
    (50000, 0),   # kick
    (50500, 1),   # stick

    # Sparse chime for tension
    (51000, 3),

    (51500, 0),   # kick
    (52000, 2),   # kick2
    (52500, 1),   # stick

    # Final chime before next section
    (53000, 3),

    (53500, 0),   # kick
    (54000, 1),   # stick
    (54500, 2),   # kick2
    (55000, 0),   # kick

    # Dramatic chime for emphasis
    (55500, 3),

    (56000, 1),   # stick
    (56500, 2),   # kick2
    (57000, 0),   # kick
    (57500, 1),   # stick

    # Light chime before next section
    (58000, 3),

    (58500, 0),   # kick
    (59000, 2),   # kick2
    (59500, 1),   # stick

    (60000, 0),   # kick
    (60500, 1),   # stick
    (61000, 2),   # kick2
    (61500, 0),   # kick

    # Dramatic chime highlight
    (62000, 3),

    (62500, 1),   # stick
    (63000, 2),   # kick2
    (63500, 0),   # kick
    (64000, 1),   # stick

    # Subtle chime for transition
    (64500, 3),

    (65000, 0),   # kick
    (65500, 2),   # kick2
    (66000, 1),   # stick
    (66500, 0),   # kick

    (67000, 0),   # kick
    (67500, 1),   # stick
    (68000, 2),   # kick2
    (68500, 0),   # kick

    # Dramatic chime accent
    (69000, 3),

    (69500, 1),   # stick
    (70000, 2),   # kick2
    (70500, 0),   # kick
    (71000, 1),   # stick

    # Light chime for mood
    (71500, 3),

    (72000, 0),   # kick
    (72500, 2),   # kick2
    (73000, 1),   # stick
    (73500, 0),   # kick

    (74000, 2),   # kick2
    (74500, 0),   # kick
    (75000, 1),   # stick

    # Dramatic chime
    (75500, 3),

    (76000, 0),   # kick
    (76500, 2),   # kick2
    (77000, 1),   # stick
    (77500, 0),   # kick

    # Subtle chime accent
    (78000, 3),

    (78500, 2),   # kick2
    (79000, 1),   # stick
    (79500, 0),   # kick
    (80000, 1),   # stick
    (80500, 0),   # kick
    (81000, 2),   # kick2

    # Dramatic chime for buildup
    (81500, 3),

    (82000, 0),   # kick
    (82500, 1),   # stick
    (83000, 2),   # kick2
    (83500, 0),   # kick

    # Subtle chime
    (84000, 3),

    (84500, 1),   # stick
    (85000, 2),   # kick2
    (85500, 0),   # kick

    (86000, 1),   # stick
    (86500, 0),   # kick
    (87000, 2),   # kick2

    # Dramatic chime to highlight change
    (87500, 3),

    (88000, 0),   # kick
    (88500, 1),   # stick
    (89000, 2),   # kick2
    (89500, 0),   # kick

    # Subtle chime
    (90000, 3),

    (90500, 1),   # stick
    (91000, 2),   # kick2
    (91500, 0),   # kick

    (92000, 1),    # stick
    (92500, 0),    # kick
    (93000, 2),    # kick2

    # Dramatic chime build-up
    (93500, 3),

    (94000, 0),    # kick
    (94500, 1),    # stick
    (95000, 2),    # kick2
    (95500, 0),    # kick

    # Small chime accent
    (96000, 3),

    (96500, 1),    # stick
    (97000, 2),    # kick2
    (97500, 0),    # kick

    (98000, 1),   # stick
    (98500, 0),   # kick
    (99000, 2),   # kick2

    # Dramatic chime for emphasis
    (99500, 3),

    (100000, 0),  # kick
    (100500, 1),  # stick
    (101000, 2),  # kick2

    (101500, 0),  # kick

    # Subtle chime during buildup
    (102000, 3),

    (102500, 1),  # stick
    (103000, 2),  # kick2
    (103500, 0),  # kick

    (104000, 1),  # stick
    (104500, 0),  # kick
    (105000, 2),  # kick2

    # Dramatic chime at transition
    (105500, 3),

    (106000, 0),  # kick
    (106500, 1),  # stick
    (107000, 2),  # kick2

    (107500, 0),  # kick
    (108000, 1),  # stick

    # Subtle chime for buildup
    (108500, 3),

    (109000, 2),  # kick2
    (109500, 0),  # kick

    (110000, 1),  # stick
    (110500, 0),  # kick
    (111000, 2),  # kick2

    # Dramatic chime for transition
    (111500, 3),

    (112000, 0),  # kick
    (112500, 1),  # stick
    (113000, 2),  # kick2

    (113500, 0),  # kick
    (114000, 1),  # stick

    # Subtle chime for buildup
    (114500, 3),

    (115000, 2),  # kick2
    (115500, 0),  # kick
    (116000, 1),  # stick

    (116500, 0),  # kick
    (117000, 2),  # kick2
    (117500, 1),  # stick

    # Dramatic chime for emphasis
    (118000, 3),

    (118500, 0),  # kick
    (119000, 1),  # stick
    (119500, 2),  # kick2

    (120000, 0),  # kick
    (120500, 1),  # stick

    # Soft chime for tension
    (121000, 3),

    (121500, 2),  # kick2
    (122000, 0),  # kick
    (122500, 1),  # stick

    (123000, 0),  # kick
    (123500, 2),  # kick2
    (124000, 1),  # stick

    # Dramatic chime for transition
    (124500, 3),

    (125000, 0),  # kick
    (125500, 1),  # stick
    (126000, 2),  # kick2

    (126500, 0),  # kick
    (127000, 1),  # stick

    # Soft chime for build-up
    (127500, 3),

    (128000, 2),  # kick2
    (128500, 0),  # kick
    (129000, 1),  # stick

    (130000, 0),  # kick
    (130500, 1),  # stick
    (131000, 2),  # kick2

    # Dramatic chime for transition
    (131500, 3),

    (132000, 0),  # kick
    (132500, 1),  # stick
    (133000, 2),  # kick2

    (133500, 0),  # kick
    (134000, 1),  # stick

    # Soft chime for build-up
    (134500, 3),

    (135000, 2),  # kick2
    (135500, 0),  # kick
    (136000, 1),  # stick

    (136500, 2),  # kick2
    (137000, 0),  # kick
    (137500, 1),  # stick

    # Dramatic chime to emphasize build-up
    (138000, 3),

    (138500, 0),  # kick
    (139000, 1),  # stick
    (139500, 2),  # kick2

    (140000, 0),  # kick
    (140500, 1),  # stick

    # Small chime to highlight transition
    (141000, 3),

    (141500, 2),  # kick2
    (142000, 0),  # kick
    (142500, 1),  # stick

    (143000, 0),  # kick
    (143500, 2),  # kick2
    (144000, 1),  # stick

    # Dramatic chime for effect
    (144500, 3),

    (145000, 0),  # kick
    (145500, 1),  # stick
    (146000, 2),  # kick2

    (146500, 0),  # kick
    (147000, 1),  # stick

    # Chime for subtle build-up
    (147500, 3),

    (148000, 2),  # kick2
    (148500, 0),  # kick
    (149000, 1),  # stick

    (149500, 0),  # kick
    (150000, 2),  # kick2
    (150500, 1),  # stick

    # Dramatic chime for emphasis
    (151000, 3),

    (151500, 0),  # kick
    (152000, 1),  # stick
    (152500, 2),  # kick2

    (153000, 0),  # kick
    (153500, 1),  # stick

    # Subtle chime during transition
    (154000, 3),

    (154500, 2),  # kick2
    (155000, 0),  # kick
    (155500, 1),  # stick

    (156000, 0),  # kick
    (156500, 2),  # kick2
    (157000, 1),  # stick

    # Dramatic chime for build-up
    (157500, 3),

    (158000, 0),  # kick
    (158500, 1),  # stick
    (159000, 2),  # kick2

    (159500, 0),  # kick
    (160000, 1),  # stick

    # Subtle chime marking phrase end
    (160500, 3),

    (161000, 2),  # kick2
    (161500, 0),  # kick
    (162000, 1),  # stick

    (162500, 0),  # kick
    (163000, 1),  # stick
    (163500, 2),  # kick2

    # Chime for subtle build-up
    (164000, 3),

    (164500, 0),  # kick
    (165000, 1),  # stick
    (165500, 2),  # kick2

    (166000, 0),  # kick
    (166500, 1),  # stick

    # Dramatic chime
    (167000, 3),

    (167500, 2),  # kick2
    (168000, 0),  # kick
    (168500, 1),  # stick

    (169000, 0),  # kick
    (169500, 1),  # stick
    (170000, 2),  # kick2

    # Dramatic chime to highlight change
    (170500, 3),

    (171000, 0),  # kick
    (171500, 1),  # stick
    (172000, 2),  # kick2

    (172500, 0),  # kick
    (173000, 1),  # stick

    # Subtle chime build-up
    (173500, 3),

    (174000, 2),  # kick2
    (174500, 0),  # kick
    (175000, 1),  # stick

    (175500, 0),  # kick
    (176000, 1),  # stick
    (176500, 2),  # kick2

    # Dramatic chime accent
    (177000, 3),

    (177500, 0),  # kick
    (178000, 1),  # stick
    (178500, 2),  # kick2

    (179000, 0),  # kick
    (179500, 1),  # stick

    # Subtle chime to keep tension
    (180000, 3),

    (180500, 2),  # kick2
    (181000, 0),  # kick
    (181500, 1),  # stick

    (182000, 0),  # kick
    (182500, 1),  # stick
    (183000, 2),  # kick2

    # Dramatic chime accent
    (183500, 3),

    (184000, 0),  # kick
    (184500, 1),  # stick
    (185000, 2),  # kick2

    (185500, 0),  # kick
    (186000, 1),  # stick

    # Subtle chime buildup
    (186500, 3),

    (187000, 2),  # kick2
    (187500, 0),  # kick
    (188000, 1),  # stick

    (188500, 0),  # kick
    (189000, 1),  # stick
    (189500, 2),  # kick2

    # Dramatic chime accent before chorus
    (190000, 3),

    (190500, 0),  # kick
    (191000, 1),  # stick
    (191500, 2),  # kick2

    (192000, 0),  # kick
    (192500, 1),  # stick

    # Soft chime to transition
    (193000, 3),

    (193500, 2),  # kick2
    (194000, 0),  # kick
    (194500, 1),  # stick

    (195000, 0),  # kick
    (195500, 1),  # stick
    (196000, 2),  # kick2

    # Dramatic chime for emphasis
    (196500, 3),

    (197000, 0),  # kick
    (197500, 1),  # stick
    (198000, 2),  # kick2

    (198500, 0),  # kick
    (199000, 1),  # stick

    # Light chime for subtle build-up
    (199500, 3),

    (200000, 2),  # kick2
    (200500, 0),  # kick
    (201000, 1),  # stick

    (201500, 0),  # kick
    (202000, 2),  # kick2
    (202500, 1),  # stick

    # Subtle chime for transition
    (203000, 3),

    (203500, 0),  # kick
    (204000, 2),  # kick2
    (204500, 1),  # stick

    (205000, 0),  # kick
    (205500, 1),  # stick
    (206000, 2),  # kick2

    # Dramatic chime for emphasis
    (206500, 3),

    (207000, 0),  # kick
    (207500, 1),  # stick
    (208000, 2),  # kick2

    (208500, 0),
    (209000, 2),

    # Chime for dramatic buildup
    (209500, 3),

    (210000, 1),
    (210500, 0),
    (211000, 2),
    (211500, 1),

    (212000, 0),
    (212500, 2),

    (213000, 0),
    (213500, 1),
    (214000, 0),

    (214500, 2),
    (215000, 1),

    # Chime for subtle effect
    (215500, 3),

    (216000, 0),
    (216500, 2),
    (217000, 1),

    (217500, 0),
    (218000, 2),
    (218500, 0),

    (219000, 1),
    (219500, 0),

    (220000, 2),
    (220500, 1),

    (221000, 0),

    # Chime for transition
    (221500, 3),

    (222000, 1),
    (222500, 2),

    (223000, 0),
    (223500, 1),
    (224000, 2),

    (224500, 0),

    (225000, 1),
    (225500, 0),
    (226000, 2),
    (226500, 1),

    (227000, 0),
    (227500, 3),  # Chime for dramatic effect

    (228000, 2),
    (228500, 1),
    (229000, 0),
    (229500, 2),
    (230000, 1),
    
    (230500, 0),
    (231000, 1),
    (231500, 2),
    (232000, 0),
    (232500, 3),  # Chime for dramatic effect
    (233000, 1),
    (233500, 2),
    (234000, 0),
    (234500, 1),
    (235000, 2),

    (235500, 0),
    (236000, 1),
    (236500, 2),
    (237000, 3),  # Chime - dramatic effect
    (237500, 0),
    (238000, 1),
    (238500, 2),
    (239000, 0),
    (239500, 1),
    (240000, 2),
    (240500, 0),

    (241000, 0),
    (241500, 1),
    (242000, 2),
    (242500, 3),  # Chime - dramatic buildup
    (243000, 0),
    (243500, 1),
    (244000, 0),
    (244500, 2),
    (245000, 1),
    (245500, 0),
    (246000, 2),

    (246500, 3),  # Chime - subtle dramatic effect
    (247000, 0),
    (247500, 1),
    (248000, 2),
    (248500, 0),
    (249000, 1),
    (249500, 2),
    (250000, 0),
    (250500, 3),  # Chime - transition moment
    (251000, 1),
    (251500, 0),

    (252000, 0),
    (252500, 2),
    (253000, 1),
    (253500, 0),
    (254000, 3),  # Chime - subtle build-up
    (254500, 1),
    (255000, 2),
    (255500, 0),
    (256000, 1),
    (256500, 2),
    (257000, 0),
    (257500, 3),  # Chime - dramatic effect

    (258000, 0),
    (258500, 1),
    (259000, 2),
    (259500, 0),
    (260000, 3),  # Chime - subtle build-up
    (260500, 1),
    (261000, 0),
    (261500, 2),
    (262000, 1),
    (262500, 0),
    (263000, 3),  # Chime - dramatic effect
    (263500, 2),

    (264000, 0),
    (264500, 1),
    (265000, 0),
    (265500, 2),
    (266000, 3),  # Chime - dramatic highlight
    (266500, 0),
    (267000, 1),
    (267500, 2),
    (268000, 0),
    (268500, 1),
    (269000, 3),  # Chime - subtle build-up
    (269500, 2),            
]

suki = [
    # Start immediately with kick at 0ms
    (0, 0),

    # Intro (kick + stick alternating, steady 500ms)
    (500, 1),
    (1000, 0),
    (1500, 1),
    (2000, 0),
    (2500, 1),

    # Dramatic chime before verse
    (2900, 3),

    # Verse 1 (kick + stick + occasional kick2, every 375ms for more groove)
    (3000, 0),
    (3375, 1),
    (3750, 0),
    (4125, 2),
    (4500, 1),
    (4875, 0),
    (5250, 2),
    (5625, 1),

    # Pre-chorus (kick only, faster pace)
    (6000, 0),
    (6350, 0),
    (6700, 0),
    (7050, 0),

    # Chorus (kick + stick + kick2, steady 375ms)
    (7400, 0),
    (7775, 1),
    (8150, 2),
    (8525, 0),
    (8900, 1),
    (9275, 2),
    (9650, 0),
    (10025, 1),

    # Chime buildup before bridge
    (10400, 3),

    # Bridge (stick + kick2 interplay, steady 375ms)
    (10750, 1),
    (11125, 2),
    (11500, 1),
    (11875, 2),
    (12250, 1),
    (12625, 2),

    # Outro (kick + stick slowing down, 500ms)
    (13100, 0),
    (13600, 1),
    (14100, 0),
    (14600, 1),

    # Final chime
    (15000, 3),

    (15500, 2),
    (15875, 1),
    (16250, 2),
    (16625, 1),

    # Quick kick hits for tension
    (17000, 0),
    (17250, 0),
    (17500, 0),
    (17750, 0),

    # Chime for dramatic effect
    (18000, 3),

    # Chorus reprise, more dense notes
    (18300, 0),
    (18675, 1),
    (19050, 2),
    (19425, 0),
    (19800, 1),
    (20175, 2),
    (20550, 0),
    (20925, 1),

    # Bridge variation, add stick-kick interplay faster
    (21300, 1),
    (21525, 0),
    (21750, 2),
    (21975, 1),
    (22200, 0),
    (22425, 2),

    # Outro closing with slowed hits and sparse chimes
    (22750, 0),
    (23250, 1),
    (23750, 0),
    (24250, 1),
    (24750, 3),

    # Build-up with alternating kick and stick, steady but denser
    (25200, 0),
    (25575, 1),
    (25950, 0),
    (26325, 1),
    (26700, 2),
    (27075, 1),
    (27450, 0),
    (27825, 2),

    # Chime for dramatic effect
    (28200, 3),

    # Quick alternating stick and kick2 patterns (no double hits)
    (28575, 1),
    (28950, 2),
    (29325, 1),
    (29700, 2),
    (30075, 1),
    (30450, 2),

    # Kick & stick interplay with varied spacing
    (30825, 0),
    (31200, 1),
    (31575, 0),
    (31950, 1),

    # Subtle chime for transition
    (32325, 3),

    # Final section with more stick and kick2 hits, spaced to keep flow
    (32700, 2),
    (33075, 1),
    (33450, 2),
    (33825, 0),
    (34200, 1),

    # Start with steady kicks and sticks, more variation
    (34575, 0),
    (34950, 1),
    (35325, 0),
    (35700, 2),
    (36075, 1),
    (36450, 0),

    # Chime for dramatic effect to mark transition
    (36825, 3),

    
]



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
        if note.hit_colour is not None:
            if note.hit_timer <= 0:
                notes.remove(note)
            continue

        if note.y > HIT_Y + MISS_MARGIN:
            points += MISS
            note.hit_colour = HIT_COLOURS["MISS"]
            note.hit_timer = DISAPPEAR_TIME
            
    return points

def spawn_notes(map, notes, lanes, elapsed_time, spawned_index):
    while spawned_index < len(map) and elapsed_time >= map[spawned_index][0]:
        spawn_time, lane_idx = map[spawned_index]
        lane_x = lanes[lane_idx]
        notes.append(Note(lane_x, -100, 50, 50, BLUE))
        spawned_index += 1
    return spawned_index

def checkKeys(event, flash_timers, notes, lanes, points, sounds):
    add_points = 0
    if event.type == pygame.KEYDOWN and event.key in KEY_TO_LANE:
        lane_index = KEY_TO_LANE[event.key]
        flash_timers[lane_index] = FLASH_DURATION # flash the lane

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
            if hit_note.y < HIT_Y - OKAY_THRESHOLD - 100: # miss
                add_points = MISS
                hit_note.hit_colour = HIT_COLOURS["MISS"]
            elif best_distance <= PERFECT_THRESHOLD: # add 200 points
                add_points = PERFECT
                hit_note.hit_colour = HIT_COLOURS["PERFECT"]
                sounds[lane_index].play()
            elif best_distance <= GOOD_THRESHOLD: # add 100 points
                add_points = GOOD
                hit_note.hit_colour = HIT_COLOURS["GOOD"]
                sounds[lane_index].play()
            elif best_distance <= OKAY_THRESHOLD: # add 50 points
                add_points = OKAY
                hit_note.hit_colour = HIT_COLOURS["OKAY"]
                sounds[lane_index].play()
            else:
                add_points = BAD
                hit_note.hit_colour = HIT_COLOURS["BAD"]

            hit_note.hit_timer = DISAPPEAR_TIME
    
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
    music_file = "music/lionHeart.mp3"
    sound = "sfx/kick.mp3"
    sound2 = "sfx/stick.mp3"
    sound3 = "sfx/kick2.mp3"
    sound4 = "sfx/chime.mp3"

    songName = lionHeart

    # load audio
    pygame.mixer.music.load(music_file)

    soundList = []
    kick = pygame.mixer.Sound(sound)
    stick = pygame.mixer.Sound(sound2)
    kick2 = pygame.mixer.Sound(sound3)
    chime = pygame.mixer.Sound(sound4)
    soundList.append(kick)
    soundList.append(stick)
    soundList.append(kick2)
    soundList.append(chime)

    # play audio
    pygame.mixer.music.play()

    lanes = [LANE_START_X + i * LANE_GAP for i in range(LANE_COUNT)]
    circle_pos_y = HIT_Y

    # setup variables
    flash_timers = [0] * LANE_COUNT
    notes = []
    points = 0

    spawn_index = 0
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            else:
                flash_timers, points = checkKeys(event, flash_timers, notes, lanes, points, soundList)

        points = update_notes(notes, dt, points)

        elapsed_time = pygame.time.get_ticks() - start_ticks + SONG_DELAY
        spawn_index = spawn_notes(songName, notes, lanes, elapsed_time, spawn_index)

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


