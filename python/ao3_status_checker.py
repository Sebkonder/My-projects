"""
Prosty checker statusu strony.

Pobiera stronę, wyciąga z niej wskazane pole (domyślnie znacznik
<dd class="status">) i dopisuje wartość wraz ze znacznikiem czasu do
pliku logu, oznaczając moment, w którym wartość się zmieniła.

Przykład użycia na dole pliku sprawdza status pracy na Archive of Our Own.
Wymaga: requests, beautifulsoup4
"""
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def open_site(url: str) -> requests.Response:
    """Pobiera stronę pod podanym adresem URL."""
    return requests.get(url)


def beautify(response: requests.Response, tag: str = "dd", class_: str = "status") -> str:
    """Wyciąga tekst pierwszego elementu pasującego do tagu i klasy CSS."""
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find_all(tag, class_=class_)[0].string


def file_manager(wpis: str = "", file: str = "Test") -> None:
    """Dopisuje wpis ze znacznikiem czasu, oznaczając zmianę wartości."""
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file + ".txt", "a+") as f:
        f.seek(0)
        lines = f.readlines()
        try:
            zmiana = lines[-1].split()[2] != wpis
        except IndexError:
            zmiana = False
        suffix = " <-- New Wpis" if zmiana else ""
        f.write(f"{date_now}\t\t{wpis}{suffix}\n")


if __name__ == "__main__":
    url = "https://archiveofourown.org/works/27548665/chapters/114242317"
    status = beautify(open_site(url))
    file_manager(status)
    print("Zapisano status:", status)
