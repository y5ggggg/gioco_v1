import arcade

# Spritesheet condiviso dal pilota
SHEET_PATH = "./pilota/pilota_sheet.png"
FRAME_W = 233
FRAME_H = 239
SHEET_COLS = 3


class SpriteAnimato(arcade.Sprite):
    """
    Sprite del pilota con animazioni già caricate dallo spritesheet.

    Animazioni disponibili:
    "idle" = fermo (default)
    "run" = corsa (←/→)
    "jump" = salto (↑/W/Space)
    "crouch" = accovacciato (loop)
    "slide" = scivolata (una volta sola, poi torna idle)
    "win" = vittoria (loop)

    Uso minimo:
    pilota = SpriteAnimato(scala=0.5)
    pilota.imposta_animazione("run") # in on_key_press
    pilota.update_animation(delta_time) # in on_update
    """

    def __init__(self, scala: float = 1.0):
        super().__init__(scale=scala)
        self.animazioni: dict = {}
        self.animazione_corrente: str | None = None
        self.animazione_default: str | None = None
        self.tempo_frame: float = 0.0
        self.indice_frame: int = 0

        # --- Carica tutte le animazioni del pilota ---
        #
        # Struttura dello spritesheet (pilota_sheet.png):
        # riga 0 → idle (1 frame)
        # riga 1 → run (3 frame: pilota5, pilota7, pilota2)
        # riga 2 → jump (3 frame: pilota10, pilota11, pilota9)
        # riga 3 → crouch (3 frame: pilota3, pilota4, pilota11)
        # riga 4 → slide (1 frame: pilota6)
        # riga 5 → win (1 frame: pilota12)
        #
        self.aggiungi_animazione("idle", SHEET_PATH, FRAME_W, FRAME_H, num_frame=1, colonne=SHEET_COLS, durata=0.6, loop=True, default=True, riga=0)
        self.aggiungi_animazione("run", SHEET_PATH, FRAME_W, FRAME_H, num_frame=3, colonne=SHEET_COLS, durata=0.4, loop=True, riga=1)
        self.aggiungi_animazione("crouch", SHEET_PATH, FRAME_W, FRAME_H, num_frame=3, colonne=SHEET_COLS, durata=0.4, loop=False, riga=2)
        self.aggiungi_animazione("jump", SHEET_PATH, FRAME_W, FRAME_H, num_frame=3, colonne=SHEET_COLS, durata=1.0, loop=False, riga=3)
        self.aggiungi_animazione("slide", SHEET_PATH, FRAME_W, FRAME_H, num_frame=1, colonne=SHEET_COLS, durata=0.3, loop=False, riga=4)
        self.aggiungi_animazione("win", SHEET_PATH, FRAME_W, FRAME_H, num_frame=1, colonne=SHEET_COLS, durata=1.0, loop=True, riga=5)

    def aggiungi_animazione(
        self,
        nome: str,
        percorso: str,
        frame_width: int,
        frame_height: int,
        num_frame: int,
        colonne: int,
        durata: float,
        loop: bool = True,
        default: bool = False,
        riga: int = 0,
    ):
        """
        Carica le texture dallo spritesheet e registra l'animazione.

        Parametri:
        nome : identificatore dell'animazione
        percorso : path al file spritesheet PNG
        frame_width : larghezza di ogni cella in pixel
        frame_height: altezza di ogni cella in pixel
        num_frame : numero di frame di QUESTA animazione
        colonne : numero totale di colonne dello spritesheet
        durata : durata totale in secondi dell'animazione
        loop : True = ripeti in loop, False = riproduci una volta sola
        default : True = torna a questa animazione quando una non-loop finisce
        riga : riga dello spritesheet (0 = prima riga)
        """
        sheet = arcade.load_spritesheet(percorso)
        offset = riga * colonne
        tutti = sheet.get_texture_grid(
        size=(frame_width, frame_height),
        columns=colonne,
        count=offset + num_frame,
    )
        self._registra(nome, tutti[offset:offset + num_frame], durata, loop, default)

    def _registra(self, nome: str, textures, durata: float, loop: bool, default: bool = False):
        self.animazioni[nome] = {
        "textures": list(textures),
        "durata_frame": durata / max(len(textures), 1),
        "loop": loop,
        }
        if default or self.animazione_default is None:
            self.animazione_default = nome
        if self.animazione_corrente is None:
            self._vai(nome)

    def imposta_animazione(self, nome: str):
        """Cambia animazione solo se diversa da quella attiva (evita reset del frame)."""
        if nome != self.animazione_corrente and nome in self.animazioni:
            self._vai(nome)

    def _vai(self, nome: str):
        self.animazione_corrente = nome
        self.indice_frame = 0
        self.tempo_frame = 0.0
        if self.animazioni[nome]["textures"]:
            self.texture = self.animazioni[nome]["textures"][0]

    def update_animation(self, delta_time: float = 1 / 60):
        if not self.animazione_corrente:
            return
        anim = self.animazioni[self.animazione_corrente]
        self.tempo_frame += delta_time

        if self.tempo_frame < anim["durata_frame"]:
            return

        self.tempo_frame -= anim["durata_frame"]
        prossimo = self.indice_frame + 1

        if prossimo < len(anim["textures"]):
            self.indice_frame = prossimo
        elif anim["loop"]:
            self.indice_frame = 0
        else:
        # Animazione finita e non-loop: torna alla default
            self._vai(self.animazione_default)
            return

        self.texture = anim["textures"][self.indice_frame]