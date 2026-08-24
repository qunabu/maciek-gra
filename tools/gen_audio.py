#!/usr/bin/env python3
"""Generuje głosy, efekty i muzykę (kosmiczne country) przez ElevenLabs do audio/."""
import json, os, subprocess, sys, time

BAZA = '/Users/mateuszwojczal/Desktop/localhost/maciek-gra'
KLUCZ = None
for linia in open(BAZA + '/.env'):
    if linia.startswith('ELEVEN_LABS_API_KEY='):
        KLUCZ = linia.split('=', 1)[1].strip()
assert KLUCZ, 'brak klucza'

KAT = BAZA + '/audio'
os.makedirs(KAT, exist_ok=True)
MODEL = 'eleven_multilingual_v2'

MACIEK = 'pNInz6obpgDQGcFmaJgB'   # Adam
URZAD  = 'ErXwobaYiN019PkySvjV'   # Antoni - lektor NFZ
KASIA  = '21m00Tcm4TlvDq8ikWAM'   # Rachel - ciocia Kasia


def poslij(url, dane, plik, proby=3):
    sciezka = os.path.join(KAT, plik)
    if os.path.exists(sciezka) and os.path.getsize(sciezka) > 2000:
        return 'pominięto (jest)'
    for p in range(proby):
        wynik = subprocess.run(
            ['curl', '-s', '-o', sciezka, '-w', '%{http_code}', '--max-time', '300',
             '-X', 'POST', url,
             '-H', 'xi-api-key: ' + KLUCZ,
             '-H', 'Content-Type: application/json',
             '-d', json.dumps(dane)],
            capture_output=True, text=True)
        kod = wynik.stdout.strip()
        rozmiar = os.path.getsize(sciezka) if os.path.exists(sciezka) else 0
        if kod == '200' and rozmiar > 1000:
            return 'OK %.0f KB' % (rozmiar / 1024)
        tresc = ''
        if os.path.exists(sciezka):
            tresc = open(sciezka, 'rb').read()[:200].decode('utf-8', 'replace')
            os.remove(sciezka)
        if p == proby - 1:
            return 'BŁĄD HTTP %s %s' % (kod, tresc)
        time.sleep(3 * (p + 1))


def mowa(plik, tekst, glos, styl=0.4, stab=0.45):
    return poslij('https://api.elevenlabs.io/v1/text-to-speech/' + glos,
                  {'text': tekst, 'model_id': MODEL,
                   'voice_settings': {'stability': stab, 'similarity_boost': 0.75,
                                      'style': styl, 'use_speaker_boost': True}},
                  plik)


def efekt(plik, opis, sek):
    return poslij('https://api.elevenlabs.io/v1/sound-generation',
                  {'text': opis, 'duration_seconds': sek, 'prompt_influence': 0.75}, plik)


def muzyka(plik, opis, ms):
    return poslij('https://api.elevenlabs.io/v1/music',
                  {'prompt': opis, 'music_length_ms': ms}, plik)


# --- Maciek ---------------------------------------------------------------
MACIEK_LINIE = {
    'm_start':     'No dobra. Znowu ja.',
    'm_strzal1':   'Masz.',
    'm_strzal2':   'Won.',
    'm_strzal3':   'Nastepny.',
    'm_drukarka':  'Znowu ta cholerna drukarka.',
    'm_monitor':   'Monitor padl. Piekna sprawa.',
    'm_paragraf':  'Kolejne rozporzadzenie. Genialnie.',
    'm_babcia':    'Prosze pani, ja tu tylko pracuje.',
    'm_debil':     'Panie, ja nie jestem od tego.',
    'm_pacjent':   'O! Pierwszorazowy! Bierzemy!',
    'm_smierc':    'No i po ptakach.',
    'm_koniec':    'Koniec. Idziemy na piwo.',
    'm_boss':      'O nie. Tylko nie ona.',
    'm_zycie':     'Jeszcze zyje. Jakims cudem.',
    'm_kara':      'Dwadziescia piec procent. Za co?!',
    'm_wygrana':   'Pokonalem ciocie Kasie. Niemozliwe.',
    'm_low':       'Malo pierwszorazowych. Bedzie kontrola.',
}

# --- lektor NFZ -----------------------------------------------------------
URZAD_LINIE = {
    'u_fala':      'Nowy okres rozliczeniowy.',
    'u_ostrzez':   'Uwaga. Zbyt niski przyrost pacjentow pierwszorazowych.',
    'u_kara':      'Kontrola. Kara: dwadziescia piec procent przychodu przez trzy fale.',
    'u_kontrola':  'Kontrola Narodowego Funduszu Zdrowia.',
    'u_boss':      'Uwaga. Wykryto jednostke nadrzedna.',
    'u_koniec':    'Umowa rozwiazana. Do widzenia.',
    'u_ratio_ok':  'Wskaznik pierwszorazowych w normie.',
    'u_bonus':     'Premia za realizacje swiadczen.',
}

# --- ciocia Kasia (mega bos) ---------------------------------------------
KASIA_LINIE = {
    'k_wejscie':   'Macius. A gdzie sprawozdanie?',
    'k_atak1':     'Paragraf drugi, ustep piaty!',
    'k_atak2':     'To sie tak nie rozlicza, Maciusiu.',
    'k_atak3':     'Zalacznik numer siedem. Poprosze.',
    'k_atak4':     'A ja mowilam, ze tak bedzie.',
    'k_trafiona':  'Jak ty sie do cioci odzywasz!',
    'k_smierc':    'Ja to jeszcze zaskarze!',
    'k_wygrana':   'Wiedzialam, ze sobie nie poradzisz.',
}

EFEKTY = {
    'sfx_strzal':   ('retro sci-fi laser pew, short punchy synth zap, arcade shooter', 0.5),
    'sfx_bum':      ('arcade explosion, crunchy retro boom with debris, short', 0.9),
    'sfx_drukarka': ('office printer jamming, grinding gears, paper crumple, short', 1.0),
    'sfx_monitor':  ('CRT monitor imploding, glass shatter with electric zap, short', 1.0),
    'sfx_paragraf': ('paper stack thud with rubber stamp bang, bureaucratic, short', 0.8),
    'sfx_pacjent':  ('bright positive pickup chime, two ascending bell notes, arcade', 0.7),
    'sfx_kara':     ('harsh alarm buzzer, official rejection sound, descending, short', 1.2),
    'sfx_boss':     ('ominous deep synth riser with metallic clang, boss appears, cinematic', 2.0),
    'sfx_hit':      ('short dull impact thud, player takes damage, arcade', 0.5),
    'sfx_smierc':   ('retro arcade game over descending tone with explosion', 1.5),
    'sfx_hiper':    ('sci-fi teleport whoosh, quick warp jump, short', 0.7),
}

MUZYKA = {
    'muz_menu': ('Lonely cosmic country, slow spaghetti western in outer space, twangy reverb-drenched '
                 'electric guitar, pedal steel slide, warm analog synth pad drone, sparse brushed drums, '
                 'wide starry atmosphere, seamless loop, instrumental, no vocals', 30000),
    'muz_gra':  ('Driving space country rock, outlaw western in orbit, twangy telecaster riff, pedal steel '
                 'wails, retro sci-fi synth arpeggio, steady train-beat drums, upright bass, dusty and '
                 'cosmic, energetic, seamless loop, instrumental, no vocals', 45000),
    'muz_boss': ('Dark cosmic country showdown, tense tremolo guitar duel, ominous pedal steel bends, heavy '
                 'synth bass pulse, galloping drums, space western standoff, dramatic, seamless loop, '
                 'instrumental, no vocals', 35000),
    'muz_koniec': ('Sad slow space country outro, lonely slide guitar with long reverb, quiet synth pad, '
                   'melancholic western farewell, short, instrumental, no vocals', 14000),
    'muz_wygrana': ('Triumphant cosmic country fanfare, celebratory twangy guitar, pedal steel, uplifting, '
                    'short, instrumental, no vocals', 12000),
}


def main():
    tylko = sys.argv[1] if len(sys.argv) > 1 else 'all'
    wynik = {}
    if tylko in ('all', 'glos'):
        print('=== MACIEK ===', flush=True)
        for k, t in MACIEK_LINIE.items():
            wynik[k] = mowa(k + '.mp3', t, MACIEK, styl=0.5)
            print('%-14s %s  "%s"' % (k, wynik[k], t), flush=True)
        print('=== LEKTOR NFZ ===', flush=True)
        for k, t in URZAD_LINIE.items():
            wynik[k] = mowa(k + '.mp3', t, URZAD, styl=0.15, stab=0.7)
            print('%-14s %s  "%s"' % (k, wynik[k], t), flush=True)
        print('=== CIOCIA KASIA ===', flush=True)
        for k, t in KASIA_LINIE.items():
            wynik[k] = mowa(k + '.mp3', t, KASIA, styl=0.6)
            print('%-14s %s  "%s"' % (k, wynik[k], t), flush=True)
    if tylko in ('all', 'sfx'):
        print('=== EFEKTY ===', flush=True)
        for k, (opis, sek) in EFEKTY.items():
            wynik[k] = efekt(k + '.mp3', opis, sek)
            print('%-14s %s' % (k, wynik[k]), flush=True)
    if tylko in ('all', 'muz'):
        print('=== MUZYKA (kosmiczne country) ===', flush=True)
        for k, (opis, ms) in MUZYKA.items():
            wynik[k] = muzyka(k + '.mp3', opis, ms)
            print('%-14s %s' % (k, wynik[k]), flush=True)

    bledy = {k: v for k, v in wynik.items() if v and v.startswith('BŁĄD')}
    stary = {}
    mp = os.path.join(KAT, 'manifest.json')
    if os.path.exists(mp):
        stary = json.load(open(mp)).get('wynik', {})
    stary.update(wynik)
    json.dump({'maciek': MACIEK_LINIE, 'urzad': URZAD_LINIE, 'kasia': KASIA_LINIE,
               'wynik': stary}, open(mp, 'w'), ensure_ascii=False, indent=1)
    print('\nGOTOWE. plików: %d, błędów: %d' % (len(wynik), len(bledy)), flush=True)
    if bledy:
        print('BŁĘDY:', json.dumps(bledy, ensure_ascii=False, indent=1), flush=True)


main()
