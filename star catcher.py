import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STAR CATCHER CHALLENGE")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("arial", 28, bold=True)
big_font = pygame.font.SysFont("arial", 65, bold=True)
small_font = pygame.font.SysFont("arial", 20)

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 220, 50)
CYAN = (40, 220, 255)
PURPLE = (100, 40, 180)
DARK = (8, 10, 35)

# Player
player = pygame.Rect(WIDTH // 2 - 45, HEIGHT - 90, 90, 45)
player_speed = 8

# Game variables
score = 0
lives = 3
stars = []
particles = []
game_over = False
star_timer = 0

# Background stars
background_stars = [
    (random.randint(0, WIDTH), random.randint(0, HEIGHT),
     random.randint(1, 3))
    for _ in range(100)
]


def draw_background():
    screen.fill(DARK)

    # Space gradient
    for y in range(HEIGHT):
        color = (
            8 + int(y / HEIGHT * 12),
            10 + int(y / HEIGHT * 5),
            35 + int(y / HEIGHT * 35)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    # Twinkling background stars
    for x, y, size in background_stars:
        brightness = random.randint(130, 255)
        pygame.draw.circle(
            screen,
            (brightness, brightness, 255),
            (x, y),
            size
        )


def draw_star(x, y, radius, color):
    points = []

    for i in range(10):
        angle = math.radians(i * 36 - 90)

        if i % 2 == 0:
            r = radius
        else:
            r = radius * 0.45

        px = x + math.cos(angle) * r
        py = y + math.sin(angle) * r
        points.append((px, py))

    pygame.draw.polygon(screen, color, points)


def create_star():
    x = random.randint(35, WIDTH - 35)

    stars.append({
        "x": x,
        "y": -30,
        "speed": random.randint(3, 6) + score // 100,
        "size": random.randint(15, 23)
    })


def draw_player():
    x = player.centerx
    y = player.centery

    # Glow
    pygame.draw.ellipse(
        screen, (20, 100, 180),
        (x - 55, y - 10, 110, 65)
    )

    # Spaceship body
    pygame.draw.polygon(
        screen, CYAN,
        [
            (x, y - 35),
            (x + 45, y + 20),
            (x + 25, y + 12),
            (x, y + 22),
            (x - 25, y + 12),
            (x - 45, y + 20)
        ]
    )

    # Cockpit
    pygame.draw.circle(screen, WHITE, (x, y - 5), 12)
    pygame.draw.circle(screen, (30, 100, 200), (x, y - 5), 8)

    # Wings
    pygame.draw.polygon(
        screen, (30, 120, 220),
        [(x - 30, y + 10), (x - 48, y + 35), (x - 15, y + 20)]
    )

    pygame.draw.polygon(
        screen, (30, 120, 220),
        [(x + 30, y + 10), (x + 48, y + 35), (x + 15, y + 20)]
    )


def draw_hud():
    # Score panel
    pygame.draw.rect(
        screen, (25, 30, 75),
        (20, 20, 210, 65), border_radius=15
    )

    score_text = font.render(f"SCORE: {score}", True, YELLOW)
    screen.blit(score_text, (38, 37))

    # Lives panel
    pygame.draw.rect(
        screen, (25, 30, 75),
        (WIDTH - 200, 20, 180, 65), border_radius=15
    )

    lives_text = font.render(f"LIVES: {lives}", True, CYAN)
    screen.blit(lives_text, (WIDTH - 185, 37))


def add_particles(x, y):
    for _ in range(12):
        particles.append({
            "x": x,
            "y": y,
            "dx": random.uniform(-3, 3),
            "dy": random.uniform(-4, 2),
            "life": 25
        })


def reset_game():
    global score, lives, stars, particles
    global game_over, star_timer

    score = 0
    lives = 3
    stars = []
    particles = []
    game_over = False
    star_timer = 0
    player.centerx = WIDTH // 2


# Main game loop
running = True

while running:

    clock.tick(60)

    draw_background()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_over and event.key == pygame.K_r:
                reset_game()

            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    if not game_over:

        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed

        player.x = max(0, min(WIDTH - player.width, player.x))

        # Create falling stars
        star_timer += 1

        spawn_delay = max(18, 45 - score // 30)

        if star_timer >= spawn_delay:
            create_star()
            star_timer = 0

        # Move stars
        for star in stars[:]:

            star["y"] += star["speed"]

            star_rect = pygame.Rect(
                star["x"] - star["size"],
                star["y"] - star["size"],
                star["size"] * 2,
                star["size"] * 2
            )

            # Catch star
            if player.colliderect(star_rect):

                score += 10
                add_particles(star["x"], star["y"])
                stars.remove(star)

            # Missed star
            elif star["y"] > HEIGHT:

                lives -= 1
                stars.remove(star)

                if lives <= 0:
                    game_over = True

        # Draw stars
        for star in stars:
            # Outer glow
            pygame.draw.circle(
                screen, (100, 80, 20),
                (int(star["x"]), int(star["y"])),
                star["size"] + 9
            )

            draw_star(
                int(star["x"]),
                int(star["y"]),
                star["size"],
                YELLOW
            )

    # Particle effects
    for p in particles[:]:

        p["x"] += p["dx"]
        p["y"] += p["dy"]
        p["life"] -= 1

        if p["life"] <= 0:
            particles.remove(p)
        else:
            pygame.draw.circle(
                screen, CYAN,
                (int(p["x"]), int(p["y"])),
                3
            )

    # Draw player and HUD
    draw_player()
    draw_hud()

    # Instructions
    instruction = small_font.render(
        "MOVE: LEFT / RIGHT ARROWS OR A / D",
        True, WHITE
    )
    screen.blit(
        instruction,
        (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 25)
    )

    # Game over screen
    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(210)
        overlay.fill((5, 5, 25))
        screen.blit(overlay, (0, 0))

        title = big_font.render("GAME OVER", True, YELLOW)
        final_score = font.render(
            f"FINAL SCORE: {score}", True, WHITE
        )
        restart = font.render(
            "PRESS R TO RESTART", True, CYAN
        )
        quit_text = small_font.render(
            "PRESS ESC TO QUIT", True, WHITE
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 190)
        )

        screen.blit(
            final_score,
            (WIDTH // 2 - final_score.get_width() // 2, 290)
        )

        screen.blit(
            restart,
            (WIDTH // 2 - restart.get_width() // 2, 355)
        )

        screen.blit(
            quit_text,
            (WIDTH // 2 - quit_text.get_width() // 2, 410)
        )

    pygame.display.flip()

pygame.quit()
sys.exit()