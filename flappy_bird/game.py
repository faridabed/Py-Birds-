# Import module
import random
import sys
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
# All the Game Variables
WIDTH = 1000
HEIGHT = 800
FRAMES_PER_SECOND = 32
obstacle = 'images/obstacle.png'
BACKGROUND = 'images/background-3.png'
BIRD = 'images/bird.png'
BASE = 'images/base.png'

# Couleur
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu du jeu")

BACKGROUND_MENU = pygame.image.load('images/background_menu.png').convert()
elevation = HEIGHT * 1.5
images = {}

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():

    while True:

        window.blit(BACKGROUND_MENU, (0, 0))

        draw_text('Main Menu', pygame.font.Font(None, 150), WHITE, window, 20, 20)

        mx, my = pygame.mouse.get_pos()

        # Boutons
        button_start = pygame.Rect(50, 200, 200, 90)
        button_quit = pygame.Rect(50, 360, 200, 90)
        button_rules = pygame.Rect(50, 520, 200, 90)

        if button_start.collidepoint((mx, my)):
            if click:
                # Commencer le jeu
                game()  # Assurez-vous d'avoir une fonction appelée `game` pour démarrer le jeu
        if button_quit.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        if button_rules.collidepoint((mx, my)):
            if click:
                rules()  # Affiche les règles; implémentez cette fonction selon vos besoins

        pygame.draw.rect(window, [254, 204, 0], button_start)
        pygame.draw.rect(window, [254, 204, 0], button_quit)
        pygame.draw.rect(window, [254, 204, 0], button_rules)

        draw_text('Start', pygame.font.Font(None, 70), WHITE, window, 70, 225)
        draw_text('Quit', pygame.font.Font(None, 70), WHITE, window, 70, 385)
        draw_text('Rules', pygame.font.Font(None, 70), WHITE, window, 70, 545)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def game ():
    def run():

        score = 0  # initialize game score to 0
        h = int(WIDTH / 5)  # set the horizontal position of the bird
        v = int(WIDTH / 2)  # set the vertical position of the bird
        base = 0  # initialize the base (ground) position
        temp_height = 100  # set the height of the obstacles

        # create the first two obstacles
        first_obstacle = create_obstacle()
        second_obstacle = create_obstacle()

        # set the initial positions of the down-facing obstacles
        down_obstacles = [
            {'x': WIDTH + 300 - temp_height,
             'y': first_obstacle[1]['y']},
            {'x': WIDTH + 300 - temp_height + (WIDTH / 2),
             'y': second_obstacle[1]['y']},
        ]

        # set the initial positions of the up-facing obstacles
        up_obstacles = [
            {'x': WIDTH + 300 - temp_height,
             'y': first_obstacle[0]['y']},
            {'x': WIDTH + 200 - temp_height + (WIDTH / 2),
             'y': second_obstacle[0]['y']},
        ]

        obstacle_speed = -4  # set the speed at which obstacles move

        bird_speed = -9  # set the initial speed of the bird
        max_bird_speed = 10  # set the maximum speed of the bird
        bird_accleration = 1  # set the acceleration of the bird

        bird_flap_speed = -8  # set the speed at which the bird flaps
        is_bird_flapped = False  # initialize whether or not the bird has flapped
        game_over = False  # initialize whether or not the game is over

        while not game_over:  # loop until the game is over
            for event in pygame.event.get():  # check for events
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    # quit the game if the user closes the window or presses escape
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    # flap the bird if the user presses space or up arrow
                    if v > 0:
                        bird_speed = bird_flap_speed
                        is_bird_flapped = True

            # check if the player has crashed into an obstacle
            game_over = player_crashed(h, v, up_obstacles, down_obstacles)
            if game_over:
                return

            # check if the bird has passed an obstacle, and increment the score if so
            bird_center_pos = h + images['bird'].get_width() / 2
            for obstacle in up_obstacles:
                obstacle_center_pos = obstacle['x'] + images['obstacle'][0].get_width() / 2
                if obstacle_center_pos <= bird_center_pos < obstacle_center_pos + 4:
                    score += 1
                    print(f"Score: {score}")



            # update the bird's speed and position
            if bird_speed < max_bird_speed and not is_bird_flapped:
                bird_speed += bird_accleration

            if is_bird_flapped:
                is_bird_flapped = False
            playerHeight = images['bird'].get_height()
            v = v + \
                min(bird_speed, elevation - v - playerHeight)

            # move the obstacles to the left
            for upperPipe, lowerPipe in zip(up_obstacles, down_obstacles):
                upperPipe['x'] += obstacle_speed
                lowerPipe['x'] += obstacle_speed

            # create a new pair of obstacles if the first pair is about to exit the screen
            if 0 < up_obstacles[0]['x'] < 5:
                newobstacle = create_obstacle()
                up_obstacles.append(newobstacle[0])
                down_obstacles.append(newobstacle[1])

            # remove the first pair of obstacles from the list if they exit the screen
            if up_obstacles[0]['x'] < -images['obstacle'][0].get_width():
                up_obstacles.pop(0)
                down_obstacles.pop(0)

            # blit the background, obstacles, and bird onto the screen
            window.blit(images['background'], (0, 0))
            for upperPipe, lowerPipe in zip(up_obstacles, down_obstacles):
                window.blit(images['obstacle'][0],
                            (upperPipe['x'], upperPipe['y']))
                window.blit(images['obstacle'][1],
                            (lowerPipe['x'], lowerPipe['y']))

            window.blit(images['base'], (base, elevation))
            window.blit(images['bird'], (h, v))

            # display the score on the screen
            numbers = [int(x) for x in list(str(score))]
            width = 0

            for num in numbers:
                width += images['score'][num].get_width()
            Xshift = (WIDTH - width) / 1.1

            for num in numbers:
                window.blit(images['score'][num],
                            (Xshift, WIDTH * 0.02))
                Xshift += images['score'][num].get_width()

            pygame.display.update()
            FRAMES_PER_SECOND_clock.tick(FRAMES_PER_SECOND)

    def player_crashed(h_position, v_position, upper_obstacles, lower_obstacles):
        # Check if bird has hit the base or flown too high
        if v_position > elevation - 25 or v_position < 0:
            return True
        for obstacle in upper_obstacles:
            obstacle_height = images['obstacle'][0].get_height()
            if (v_position < obstacle_height + obstacle['y']) and \
                    abs(h_position - obstacle['x']) < images['obstacle'][0].get_width():
                return True

        # Check if bird has collided with lower obstacles
        for obstacle in lower_obstacles:
            if (v_position + images['bird'].get_height() > obstacle['y']) and \
                    abs(h_position - obstacle['x']) < images['obstacle'][0].get_width():
                return True

        return False

    def create_obstacle():
        # set an shift for the gap between obstacles
        shift = HEIGHT / 3

        # get the height of a single obstacle image
        obstacle_height = images['obstacle'][0].get_height()

        # set the y-coordinate of the bottom of the gap between obstacles randomly
        y2 = shift + random.randrange(0, int(HEIGHT - images['base'].get_height() - 1.2 * shift))

        # set the x-coordinate of the obstacles off the right side of the screen
        obstacle_x = WIDTH + 10

        # calculate the y-coordinate of the top of the gap based on the bottom of the gap and the obstacle height
        y1 = obstacle_height - y2 + shift

        # create a dictionary for each obstacle with its x and y coordinates
        obstacle = [
            # upper obstacle
            {'x': obstacle_x, 'y': -y1},

            # lower obstacle
            {'x': obstacle_x, 'y': y2}
        ]

        return obstacle

    if __name__ == "__main__":
        # For initializing modules of pygame library
        pygame.init()
        FRAMES_PER_SECOND_clock = pygame.time.Clock()

        # Sets the title on top of game window
        pygame.display.set_caption('Flappy Bird Game')

        # Load all the images which we will use in the game
        images['score'] = tuple(pygame.image.load(f'images/{i}.png').convert_alpha() for i in range(10))
        images['bird'] = pygame.image.load(BIRD).convert_alpha()
        images['base'] = pygame.image.load(BASE).convert_alpha()
        images['background'] = pygame.image.load(BACKGROUND).convert_alpha()
        images['obstacle'] = (pygame.transform.rotate(pygame.image.load(obstacle).convert_alpha(), 180),
                              pygame.image.load(obstacle).convert_alpha())

        print("Welcome!")
        print("Press space to jump")

        # Here starts the main game
        while True:
            # sets the coordinates of flappy bird
            h = int(WIDTH / 5)
            v = int((HEIGHT - images['bird'].get_height()) / 2)
            base = 0

            for event in pygame.event.get():
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # If the user presses space or up key, start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    run()
            # if user doesn't press any key, display the game without any action
            window.blit(images['background'], (0, 0))
            window.blit(images['bird'], (h, v))
            window.blit(images['base'], (base, elevation))
            pygame.display.update()
            FRAMES_PER_SECOND_clock.tick(FRAMES_PER_SECOND)
    pass


def rules():
    running = True
    while running:
        window.fill(BLACK)  # Remplir l'arrière-plan

        # Afficher les règles
        draw_text('Règles du jeu', pygame.font.Font(None, 40), WHITE, window, 20, 20)
        rules_text = [
            "1. Appuyez sur ESPACE ou HAUT pour sauter.",
            "2. Évitez les obstacles pour gagner des points.",
            "3. Le jeu se termine si vous touchez un obstacle.",
            "",
            "Appuyez sur ESC pour retourner au menu principal."
        ]

        for i, line in enumerate(rules_text):
            draw_text(line, pygame.font.Font(None, 32), WHITE, window, 20, 100 + i * 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Retour au menu principal
                    running = False

        pygame.display.update()

if __name__ == "__main__":
    main_menu()



