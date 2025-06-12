import pygame
import math

class Tower:
    name = "Basic"
    description = "Standard tower"
    value = 100
    sprite_location = "assets/basic_tower.png"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.damage = 15
        self.cooldown = 60  # frames
        self.counter = 0
        self.show_range = True
        self.range_timer = 180  # 3초 = 60프레임 × 3
        # 업그레이드 관련 속성 추가
        self.upgrade_level = 0
        self.max_upgrade = 3
        self.base_damage = 15
        self.base_cooldown = 60

    def find_target(self, enemies):
        for enemy in enemies:
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if dist <= self.range:
                return enemy
        return None

    def shoot(self, target):
        return Bullet(self.x, self.y, target, self.damage)

    def update(self, enemies, bullets):
        self.counter += 1
        if self.counter >= self.cooldown:
            target = self.find_target(enemies)
            if target:
                bullet = self.shoot(target)
                bullets.append(bullet)
                self.counter = 0

    def upgrade(self):
        if self.upgrade_level < self.max_upgrade:
            self.upgrade_level += 1
            # 데미지 20% 증가, 공격 속도 15% 증가
            self.damage = int(self.base_damage * (1 + 0.2 * self.upgrade_level))
            self.cooldown = int(self.base_cooldown * (1 - 0.15 * self.upgrade_level))
            return True
        return False

    def draw(self, win):
        image = pygame.image.load(self.sprite_location)
        image = pygame.transform.scale(image, (50, 50))
        win.blit(image, (self.x - 25, self.y - 25))
        
        # 업그레이드 레벨 표시
        if self.upgrade_level > 0:
            font = pygame.font.Font(None, 20)
            level_text = font.render(f"+{self.upgrade_level}", True, (255, 215, 0))
            win.blit(level_text, (self.x + 15, self.y - 25))

        if self.show_range and self.range_timer > 0:
            pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), self.range, 1)
            self.range_timer -= 1
            if self.range_timer <= 0:
                self.show_range = False


class Bullet:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 6
        self.damage = damage
        self.hit = False
        self.slow_effect = False

    def move(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist > self.speed:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist
        else:
            self.target.hp -= self.damage
            if self.slow_effect:
                self.target.speed *= 0.5  # 감속 적용
            self.hit = True

    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (int(self.x), int(self.y)), 5)


class SniperTower(Tower):
    name = "Sniper"
    description = "Sniper tower"
    value = 200
    sprite_location = "assets/sniper_tower.png"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 200
        self.damage = 50
        self.cooldown = 120
        # 업그레이드 기본값 설정
        self.base_damage = 50
        self.base_cooldown = 120

    def draw(self, win):
        image = pygame.image.load(self.sprite_location)
        image = pygame.transform.scale(image, (50, 50))
        win.blit(image, (self.x - 25, self.y - 25))
        if self.show_range and self.range_timer > 0:
            pygame.draw.circle(win, (255, 255, 0), (self.x, self.y), self.range, 1)
            self.range_timer -= 1
            if self.range_timer <= 0:
                self.show_range = False


class SlowTower(Tower):
    name = "Slow"
    description = "Slows enemies"
    value = 150
    sprite_location = "assets/slow_tower.png"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 120
        self.damage = 5
        self.cooldown = 80
        # 업그레이드 기본값 설정
        self.base_damage = 5
        self.base_cooldown = 80

    def shoot(self, target):
        bullet = super().shoot(target)
        bullet.slow_effect = True
        return bullet

    def draw(self, win):
        image = pygame.image.load(self.sprite_location)
        image = pygame.transform.scale(image, (50, 50))
        win.blit(image, (self.x - 25, self.y - 25))
        if self.show_range and self.range_timer > 0:
            pygame.draw.circle(win, (0, 255, 255), (self.x, self.y), self.range, 1)
            self.range_timer -= 1
            if self.range_timer <= 0:
                self.show_range = False
