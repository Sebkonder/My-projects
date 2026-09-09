# Instrukcja obsługi

![image desc](./ssapka.png)

* A - Kamera
* B - Obszar w którym wychwytywane są gesty ręki
* C - Tekst który opisuje jaki gest jest obecnie pokazywany, obecnie obsługiwane gesty to: Kamień, papier, nożyce, wskazywanie, machanie. 
* D - Przycisk zapisujący obecny gest wskazywany przez **C**
* E - Pole tekstowe w którym można wpisać wiadomość do zaszyfrowania
* F - Przycisk który potwierdza kombinację gestów wskazywanych przez **I** i napis wpisany w **E**
* G - Przycisk kalibrujący kamerę na nowo
* H - Przycisk czyszczący zapisane szyfry
* I - Pole z obecnym szyfrem, reprezentowanym przez pierwsze litery gestów
* J - Pole informacyjne
* K - Przycisk zamykający okno

## Działanie programu
1. Po uruchomieniu, program automatycznie kalibruje kamerę po raz pierwszy (napis 'Kalibracja...' w polu **C**). Najlepiej aby tło było możliwie jednolite, dobrze oświetlone i koloru kontrastującego kolor skóry (szczególnie pole **B**).
2. Możemy zacząć używać programu. W polu **C** możemy zobaczyć aktualnie pokazywany gest. Używając pól obsługi (od **D** do **F**) możemy utworzyć szyfr, wpisać szyfrowaną wiadomość oraz zapisać je do bazy danych. Gdy podany szyfr jest już w bazie, to odczytamy jego zawartość.
3. W przypadku, gdy gesty nie są odczytywane prawidłowo lub chcemy zmienić pozycję, można użyć przycisku **G** do powtórnej kalibracji kamery.
4. Używając przycisku **H** możemy całkowicie wyczyścić bazę szyfrów.
5. Po zakończeniu pracy z programem możemy wyjść używając **K**. Uwaga: Baza danych nie jest zachowywana po wyjściu z programu.

---

# User Guide (English)

A hand gesture recognition application developed as a university team project, using OpenCV for webcam image processing and Tkinter for the desktop interface.

![Application interface](./ssapka.png)

* A - Camera view.
* B - The area where hand gestures are detected.
* C - Text describing the current gesture. Supported gestures: rock, paper, scissors, pointing, and waving.
* D - Button that saves the current gesture shown in **C**.
* E - Text field for entering a message to encode.
* F - Button that confirms the gesture sequence shown in **I** and the text entered in **E**.
* G - Button that recalibrates the camera.
* H - Button that clears the saved codes.
* I - The current code, represented by the first letters of the gestures.
* J - Information panel.
* K - Window close button.

## How the program works

1. On startup, the program automatically calibrates the camera (`Kalibracja...` in **C**). For best results, use a background that is as uniform as possible, well lit, and contrasting with your skin tone, especially in area **B**.
2. You can then start using the program. Field **C** shows the currently detected gesture. Use controls **D** through **F** to create a code, enter a message, and save them to the database. If the code already exists in the database, its associated message is displayed.
3. If gestures are not recognized correctly or you want to change position, use button **G** to recalibrate the camera.
4. Use button **H** to clear the entire code database.
5. When finished, close the program using **K**. Note: the database is not retained after the program closes.

The interface remains in Polish, so codes use the Polish gesture initials: **K** (rock / Kamień), **P** (paper / Papier), **N** (scissors / Nożyce), **W** (pointing / Wskazywanie), and **M** (waving / Machanie). Messages are stored in an in-memory dictionary indexed by gesture sequences; the program does not cryptographically encrypt them.

## Uruchamianie / Running

**Polski:** Program wymaga Pythona 3, Tkintera oraz podłączonej kamery internetowej. W folderze zawierającym `gesty.py` zainstaluj zależności i uruchom plik:

**English:** The program requires Python 3, Tkinter, and a connected webcam. From the folder containing `gesty.py`, install the dependencies and run the file:

```bash
python -m pip install numpy opencv-python Pillow
python gesty.py
```

**Polski:** Tkinter musi być dostępny w instalacji Pythona; nie jest instalowany powyższym poleceniem `pip`. Program otwiera lokalne okno aplikacji i korzysta z domyślnej kamery (`0`). Podczas kalibracji trzymaj dłoń poza zaznaczonym obszarem, a następnie umieść ją w tym obszarze, aby pokazać gest.

**English:** Tkinter must be available in your Python installation; it is not installed by the `pip` command above. The program opens a local desktop window and uses the default camera (`0`). Keep your hand outside the marked area during calibration, then place it inside the area to show a gesture.
