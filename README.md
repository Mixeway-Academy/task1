# Security By Design - Zadanie 1

## Wymagania
1. Zainstalowana komenda `git` na stacji roboczej
2. Zainstalowany `docker` na stacji roboczej
3. Bezpośredni dostęp do internetu (nie przez proxy)

## Przygotowanie
1. **Założenie konta na GitHub** (jeśli jeszcze nie jesteś zarejestrowany)  
   Aby wykonać ćwiczenie, konieczne jest posiadanie zarejestrowanego użytkownika na portalu github.com.

2. **Wykonanie "fork'a" projektu**  
   Wykonaj "fork'a" projektu [https://github.com/Mixeway-Academy/task1](https://github.com/Mixeway-Academy/task1) - w wyniku tej operacji, w twojej przestrzeni na GitHubie powstanie kopia repozytorium.  
   Zadanie zakłada wykonanie listy operacji na kodzie źródłowym, ale aby nie wprowadzać zmian w przestrzeni, z której korzystają inni użytkownicy, wygodnie jest wykonać kopię w swojej przestrzeni. Więcej informacji znajdziesz [tutaj](https://docs.github.com/en/get-started/quickstart/fork-a-repo).  
   ![img.png](.github/img.png)

3. **Pobranie kopi projektu na swoją stację roboczą**  
   Aby pobrać 'sforkowany' projekt na swoją stację roboczą, wykonaj poniższą komendę:

```shell
git clone https://github.com/{username}/task1

#gdzie {username} to nazwa użytkownika. Wchodząc w swoją kopie repozytoroium przez przeglądarkę można też skorzystać z adresu URL.
```


## Zadanie 1 - Domain Driven Design
**Cel:** Celem zadania jest zamodelowanie bezpiecznej aplikacji bankowej (fragmentu) wykorzystując zasady Domain Driven Design.

**UWAGA:** zadanie nie ma na celu stworzenia kompletnego modelu dla bankowości, a jedynie usystematyzowanie wiedzy o Domain Driven Design. Skup się na wybranym elemencie, maksymalnie 5-6 encjach i wybranym fragmencie.

### Instrukcja:
1. **Definiowanie Bounded Context:**  
   Zidentyfikuj i zdefiniuj konteksty w obrębie systemu bankowego (np. Zarządzanie Kontem, Przelewy, Uwierzytelnienie).

2. **Modelowanie Agregatów, Encji i Obiektów Wartości:**  
   Zdefiniuj agregaty, takie jak KontoBankowe i Przelew.  
   Zdefiniuj encje i obiekty wartości, takie jak Klient, Adres, KwotaPrzelewu, itp.

3. **Zdefiniowanie przyjętych założeń:**  
   Określ, jakie atrybuty mają encje i obiekty wartości oraz jakie formaty danych są akceptowane.

4. **Przygotowanie wyników:**  
   Wyniki powinny być zaprezentowane w formie pliku w formacie Markdown (.md). Stwórz w repozytorium (swojej kopii) plik `DDD.md` a następnie umieść w nim:
    - krótki (3-4 zdania) opis zadania,
    - obrazek przedstawiający model (może być przygotowany w Paintcie, Draw.io czy innym narzędziu),
    - tabelkę lub listę przedstawiającą i opisującą przyjęte założenia (ograniczenia dotyczące tego, jak mają wyglądać konkretne encje i ewentualnie opisującą możliwe operacje w integracji pomiędzy obiektami/kontekstami).

Aby umieścić plik w repozytorium:

```shell
cd {ścieżka do lokalnej kopi swojego repozutorium}
git add DDD.md
git commit -m "dodanie zadania 1"
git push origin main
```

## Zadanie 2 - Weryfikacja danych wejściowych do aplikacji
Zadanie polega na uruchomieniu wybranej aplikacji (python lub java), następnie zidentyfikowaniu miejsca, w którym może występować podatność typu Cross Site Scripting - persistent (XSS), a następnie zaproponowaniu poprawki, która usunie podatność.

### Instrukcja

1. **Uruchomienie wybranej aplikacji**  
   Zadanie można zrealizować w jednym z dwóch wybranych wariantów: Java lub Python. Obydwa warianty zostały zawarte w katalogach:

```shell
Java/
Python/
```

W repozytorium z zadaniem, pierwszym krokiem, który należy wykonać, jest wybór technologii. O ile wybór nie ma znaczenia przy zadaniu związanym z wyszukiwaniem podatności, o tyle zadanie polegające na zaproponowaniu poprawki wymagać będzie niewielkiej wiedzy dotyczącej programowania w wybranej technologii.

Aby uruchomić aplikację JAVA, należy wykonać operacje:

```shell
cd Java/spring-thymeleaf-crud-example
docker build -t task1-java .
docker run -p 8080:8080 task1-java
```
W wyniku tych operacji na stacji roboczej zostanie uruchomiony kontener dockerowy z aplikacją JAVA, wyeksponowany na porcie 8080. Przez przeglądarkę aplikacja będzie dostępna pod adresem http://localhost:8080.

Aby uruchomić aplikację Python, należy wykonać operacje:

```shell
cd Python/Flask_Book_Library
docker build -t task1-python .
docker run -p 5000:5000 task1-python
```
W wyniku tych operacji na stacji roboczej zostanie uruchomiony kontener dockerowy z aplikacją Python (Flask), wyeksponowany na porcie 5000. Przez przeglądarkę aplikacja będzie dostępna pod adresem http://localhost:5000.


2. **Znalezienie podatności `XSS`**

   Aplikacja Java to aplikacja pozwalająca na rejestrowanie studentów przez GUI.

   Aplikacja Python to aplikacja, która implementuje wybrane możliwości biblioteki - istnieje możliwość dodawania książek itp.

   W tej części zadania należy zweryfikować aplikacje (przeklikać ją) a następnie spróbować w wybranych formularzach wstrzyknąć kod JavaScript (XSS). W przypadku zaobserwowania poprawnego wykonania kodu, należy udokumentować wystąpienie podatności.

3. **Zaproponowanie poprawy**

   Jak tylko zidentyfikowane zostanie miejsce, w którym istnieje podatność typu XSS, konieczne jest zaproponowanie sposobu jej usunięcia. Otwórz kod źródłowy (via IDE albo web IDE na GitHub) a następnie zidentyfikuj miejsce, które odpowiada za reprezentację obiektu, w ramach którego znaleziono błąd bezpieczeństwa. Zaproponuj założenia dotyczące weryfikacji danych wejściowych, a następnie zaimplementuj weryfikację.

   **Uwaga - weryfikacja ma być zrealizowana na poziomie tworzenia obiektu w backendzie, a nie na poziomie wyświetlania go.**
Przesłanie wyników

4. **Przesłanie wyników**

   Wynikiem ćwiczenia ma być przygotowany Pull Request z zaimplementowaną poprawką. Informacje jak przygotować Pull Request znajdują się tutaj.

   Co musi zawierać Pull Request:

   W opisie musi znaleźć się informacja o znalezionej podatności - co to za podatność, gdzie została znaleziona, sposób jej odtworzenia oraz screen udowadniający jej wystąpienie.
Commit (zmianę w kodzie), która zawiera wprowadzoną zmianę.
Oceniany będzie przygotowany Pull Request.

   Aby podesłać zadanie do oceny, konieczne jest nadanie uprawnienia do repozytorium użytkownikowi o nazwie siewer - instrukcja jak nadać dostęp do repozytorium znajduje się tutaj.

   Punktowane będzie wykonanie zadania tylko dla 1 aplikacji - wykonanie zadania zarówno dla aplikacji Java i Python nie będzie dodatkowo punktowane. Możliwe jest jednak uzyskanie dodatkowego punktu (ponad 5) w przypadku zaimplementowania mechanizmu testowania danych wejściowych w scenariuszu weryfikacji poprawnego i niepoprawnego wariantu.

## Punktowanie (ćwiczenie oceniane w skali 0-5 pkt):
* 1 punkt za zadanie Domain Driven Design (weryfikacja pliku DDD.md)
* 1 punkt za udokumentowanie wystąpienia podatności XSS
* 2 punkty za implementację poprawki
* 1 punkt za poprawnie stworzony Pull Request
* 1 BONUSowy punkt za zaimplementowany test jednostkowy weryfikujący walidator



## Credits
* Java application - [GitHub Repo](https://github.com/pedrohenriquelacombe/spring-thymeleaf-crud-example)
* Python application - [GitHub Repo](https://github.com/MohammadSatel/Flask_Book_Library)
