from pathlib import Path
from time import monotonic, sleep

import cv2
import mediapipe as mp
import serial
from mediapipe.tasks.python import BaseOptions, vision


def policz_palce(p):
    liczba = sum(p[a].y < p[b].y for a, b in [(8, 6), (12, 10), (16, 14), (20, 18)])
    kciuk = abs(p[4].x - p[5].x) > abs(p[3].x - p[5].x) + 0.015
    return liczba + int(kciuk)

def main():
    model = Path(__file__).with_name("hand_landmarker.task")
    opcje = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(model)),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
    )
    gesty = {1: "START", 2: "STOP", 5: "RESET"}
    poprzedni = None
    od_kiedy = monotonic()
    kamera = cv2.VideoCapture(0)
    try:
        if not kamera.isOpened():
            raise SystemExit("Nie udalo sie otworzyc kamery.")
        with (
            serial.Serial('COM3', 9600, write_timeout=1) as arduino,
            vision.HandLandmarker.create_from_options(opcje) as detektor,
        ):
            sleep(2)  # Uno moze sie zresetowac po otwarciu portu.
            polecenia = {'START': b'1', 'STOP': b'0', 'RESET': b'R'}
            wyslano = False
            while True:
                ok, klatka = kamera.read()
                if not ok:
                    raise SystemExit("Nie udalo sie odczytac klatki.")
                klatka = cv2.flip(klatka, 1)
                rgb = cv2.cvtColor(klatka, cv2.COLOR_BGR2RGB)
                obraz = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                teraz = monotonic()
                wynik = detektor.detect_for_video(obraz, int(teraz * 1000))
                gest = None
                napis = "Pokaz dlon"
                if wynik.hand_landmarks:
                    punkty = wynik.hand_landmarks[0]
                    h, w = klatka.shape[:2]
                    for punkt in punkty:
                        cv2.circle(klatka, (int(punkt.x * w), int(punkt.y * h)), 4, (0, 255, 0), -1)
                    liczba = policz_palce(punkty)
                    gest = gesty.get(liczba)
                    napis = f"Palce: {liczba}"
                if gest != poprzedni:
                    poprzedni, od_kiedy = gest, teraz
                    wyslano = False
                if gest and teraz - od_kiedy >= 0.5:
                    napis += f" | {gest}"
                    if gest in polecenia and not wyslano:
                        arduino.write(polecenia[gest])
                        wyslano = True
                cv2.putText(klatka, napis, (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.imshow("VisionControl - gesty", klatka)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    except serial.SerialException as blad:
        raise SystemExit(f'Blad COM3: {blad}. Sprawdz port i zamknij Monitor portu szeregowego.') from blad
    finally:
        kamera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
