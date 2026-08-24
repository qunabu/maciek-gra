# MACIEK KONTRA NFZ

Asteroids w klimacie **kosmicznego country**. Maciek lata po orbicie i rozwala to,
co go co dzień dojeżdża: rozporządzenia, zepsute drukarki, martwe monitory,
roszczeniowych pacjentów i debili z ulicy. Mega bos: **ciocia Kasia**.

▶ **Gra:** https://qunabu.github.io/maciek-gra/

## Zasady

| rzecz | co robi |
|---|---|
| **Kutas 3000** | podstawowe uzbrojenie, spacja |
| **§ ROZPORZĄDZENIE** | stos papierów, rozpada się na mniejsze stosy |
| **DRUKARKA** | zacięta, miga na czerwono |
| **MONITOR** | padł, świeci `:(` |
| **ROSZCZENIOWA** | szybka, wredna, co kilka sekund któraś rzuca pretensją („Panie Maćku, ten przycisk to trochę za mały") — 12 kwestii z głosem |
| **DEBIL Z ULICY** | jeszcze szybszy |
| **KONTROLA NFZ** | czerwona teczka, **namierza cię i leci prosto na ciebie** |
| **ARTUR DZWONI** | zielone pulsujące kółko z telefonem, też cię namierza i nie odpuszcza. „Maciek, kurwa, czemu nie odebrałeś sekundę temu telefonu?" |
| **MATEUSZ ŚPIEWA** | wolny, gruby na 6 trafień, nie rozpada się na mniejsze. Leci zwrotkę po zwrotce, akordeon i nutki. Wchodzi raz na falę od trzeciej |
| 💚 **PIERWSZORAZOWY** | zielone serce — **łapiesz, nie strzelasz** |
| 💛 **kontynuacja** | żółte serce — przylatuje samo i psuje ci wskaźnik |
| 🔧 **DRUKARKA DO NAPRAWY** | zostaje po rozbitej drukarce — **wleć i przytrzymaj** ~1,2 s, dostajesz punkty i **TONER 3000** (podwójny ogień, 9 s). Strzelisz w nią — zepsuta na amen |

### Mechanika wskaźnika (czyli to, o co poszło)

Na górze po prawej masz **wskaźnik pierwszorazowych**: `pierwszorazowi / wszyscy`.
Pacjenci na kontynuację przylatują sami — nic nie musisz robić, a i tak wchodzą do
statystyki. Pierwszorazowych musisz **aktywnie złapać**, wlatując w nie.

Jeśli na koniec fali wskaźnik spadnie poniżej **34%**:

> **KONTROLA NFZ** — od razu tracisz 25% dorobku i przez **3 kolejne fale**
> każdy punkt liczy się razy 0,75.

Nie twoja wina, że pacjent z ulicy sam nie przyszedł. Nikogo to nie obchodzi.

Jak wskaźnik jest w normie — premia rosnąca z numerem fali.

### Ciocia Kasia

Co **piątą falę** schodzi mega bos. Trzy wzory ataku (seria decyzji w ciebie,
wachlarz paragrafów, dorzucanie problemów), gada po drodze, im mniej HP tym
bardziej wkurzona. Za ubicie: gruba premia i **jedno życie z powrotem**.

### Twarze

Wrogowie z twarzą (`babcia`, `artur`, `mateusz`) rysują się jako zdjęcie
w kółku, a jak plik nie dojdzie — jako rysowany zapas, żeby gra nigdy nie
padła na brakującym obrazku. Do repo idą tylko gotowe `*_sprite.png`;
materiał źródłowy siedzi w `.gitignore`.

Sześć roszczeniowych bab pochodzi z obrazka generowanego przez AI
(`grid_baby.png`, 3×2), pociętego na kafelki i przepuszczonego przez Vision.

## Sterowanie

| klawisz | akcja |
|---|---|
| `←` `→` | obrót |
| `↑` | ciąg |
| `SPACJA` | ognia |
| `SHIFT` | hiperprzestrzeń (teleport awaryjny, 4 s cooldownu) |
| `M` | dźwięk on/off |
| `P` | pauza |

### Telefon

`START` od razu wchodzi w pełny ekran i próbuje zablokować ekran w poziomie.
Kontrolki dotykowe pokazują się tylko w trakcie gry:

* lewy dół — obrót w lewo / w prawo,
* prawy dół — hiperprzestrzeń, ciąg, wielki różowy ogień (z wibracją),
* góra — pauza, pełny ekran, dźwięk.

Obsługa idzie przez `pointerdown` + `setPointerCapture`, więc dwa palce naraz
(obrót i ogień) działają, a zjechanie palcem z przycisku nie zostawia klawisza
wciśniętego. W pionie gra prosi o obrócenie telefonu. Zejście karty w tło
pauzuje grę.

Na iPhonie `requestFullscreen` nie działa na zwykłym elemencie — tam pełny
ekran daje dopiero zainstalowanie PWA (`display: fullscreen` w manifeście).

## PWA

Gra jest instalowalna i działa offline.

* **⤓ ZAINSTALUJ** w menu (Chrome/Edge/Android). Na iPhonie: *Udostępnij ⤴ →
  „Dodaj do ekranu początkowego"*.
* **↻ SPRAWDŹ WERSJĘ** wymusza sprawdzenie aktualizacji.
* Nowa wersja **nie wchodzi na siłę** — na górze pojawia się pasek
  „NOWA WERSJA · ODŚWIEŻ", gracz decyduje kiedy przeładować.
* Service worker: `index.html` / manifest → **najpierw sieć**, obrazki i audio →
  **najpierw cache**, odświeżane w tle. Cały audio (~3,6 MB) dociąga się po
  cichu po instalacji, więc gra chodzi bez internetu.

**Wypuszczanie nowej wersji:** podbij `WERSJA` w [`sw.js`](sw.js) i wypchnij na
`main`. GitHub Pages podmieni pliki, a graczom pokaże się pasek aktualizacji.

## Audio

Wszystko wygenerowane przez ElevenLabs — 59 kwestii mówionych (Maciek, lektor
NFZ, ciocia Kasia, roszczeniowe baby, Artur, Mateusz), 16 efektów i 5 kawałków muzyki w stylu
kosmicznego country (menu / gra / boss / koniec / wygrana).

Dźwięk silnika **nie** jest plikiem — to brązowy szum przez filtr
dolnoprzepustowy plus dwa niskie oscylatory, składane w Web Audio. Pętla z mp3
przy ciągłym dźwięku zawsze słyszalnie „klika".

```bash
echo 'ELEVEN_LABS_API_KEY=...' > .env
python3 tools/gen_audio.py          # wszystko
python3 tools/gen_audio.py sfx      # tylko efekty
python3 tools/gen_audio.py glos     # tylko kwestie
python3 tools/gen_audio.py muz      # tylko muzyka
```

Skrypt **pomija pliki, które już są** — żeby dograć nową kwestię, dopisz ją do
słownika i puść ponownie.

## Grafika

Maciek to wycięte zdjęcie (Vision `VNGenerateForegroundInstanceMaskRequest`),
reszta rysowana proceduralnie w canvasie.

```bash
swiftc -O tools/cutout.swift -o tools/cutout
./tools/cutout maciek.jpg maciek_head.png <x> <y> <w> <h>
sips -Z 360 maciek_head.png --out maciek_ship.png

swiftc -O tools/gen_ikony.swift -o tools/gen_ikony
./tools/gen_ikony "$PWD"            # ikony PWA z maciek_ship.png
```

## Odpalenie lokalnie

```bash
python3 -m http.server 8777
open http://localhost:8777
```

(Service worker wymaga `http://localhost` albo HTTPS — z `file://` nie zadziała.)
