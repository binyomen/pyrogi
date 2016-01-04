import pygame
import engine
from engine.graphics.pygame_graphics import PyGameGraphics
from engine.backend import Backend
from engine.events import KeyDownEvent, KeyUpEvent, MouseMovedEvent, MouseButtonDownEvent, MouseButtonUpEvent, MouseWheelScrolledEvent
from engine.util.vector import Vec2

TARGET_FRAMERATE = 60

class PyGameBackend(Backend):
    def __init__(self, window_dimensions, tile_dimensions, caption, starting_screen):
        super(PyGameBackend, self).__init__(
            window_dimensions, tile_dimensions,
            caption, starting_screen
        )
        pygame.init()
    
    def run(self):
        clock = pygame.time.Clock()
        g = PyGameGraphics()
        g.init_window(
            self.window_dimensions, self.tile_dimensions, self.caption
        )
        while True:
            if pygame.event.peek(pygame.QUIT):
                break
            else:
                self._handleEvents(pygame.event.get())
            
            fps = clock.get_fps()
            pygame.display.set_caption('FPS: ' + str(fps))
            
            millis = clock.tick(TARGET_FRAMERATE)
            self.onTick(millis)
            self.onDraw(g)
            pygame.display.update()
    
    def _handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handleKeyDown(KeyDownEvent(event.unicode, event.key, event.mod))
            elif event.type == pygame.KEYUP:
                self.handleKeyUp(KeyUpEvent(event.key, event.mod))
            elif event.type == pygame.MOUSEMOTION:
                self.handleMouseMoved(MouseMovedEvent(event.pos, event.rel, event.buttons))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == engine.events.SCROLL_WHEEL_UP:
                    self.handleMouseWheelScrolled(MouseWheelScrolledEvent(event.pos, 1))
                elif event.button == engine.events.SCROLL_WHEEL_DOWN:
                    self.handleMouseWheelScrolled(MouseWheelScrolledEvent(event.pos, -1))
                else:
                    self.handleMouseButtonDown(MouseButtonDownEvent(event.pos, event.button))
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handleMouseButtonUp(MouseButtonUpEvent(event.pos, event.button))