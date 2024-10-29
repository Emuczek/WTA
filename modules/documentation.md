# Problem Przydziału Celów do Broni (WTA)

Problem Przydziału Celów do Broni (ang. Weapon Target Assignment, WTA) to klasyczny problem optymalizacyjny w badaniach operacyjnych i planowaniu wojskowym. Polega on na przydzieleniu zestawu broni do zestawu celów w sposób, który maksymalizuje ogólne oczekiwane obrażenia lub minimalizuje ogólny koszt, z uwzględnieniem różnych ograniczeń.

## Opis Problemu

Wyobraź sobie scenariusz, w którym masz zestaw broni (np. pociski, samoloty) i zestaw celów (np. instalacje wroga, pojazdy). Każda broń ma pewne prawdopodobieństwo zniszczenia każdego celu (prawdopodobieństwo to może zależeć od takich czynników, jak typ broni, podatność celu na zniszczenie i odległość między nimi). Celem jest znalezienie optymalnego przydziału broni do celów, który zapewni najlepszy ogólny wynik.

## Funkcja Celu

Funkcja celu w problemie WTA zazwyczaj reprezentuje ogólną skuteczność przydziału. Istnieją dwa powszechne podejścia:

* **Maksymalizacja oczekiwanych obrażeń:** Celem jest zadanie wrogowi jak największych obrażeń. Funkcja celu byłaby sumą oczekiwanych obrażeń zadanych każdemu celowi, biorąc pod uwagę prawdopodobieństwo zniszczenia dla każdej pary broń-cel.

* **Minimalizacja kosztów/zużycia zasobów:** Celem jest osiągnięcie pożądanego poziomu obrażeń przy jednoczesnym wykorzystaniu jak najmniejszej ilości zasobów. Funkcja celu może być sumą kosztów użycia każdej broni lub kombinacją kosztu i obrażeń.

## Ograniczenia

W problemie WTA można nałożyć kilka ograniczeń, w tym:

* **Przydział jeden do jednego (lub wiele do jednego, jeśli broń może atakować wiele celów):** Każda broń może zostać przydzielona do co najwyżej jednego celu (w podstawowym sformułowaniu) lub ograniczonej liczby celów (w bardziej złożonych scenariuszach). Analogicznie, czasami nakłada się ograniczenia na to, ile broni może atakować jeden cel.
* **Ograniczone zasoby:** Może istnieć ograniczona liczba każdego rodzaju dostępnej broni.
* **Priorytety celów:** Niektóre cele mogą być ważniejsze niż inne, a przydział powinien priorytetyzować niszczenie celów o wysokiej wartości.
* **Okna czasowe ataku:** Mogą istnieć określone okna czasowe, w których cel może zostać zaatakowany.
* **Ograniczenia dotyczące tras/ścieżek ataku:** W bardziej realistycznych scenariuszach można uwzględnić ograniczenia związane z trajektoriami broni lub dostępnością tras ataku.

## Sformułowanie Matematyczne (Przykłąd - Maksymalizacja Oczekiwanych Obrażeń)

Niech:

* `n` będzie liczbą broni.
* `m` będzie liczbą celów.
* `p_ij` będzie prawdopodobieństwem, że broń `i` zniszczy cel `j`.
* `v_j` będzie wartością celu `j` (reprezentującą jego ważność).
* `x_ij` będzie binarną zmienną decyzyjną: `x_ij = 1`, jeśli broń `i` jest przypisana do celu `j`, a `x_ij = 0` w przeciwnym razie.


**Funkcja Celu (Maksymalizacja):**

Maksymalizuj  ∑_(i=1)^n ∑_(j=1)^m  p_ij * v_j * x_ij

**Ograniczenia:**

* **Każda broń przypisana do co najwyżej jednego celu:**

∑_(j=1)^m x_ij <= 1, dla wszystkich i = 1, ..., n

* **Zmienne decyzyjne są binarne:**

x_ij ∈ {0, 1}, dla wszystkich i = 1, ..., n i j = 1, ..., m

Inne ograniczenia, takie jak ograniczone zasoby lub priorytety celów, można dodać w razie potrzeby.


## Metody Rozwiązywania

Do rozwiązania problemu WTA można wykorzystać różne techniki optymalizacyjne, w tym:

* **Programowanie całkowitoliczbowe:** Powyższe sformułowanie matematyczne można rozwiązać bezpośrednio za pomocą solverów programowania całkowitoliczbowego.
* **Algorytmy przepływu w sieci:** Problem można modelować jako problem przepływu w sieci i rozwiązać za pomocą wyspecjalizowanych algorytmów.
* **Algorytmy heurystyczne i metaheurystyczne:** W przypadku większych lub bardziej złożonych instancji, algorytmy heurystyczne, takie jak algorytmy genetyczne, symulowane wyżarzanie lub przeszukiwanie tabu, mogą być użyte do znalezienia dobrych rozwiązań w efektywny sposób.

## Zastosowania

Problem WTA ma zastosowania w różnych dziedzinach, w tym:

* **Planowanie i operacje wojskowe:** Przypisywanie broni do celów w scenariuszach bojowych.
* **Obrona przeciwrakietowa:** Przechwytywanie nadlatujących pocisków.
* **Alokacja zasobów:** Przypisywanie zasobów do zadań w ogólnych problemach optymalizacyjnych.
