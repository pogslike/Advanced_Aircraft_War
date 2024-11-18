import pgzrun  # 
import random  # 

# Screen dimensions
WIDTH = 480
HEIGHT = 800
TITLE = 'Python Aircraft'

# Define initial game states
show_start_screen = True  # Indicates whether the start screen is active
game_started = False  # Indicates whether the game has started

# Load the start button with default image
start_button = Actor('start_no')
start_button.pos = (WIDTH // 2, HEIGHT // 2)

# Define other game elements
background1 = Actor('background')
background1.x = 480 / 2
background1.y = 852 / 2
background2 = Actor('background')
background2.x = 480 / 2
background2.y = -852 / 2

hero = Actor('hero')
hero.x = WIDTH / 2
hero.y = HEIGHT * 2 / 3

enemy = Actor('enemy')
enemy.x = WIDTH / 2
enemy.y = 0

bullets = []  # List to store multiple bullets
score = 0
isLoose = False

# Game sounds
sounds.game_music.play(-1)


# Function to draw everything on the screen
def draw():
    if show_start_screen:
        screen.clear()
        start_button.draw()  # Draw the start button
    else:
        background1.draw()
        background2.draw()
        hero.draw()
        enemy.draw()
        for bullet in bullets:
            bullet.draw()
        screen.draw.text("score: " + str(score), (200, HEIGHT - 50),
                         fontsize=30, fontname='s', color='black')
        if isLoose:
            screen.draw.text("Fail!", (50, HEIGHT / 2),
                             fontsize=90, fontname='s', color='red')


# Function to update the game state
def update():
    global show_start_screen, score, isLoose

    # If start screen is active, skip updating the game elements
    if show_start_screen:
        return

    if isLoose:
        return

    # Move the backgrounds for the scrolling effect
    if background1.y > 852 / 2 + 852:
        background1.y = -852 / 2
    if background2.y > 852 / 2 + 852:
        background2.y = -852 / 2
    background1.y += 1
    background2.y += 1

    # Update bullets
    for bullet in bullets[:]:  # Iterate over a copy of the bullets list
        bullet.y -= 10  # Move the bullet upwards
        if bullet.y < 0:  # Remove bullets that move off the screen
            bullets.remove(bullet)
        elif bullet.colliderect(enemy):  # Check for collisions with the enemy
            sounds.got_enemy.play()
            enemy.y = 0
            enemy.x = random.randint(50, WIDTH - 50)
            score += 1
            bullets.remove(bullet)

    # Move the enemy
    enemy.y += 3
    if enemy.y > HEIGHT:  # Reset enemy position when it moves off screen
        enemy.y = 0
        enemy.x = random.randint(50, WIDTH - 50)

    # Check collision between hero and enemy
    if hero.colliderect(enemy):
        sounds.explode.play()
        isLoose = True
        hero.image = 'hero_blowup'


# Handle mouse movement
def on_mouse_move(pos, rel, buttons):
    global show_start_screen

    if show_start_screen:
        # Switch button image based on mouse hover
        if start_button.collidepoint(pos):
            start_button.image = 'start_yes'
        else:
            start_button.image = 'start_no'
    else:
        if isLoose:
            return
        hero.x = pos[0]
        hero.y = pos[1]


# Handle mouse clicks
def on_mouse_down(pos):
    global show_start_screen, game_started

    if show_start_screen:
        # Check if the start button is clicked
        if start_button.collidepoint(pos):
            sounds.gun.play()  # Play click sound (optional)
            show_start_screen = False  # Hide start screen
            game_started = True  # Start the game
    else:
        if isLoose:
            return
        # Create a new bullet and set its position
        bullet = Actor('bullet')
        bullet.x = hero.x
        bullet.y = hero.y - 70
        bullets.append(bullet)


pgzrun.go()
