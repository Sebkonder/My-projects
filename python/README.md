# Python Projects

A small collection of Python programs I wrote while learning the language. They
cover the fundamentals: object-oriented programming, custom data structures,
text processing and a simple web-scraping utility. Each folder is a
self-contained topic.

## Contents

### `oop` — Object-oriented programming
`classes.ipynb` demonstrates core OOP concepts:
- **`Osoba` (Person)** — validates a Polish *PESEL* national-ID number using its
  checksum and derives the birth date from it. Fields are guarded by properties
  with validation in the setters.
- **`Vector`** — a 3D vector built with operator overloading (`+`, `-`, scalar
  `*`, dot product, equality, indexing) plus length, cross product and the angle
  between two vectors.
- **`Fib`** — a Fibonacci iterator (`__iter__` / `__next__`).
- **`factorial`** — a function documented and tested with `doctest`.

### `data_structures`
`linked_list.ipynb` — from-scratch implementations of a singly **linked list**
(`append`, `pop`, `isEmpty`, string representation) and a simple directed
**graph** based on an adjacency set.

### `text_processing`
`file_spellcheck.ipynb` — a `Plik` ("File") class that reads a text file and
interactively corrects a common Polish spelling pattern (**uw → ów**), keeping a
list of exceptions.

### `web_scraping`
`ao3_status_checker.py` — a script using `requests` and `BeautifulSoup` that
fetches a web page, extracts a status field and appends it to a timestamped log,
flagging when the value changes.

### `Dynamical Systems`
Numerical exploration of how simple nonlinear maps transition from stable
equilibria, through period-doubling, into chaos. The work combines fixed-point
analysis, iteration, root-finding and bifurcation diagrams, applied to the
classic logistic map and a discrete host–parasitoid ecological model.

**Tools:** Python · NumPy · SciPy (`fsolve`) · Matplotlib

See [`dynamical_systems.ipynb`](dynamical_systems.ipynb) for the full notebook
with code and explanations.

## Tech
Python 3 · Jupyter Notebook · requests · BeautifulSoup4

## Running
The notebooks open directly in Jupyter or Google Colab. 

### For the scraper:

```bash
pip install requests beautifulsoup4
python web_scraping/ao3_status_checker.py
```

### For the dynamical system

```bash
pip install numpy scipy matplotlib
jupyter notebook dynamical_systems.ipynb
```
