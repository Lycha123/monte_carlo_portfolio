Actuarial Portfolio Simulator

Krótki skrypt w Pythonie służący do symulacji wartości portfela inwestycyjnego przy użyciu metody Monte Carlo 
(opartej na historycznych zwrotach i macierzy kowariancji). Narzędzie pobiera dane z Yahoo Finance, przeprowadza tysiące symulacji przyszłych notowań i oblicza kluczowe metryki ryzyka.

Kluczowe funkcje
* **Automatyczne pobieranie danych:** Wykorzystuje `yfinance` do ściągania historycznych cen akcji.
* **Symulacja Monte Carlo:** Generuje tysiące możliwych ścieżek cenowych dla portfela (domyślnie 10 000 symulacji na 252 dni robocze).
* **Zaawansowane metryki ryzyka:** Oblicza Oczekiwany zwrot, Value at Risk (VaR), Conditional Value at Risk (CVaR) oraz średni Maximum Drawdown (MDD).
* **Wizualizacja:** Automatycznie generuje wykresy przedstawiające wybrane ścieżki cenowe oraz rozkład (histogram) końcowej wartości portfela po symulowanym okresie.

Wymagania i instalacja

Aby uruchomić projekt, upewnij się, że masz zainstalowanego Pythona w wersji 3.7+ oraz niezbędne biblioteki. 
