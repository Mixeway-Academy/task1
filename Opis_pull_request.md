# Podatności w aplikacji
Jako przykładowy exploit posłużył mi następujący kod
```
<script>alert('Atak')</script>
```
Skutkiem jego działania powinno być wyświetlenie komunikatu `Atak`
## Książki
W aplikacji zostały znalezione następujące podatności:
Podczas dodawania książki jako jej nazwę oraz autora można dodać skrypt, który zostanie zapisany do bazy.
![AddBokk](https://github.com/KarolZebala/tbo-task1-kz/blob/main/AddBook.png?raw=true)
Skrypt wykona się podczas wyświetlania listy
![ReeadBooks](https://github.com/KarolZebala/tbo-task1-kz/blob/main/ReadBook.png?raw=true)
Podatność ta występuję w sposób analogiczny podczas edycji książki
## Klienci
Analogiczna podatność występuje podczas dodawania klientów
![AddCustomer](https://github.com/KarolZebala/tbo-task1-kz/blob/main/AddCustomer.png?raw=true)
Skrypt wykona się podczas wyświetlania listy
![ReadCustomer](https://github.com/KarolZebala/tbo-task1-kz/blob/main/ReadCustomer.png?raw=true)
Podatność ta występuję w sposób analogiczny podczas edycji klienta

## Wypożyczenia
Kolejna podatność występuję przy tworzeniu wypożyczenia przy wyborze książki lub autora, których nazwa jest zainfekowana.
Ewentualnie można w konsoli zmienić kod HTML i dodać opcje w której value będzie zawierało exploita.
![AddLoan](https://github.com/KarolZebala/tbo-task1-kz/blob/main/AddLoan.png?raw=true)
Ponownie skrypt zostanie wykonany przy wejściu na listę 
![ReadLoan](https://github.com/KarolZebala/tbo-task1-kz/blob/main/ReadLoan.png?raw=true)

# Rozwiązania podatności
W ramach poprawki dodałem:
- Ograniczenie liczby znaków w request modelach, aby odpowiadały ograniczeniom w bazie
- Listę dozwolonych znaków dla odpowiednich pól
- Dodatkowo skorzystałem z biblioteki `bleach`, która odpowiada za sanityzacje danych wejściowych
- w plikach html była użyta opcja `safe` która powodowała brak escapowania html przez django. Opcja ta została usunięta

# Testy jednostkowe
Został napisany jeden przykładowy test dla nazwy książki, sprawdza on tylko czy nazwa książki zawiera dopuszczalne znaki.
