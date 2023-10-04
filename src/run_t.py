import importlib
import time
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))

    clock = pygame.time.Clock()
    running = True
    indicators = importlib.import_module("indicators")
    sd = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        try:
            print("recargo")

            importlib.reload(indicators)

            sd = indicators.Speedometer(500)

            for i in range(400):
                screen.fill("#000000")
                sd.actual = i
                screen.blit(sd.draw(), (0, 0))
                pygame.display.flip()
                clock.tick(100)
                if i == 0:
                    time.sleep(1)
            time.sleep(1)
        except ArithmeticError:
            print("Error importando")


if __name__ == "__main__":
    main()
