# Zadanie 1 - model DDD i poprawka stored XSS

Autor: Mateusz Orzełowski

## Zadanie 1 - DDD

W pliku [DDD.md](https://github.com/morzelowski/task1/blob/main/DDD.md) opisałem fragment bankowości dotyczący przelewu krajowego. Diagram w `docs/ddd-model.svg` pokazuje trzy bounded contexts, pięć encji, granice agregatów, obiekty wartości i komunikację między kontekstami.

## Zadanie 2 - podatność

W aplikacji Python występował stored XSS. Dane przesłane w formularzach były zapisywane w bazie, a widoki list używały filtra Jinja `safe`, przez co przeglądarka interpretowała zapisany HTML i wykonywała kod z atrybutu `onerror`.

| Miejsce | Droga danych | Wynik przed poprawką |
| --- | --- | --- |
| Książki | `POST /books/create` lub `/books/<id>/edit` -> `Book.author` lub `Book.name` -> `/books/` | Kod wykonuje się przy każdym otwarciu listy książek. |
| Klienci | `POST /customers/create` lub `/customers/<id>/edit` -> `Customer.city` lub `Customer.name` -> `/customers/` | Kod wykonuje się przy każdym otwarciu listy klientów. |
| Wypożyczenia | `POST /loans/create` -> `Loan.customer_name` -> `/loans/` | Kod wykonuje się przy każdym otwarciu listy wypożyczeń. Do zapisu wystarcza dostępna książka. |

### Odtworzenie na wersji przed poprawką

Uruchomić aplikację z oryginalnego kodu poleceniami `docker build -t task1-python .` i `docker run -p 5000:5000 task1-python` w katalogu `Python/Flask_Book_Library`. Następnie wysłać przykładowe żądania:

```bash
curl -i -X POST http://localhost:5000/books/create \
  -H 'Content-Type: application/json' \
  -d '{"name":"PoC książka","author":"<img src=x onerror=alert(1)>","year_published":2024,"book_type":"2days"}'

curl -i -X POST http://localhost:5000/customers/create \
  --data-urlencode 'name=PoC klient' \
  --data-urlencode 'city=<img src=x onerror=alert(1)>' \
  --data-urlencode 'age=25'

curl -i -X POST http://localhost:5000/books/create \
  -H 'Content-Type: application/json' \
  -d '{"name":"PoC wypożyczenie","author":"Jan Kowalski","year_published":2024,"book_type":"2days"}'

curl -i -X POST http://localhost:5000/loans/create \
  --data-urlencode 'customer_name=<img src=x onerror=alert(1)>' \
  --data-urlencode 'book_name=PoC wypożyczenie' \
  --data-urlencode 'loan_date=2026-11-10' \
  --data-urlencode 'return_date=2026-11-15'
```

Po wejściu odpowiednio na `/books/`, `/customers/` i `/loans/` kod z `onerror` wykonuje się ponownie. W zrzutach użyłem wariantu, który zmienia nagłówek strony na czerwony komunikat. Dzięki temu wykonanie skryptu jest widoczne bez wysyłania danych poza lokalną aplikację.

**Książki - przed poprawką:**

![Wykonanie XSS na liście książek](https://raw.githubusercontent.com/morzelowski/task1/main/docs/evidence/xss-books-before.png)

**Klienci - przed poprawką:**

![Wykonanie XSS na liście klientów](https://raw.githubusercontent.com/morzelowski/task1/main/docs/evidence/xss-customers-before.png)

**Wypożyczenia - przed poprawką:**

![Wykonanie XSS na liście wypożyczeń](https://raw.githubusercontent.com/morzelowski/task1/main/docs/evidence/xss-loans-before.png)

## Poprawka

Walidacja w `project/input_validation.py` używa parsera `nh3.is_html()` do odrzucania znaczników HTML w polach, które trafiały do podatnych widoków. Jest wywoływana przez walidatory atrybutów modeli `Book`, `Customer` i `Loan` zarówno podczas tworzenia, jak i edycji obiektów. Zwykły tekst, w tym polskie znaki, apostrofy, `&` oraz porównania typu `A < B`, jest zachowywany bez zmiany. Próby zapisu HTML otrzymują 400, a transakcja jest wycofywana.

Usunąłem też filtr `safe` z sześciu komórek tabel. Chroni to widoki przed wykonaniem kodu z rekordów zapisanych przed poprawką. Jeśli stare wypożyczenie zawiera niebezpieczne dane książki, jego automatyczne zakończenie zwraca 409 i wymaga przeglądu danych, zamiast odtwarzać niebezpieczny rekord.

Te same rekordy ze zrzutów przed poprawką, otwarte w poprawionej aplikacji:

- [Książki po poprawce](https://raw.githubusercontent.com/morzelowski/task1/main/docs/evidence/xss-books-after.png)
- [Klienci po poprawce](https://raw.githubusercontent.com/morzelowski/task1/main/docs/evidence/xss-customers-after.png)
- [Wypożyczenia po poprawce](https://raw.githubusercontent.com/morzelowski/task1/main/docs/evidence/xss-loans-after.png)

## Testy

Testy jednostkowe w `tests/test_input_validation.py` obejmują poprawne wartości oraz niepoprawne warianty dla wszystkich trzech modeli, w tym tworzenie i edycję. Uruchomienie:

```bash
docker build -t task1-python .
docker run --rm task1-python python -m unittest discover -s tests -v
```

Wynik: 5 testów zakończonych powodzeniem. Dodatkowo sprawdziłem żądania HTTP: zapis trzech payloadów i niepoprawne edycje zwracają 400 bez częściowych zmian, a poprawne tworzenie, edycja, wypożyczenie i zwrot działają. Błędny JSON nadal zwraca 400, a niewłaściwy typ danych dla `/books/create` zwraca 415.
