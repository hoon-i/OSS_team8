from UI import *

# Scene 클래스: 모든 씬의 공통 기능을 정의한 추상 클래스
class Scene:
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(100, 100, screen_size[0]-200, screen_size[1]-200)
        self.game_screen = screen.subsurface(self.rect)

    def update(self, **kwargs):
        pass

    def render(self, **kwargs):
        pass

# MainMenu 클래스: 메인 메뉴 씬 정의
class MainMenu(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])
        self.menu_screen = screen.subsurface(self.rect)

        # 게임 제목
        self.title = TextDisplay(pygame.Rect(0, 100, screen_size[0], 100), "Tower Defence Game", TEXT_COLOUR, 100)
        self.title.create_image()

        # 게임 설명 텍스트
        self.instructions = []
        instruction_texts = [
            "Left click a free space to place a tower",
            "Click a tower in the shop or press a number to change the tower you place",
            "Right click a tower to sell it",
            "Press 'Next wave' or press the space bar to start the wave",
            "Try to survive as long as you can"
        ]
        for i, text in enumerate(instruction_texts):
            td = TextDisplay(pygame.Rect(0, 300 + i * 65, screen_size[0], 65), text, TEXT_COLOUR, 50)
            td.create_image()
            self.instructions.append(td)

        # 시작 및 종료 버튼
        self.play_button = Button(pygame.Rect((screen_size[0]/2) - 150, 630, 150, 80), "Play", BUTTON_COLOUR, TEXT_COLOUR, 50)
        self.quit_button = Button(pygame.Rect((screen_size[0]/2) + 50, 630, 150, 80), "Quit", BUTTON_COLOUR, TEXT_COLOUR, 50)
        self.play_button.create_image()
        self.quit_button.create_image()

        # 음악 저작권 표기
        self.music_credit = TextDisplay(pygame.Rect(100, 900, 700, 50), "Music: 'Quando a revolução vier' by OVO (Released under CC)", TEXT_COLOUR, 30)
        self.music_credit.create_image()

    def render(self, **kwargs):
        self.menu_screen.blit(self.title.image, self.title.rect)
        for instruction in self.instructions:
            self.menu_screen.blit(instruction.image, instruction.rect)
        self.menu_screen.blit(self.play_button.image, self.play_button.rect)
        self.menu_screen.blit(self.quit_button.image, self.quit_button.rect)
        self.menu_screen.blit(self.music_credit.image, self.music_credit.rect)

# GameOver 클래스: 게임 오버 화면을 그리는 씬
class GameOver(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect((0, 0), screen_size)
        self.screen = screen.subsurface(self.rect)

        # 타이틀 및 버튼 생성
        self.title = TextDisplay(pygame.Rect((screen_size[0] // 2 - 300, 300), (600, 100)),
                                 "YOU LOSE", TEXT_COLOUR, 100)
        self.title.create_image()

        self.restart_button = Button(pygame.Rect((screen_size[0] // 2 - 200, 500), (180, 80)),
                                     "Restart", BUTTON_COLOUR, TEXT_COLOUR, 50)
        self.quit_button = Button(pygame.Rect((screen_size[0] // 2 + 20, 500), (180, 80)),
                                  "Quit", BUTTON_COLOUR, TEXT_COLOUR, 50)

        self.restart_button.create_image()
        self.quit_button.create_image()

    def render(self):
        self.screen.fill((100, 100, 100))  # 회색 배경
        self.screen.blit(self.title.image, self.title.rect)
        self.screen.blit(self.restart_button.image, self.restart_button.rect)
        self.screen.blit(self.quit_button.image, self.quit_button.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.restart_button.rect.collidepoint(pos):
                return "restart"
            elif self.quit_button.rect.collidepoint(pos):
                return "quit"
        return None
# Pause 클래스: 일시 정지 화면을 나타내는 씬
class Pause(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])
        self.pause_overlay = screen.subsurface(self.rect)

        # 타이틀, 버튼 생성
        self.pause_message = TextDisplay(pygame.Rect(600, 200, 300, 100), "PAUSED", TEXT_COLOUR, 72)
        self.pause_message.create_image()
        self.resume_button = Button(pygame.Rect(500, 400, 200, 80), "Resume", BUTTON_COLOUR, TEXT_COLOUR, 50)
        self.quit_button = Button(pygame.Rect(800, 400, 200, 80), "Main Menu", BUTTON_COLOUR, TEXT_COLOUR, 50)
        self.resume_button.create_image()
        self.quit_button.create_image()

    def render(self, **kwargs):
        self.pause_overlay.fill((30, 30, 30))
        self.pause_overlay.blit(self.pause_message.image, self.pause_message.rect)
        self.pause_overlay.blit(self.resume_button.image, self.resume_button.rect)
        self.pause_overlay.blit(self.quit_button.image, self.quit_button.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.resume_button.rect.collidepoint(pos):
                return "resume"
            elif self.quit_button.rect.collidepoint(pos):
                return "menu"
        return None

# 게임 클리어 화면 클래스
class ClearScene:
    def __init__(self, screen_size, screen):
        self.screen = screen
        self.width, self.height = screen_size
        self.font = pygame.font.Font(None, 80)  # 큰 글씨 폰트
        self.button_font = pygame.font.Font(None, 50)  # 버튼용 폰트

        # 클리어 메시지
        self.message = self.font.render("🎉 GAME CLEARED! 🎉", True, (255, 255, 0))
        self.message_rect = self.message.get_rect(center=(self.width // 2, self.height // 3))

        # 메인 메뉴로 돌아가기 버튼
        self.menu_button = Button(pygame.Rect(self.width // 2 - 150, self.height // 2, 300, 60), 
                                  "Main Menu", pygame.Color("green"), pygame.Color("white"), 36)
        self.menu_button.create_image()

        # 게임 종료 버튼
        self.quit_button = Button(pygame.Rect(self.width // 2 - 150, self.height // 2 + 100, 300, 60), 
                                  "Quit Game", pygame.Color("red"), pygame.Color("white"), 36)
        self.quit_button.create_image()

    # 클리어 화면 렌더링
    def render(self):
        self.screen.fill((0, 0, 50))  # 진한 파랑 배경
        self.screen.blit(self.message, self.message_rect)
        self.screen.blit(self.menu_button.image, self.menu_button.rect)
        self.screen.blit(self.quit_button.image, self.quit_button.rect)

    # 클릭 이벤트 처리
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.menu_button.rect.collidepoint(pos):
                return "menu"
            elif self.quit_button.rect.collidepoint(pos):
                return "quit"
        return None

