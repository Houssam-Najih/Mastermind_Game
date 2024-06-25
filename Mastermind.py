import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des dimensions de la fenêtre
WIDTH, HEIGHT, FPS = 500, 600, 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mastermind Game')
clock = pygame.time.Clock()

# Couleurs utilisées dans le jeu
COLORS = {
    'bg': (110, 11, 20), 'green': (0, 255, 0), 'blue': (0, 0, 255), 'purple': (128, 0, 128),
    'white': (255, 255, 255), 'gray': (128, 128, 128), 'black': (0, 0, 0), 'red': (255, 0, 0),
    'orange': (255, 165, 0), 'yellow': (255, 255, 0), 'light_gray': (211, 211, 211)
}

# Choix des couleurs et réponse à deviner
CHOICE_COLORS = ['green', 'blue', 'purple', 'red', 'orange', 'yellow']
ANSWER_COLORS = [random.choice(CHOICE_COLORS) for _ in range(4)]

# Initialisation des variables de jeu
guess_colors = [[COLORS['white']] * 4 for _ in range(10)]
feedback_colors = [[COLORS['white']] * 4 for _ in range(10)]
selected_color, solved_color = COLORS['white'], COLORS['black']
selected_index, turn, menu_active, check_guess, game_over, win = 0, 0, False, False, False, False

# Images et police de caractères
font = pygame.font.Font('freesansbold.ttf', 20)
menu_img = pygame.transform.scale(pygame.image.load('MASTERMIND.jpeg'), (WIDTH // 2, HEIGHT // 2))


# Classe pour les boutons
class Button:
    def __init__(self, text, pos, size):
        self.text, self.rect = text, pygame.Rect(pos, size)

    def draw(self):
        pygame.draw.rect(screen, COLORS['gray'], self.rect)
        pygame.draw.rect(screen, COLORS['black'], self.rect, 5)
        text_surface = font.render(self.text, True, COLORS['black'])
        screen.blit(text_surface, (self.rect.x + self.rect.width / 4, self.rect.y + self.rect.height / 3))


# Initialisation des boutons
menu_btn = Button('Menu', (3 * WIDTH // 4, 12 * HEIGHT // 13), (25 * WIDTH // 100, HEIGHT // 13))
submit_btn = Button('Submit', (WIDTH // 3, 12 * HEIGHT // 13), (45 * WIDTH // 100, HEIGHT // 13))
start_btn = Button('Start', (0, 12 * HEIGHT // 13), (40 * WIDTH // 100, HEIGHT // 13))


# Fonction pour dessiner l'écran de jeu
def dessiner_écran():
    screen.fill(COLORS['bg'])
    pygame.draw.rect(screen, COLORS['light_gray'], [0, 10 * HEIGHT // 13 - turn * HEIGHT // 13, WIDTH, HEIGHT // 13])

    for i in range(10):
        for j in range(4):
            pygame.draw.circle(screen, guess_colors[i][j],
                               (WIDTH // 5 * (j + 1.5), (11 * HEIGHT // 13) - (HEIGHT // 13 * i) - HEIGHT // 26),
                               HEIGHT // 30)
            row, col = j // 2, j % 2
            pygame.draw.circle(screen, feedback_colors[i][j], (
            25 + (col * WIDTH // 12), (11 * HEIGHT // 13) - (HEIGHT // 13 * i) - (HEIGHT // 26 * (row + 0.5))),
                               HEIGHT // 60)

    for i in range(4):
        pygame.draw.circle(screen, ANSWER_COLORS[i], (WIDTH // 5 * (i + 1.5), HEIGHT // 26), HEIGHT // 30)

    if not game_over:
        pygame.draw.rect(screen, solved_color, [WIDTH // 5, 0, 4 * WIDTH // 5, HEIGHT // 13])

    pygame.draw.circle(screen, selected_color, (WIDTH // 7 * (selected_index + 1), 11.5 * HEIGHT // 13), HEIGHT // 26)
    for i in range(6):
        pygame.draw.circle(screen, COLORS[CHOICE_COLORS[i]], (WIDTH // 7 * (i + 1), 11.5 * HEIGHT // 13), HEIGHT // 30)

    menu_btn.draw()
    submit_btn.draw()
    start_btn.draw()

    for i in range(14):
        pygame.draw.line(screen, COLORS['black'], (0, HEIGHT // 13 * i), (WIDTH, HEIGHT // 13 * i), 5)
    pygame.draw.line(screen, COLORS['black'], (WIDTH // 5, HEIGHT // 13), (WIDTH // 5, 11 * HEIGHT // 13), 5)
    pygame.draw.line(screen, COLORS['black'], (0, HEIGHT // 13), (0, HEIGHT), 5)
    pygame.draw.line(screen, COLORS['black'], (WIDTH - 1, 0), (WIDTH - 1, HEIGHT), 5)


# Fonction pour vérifier la devinette
def vérifier_devinette():
    global game_over, win
    current_guess = guess_colors[turn]
    feedback = [COLORS['white']] * 4

    for i in range(4):
        if current_guess[i] == ANSWER_COLORS[i]:
            feedback[i] = COLORS['black']
        elif current_guess[i] in ANSWER_COLORS:
            feedback[i] = COLORS['gray']

    feedback.sort(reverse=True)
    feedback_colors[turn] = feedback

    if feedback.count(COLORS['black']) == 4:
        game_over, win = True, True
    elif turn == 9:
        game_over, win = True, False


# Fonction pour dessiner le message de fin
def dessiner_message_fin():
    message = "Vous avez gagné !" if win else "Vous avez perdu !"
    message_surface = font.render(message, True, COLORS['black'])
    screen.blit(message_surface, (WIDTH // 4, HEIGHT // 3))
    if not win:
        reveal = "Réponse: " + " ".join(ANSWER_COLORS)
        reveal_surface = font.render(reveal, True, COLORS['white'])
        screen.blit(reveal_surface, (WIDTH // 4, HEIGHT // 3 + 50))


# Variable de boucle principale
running = True

# Boucle principale du jeu
while running:
    clock.tick(FPS)
    screen.fill(COLORS['bg'])
    mouse_pos = pygame.mouse.get_pos()

    dessiner_écran()

    if menu_active:
        pygame.draw.rect(screen, COLORS['black'], [WIDTH // 4 - 5, HEIGHT // 4 - 5, WIDTH // 2 + 10, HEIGHT // 2 + 10])
        screen.blit(menu_img, (WIDTH // 4, HEIGHT // 4))

    if check_guess:
        vérifier_devinette()
        turn += 1
        if turn < 10:
            guess_colors[turn] = [COLORS['white']] * 4
        check_guess = False

    if game_over:
        dessiner_message_fin()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_btn.rect.collidepoint(event.pos):
                menu_active, game_over, win, turn = False, False, False, 0
                ANSWER_COLORS = [random.choice(CHOICE_COLORS) for _ in range(4)]
                guess_colors = [[COLORS['white']] * 4 for _ in range(10)]
                feedback_colors = [[COLORS['white']] * 4 for _ in range(10)]
            elif menu_btn.rect.collidepoint(event.pos):
                menu_active = not menu_active
            elif not menu_active and not game_over:
                if WIDTH // 14 < event.pos[0] < 13 * WIDTH // 14 and 11 * HEIGHT // 13 < event.pos[
                    1] < 12 * HEIGHT // 13:
                    selected_index = int((event.pos[0] // (WIDTH // 14) - 1) // 2)
                elif WIDTH // 5 < event.pos[0] and (10 - turn) * HEIGHT // 13 < event.pos[1] < (
                        11 - turn) * HEIGHT // 13:
                    x_pos = int(event.pos[0] // (WIDTH // 5))
                    guess_colors[turn][x_pos - 1] = CHOICE_COLORS[selected_index]
                elif submit_btn.rect.collidepoint(event.pos):
                    if COLORS['white'] not in guess_colors[turn]:
                        check_guess = True

    pygame.display.flip()

pygame.quit()
