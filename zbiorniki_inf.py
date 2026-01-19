import pygame
import sys
import math

# Inicjalizacja
pygame.init()
SZEROKOSC, WYSOKOSC = 850, 650
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Napełnianie zbiorników z pompą")

# Kolory
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
NIEBIESKI = (30, 144, 255)
SZARY = (150, 150, 150)
CIEMNY_SZARY = (80, 80, 80)

class Zbiornik:
    def __init__(self, x, y, nazwa):
        self.x = x
        self.y = y
        self.nazwa = nazwa
        self.poziom = 0.0
        self.punkty = [(0, 0), (120, 0), (90, 40), (90, 140), (30, 140), (30, 40)]

    def rysuj(self, powierzchnia_ekranu):
        temp_surface = pygame.Surface((120, 141), pygame.SRCALPHA)
        wys_wody = (self.poziom / 100) * 140
        
        if self.poziom > 0:
            pygame.draw.rect(temp_surface, NIEBIESKI, (0, 140 - wys_wody, 120, wys_wody))
            maska = pygame.Surface((120, 141), pygame.SRCALPHA)
            pygame.draw.polygon(maska, (255, 255, 255, 255), self.punkty)
            temp_surface.blit(maska, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        powierzchnia_ekranu.blit(temp_surface, (self.x, self.y))

        punkty_globalne = [(p[0] + self.x, p[1] + self.y) for p in self.punkty]
        pygame.draw.polygon(powierzchnia_ekranu, CZARNY, punkty_globalne, 3)
        
        czcionka = pygame.font.SysFont("Arial", 16, True)
        tekst = czcionka.render(f"{self.nazwa}: {int(self.poziom)}%", True, CZARNY)
        powierzchnia_ekranu.blit(tekst, (self.x + 15, self.y - 25))

class Pompa:
    def __init__(self, x, y):
        self.x, self.y, self.kat = x, y, 0
    def rysuj(self, powierzchnia, active):
        pygame.draw.rect(powierzchnia, CIEMNY_SZARY, (self.x - 30, self.y - 15, 60, 30))
        pygame.draw.circle(powierzchnia, SZARY, (self.x, self.y), 25)
        pygame.draw.circle(powierzchnia, CZARNY, (self.x, self.y), 25, 2)
        if active: self.kat += 15
        for i in range(4):
            a = math.radians(self.kat + i * 90)
            koniec = (self.x + 20 * math.cos(a), self.y + 20 * math.sin(a))
            pygame.draw.line(powierzchnia, CZARNY, (self.x, self.y), koniec, 3)

z1_p = (100, 100)
z2_p = (430, 100)  
z3_p = (460, 350)
z4_p = (100, 350)

zbiorniki = [Zbiornik(*z1_p, "Zb. 1"), Zbiornik(*z2_p, "Zb. 2"), 
             Zbiornik(*z3_p, "Zb. 3"), Zbiornik(*z4_p, "Zb. 4")]

pompy = [Pompa(325, 170), Pompa(610, 300), Pompa(325, 470)]

aktywny, id_akt, zegar = False, 0, pygame.time.Clock()

while True:
    ekran.fill(BIALY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: aktywny = True

    if aktywny and id_akt < len(zbiorniki):
        zbiorniki[id_akt].poziom += 0.5
        if zbiorniki[id_akt].poziom >= 100: id_akt += 1
    else: aktywny = False

    # 1 rura
    k1 = NIEBIESKI if (aktywny and id_akt == 1) else SZARY
    # Ścianka Z1 (x+90, y+90) do ścianki Z2 (x, y+90) - dopasowane kolanko
    pygame.draw.lines(ekran, k1, False, [(190, 190), (325, 190), (325, 150), (460, 150)], 8)
    pompy[0].rysuj(ekran, (aktywny and id_akt == 1))

    # 2 rura
    k2 = NIEBIESKI if (aktywny and id_akt == 2) else SZARY
    # Wyjście z dołu Z2 do wejścia bocznego Z3
    pygame.draw.lines(ekran, k2, False, [(520, 240), (610, 240), (610, 400), (550, 400)], 8)
    pompy[1].rysuj(ekran, (aktywny and id_akt == 2))

    # 3 rura
    k3 = NIEBIESKI if (aktywny and id_akt == 3) else SZARY
    pygame.draw.lines(ekran, k3, False, [(490, 490), (325, 490), (325, 450), (190, 450)], 8)
    pompy[2].rysuj(ekran, (aktywny and id_akt == 3))

    for z in zbiorniki: z.rysuj(ekran)
    
    f = pygame.font.SysFont("Arial", 20, True)
    msg = f.render("SPACJA: Start Procesu ", True, (30, 30, 30))
    ekran.blit(msg, (220, 600))

    pygame.display.flip()
    zegar.tick(60)