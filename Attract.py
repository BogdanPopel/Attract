import copy
import math
import sys
import time
from statistics import median

import pygame


class Joc:
    NR_COLOANE = 8
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):  # Joc()
        if tabla:
            self.matr = tabla
        else:
            self.matr = [Joc.GOL] * self.NR_COLOANE ** 2

    @classmethod
    def initializeaza(cls, display, NR_COLOANE=8, dim_celula=100):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('alb.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (
            dim_celula, math.floor(dim_celula * cls.x_img.get_height() / cls.x_img.get_width())))
        cls.zero_img = pygame.image.load('negru.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (
            dim_celula, math.floor(dim_celula * cls.zero_img.get_height() / cls.zero_img.get_width())))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        for linie in range(NR_COLOANE):
            cls.celuleGrid.append([])
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid[linie].append(patr)

    def deseneaza_grid(self, marcaj=None, pozitii_castigatoare=None):  # tabla de exemplu este ["#","x","#","0",......]

        for linie in range(Joc.NR_COLOANE):
            for coloana in range(Joc.NR_COLOANE):
                if pozitii_castigatoare == None:
                    if marcaj == linie * Joc.NR_COLOANE + coloana:
                        # daca am o patratica selectata, o desenez cu rosu
                        culoare = (224, 224, 148)
                    else:
                        # altfel o desenez cu alb
                        culoare = (255, 255, 255)
                    pygame.draw.rect(self.__class__.display, culoare,
                                     self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                    if self.matr[linie * Joc.NR_COLOANE + coloana] == 'alb':
                        self.__class__.display.blit(self.__class__.x_img,
                                                    (coloana * (self.__class__.dim_celula + 1),
                                                     linie * (self.__class__.dim_celula + 1)
                                                     + (
                                                             self.__class__.dim_celula - self.__class__.x_img.get_height()) // 2))
                    elif self.matr[linie * Joc.NR_COLOANE + coloana] == 'negru':
                        self.__class__.display.blit(self.__class__.zero_img,
                                                    (coloana * (self.__class__.dim_celula + 1),
                                                     linie * (self.__class__.dim_celula + 1)
                                                     + (
                                                             self.__class__.dim_celula - self.__class__.zero_img.get_height()) // 2))
                else:
                    culoare = (50, 205, 50)
                    if linie * Joc.NR_COLOANE + coloana in pozitii_castigatoare:
                        pygame.draw.rect(self.__class__.display, culoare,
                                         self.__class__.celuleGrid[linie][coloana])
                    else:
                        culoare = (255, 255, 255)
                        pygame.draw.rect(self.__class__.display, culoare,
                                         self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                        if self.matr[linie * Joc.NR_COLOANE + coloana] == 'alb':
                            self.__class__.display.blit(self.__class__.x_img,
                                                        (coloana * (self.__class__.dim_celula + 1),
                                                         linie * (self.__class__.dim_celula + 1)
                                                         + (
                                                                 self.__class__.dim_celula - self.__class__.x_img.get_height()) // 2))
                        elif self.matr[linie * Joc.NR_COLOANE + coloana] == 'negru':
                            self.__class__.display.blit(self.__class__.zero_img,
                                                        (coloana * (self.__class__.dim_celula + 1),
                                                         linie * (self.__class__.dim_celula + 1)
                                                         + (
                                                                 self.__class__.dim_celula - self.__class__.zero_img.get_height()) // 2))
        # pygame.display.flip() # !!! obligatoriu pentru a actualiza interfata (desenul)
        pygame.display.update()

    @classmethod
    def jucator_opus(cls, jucator):
        # val_true if conditie else val_false
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        l_mutari = []
        for i in range(len(self.matr)):
            if self.matr[i] == Joc.GOL:
                copie_matr = copy.deepcopy(self.matr)
                copie_matr[i] = jucator
                for j in range(i + Joc.NR_COLOANE, Joc.NR_COLOANE ** 2, 8):  # cautam in jos
                    if copie_matr[j] != Joc.GOL and copie_matr[j - Joc.NR_COLOANE] == Joc.GOL:
                        simbolGasit = copie_matr[j]
                        copie_matr[j] = Joc.GOL
                        copie_matr[j - Joc.NR_COLOANE] = simbolGasit

                for j in range(i - Joc.NR_COLOANE, 0, -8):  # cautam in sus
                    if copie_matr[j] != Joc.GOL and copie_matr[j + Joc.NR_COLOANE] == Joc.GOL:
                        simbolGasit = copie_matr[j]
                        copie_matr[j] = Joc.GOL
                        copie_matr[j + Joc.NR_COLOANE] = simbolGasit

                coloana_curenta = i % self.NR_COLOANE
                for j in range(i + 1, i + (Joc.NR_COLOANE - coloana_curenta - 1)):  # cautam in dreapta
                    if copie_matr[j] != Joc.GOL and copie_matr[j - 1] == Joc.GOL:
                        simbolGasit = copie_matr[j]
                        copie_matr[j] = Joc.GOL
                        copie_matr[j - 1] = simbolGasit

                for j in range(i - 1, i - coloana_curenta - 1, -1):  # cautam in stanga
                    if copie_matr[j] != Joc.GOL and copie_matr[j + 1] == Joc.GOL:
                        simbolGasit = copie_matr[j]
                        copie_matr[j] = Joc.GOL
                        copie_matr[j + 1] = simbolGasit

                l_mutari.append(Joc(copie_matr))
        return l_mutari

    def final(self):
        pozitii = {}
        pozitii.update()
        contor_Jmin = 0
        contor_Jmax = 0
        pozitii_castigatoareJmin = []
        pozitii_castigatoareJmax = []
        for i in range(len(self.matr)):
            if i not in [i for i in range(1, 7, 1)] + [i for i in range(7, 64, 8)] + \
                    [i for i in range(0, 57, 8)] + [i for i in range(57,63, 1)]:
                # #daca pozitia piesei nu este pe o margine:
                # [0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 31, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63]
                if self.matr[i] == self.JMIN \
                        and self.matr[i - Joc.NR_COLOANE - 1] == self.__class__.JMAX \
                        and self.matr[i - Joc.NR_COLOANE + 1] == self.__class__.JMAX \
                        and self.matr[i + Joc.NR_COLOANE - 1] == self.__class__.JMAX \
                        and self.matr[i + Joc.NR_COLOANE + 1] == self.__class__.JMAX:
                    contor_Jmin += 1
                    pozitii_castigatoareJmin.append(i)
                elif self.matr[i] == self.__class__.JMAX \
                        and self.matr[i - Joc.NR_COLOANE - 1] == self.__class__.JMIN \
                        and self.matr[i - Joc.NR_COLOANE + 1] == self.__class__.JMIN \
                        and self.matr[i + Joc.NR_COLOANE - 1] == self.__class__.JMIN \
                        and self.matr[i + Joc.NR_COLOANE + 1] == self.__class__.JMIN:
                    contor_Jmax += 1
                    pozitii_castigatoareJmax.append(i)
        if contor_Jmax > contor_Jmin:
            return self.__class__.JMAX, pozitii_castigatoareJmax
        elif contor_Jmin > contor_Jmax:
            return self.__class__.JMIN, pozitii_castigatoareJmin
        if Joc.GOL not in self.matr:
            return "remiza", None
        else:
            return False, None

    def numara_pozitii_influente(self):
        pozitii = 0
        for i in range(len(self.matr)):
            # daca exista o pozitie libera cu spatiu oriunde in jurul
            if self.matr[i] == self.__class__.GOL:
                if i - Joc.NR_COLOANE >= 0 \
                        and self.matr[i - Joc.NR_COLOANE] == self.__class__.GOL:
                    pozitii += 1
                elif i + Joc.NR_COLOANE < len(self.matr) \
                        and self.matr[i + Joc.NR_COLOANE] == self.__class__.GOL:
                    pozitii += 1
                elif i + 1 < len(self.matr) \
                        and self.matr[i + 1] == self.__class__.GOL:
                    pozitii += 1
                elif i - 1 < len(self.matr) \
                        and self.matr[i - 1] == self.__class__.GOL:
                    pozitii += 1
        return pozitii

    def numara_piese_diag(self):
        diagonale = 0
        for i in range(len(self.matr)):
            if self.matr[i] != self.__class__.GOL:
                piesa = self.matr[i]
                if i - Joc.NR_COLOANE - 1 >= 0 and self.matr[i - Joc.NR_COLOANE - 1] == self.jucator_opus(piesa):
                    diagonale += 1
                if i - Joc.NR_COLOANE + 1 >= 0 and self.matr[i - Joc.NR_COLOANE + 1] == self.jucator_opus(piesa):
                    diagonale += 1
                if i + Joc.NR_COLOANE - 1 < len(self.matr) and self.matr[i + Joc.NR_COLOANE - 1] == self.jucator_opus(
                        piesa):
                    diagonale += 1
                if i + Joc.NR_COLOANE + 1 < len(self.matr) and self.matr[i + Joc.NR_COLOANE + 1] == self.jucator_opus(
                        piesa):
                    diagonale += 1
        return diagonale

    def estimeaza_scor(self, adancime):
        t_final = self.final()[0]
        # if (adancime==0):
        if t_final == self.__class__.JMAX:  # self.__class__ referinta catre clasa instantei
            return 1000 + adancime
        elif t_final == self.__class__.JMIN:
            return -1000 - adancime
        elif t_final == 'remiza':
            return 0
        else:
            return self.numara_pozitii_influente()

            # 2) return self.numara_piese_diag()

            # return nr de piese care au piese inamice in diagonala
            # return (self.linii_deschise(self.__class__.JMAX)- self.linii_deschise(self.__class__.JMIN))
            # nr de linii pe care se mai poate realiza o configuratie castigatoare:
            # practic nr de simboluri jmax - nr simboluri jmin + nr joc.GOL/2 (toate piesele ar putea avea o sansa sa fie in config optima)


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    O instanta din clasa stare este un nod din arborele minimax
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile
    posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent
        # adancimea in arborele de stari
        self.adancime = int(adancime)
        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare
        # lista de mutari posibile (tot de tip Stare) din starea curenta
        self.mutari_posibile = []
        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        # e de tip Stare (cel mai bun succesor)
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)  # lista de informatii din nodurile succesoare
        juc_opus = Joc.jucator_opus(self.j_curent)
        # mai jos calculam lista de noduri-fii (succesori)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = ""
        for i in range(0, Joc.NR_COLOANE ** 2):
            if self.tabla_joc.matr[i] == "alb":
                sir += "A "
            elif self.tabla_joc.matr[i] == "negru":
                sir += "N "
            elif self.tabla_joc.matr[i] == "#" or None:
                sir += "# "
            if i in [j for j in range(7, 64, 8)]:
                sir += "\n"

        sir += "\n(Juc curent:" + self.j_curent + ")\n"
        return sir


class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


""" Algoritmul MinMax """


def min_max(stare):
    contorNoduriCalc = 0
    # daca sunt la o frunza in arborele minimax sau la o stare finala
    if stare.adancime == 0 or stare.tabla_joc.final()[0]:
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare, contorNoduriCalc
    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(x)[0] for x in
                        stare.mutari_posibile]  # expandez(constr subarb) fiecare nod x din mutari posibile
    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)  # def f(x): return x.estimare -----> key=f
        contorNoduriCalc = len(mutariCuEstimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)

    stare.estimare = stare.stare_aleasa.estimare
    return stare, contorNoduriCalc

""" Algoritmul AlphaBeta """
def alpha_beta(alpha, beta, stare, contorNoduriCalc):
    if stare.adancime == 0 or stare.tabla_joc.final()[0]:
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare, contorNoduriCalc

    if alpha > beta:
        return stare, contorNoduriCalc  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')  # in aceasta variabila calculam maximul

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare, contorNoduriCalc)[
                0]  # aici construim subarborele pentru stare_noua
            contorNoduriCalc += 1
            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:  # interval invalid
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')
        # completati cu rationament similar pe cazul stare.j_curent==Joc.JMAX
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea
            stare_noua = alpha_beta(alpha, beta, mutare, contorNoduriCalc)[
                0]  # aici construim subarborele pentru stare_noua

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.estimare = stare.stare_aleasa.estimare
    return stare, contorNoduriCalc


def afis_daca_final(stare_curenta):
    final, pozitii_castigatoare = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
            return "Remiza", pozitii_castigatoare
        else:
            print("A castigat " + final)
            return "A castigat " + final + "!", pozitii_castigatoare

    return False, pozitii_castigatoare


def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[Buton(display=display, w=130, h=30, text="Minimax", valoare="minimax"),
                      Buton(display=display, w=130, h=30, text="Alphabeta", valoare="alphabeta")], indiceSelectat=1)
    btn_juc = GrupButoane(top=100, left=30,
                          listaButoane=[
                              Buton(display=display, w=100, h=30, text="ALB", valoare="alb"),
                              Buton(display=display, w=100, h=30, text="NEGRU", valoare="negru")],
                          indiceSelectat=0)
    btn_dificultate = GrupButoane(top=170,
                                  left=30,
                                  listaButoane=[
                                      Buton(display=display, w=80, h=30, text="Usor", valoare=1),
                                      Buton(display=display, w=80, h=30, text="Mediu", valoare=2),
                                      Buton(display=display, w=80, h=30, text="Greu", valoare=3)
                                  ],
                                  indiceSelectat=1)
    start = Buton(display=display, top=250, left=30, w=40, h=30, text="Start", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dificultate.deseneaza()
    start.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_dificultate.selecteazaDupacoord(pos):
                            if start.selecteazaDupacoord(pos):
                                display.fill((0, 0, 0))  # stergere ecran
                                tabla_curenta.deseneaza_grid()
                                return btn_juc.getValoare(), btn_alg.getValoare(), btn_dificultate.getValoare()
        pygame.display.update()


def main():
    # raspuns_valid = False
    # while not raspuns_valid:
    #     tip_algoritm = input("Algoritmul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
    #     if tip_algoritm in ['1', '2']:
    #         raspuns_valid = True
    #     else:
    #         print("Nu ati ales o varianta corecta.")
    # # initializare jucatori
    # raspuns_valid = False
    #
    # while not raspuns_valid:
    #     Joc.JMIN = input("Doriti sa jucati cu ALB sau cu NEGRU? ").lower()
    #     if (Joc.JMIN in ["alb", "negru"]):
    #         raspuns_valid = True
    #     else:
    #         print("Raspunsul trebuie sa fie ALB sau NEGRU.")
    # Joc.JMAX = "alb" if Joc.JMIN == "negru" else "negru"
    # # expresie= val_true if conditie else val_false  (conditie? val_true: val_false)
    #
    # tabla_curenta = Joc()  # apelam constructorul
    # print("Tabla initiala")
    # print(str(tabla_curenta))
    contor_mutari_utilizator = 0
    contor_mutari_calculator = 0
    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('ATTRACT')
    # dimensiunea ferestrei in pixeli
    # dim_celula=..
    ecran = pygame.display.set_mode(
        size=(807, 807))  # N *100+ (N-1)*dimensiune_linie_despartitoare (dimensiune_linie_despartitoare=1)
    Joc.initializeaza(ecran)
    tabla_curenta = Joc()
    Joc.JMIN, tip_algoritm, dificultate = deseneaza_alegeri(ecran, tabla_curenta)
    print(Joc.JMIN, tip_algoritm, "Adancime:", dificultate)
    Joc.JMAX = 'alb' if Joc.JMIN == 'negru' else 'negru'
    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, "alb", dificultate)
    de_mutat = False
    tabla_curenta.deseneaza_grid()
    run = True
    contor_undo = 0
    while run:
        if (stare_curenta.j_curent == Joc.JMIN):
            t_inainte = int(round(time.time() * 1000))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # inchide fereastra
                    print("Timp de gandire calc minim:", min(timp_gandire_calc))
                    print("Timp de gandire calcmaxim:", max(timp_gandire_calc))
                    print("Timp de gandire calc mediu:", sum(timp_gandire_calc) / len(timp_gandire_calc))
                    print("Timp de gandire, calc mediana:", median(timp_gandire_calc))
                    print("Mutari calculator:", contor_mutari_calculator)
                    print("Mutari utilizator:", contor_mutari_utilizator)
                    print("Medie noduri create: ", sum(noduri_calculator) / len(noduri_calculator))
                    print("Minim noduri create: ", min(noduri_calculator))
                    print("Maxim noduri create: ", max(noduri_calculator))
                    print("Mediana noduri create: ", median(noduri_calculator))
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.quit()
                        time.sleep(1)
                        main()
                        run = False
                    if event.key == pygame.K_u:
                        contor_undo += 1
                        stare_curenta = stari[len(stari) - contor_undo]
                        stare_curenta.tabla_joc.deseneaza_grid()
                        break
                if event.type == pygame.MOUSEMOTION:

                    pos = pygame.mouse.get_pos()  # coordonatele cursorului
                    for linie in range(len(Joc.celuleGrid)):
                        for coloana in range(len(Joc.celuleGrid)):
                            if Joc.celuleGrid[linie][coloana].collidepoint(pos):
                                stare_curenta.tabla_joc.deseneaza_grid(linie * Joc.NR_COLOANE + coloana)
                                break
                elif event.type == pygame.MOUSEBUTTONDOWN:  # click

                    pos = pygame.mouse.get_pos()  # coordonatele clickului

                    for linie in range(Joc.NR_COLOANE):
                        for coloana in range(Joc.NR_COLOANE):

                            if Joc.celuleGrid[linie][coloana].collidepoint(
                                    pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                ###############################
                                if stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] == Joc.JMIN:
                                    if (de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]):
                                        # daca am facut click chiar pe patratica selectata, o deselectez
                                        de_mutat = False
                                        stare_curenta.tabla_joc.deseneaza_grid()
                                    else:
                                        de_mutat = (linie, coloana)
                                        # desenez gridul cu patratelul marcat
                                        stare_curenta.tabla_joc.deseneaza_grid(de_mutat)
                                elif stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] == Joc.GOL:
                                    if de_mutat:
                                        stare_curenta.tabla_joc.matr[
                                            de_mutat[0] * Joc.NR_COLOANE + de_mutat[1]] = Joc.GOL
                                        de_mutat = False
                                    # plasez simbolul pe "tabla de joc"
                                    stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] = Joc.JMIN
                                    i = linie * Joc.NR_COLOANE + coloana
                                    t_dupa = int(round(time.time() * 1000))
                                    for j in range(i + Joc.NR_COLOANE, Joc.NR_COLOANE ** 2, 8):  # cautam in jos
                                        if stare_curenta.tabla_joc.matr[j] != Joc.GOL and stare_curenta.tabla_joc.matr[
                                            j - Joc.NR_COLOANE] == Joc.GOL:
                                            simbolGasit = stare_curenta.tabla_joc.matr[j]
                                            stare_curenta.tabla_joc.matr[j] = Joc.GOL
                                            stare_curenta.tabla_joc.matr[j - Joc.NR_COLOANE] = simbolGasit

                                    for j in range(i - Joc.NR_COLOANE, 0, -8):  # cautam in sus
                                        if stare_curenta.tabla_joc.matr[j] != Joc.GOL and stare_curenta.tabla_joc.matr[
                                            j + Joc.NR_COLOANE] == Joc.GOL:
                                            simbolGasit = stare_curenta.tabla_joc.matr[j]
                                            stare_curenta.tabla_joc.matr[j] = Joc.GOL
                                            stare_curenta.tabla_joc.matr[j + Joc.NR_COLOANE] = simbolGasit

                                    coloana_curenta = i % Joc.NR_COLOANE
                                    for j in range(i + 1,
                                                   i + (Joc.NR_COLOANE - coloana_curenta - 1) + 1):  # cautam in dreapta
                                        if stare_curenta.tabla_joc.matr[j] != Joc.GOL and stare_curenta.tabla_joc.matr[
                                            j - 1] == Joc.GOL:
                                            simbolGasit = stare_curenta.tabla_joc.matr[j]
                                            stare_curenta.tabla_joc.matr[j] = Joc.GOL
                                            stare_curenta.tabla_joc.matr[j - 1] = simbolGasit

                                    for j in range(i - 1, i - coloana_curenta - 1, -1):  # cautam in stangsThe
                                        if stare_curenta.tabla_joc.matr[j] != Joc.GOL and stare_curenta.tabla_joc.matr[
                                            j + 1] == Joc.GOL:
                                            simbolGasit = stare_curenta.tabla_joc.matr[j]
                                            stare_curenta.tabla_joc.matr[j] = Joc.GOL
                                            stare_curenta.tabla_joc.matr[j + 1] = simbolGasit
                                    stare_curenta.tabla_joc.deseneaza_grid()
                                    # afisarea starii jocului in urma mutarii utilizatorului
                                    print("\nTabla dupa mutarea jucatorului")
                                    print(str(stare_curenta))
                                    print("Utilizatorul a \"gandit\" timp de " + str(
                                        t_dupa - t_inainte) + " milisecunde.")
                                    timp_gandire_utiliz.append(int(t_dupa - t_inainte))
                                    contor_mutari_utilizator += 1
                                    # testez daca jocul a ajuns intr-o stare finala
                                    # si afisez un mesaj corespunzator in caz ca da
                                    response, pozitii_castigatoare = afis_daca_final(stare_curenta);
                                    if (response):
                                        stare_curenta.tabla_joc.deseneaza_grid(marcaj=None,
                                                                               pozitii_castigatoare=pozitii_castigatoare)
                                        time.sleep(5)
                                        ecran.fill((0, 0, 0))
                                        font = pygame.font.Font('freesansbold.ttf', 40)
                                        text = font.render(response, True, (0, 255, 0))
                                        textRect = text.get_rect()
                                        textRect.center = (200, 200)
                                        ecran.blit(text, textRect)
                                        pygame.display.update()
                                        print("Timp de gandire utiliz minim:", min(timp_gandire_utiliz))
                                        print("Timp de gandire utiliz maxim:", max(timp_gandire_utiliz))
                                        print("Timp de gandire utiliz mediu:",
                                              sum(timp_gandire_utiliz) / len(timp_gandire_utiliz))
                                        print("Timp de gandire utiliz, mediana:", median(timp_gandire_utiliz))
                                        print("Timp de gandire calc minim:", min(timp_gandire_calc))
                                        print("Timp de gandire calc maxim:", max(timp_gandire_calc))
                                        print("Timp de gandire calc mediu:",
                                              sum(timp_gandire_calc) / len(timp_gandire_calc))
                                        print("Timp de gandire calc, mediana:", median(timp_gandire_calc))
                                        print("Mutari calculator:", contor_mutari_calculator)
                                        print("Mutari utilizator:", contor_mutari_utilizator)
                                        print("Total noduri create: ", sum(noduri_calculator))
                                        print("Medie noduri create: ", sum(noduri_calculator) / len(noduri_calculator))
                                        print("Minim noduri create: ", min(noduri_calculator))
                                        print("Maxim noduri create: ", max(noduri_calculator))
                                        print("Mediana noduri create: ", median(noduri_calculator))
                                        time.sleep(2)
                                        break

                                    # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                    stari.append(stare_curenta)
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator
            contor_mutari_calculator += 1
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == 'minimax':
                contorNoduriCalc = 0
                stare_actualizata, contorNoduriCalc = min_max(stare_curenta)
                noduri_calculator.append(contorNoduriCalc)
                print("Noduri create pentru calculator: ", contorNoduriCalc)
                print("Estimare min_max", stare_actualizata.estimare)
            else:  # tip_algoritm==2
                contorNoduriCalc = 0
                stare_actualizata, contorNoduriCalc = alpha_beta(-500, 500, stare_curenta, contorNoduriCalc)
                noduri_calculator.append(contorNoduriCalc)
                print("Noduri create pentru calculator: ", contorNoduriCalc)
                print("Estimare alpha_beta", stare_actualizata.estimare)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            stare_curenta.tabla_joc.deseneaza_grid()
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            timp_gandire_calc.append(int(t_dupa - t_inainte))
            response, pozitii_castigatoare = afis_daca_final(stare_curenta);
            if (response):
                stare_curenta.tabla_joc.deseneaza_grid(marcaj=None, pozitii_castigatoare=pozitii_castigatoare)
                time.sleep(5)
                ecran.fill((0, 0, 0))
                font = pygame.font.Font('freesansbold.ttf', 20)
                text = font.render(response, True, (0, 255, 0))
                textRect = text.get_rect()
                textRect.center = (200, 200)
                ecran.blit(text, textRect)
                pygame.display.update()
                print("Timp de gandire utiliz minim:", min(timp_gandire_utiliz))
                print("Timp de gandire utiliz maxim:", max(timp_gandire_utiliz))
                print("Timp de gandire utiliz mediu:", sum(timp_gandire_utiliz) / len(timp_gandire_utiliz))
                print("Timp de gandire, utiliz mediana:", median(timp_gandire_utiliz))
                print("Timp de gandire calc minim:", min(timp_gandire_calc))
                print("Timp de gandire calc maxim:", max(timp_gandire_calc))
                print("Timp de gandire calc mediu:", sum(timp_gandire_calc) / len(timp_gandire_calc))
                print("Timp de gandire, calc mediana:", median(timp_gandire_calc))
                print("Mutari calculator:", contor_mutari_calculator)
                print("Mutari utilizator:", contor_mutari_utilizator)
                print("Medie noduri create: ", sum(noduri_calculator) / len(noduri_calculator))
                print("Minim noduri create: ", min(noduri_calculator))
                print("Maxim noduri create: ", max(noduri_calculator))
                print("Mediana noduri create: ", median(noduri_calculator))
                time.sleep(2)
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus

            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
            stari.append(stare_curenta)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    t_inainte = int(round(time.time() * 1000))
    stari = []
    timp_gandire_utiliz = []
    timp_gandire_calc = []
    noduri_calculator = []

    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t_dupa = int(round(time.time() * 1000))
                print("Timp total de rulare:", t_dupa - t_inainte, "ms")
                pygame.quit()
                sys.exit()
