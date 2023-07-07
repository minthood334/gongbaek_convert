import sys
import pygame
from random import randint
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE

pygame.init()
pygame.key.set_repeat(5, 5)
pygame.display.set_caption("Cave")
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    score_font = pygame.font.SysFont(None, 32, True, False)
    end_font = pygame.font.SysFont(None, 70, True, False)
    boat_rect = Rect(40, 300, 40, 40)
    boat_rect.center = (60, 300)
    game_over = False
    score = 0
    walls = 81
    slope = randint(1, 10)
    holes = []
    v = 0
    for xpos in range(walls):
        holes.append(Rect(xpos * 10, 100, 10 ,400))
    while True:
        # 이벤트 가져오기
        key_down = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                key_down = True
        if game_over:
            SURFACE.fill((0, 0, 0))
            end_rend = end_font.render("Game Over", True, (255, 255, 255))
            end_rect = end_rend.get_rect()
            end_rect.center = (400, 300)
            SURFACE.blit(end_rend, end_rect)
            score_rend = score_font.render("Time : %s s"%( format((score / 60), '.2f') ), True, (0, 0, 225))
            score_rect = score_rend.get_rect()
            score_rect.center = (400, 350)
            SURFACE.blit(score_rend, score_rect)
        else:
            score += 1
            score_rend = score_font.render("Time : %s"%( format((score / 60), '.2f') ), True, (0, 0, 225))
            score_rect = score_rend.get_rect()
            score_rect.topright = (750, 50)
            v += -(0.25) if key_down else (0.25)
            boat_rect.y += v
            if holes[0].right - 10 <= 0:
                del holes[0]
                edge = holes[-1].copy()
                edge.x += 10
                if (slope < 0 and edge.top <= 0) or (slope > 0 and edge.bottom >= 600):
                    slope = randint(1, 10) * (-1 if slope > 0 else 1)
                edge.y += slope
                holes.append(edge)
            holes = [x.move(-10, 0) for x in holes]
            if holes[4].top >= boat_rect.top or holes[7].bottom <= boat_rect.bottom:
                game_over = True
            SURFACE.fill((0, 255, 0))
            for x in holes:
                pygame.draw.rect(SURFACE, (0, 0, 0), x)
            SURFACE.blit(score_rend, score_rect)
            pygame.draw.rect(SURFACE, (255, 255, 255), boat_rect)
        FPSCLOCK.tick(60)
        pygame.display.update()

if __name__ == '__main__':
    main()
