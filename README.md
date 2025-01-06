# Symulacja modelu Drudego

Projekt symuluje ruch elektronów w nieskończonym metalu pod wpływem pola elektrycznego, zgodnie z założeniami modelu Drudego.

## Funkcjonalność

* **Dynamiczna symulacja**: wizualizacja trajektorii ruchu elektronów w czasie rzeczywistym pod wpływem różnych warunków fizycznych.
* **Konfigurowalne parametry**: inteaktywne suwaki umożliwiają precyzyjną regulację wartości natężenia pola elektrycznego i czasu relaksacji.
* **Kompleksowe grafy**: generowane są wykresy, ilustrujące średnie zmiany pozycji w wymiarach x i y chmury elektronów w czasie.
* **Argumenty wiersza poleceń**: łatwe dostosowywanie ilości elektronów przez argumenty wiersza poleceń.

## Wymagania

### Wersja Pythona
Python 3.x

### Zależności

* `vpython`
* Biblioteki standardowe: `math`, `argparse`, `threading`

### Instalacja

Aby zainstalować wymagane pakiety należy skorzystać z komendy:

`pip install -r requirements.txt`

## Instrukcja użycia

### Uruchamianie symulacji

Uruchom program za pomocą komendy:

`python drude_model_sim.py`

### Argumenty wiersza poleceń

* `--num-electrons`: Definiuje liczbę elektronów w oknie symulacji (wartość domyślna: 30)

Przykład zastosowania:

`python drude_model_sim.py --num-electrons 50`

### Interaktywna kontrola
Za pomocą suwaków można dostosować wartości:
* **Natężenia pola elektrycznego** \[ $\frac{V}{m}$ \]
* **Czasu relaksacji** \[ $s$ \], czyli średniego czasu między zderzeniami

Parametry mogą być dostosowywane w dowolnym momencie czasu wykonywania programu.

Zmiany tych wartości są dynamicznie odwzorowywane w wartości prędkości dryfu, liczonej według wzoru:

$v_d = \frac{\tau q E}{m} $, gdzie
* $\tau$ - czas relaksacji
* $q$ - ładunek elektronu
* $E$ - wartość natężenia pola elektrycznego
* $m$ - masa elektronu

## Kontrola Symulacji
Aby zakończyć symulację w sposób kontrolowany, wprowadź `q` w terminalu. Następnie można w przeglądarce zamknąć okno localhost, gdzie hostowana jest symulacja.

## Wyniki
Program umożliwia badanie reakcji elektronów na łączony wpływ pola elektrycznego i procesów zderzania elektronów z jonami sieci krystalicznej. Aby umożliwić głębszą analizę, wyświetlane są również wykresy średnich pozycji w czasie. Aktualizacje dotyczące parametrów symulacji i ustawień są wyświetlane w czasie rzeczywistym.

## Wykorzystanie generatywnej sztucznej inteligencji
W trakcie tworzenia projektu wykorzystany był model językowy *gpt-4o* w celu:
* poprawienia czytelności kodu: zostały dodane komentarze oraz zmienione nazwy zmiennych na bardziej czytelne;
* 