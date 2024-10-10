import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60

# Load player images
player1_idle = pygame.image.load('player1_idle.png')
player1_attack = pygame.image.load('player1_attack.png')
player2_idle = pygame.image.load('player2_idle.png')
player2_attack = pygame.image.load('player2_attack.png')

# Player class
class Player:
    def __init__(self, x, y, idle_image, attack_image):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.idle_image = idle_image
        self.attack_image = attack_image
        self.image = idle_image
        self.health = 100
        self.attack_cooldown = 0
        self.attacking = False

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def attack(self):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.image = self.attack_image
            self.attack_cooldown = 30  # Reset cooldown
            return 1  # Normal attack damage
        return 0

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.attacking = False
            self.image = self.idle_image

# AI Player class
class AIPlayer(Player):
    def __init__(self, x, y, idle_image, attack_image):
        super().__init__(x, y, idle_image, attack_image)
        self.attack_range = 70

    def update(self, target):
        super().update()
        if self.rect.colliderect(target.rect) and target.attacking:
            if self.rect.centerx < target.rect.centerx:
                self.move(1, 0)
            else:
                self.move(-1, 0)
            if self.attack_range >= abs(self.rect.centerx - target.rect.centerx):
                return self.attack()
        else:
            if self.rect.centerx < target.rect.centerx:
                self.move(1, 0)
            else:
                self.move(-1, 0)
        return 0

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighting Game with AI")

# Game loop
def main():
    clock = pygame.time.Clock()
    player1 = Player(100, HEIGHT // 2, player1_idle, player1_attack)
    player2 = AIPlayer(WIDTH - 150, HEIGHT // 2, player2_idle, player2_attack)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: player1.move(-5, 0)  # Move left
        if keys[pygame.K_d]: player1.move(5, 0)   # Move right
        if keys[pygame.K_j]: player1.attack()      # Normal attack

        # Player attacks
        if player1.attacking:
            damage = player1.attack()
            if damage > 0:
                player2.health -= damage

        # Update AI Player
        damage = player2.update(player1)
        if damage > 0:
            player1.health -= damage

        # Check for win conditions
        if player1.health <= 0 or player2.health <= 0:
            running = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw players
        player1.draw(screen)
        player2.draw(screen)

        # Draw health bars
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, player1.health * 2, 20))  # Player 1 health
        pygame.draw.rect(screen, (0, 0, 255), (WIDTH - 210, 10, player2.health * 2, 20))  # Player 2 health

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    # Game over message
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    if player1.health <= 0:
        text = font.render("Player 2 Wins!", True, (0, 0, 0))
    else:
        text = font.render("Player 1 Wins!", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Display message for 2 seconds

    pygame.quit()

if __name__ == "__main__":
    main()
