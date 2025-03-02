from tkinter import *
import datetime
from tkinter import ttk

shown_widgets = []

class Asztal:
    def __init__(self, id, hany_fo, foglalt_e, datum):
        self.id = id
        self.hany_fo = hany_fo
        self.foglalt_e = foglalt_e
        self.datum = datum

    def __repr__(self):
        return f"{self.id};{self.hany_fo};{self.foglalt_e};{self.datum}"

class Etel:
    def __init__(self, nev, ar):
        self.nev = nev
        self.ar = ar

    def __repr__(self):
        return f"{self.nev} - {self.ar}Ft"

class Rendeles:
    def __init__(self, rendelesszama, asztalszam, rendelt_kajak):
        self.rendeles_szama = rendelesszama
        self.asztalszam = asztalszam
        self.rendelt_kajak = rendelt_kajak

    def __repr__(self):
        return f"{self.rendeles_szama};{self.asztalszam};{';'.join(self.rendelt_kajak)}"

class Gomb:
    def __init__(self, parentelement, text, command, style):
        self.parentelement = parentelement
        self.text = text
        self.command = command
        self.style = style
        
    def Letrehoz(self):
        return ttk.Button(self.parentelement, text=self.text, command=self.command, style=self.style)
        
class Felirat:
    def __init__(self, parentelement, text, fontsize, fg):
        self.parentelement = parentelement
        self.text = text
        self.fontsize = int(fontsize)
        self.bg = parentelement.cget("bg")
        self.fg = fg
    def Letrehoz(self):
        return Label(self.parentelement, text=self.text, font=("Comfortaa", self.fontsize), bg=self.bg, fg=self.fg)

# Asztalok beolvasása
asztalok_f, minden_asztal = open("asztalok.csv", "r", encoding="utf-8"), list()

for asztal in asztalok_f:
    w, x, y, z = asztal.strip().split(";")
    minden_asztal.append(Asztal(w, x, y, z))

asztalok_f.close()

# Étlap beolvasása
etlap_f, minden_etel = open("etlap.csv", "r", encoding="utf-8"), list()

for etel in etlap_f:
    x = etel.strip().split(";")
    a, b = x[0], x[1]
    minden_etel.append(Etel(a, b))

# Rendelések beolvasása
rendelesek_f,  minden_rendeles = open("rendelesek.csv", "r", encoding="utf-8"), list()

for rendeles in rendelesek_f:
    x = rendeles.strip().split(";")
    a, b = rendeles.strip().split(';')[0], rendeles.strip().split(';')[1]
    et = []
    for i in range(2, len(x)):
        et.append(x[i])
    minden_rendeles.append(Rendeles(a, b, et))

# Mentés csv-fájlba

def MentesCSV(osztaly_lista, filename):
    ki = open(filename, "w", encoding="utf-8")
    for sor in osztaly_lista:
        if type(sor) != list:
            print(sor, file = ki)
        else:
            for elem in sor[2]:
                print(elem, file=ki)

 
aktiv_rendeles_gombok = list()

# Függvények

def RemoveChildrenFrmWin(ablak):
    for child in ablak.winfo_children():
        child.grid_forget()



# Főablak

r = Tk()
r.title("Éttermi kiszolgáló rendszer")
r.call("source", "theme.tcl")
style = ttk.Style(r)
style.theme_use("theme")



# Asztalok állapota functions

global asztal_row, asztal_col
asztal_row, asztal_col = 1, 1

def AsztalKiiras():
    asztal_ki = open('asztalok.csv', 'w')
    for asztal in minden_asztal:
        rnd_str = f"{asztal.id};{asztal.hany_fo};{asztal.foglalt_e};{asztal.datum}"
        print(rnd_str, file=asztal_ki)

    asztal_ki.close()

def Asztalfoglalas(asztalszam):
    if minden_asztal[int(asztalszam)-1].foglalt_e == "S":
        minden_asztal[int(asztalszam)-1].foglalt_e = 'F'
        minden_asztal[int(asztalszam)-1].datum = datetime.datetime.now()
        foglalas_r.destroy()
        AsztalKiiras()
        asztal_allapot_cmd()

def AsztalFelszabaditas(asztalszam):
    minden_asztal[asztalszam-1].foglalt_e = "S"
    minden_asztal[asztalszam-1].datum = "0"
    AsztalKiiras()
    asztal_allapot_cmd()
    foglalas_r.destroy()    
    

def foglalasAblak(asztalszam):
    global foglalas_r
    foglalas_r = Tk()
    foglalas_r.call("source", "theme.tcl")

    style = ttk.Style(foglalas_r)
    style.theme_use('theme')
    foglalas_r.title("Foglalás")
    
    if minden_asztal[int(asztalszam)-1].foglalt_e == "S":
        Felirat(foglalas_r, f'Lefoglalja ezt az asztalt? ({asztalszam}.)', 15, 'white').Letrehoz().grid(row=0, column=0, columnspan=2, pady=(5,0))
        Gomb(foglalas_r, 'Igen', lambda:Asztalfoglalas(asztalszam), "simagomb.TButton").Letrehoz().grid(row=1, column=0, padx=5, pady=10)
        Gomb(foglalas_r, 'Nem', lambda:foglalas_r.destroy(), "simagomb.TButton").Letrehoz().grid(row=1, column=1, padx=5, pady=10)

    else:
        Felirat(foglalas_r, f'Ez az asztal már foglalt.\nKérem válasszon másik asztalt!\n\nAz asztalt ekkor foglalták le:\n{str(minden_asztal[int(asztalszam)-1].datum).split(".")[0]}\n\nFoglalt még a(z) {asztalszam}. számú asztal?', 12, 'white').Letrehoz().grid(row=0, column=0, columnspan=2, pady=(5,0))
        Gomb(foglalas_r, 'Megértettem', lambda:foglalas_r.destroy(), "simagomb.TButton").Letrehoz().grid(row=1, column=0)
        Gomb(foglalas_r, 'Az asztal szabadnak\njelölése', lambda:AsztalFelszabaditas(int(asztalszam)), "simagomb.TButton").Letrehoz().grid(row=1, column=1, padx=5, pady=10)

def BiztosFelszabadit():
    for asztal in minden_asztal:
        asztal.foglalt_e = "S"
        asztal.datum = "0"
    kisablak.destroy()
    AsztalKiiras()
    asztal_allapot_cmd()

def MindenAsztalFelszabaditasa():
    global kisablak
    kisablak = Tk()
    kisablak.call('source', 'theme.tcl')
    style = ttk.Style(kisablak)
    style.theme_use('theme')
    kisablak.title("Megerősítés")
    Felirat(kisablak, 'Biztosan minden asztalt\nszabadként szeretne megjelölni?', 12, 'white').Letrehoz().grid(row=0, column=0, columnspan=2, pady=(0, 4))

    Gomb(kisablak, 'Igen', BiztosFelszabadit, 'simagomb.TButton').Letrehoz().grid(row=1, column=0, padx=3)
    Gomb(kisablak, 'Mégsem', lambda: kisablak.destroy(), 'simagomb.TButton').Letrehoz().grid(row=1, column=1, padx=3)

szerkesztik_e = False

foszam_felirat = 0
foszam_minusz_gomb = Button()

def fok_m():
    global foszam_felirat
    global foszam_minusz_gomb
    
    if int(foszam_felirat) > 1:
        foszam_felirat = int(foszam_felirat) - 1
        foszam_felirat_felirat.config(text=foszam_felirat)
    
    else:
        foszam_minusz_gomb.config(state='disabled', bg="lightgrey")
        


def fok_p():
    global foszam_felirat
    foszam_felirat = int(foszam_felirat) + 1
    foszam_felirat_felirat.config(text=foszam_felirat)

def aszt_kap_valt_save(index, ertek):
    minden_asztal[index].hany_fo = ertek
    MentesCSV(minden_asztal, "asztalok.csv")
    asztal_allapot_cmd()
    r2.destroy()

def asztal_torlese_cmd(index):
    minden_asztal.pop(index)
    id_ind = 1
    for peldany in minden_asztal:
        peldany.id = id_ind
        id_ind += 1
    MentesCSV(minden_asztal, "asztalok.csv")
    asztal_allapot_cmd()
    r2.destroy()


def szerkesztesAblak(asztalszam):
    global foszam_felirat
    global foszam_felirat_felirat
    global r2
    r2 = Tk()
    r2.title("Asztalok módosítása")
    r2.call("source", "theme.tcl")
    style = ttk.Style(r2)
    style.theme_use("theme")  

    # címek
    Felirat(r2, f'{asztalszam}. asztal szerkesztése', 15, 'white').Letrehoz().grid(row=0, column=0, columnspan=3, pady=(0,5))
    Felirat(r2, 'Asztal kapacitása (fő)', 10, 'white').Letrehoz().grid(row=1, column=0, columnspan=3, pady=5)
    
    # minusz gomb
    foszam_minusz_gomb = Gomb(r2, '-', fok_m, "kisGomb.TButton").Letrehoz()
    foszam_minusz_gomb.grid(row=2, column=0)

    # felirat
    foszam_felirat = minden_asztal[int(asztalszam) - 1].hany_fo
    foszam_felirat_felirat = Felirat(r2, foszam_felirat, 15, 'white').Letrehoz()
    foszam_felirat_felirat.grid(row=2, column=1, pady=5)

    # plusz gomb
    Gomb(r2, '+', fok_p, "kisGomb.TButton").Letrehoz().grid(row=2, column=2)

    # mentés gomb
    Gomb(r2, 'Mentés', lambda: aszt_kap_valt_save(int(asztalszam) - 1, foszam_felirat), "simagomb.TButton").Letrehoz().grid(row=3, column=0, columnspan=3, pady=10)
    
    # asztal törlés gomb
    Gomb(r2, 'Asztal törlése', lambda: asztal_torlese_cmd(int(asztalszam) - 1), "simagomb.TButton").Letrehoz().grid(row=4, column=0, columnspan=3)
    


def szerkesztes_mod():
    global szerkesztik_e
    if szerkesztik_e:
        szerkesztik_e = False
    else:
        szerkesztik_e = True

    asztal_allapot_cmd()

foszam_felirat_felirat = Button()
foszam_minusz_gomb = Button()

def fok_m_2():
    global foszam
    global foszam_minusz_gomb

    if foszam > 1:
        foszam -= 1
        foszam_felirat_felirat.config(text=foszam)

    if foszam <= 1:
        foszam_minusz_gomb.config(state = "disabled", bg="lightgrey")

def fok_p_2():
    global foszam
    foszam += 1
    foszam_felirat_felirat.config(text=foszam)

foszam = 0

def uj_asztal_add():
    global foszam_felirat_felirat, foszam, foszam_minusz_gomb, r2
    r2 = Tk()
    r2.title("Asztal hozzáadása")
    r2.call('source', 'theme.tcl')
    style = ttk.Style(r2)
    style.theme_use('theme')

    # címek
    Felirat(r2, 'Új asztal hozzáadása', 15, 'white').Letrehoz().grid(row=0, column=0, columnspan=4, pady=(0,5))
    Felirat(r2, 'Asztal kapacitása (fő)', 10, 'white').Letrehoz().grid(row=1, column=0, columnspan=4, pady=5)
    
    # felirat
    foszam = 5
    foszam_felirat_felirat = Felirat(r2, foszam, 15, 'white').Letrehoz()
    
    foszam_felirat_felirat.grid(row=2, column=1, columnspan=2, pady=5)

    # minusz gomb
    foszam_minusz_gomb = Gomb(r2, '-', fok_m_2, "kisGomb.TButton").Letrehoz()
    foszam_minusz_gomb.grid(row=2, column=0)

    
    
    # plusz gomb
    Gomb(r2, '+', fok_p_2, "kisGomb.TButton").Letrehoz().grid(row=2, column=3)

    # mentés gomb
    Gomb(r2, 'Mentés', save_table, "simagomb.TButton").Letrehoz().grid(row=3, column=0, columnspan=2, pady=10, padx=4)
    
    # mégse gomb
    Gomb(r2, 'Mégse', lambda: r2.destroy(), "simagomb.TButton").Letrehoz().grid(row=3, column=2, columnspan=2, pady=10, padx=4)

def save_table():
    global r2
    r2.destroy()
    minden_asztal.append(Asztal(len(minden_asztal)+1, foszam, "S", "0"))
    MentesCSV(minden_asztal, "asztalok.csv")
    asztal_allapot_cmd()
    


def asztal_allapot_cmd():
    global n_row, n_col, szerkesztik_e
    
    RemoveChildrenFrmWin(r)

    n_row, n_col = 1, 0

    k1 = Frame(r, background="#007FFF")
    k1.grid(row=0, column=0, columnspan=2, padx=4, pady=(10,20))
    asztal_gomb1 = Gomb(k1, "\nMenü\n", MenuGombokShow, "szelesGombFelso.TButton").Letrehoz()
    asztal_gomb1.grid(row=0, column=0, columnspan=2, padx=3, pady=3)

    k2 = Frame(r, background="#007FFF")
    k2.grid(row=0, column=2, columnspan=2, padx=4, pady=(10,20))
    asztal_gomb2 = Gomb(k2, "\nMinden asztal felszabadítása\n", MindenAsztalFelszabaditasa, "szelesGombFelso.TButton").Letrehoz()
    asztal_gomb2.grid(row=0, column=2, columnspan=2, padx=3, pady=3)

    k3 = Frame(r, background="#007FFF")
    k3.grid(row=0, column=4, columnspan=2, padx=4, pady=(10,20))

    k4 = Frame(r, background="#007FFF")
    k4.grid(row=0, column=6, columnspan=2, padx=4, pady=(10,20))
    asztal_gomb4 = Gomb(k4, "\nMentés & bezárás\n", lambda: r.destroy(), "szelesGombFelso.TButton").Letrehoz()
    asztal_gomb4.grid(row=0, column=6, columnspan=2, padx=3, pady=3)

    if szerkesztik_e:
        gomb3 = Gomb(k3, "\nSzerkesztés befejezése\n", szerkesztes_mod, "szelesGombFelso.TButton").Letrehoz()
        gomb3.grid(row=0, column=4, columnspan=2, padx=3, pady=3)
        asztal_gomb1.config(style='szelesGombFelsoDisabled.TButton', state='disabled')
        asztal_gomb2.config(style='szelesGombFelsoDisabled.TButton', state='disabled')
        asztal_gomb4.config(style='szelesGombFelsoDisabled.TButton', state='disabled')

        for asztal in minden_asztal:
            a = Gomb(r, f'{asztal.id}. asztal\n{asztal.hany_fo} fő', lambda x = asztal.id: szerkesztesAblak(x), "simagomb.TButton").Letrehoz()
            a.grid(row=n_row, column=n_col, padx=5, pady=5)
            shown_widgets.append(a)
            n_col += 1
            if n_col == 8:
                n_col = 0
                n_row += 1

        # Új asztal hozzáadása GOMB
        plusz_asztal_but = Gomb(r, '+', uj_asztal_add, "kisGomb.TButton").Letrehoz()
        plusz_asztal_but.grid(row=n_row, column=n_col)

    else:
        gomb3 = Gomb(k3, "\nAsztalok módosítása \n", szerkesztes_mod, "szelesGombFelso.TButton").Letrehoz()
        gomb3.grid(row=0, column=4, columnspan=2, padx=3, pady=3)

        for asztal in minden_asztal:
            if asztal.foglalt_e == "S":
                a = Gomb(r, f'{asztal.id}. asztal\n{asztal.hany_fo} fő', lambda x = asztal.id: foglalasAblak(x), "szabadAsztal.TButton").Letrehoz()
            else:
                a = Gomb(r, f'{asztal.id}. asztal\n{asztal.hany_fo} fő', lambda x = asztal.id: foglalasAblak(x), "foglaltAsztal.TButton").Letrehoz()
            a.grid(row=n_row, column=n_col, padx=5, pady=5)
            shown_widgets.append(a)
            n_col += 1
            if n_col == 8:
                n_col = 0
                n_row += 1

def hide_all(): # Az összes olyan widget eltüntetése, ami nem kell csak kattintáskor és benne van a "shown_widgets" listában.
    global n_row, n_col
    for w in shown_widgets:
        w.grid_forget()


def hide_all_w(ablak):
    for child in ablak.winfo_children():
        child.grid_forget()
    

    n_row, n_col = 1, 0
# Asztalok állapota functions vége

# Felvett rendelések functions

def elkeszult_rendeles(index):
    global masik_kisablak
    minden_rendeles.pop(index)
    MentesCSV(minden_rendeles, 'rendelesek.csv')
    hide_all()
    felvett_rendelesek_cmd()
    masik_kisablak.destroy()

def RendelesAdatai(rend_szam):
    global masik_kisablak

    for rendeles in minden_rendeles:
        if rendeles.rendeles_szama == rend_szam:
            ez_egy_szam = minden_rendeles.index(rendeles)

    masik_kisablak = Tk()
    masik_kisablak.title(f"{minden_rendeles[ez_egy_szam].rendeles_szama}. számú rendelés adatai")
    masik_kisablak.call('source', 'theme.tcl')
    style = ttk.Style(masik_kisablak)
    style.theme_use('theme')

    Felirat(masik_kisablak, f'{minden_rendeles[ez_egy_szam].rendeles_szama}. számú rendelés adatai', 15, "white").Letrehoz().pack(pady=10)
    Felirat(masik_kisablak, f"Asztal: {minden_rendeles[ez_egy_szam].asztalszam}", 10, "white").Letrehoz().pack(pady=10)

    Gomb(masik_kisablak, "Elkészült a rendelés", lambda: elkeszult_rendeles(ez_egy_szam), "simagomb.TButton").Letrehoz().pack(pady=10)

    Felirat(masik_kisablak, 'Rendelt ételek: ', 15, "white").Letrehoz().pack(pady=10)

    for item in minden_rendeles[int(ez_egy_szam)].rendelt_kajak:
        Felirat(masik_kisablak, item.strip("'").strip("[").strip("]").strip(" '"),  10, "white").Letrehoz().pack()

def felvett_rendelesek_cmd():
    global shown_widgets, n_row, n_col

    for child in r.winfo_children():
        child.grid_forget()

    k1 = Frame(r, background="#007FFF")
    k1.grid(row=0, column=0, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb1 = Gomb(k1, "\nMenü\n", MenuGombokShow, "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb1.grid(row=0, column=0, columnspan=2, padx=3, pady=3)

    k2 = Frame(r, background="#007FFF")
    k2.grid(row=0, column=2, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb2 = Gomb(k2, "\n\n", semmi_sem, "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb2.grid(row=0, column=2, columnspan=2, padx=3, pady=3)

    k3 = Frame(r, background="#007FFF")
    k3.grid(row=0, column=4, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb3 = Gomb(k3, "\n\n", semmi_sem, "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb3.grid(row=0, column=4, columnspan=2, padx=3, pady=3)

    k4 = Frame(r, background="#007FFF")
    k4.grid(row=0, column=6, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb4 = Gomb(k4, "\nMentés és bezárás\n", lambda: r.destroy(), "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb4.grid(row=0, column=6, columnspan=2, padx=3, pady=3)

    n_row, n_col = 1, 0
    for rendeles in minden_rendeles:
        r_gomb = Gomb(r, f'{rendeles.rendeles_szama}\nAsztal: {rendeles.asztalszam}', lambda x = rendeles.rendeles_szama: RendelesAdatai(x), "rendelesekGomb.TButton").Letrehoz()
        r_gomb.grid(row=n_row, column=n_col, pady=10, padx=10)
        shown_widgets.append(r_gomb)
        aktiv_rendeles_gombok.append(r_gomb)
        n_col += 1
        if n_col == 8:
            n_col = 0
            n_row += 1

# Felvett rendelések functions vége

# Új rendelés felvétele functions

rendeles_reszei = {}

def add_hozza(kaja, frame):
    global rendeles_reszei
    for elem in rendeles_reszei.keys():
        if elem == kaja:
            rendeles_reszei[kaja] += 1
    if kaja not in rendeles_reszei.keys():
        rendeles_reszei[kaja] = 1

    JobbOldaliWidUpdate(frame)

def ossz_kaja_del(frame):
    global rendeles_reszei
    rendeles_reszei = {}
    JobbOldaliWidUpdate(frame)

def rendeles_leadas(asztalszam):
    global rendeles_reszei
    if asztalid_final != 0:
        s_lista = list()
        for etel in rendeles_reszei.keys():
            rng = rendeles_reszei[etel]
            for e in range(rng):
                s_lista.append(etel)

        if len(minden_rendeles) > 0:
            minden_rendeles.append(Rendeles((int(minden_rendeles[-1].rendeles_szama) + 1), asztalszam, s_lista))
        else:
            minden_rendeles.append(Rendeles(101, asztalszam, s_lista))
        rendeles_reszei = {}
        for x in minden_asztal:
            if x.id == asztalid_final:
                x.foglalt_e = "F"
        MentesCSV(minden_asztal, "asztalok.csv")
        MentesCSV(minden_rendeles, 'rendelesek.csv')
        AsztalKivalasztva(asztalszam)
    MenuGombokShow()

def AsztalKivalasztva(asztalid):
    global asztalid_final, r
    asztalid_final = asztalid

    n_row, n_col = 1, 0
    RemoveChildrenFrmWin(r)

    k1 = Frame(r, background="#007FFF")
    k1.grid(row=0, column=0, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb1 = Gomb(k1, "\nMégsem\n", MenuGombokShow, "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb1.grid(row=0, column=2, columnspan=2, padx=3, pady=3)

    k2 = Frame(r, background="#007FFF")
    k2.grid(row=0, column=2, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb2 = Gomb(k2, "\nRendelés leadása\n", lambda: rendeles_leadas(asztalid_final), "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb2.grid(row=0, column=2, columnspan=2, padx=3, pady=3)

    k3 = Frame(r, background="#007FFF")
    k3.grid(row=0, column=4, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb3 = Gomb(k3, "\n\n", semmi_sem, "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb3.grid(row=0, column=4, columnspan=2, padx=3, pady=3)

    k4 = Frame(r, background="#007FFF")
    k4.grid(row=0, column=6, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb1 = Gomb(k4, "\n\n", semmi_sem, "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb1.grid(row=0, column=6, columnspan=2, padx=3, pady=3)

    for asztal in minden_asztal:
        if asztal.id == asztalid:
            a = Gomb(r, f'{asztal.id}. asztal\n{asztal.hany_fo} fő', lambda x = asztal.id: AsztalKivalasztva(x), "kivalasztottAsztal.TButton").Letrehoz()
        elif asztal.foglalt_e == "S":
            a = Gomb(r, f'{asztal.id}. asztal\n{asztal.hany_fo} fő', lambda x = asztal.id: AsztalKivalasztva(x), "szabadAsztal.TButton").Letrehoz()
        else:
            a = Gomb(r, f'{asztal.id}. asztal\n{asztal.hany_fo} fő', semmi_sem, "foglaltAsztal.TButton").Letrehoz()
            a.config(state='disabled')
        a.grid(row=n_row, column=n_col, padx=5, pady=5)
        shown_widgets.append(a)
        n_col += 1
        if n_col == 8:
            n_col = 0
            n_row += 1

asztalid_final = 0

def AsztalValasztas():
    global r, asztalid_final, rendeles_reszei

    if len(rendeles_reszei) > 0:

        RemoveChildrenFrmWin(r)

        asztalid_final = 0

        n_row, n_col = 1, 0

        k1 = Frame(r, background="#007FFF")
        k1.grid(row=0, column=0, columnspan=2, padx=4, pady=(10,20))
        uj_rend_gomb1 = Gomb(k1, "\nMégsem\n", megsem_cmd_cmd, "szelesGombFelso.TButton").Letrehoz()
        uj_rend_gomb1.grid(row=0, column=2, columnspan=2, padx=3, pady=3)

        k2 = Frame(r, background="#007FFF")
        k2.grid(row=0, column=2, columnspan=2, padx=4, pady=(10,20))
        uj_rend_gomb2 = Gomb(k2, "\nRendelés leadása\n", lambda: rendeles_leadas(asztalid_final), "szelesGombFelso.TButton").Letrehoz()
        uj_rend_gomb2.grid(row=0, column=2, columnspan=2, padx=3, pady=3)

        k3 = Frame(r, background="#007FFF")
        k3.grid(row=0, column=4, columnspan=2, padx=4, pady=(10,20))
        uj_rend_gomb3 = Gomb(k3, "\n\n", semmi_sem, "szelesGombFelso.TButton").Letrehoz()
        uj_rend_gomb3.grid(row=0, column=4, columnspan=2, padx=3, pady=3)

        k4 = Frame(r, background="#007FFF")
        k4.grid(row=0, column=6, columnspan=2, padx=4, pady=(10,20))
        uj_rend_gomb1 = Gomb(k4, "\n\n", semmi_sem, "szelesGombFelso.TButton").Letrehoz()
        uj_rend_gomb1.grid(row=0, column=6, columnspan=2, padx=3, pady=3)

        for asztal in minden_asztal:
            if asztal.foglalt_e == "S":
                a = Gomb(r, f'{asztal.id}. asztal\n{asztal.hany_fo} fő', lambda x = asztal.id: AsztalKivalasztva(x), "szabadAsztal.TButton").Letrehoz()
            else:
                a = Gomb(r, f'{asztal.id}. asztal\n{asztal.hany_fo} fő', semmi_sem, "foglaltAsztal.TButton").Letrehoz()
                a.config(state='disabled')
            a.grid(row=n_row, column=n_col, padx=5, pady=5)
            shown_widgets.append(a)
            n_col += 1
            if n_col == 8:
                n_col = 0
                n_row += 1

def megsem_cmd_cmd():
    global rendeles_reszei
    MenuGombokShow()
    rendeles_reszei = dict()
    
def uj_rendeles_cmd(): # Új rendelés felvétele (főmenü gomb)
    global n_row, plusz

    RemoveChildrenFrmWin(r)

    k1 = Frame(r, background="#007FFF")
    k1.grid(row=0, column=0, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb1 = Gomb(k1, "\nMégsem\n", megsem_cmd_cmd, "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb1.grid(row=0, column=0, columnspan=2, padx=3, pady=3)

    k2 = Frame(r, background="#007FFF")
    k2.grid(row=0, column=2, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb2 = Gomb(k2, "\nÖsszes étel törlése\n", lambda: ossz_kaja_del(scrollable_frame2), "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb2.grid(row=0, column=4, columnspan=2, padx=3, pady=3)

    k3 = Frame(r, background="#007FFF")
    k3.grid(row=0, column=4, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb3 = Gomb(k3, "\nTovább >>\n", AsztalValasztas, "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb3.grid(row=0, column=2, columnspan=2, padx=3, pady=3)

    k4 = Frame(r, background="#007FFF")
    k4.grid(row=0, column=6, columnspan=2, padx=4, pady=(10,20))
    uj_rend_gomb4 = Gomb(k4, "\n\n", semmi_sem, "szelesGombFelso.TButton").Letrehoz()
    uj_rend_gomb4.grid(row=0, column=6, columnspan=2, padx=3, pady=3)

    # Új rendelés - JOBB oldal

    tarolo2 = Frame(r, pady=5)
    canvas2 = Canvas(tarolo2, height=320, width=500)
    scrollbar2 = Scrollbar(tarolo2, orient="vertical", command=canvas2.yview)
    scrollable_frame2 = Frame(canvas2, pady=5)

    scrollable_frame2.bind(
        "<Configure>",
        lambda e: canvas2.configure(
            scrollregion=canvas2.bbox("all")
        )
    )

    canvas2.create_window((0, 0), window=scrollable_frame2, anchor="nw")
    canvas2.configure(yscrollcommand=scrollbar2.set)
    tarolo2.grid(row=1, column=4, columnspan=4)
    canvas2.pack(side="left", fill="both", expand=True)
    scrollbar2.pack(side="right", fill="y")


    # Új rendelés - BAL oldal

    tarolo = Frame(r, pady=5)
    canvas = Canvas(tarolo, height=320, width=450)
    scrollbar = Scrollbar(tarolo, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, pady=5)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    sor = 0
    for etel in minden_etel:
        rend = Gomb(scrollable_frame, f'{etel.nev} {etel.ar}', lambda kaja = etel.nev: add_hozza(kaja, scrollable_frame2), "simagomb.TButton").Letrehoz()
        rend.config(width=60, compound='left')
        rend.grid(row=sor, column=0, pady=1)
        sor += 1

    tarolo.grid(row=1, column=0, columnspan=4)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # BAL oldal vége

def semmi_sem():
    pass

def m_minusz(gomb, kajagomb):
    rendeles_reszei[kajagomb.cget('text')] -= 1
    gomb.config(text=rendeles_reszei[kajagomb.cget('text')])
    if gomb.cget('text') == 0:
        rendeles_reszei.pop(kajagomb.cget('text'))
        gomb.destroy()
        kajagomb.destroy()


def JobbOldaliWidUpdate(sc_fr):
    sor = 0
    for child in sc_fr.winfo_children():
        child.grid_forget()

    for elem in rendeles_reszei.keys():
        g = Gomb(sc_fr, elem, semmi_sem,"simagomb.TButton").Letrehoz()
        g.config(width=40)
        g.grid(row=sor, column=0, pady=2)
        t = Gomb(sc_fr, rendeles_reszei[elem], semmi_sem, 'nostyleGomb.TButton').Letrehoz()
        t.grid(row=sor, column=1)
        t.config(image=kuka, compound='left', command=lambda x = t, y = g: m_minusz(x, y))
        sor += 1

# Rendelés felvétele funtions vége
        
# Ikonok
asztalok_kep = PhotoImage(file='theme/asztalok.png')
mentes_bezaras_kep = PhotoImage(file='theme/mentes-bezaras.png')
uj_rendeles_kep = PhotoImage(file='theme/uj_rendeles.png')
aktiv_rendeles_kep = PhotoImage(file='theme/aktiv_rendeles.png')
kuka = PhotoImage(file='theme/kuka.png')
#Ikonok vége

# Kezdő gombok
def MenuGombokShow():
    RemoveChildrenFrmWin(r)
    

    k1 = Frame(r, background= "#007FFF")
    k1.grid(row=0, column=0, pady=10, padx=10)
    asztal_allapot_but = Gomb(k1, "\n\nAsztalok állapota\n\n", asztal_allapot_cmd, "szelesGomb.TButton").Letrehoz()
    asztal_allapot_but.config(image=asztalok_kep, compound='right')
    asztal_allapot_but.grid(row=0, column=0, pady=6, padx=6)

    k2 = Frame(r, background= "#007FFF")
    k2.grid(row=0, column=1, pady=10, padx=10)
    uj_rendeles_but = Gomb(k2, "\n\nÚj rendelés felvétele\n\n", uj_rendeles_cmd, "szelesGomb.TButton").Letrehoz()
    uj_rendeles_but.config(image=uj_rendeles_kep, compound='right')
    uj_rendeles_but.grid(row=0, column=1, pady=6, padx=6)

    k3 = Frame(r, background= "#007FFF")
    k3.grid(row=1, column=0, pady=10, padx=10)
    felvett_rendelesek_but = Gomb(k3, "\n\nFelvett rendelések\n\n", felvett_rendelesek_cmd, "szelesGomb.TButton").Letrehoz()
    felvett_rendelesek_but.config(image=aktiv_rendeles_kep, compound='right')
    felvett_rendelesek_but.grid(row=1, column=0, pady=6, padx=6)

    k4 = Frame(r, background= "#007FFF")
    k4.grid(row=1, column=1, pady=10, padx=10)
    save_close_but = Gomb(k4, "\n\nMentés & bezárás\n\n", lambda: r.destroy(), "szelesGomb.TButton").Letrehoz()
    save_close_but.config(image=mentes_bezaras_kep, compound='right')
    save_close_but.grid(row=1, column=1, pady=6, padx=6)

#Kezdő gombok vége

MenuGombokShow()

r.mainloop()