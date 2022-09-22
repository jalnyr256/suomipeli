import pygame

class suomipeli:
    def __init__(self):
        pygame.init()
        
        self.lataa_kuvat()
        self.uusi_peli()
        
        self.korkeus = len(self.kartta)
        self.leveys = len(self.kartta[0])
        self.skaala = self.kuvat[0].get_width()

        nayton_korkeus = self.skaala * self.korkeus
        nayton_leveys = self.skaala * self.leveys
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus))

        pygame.display.set_caption("SUOMIPELI")

        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus + self.skaala))

        self.fontti = pygame.font.SysFont("Arial", 24)

        self.silmukka()

    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["lattia", "seina", "kohde", "skidi", "hai", "valmis", "hai", "norppa"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))

    def uusi_peli(self):
        self.kartta = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 7, 0, 1, 0, 1, 0, 0, 0, 1],
                       [1, 0, 4, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 3, 0, 0, 0, 1],
                       [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
                       [1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                       [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
                       
        self.siirrot = 0

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
    def etsi_robo(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [4, 6]:
                    return (y, x)

    def etsi_varjo(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [7]:
                    return (y, x)

    def liiku(self, liike_y, liike_x):
        if self.peli_lapi():
            return
        if self.peli_havio():
            return
        robon_vanha_y, robon_vanha_x = self.etsi_robo()
        robon_uusi_y = robon_vanha_y + liike_y
        robon_uusi_x = robon_vanha_x + liike_x

        if self.kartta[robon_uusi_y][robon_uusi_x] == 1:
            return

        if self.kartta[robon_uusi_y][robon_uusi_x] in [3, 5]:
            laatikon_uusi_y = robon_uusi_y + liike_y
            laatikon_uusi_x = robon_uusi_x + liike_x

            self.kartta[robon_uusi_y][robon_uusi_x] -= 3
            self.kartta[laatikon_uusi_y][laatikon_uusi_x] += 0
            self.siirrot += 1
        
        if self.kartta[robon_uusi_y][robon_uusi_x] in [7]:
            varjon_uusi_y = robon_uusi_y + liike_y
            varjon_uusi_x = robon_uusi_x + liike_x
            
            self.kartta[robon_uusi_y][robon_uusi_x] -= 4
            self.kartta[varjon_uusi_y][varjon_uusi_x] += 0

        self.kartta[robon_vanha_y][robon_vanha_x] -= 4
        self.kartta[robon_uusi_y][robon_uusi_x] += 4

    def varjo_siirry(self, varjo_y, varjo_x):
        if self.peli_havio():
            return
        if self.peli_lapi():
            return
        varjon_vanha_y, varjon_vanha_x = self.etsi_varjo()
        varjon_uusi_y = varjon_vanha_y + varjo_y
        varjon_uusi_x = varjon_vanha_x + varjo_x

        if self.kartta[varjon_uusi_y][varjon_uusi_x] == 1:
            return
        if self.kartta[varjon_uusi_y][varjon_uusi_x] == 2:
            return
        if self.kartta[varjon_uusi_y][varjon_uusi_x] == 3:
            return

        if self.kartta[varjon_uusi_y][varjon_uusi_x] in [4, 6]:
            robon_uusi_y = varjon_uusi_y + varjo_y
            robon_uusi_x = varjon_uusi_x + varjo_x

            self.kartta[varjon_uusi_y][varjon_uusi_x] -= 4
            self.kartta[robon_uusi_y][robon_uusi_x] += 0

        self.kartta[varjon_vanha_y][varjon_vanha_x] -= 7
        self.kartta[varjon_uusi_y][varjon_uusi_x] += 7

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.liiku(0, -1)
                if tapahtuma.key == pygame.K_RIGHT:
                    self.liiku(0, 1)
                if tapahtuma.key == pygame.K_UP:
                    self.liiku(-1, 0)
                if tapahtuma.key == pygame.K_DOWN:
                    self.liiku(1, 0)
                if tapahtuma.key == pygame.K_a:
                    self.varjo_siirry(0, -1)
                if tapahtuma.key == pygame.K_d:
                    self.varjo_siirry(0, 1)
                if tapahtuma.key == pygame.K_w:
                    self.varjo_siirry(-1, 0)
                if tapahtuma.key == pygame.K_s:
                    self.varjo_siirry(1, 0)
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
            if tapahtuma.type == pygame.QUIT:
                exit()

    def piirra_naytto(self):
        self.naytto.fill((0, 0, 0))

        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.kartta[y][x]
                self.naytto.blit(self.kuvat[ruutu], (x * self.skaala, y * self.skaala))

        teksti = self.fontti.render("kätyreitä tuhottu: " + str(self.siirrot), True, (255, 0, 0))
        self.naytto.blit(teksti, (25, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("F2 = uusi peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (200, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("Esc = sulje peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (400, self.korkeus * self.skaala + 10))

        if self.peli_lapi():
            teksti = self.fontti.render("hai voitti!", True, (255, 0, 0))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))
        if self.peli_havio():
            teksti = self.fontti.render("norppa voitti!", True, (255, 0, 0))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))

        pygame.display.flip()

    def peli_lapi(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [3]:
                    return False
        return True

    def peli_havio(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [4, 6]:
                    return False
        return True

if __name__ == "__main__":
    suomipeli()