import pygame
import sys
import math

# Inicjalizacja
pygame.init()
SZEROKOSC, WYSOKOSC = 950, 650 
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("System SCADA v4.0 - Fizyczny Przepływ")

# Kolory
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
NIEBIESKI = (30, 144, 255)
SZARY = (150, 150, 150)
CIEMNO_SZARY = (80, 80, 80)
ZIELONY = (50, 200, 50)
CZERWONY = (200, 50, 50)

class Zbiornik:
    def __init__(self, x, y, nazwa, start_poziom=0.0):
        self.x, self.y, self.nazwa = x, y, nazwa
        self.poziom = start_poziom
        self.zawor_otwarty = True 
        self.punkty = [(0, 0), (120, 0), (90, 40), (90, 140), (30, 140), (30, 40)]

    def rysuj(self, pow):
        temp = pygame.Surface((121, 141), pygame.SRCALPHA)
        wys = (self.poziom / 100) * 140
        if self.poziom > 0:
            pygame.draw.rect(temp, NIEBIESKI, (0, 140 - wys, 120, wys))
            maska = pygame.Surface((121, 141), pygame.SRCALPHA)
            pygame.draw.polygon(maska, BIALY, self.punkty)
            temp.blit(maska, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        pow.blit(temp, (self.x, self.y))
        
        p_glob = [(p[0] + self.x, p[1] + self.y) for p in self.punkty]
        pygame.draw.polygon(pow, CZARNY if self.zawor_otwarty else (200,200,200), p_glob, 3)
        
        f = pygame.font.SysFont("Arial", 16, True)
        tekst = f.render(f"{self.nazwa}: {int(self.poziom)}%", True, CZARNY)
        pow.blit(tekst, (self.x + 15, self.y - 25))
        
        self.btn_rect = pygame.Rect(self.x + 20, self.y + 150, 80, 25)
        pygame.draw.rect(pow, ZIELONY if self.zawor_otwarty else CZERWONY, self.btn_rect)
        btn_txt = "ON" if self.zawor_otwarty else "OFF"
        label = pygame.font.SysFont("Arial", 12, True).render(btn_txt, True, BIALY)
        pow.blit(label, (self.x + 50, self.y + 155))

class Pompa:
    def __init__(self, x, y):
        self.x, self.y, self.kat = x, y, 0
    def rysuj(self, pow, active):
        pygame.draw.rect(pow, CIEMNO_SZARY, (self.x - 30, self.y - 15, 60, 30))
        pygame.draw.circle(pow, SZARY, (self.x, self.y), 25)
        pygame.draw.circle(pow, CZARNY, (self.x, self.y), 25, 2)
        if active: self.kat += 15
        for i in range(4):
            a = math.radians(self.kat + i * 90)
            pygame.draw.line(pow, CZARNY, (self.x, self.y), (self.x+20*math.cos(a), self.y+20*math.sin(a)), 3)

class Suwak:
    def __init__(self, x, y, min_val, max_val, start_val, label):
        self.rect = pygame.Rect(x, y, 150, 10)
        self.min, self.max = min_val, max_val
        self.val = start_val
        self.label = label
        self.uchwyt_x = x + (start_val - min_val) / (max_val - min_val) * 150

    def rysuj(self, pow):
        pygame.draw.rect(pow, SZARY, self.rect)
        pygame.draw.circle(pow, NIEBIESKI, (int(self.uchwyt_x), self.rect.centery), 10)
        f = pygame.font.SysFont("Arial", 16, True)
        t = f.render(f"{self.label}: {self.val:.1f}", True, CZARNY)
        pow.blit(t, (self.rect.x, self.rect.y - 30))

    def sprawdz(self, pos):
        if self.rect.inflate(20, 20).collidepoint(pos):
            self.uchwyt_x = max(self.rect.left, min(pos[0], self.rect.right))
            rel = (self.uchwyt_x - self.rect.left) / self.rect.width
            self.val = self.min + rel * (self.max - self.min)

# Obiekty - Zbiornik 1 startuje pełny
z_pos = [(100, 100), (430, 100), (460, 350), (100, 350)]
zbiorniki = [
    Zbiornik(z_pos[0][0], z_pos[0][1], "Zb. 1 (Główny)", 100.0),
    Zbiornik(z_pos[1][0], z_pos[1][1], "Zb. 2"),
    Zbiornik(z_pos[2][0], z_pos[2][1], "Zb. 3"),
    Zbiornik(z_pos[3][0], z_pos[3][1], "Zb. 4")
]
pompy = [Pompa(325, 170), Pompa(610, 300), Pompa(325, 470)]
suwak = Suwak(720, 100, 0.1, 2.5, 0.5, "Przepływ")

aktywny = False
zegar = pygame.time.Clock()

while True:
    ekran.fill(BIALY)
    mysz = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: aktywny = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            for z in zbiorniki:
                if z.btn_rect.collidepoint(mysz): z.zawor_otwarty = not z.zawor_otwarty

    if pygame.mouse.get_pressed()[0]: suwak.sprawdz(mysz)

    # LOGIKA PRZEPŁYWU FIZYCZNEGO
    aktualny_transfer = -1 # -1 brak, 0 rura1, 1 rura2, 2 rura3
    
    if aktywny:
        # Sprawdzamy połączenia między i oraz i+1
        for i in range(len(zbiorniki) - 1):
            nadawca = zbiorniki[i]
            odbiorca = zbiorniki[i+1]
            
            # Woda płynie jeśli: nadawca ma wodę, odbiorca ma miejsce i zawory są ON
            if nadawca.poziom > 0 and odbiorca.poziom < 100 and odbiorca.zawor_otwarty:
                ilosc = min(suwak.val, nadawca.poziom, 100 - odbiorca.poziom)
                nadawca.poziom -= ilosc
                odbiorca.poziom += ilosc
                aktualny_transfer = i
                break # Płynie tylko jedna rura na raz dla przejrzystości

    # RYSOWANIE RUR I POMP Z KOLOREM PRZEPŁYWU
    # Rura 1 -> 2
    f1 = aktualny_transfer == 0
    pygame.draw.lines(ekran, NIEBIESKI if f1 else SZARY, False, [(190, 190), (325, 190), (325, 150), (460, 150)], 8)
    pompy[0].rysuj(ekran, f1)

    # Rura 2 -> 3
    f2 = aktualny_transfer == 1
    pygame.draw.lines(ekran, NIEBIESKI if f2 else SZARY, False, [(520, 240), (610, 240), (610, 400), (550, 400)], 8)
    pompy[1].rysuj(ekran, f2)

    # Rura 3 -> 4
    f3 = aktualny_transfer == 2
    pygame.draw.lines(ekran, NIEBIESKI if f3 else SZARY, False, [(490, 490), (325, 490), (325, 450), (190, 450)], 8)
    pompy[2].rysuj(ekran, f3)

    for z in zbiorniki: z.rysuj(ekran)
    suwak.rysuj(ekran)
    
    pygame.draw.line(ekran, SZARY, (690, 0), (690, 650), 2)
    inst = pygame.font.SysFont("Arial", 14, True).render("PRZEPŁYW WODY:", True, CIEMNO_SZARY)
    ekran.blit(inst, (710, 150))
    desc = pygame.font.SysFont("Arial", 12).render("Woda wypływa z poprzedniego zbiornika.", True, CIEMNO_SZARY)
    ekran.blit(desc, (710, 175))

    pygame.display.flip()
    zegar.tick(60)