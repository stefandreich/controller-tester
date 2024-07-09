import platform
import time
import pygame

pygame.init()
pygame.joystick.init()


class TextPrint:
    def __init__(self):
        self.line_height = None
        self.y = None
        self.x = None
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text, color=(0, 0, 0)):
        text_bitmap = self.font.render(text, True, color)
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


def main():
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("Controller Tester")

    clock = pygame.time.Clock()

    text_print = TextPrint()

    joysticks = {}

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joy.init()
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connected.")

            if event.type == pygame.JOYDEVICEREMOVED:
                if event.instance_id in joysticks:
                    del joysticks[event.instance_id]
                    print(f"Joystick {event.instance_id} disconnected.")
                else:
                    print(f"Attempted to remove non-existent joystick with ID {event.instance_id}")

        joysticks_count = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        screen.fill((255, 255, 255))
        text_print.reset()

        text_print.tprint(screen, "> Welcome to Controller Test LAB!", color=(235, 125, 52))
        text_print.tprint(screen, " ")
        text_print.tprint(screen, " ")

        if not joysticks_count:
            text_print.tprint(screen, "No controller found.")
            text_print.indent()
        else:
            text_print.tprint(screen, f"Found {len(joysticks_count)} controller(s).")
            text_print.indent()

            for idx, joystick in enumerate(joysticks_count):
                text_print.tprint(screen, f"{idx + 1}. {joystick.get_name()}")
                for i in range(3):
                    text_print.indent()

                os_name = platform.system()
                uname = platform.uname()
                os_version = uname.version
                text_print.tprint(screen, f"Operating System: {os_name} {os_version}")

                connection_type = joystick.get_power_level()
                text_print.tprint(screen, f"Controller's connection type: {connection_type}")

                buttons = joystick.get_numbuttons()
                text_print.tprint(screen, f"Number of buttons: {buttons}")
                text_print.indent()

                for i in range(buttons):
                    button = joystick.get_button(i)
                    status = "pressed" if button else "unpressed"
                    text_print.tprint(screen, f"Button {i:>2} value: {status}")
                text_print.unindent()

        pygame.display.flip()

        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
