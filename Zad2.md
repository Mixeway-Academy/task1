# Podatności XSS

Formularz akceptuje nieprzefiltrowane dane i renderuje je jako HTML. Przykładowy payload, który demonstruje problem:

```html
<script>alert('Customer Name hacked')</script>
```
### Reprodukcja:
1. Należy otworzyć jakikolwiek formularz z dostępnych (w tym przypadku Customer)
2. Wypisać dane:
![XSS1](https://raw.githubusercontent.com/Yibux/task1/refs/heads/main/XSS1.png)
3. Wcisnąć przycisk `Add Customer`

### Skutki:
- Możliwość uruchomienia dowolnego kodu JS w kontekście użytkownika
![XSS2](https://raw.githubusercontent.com/Yibux/task1/refs/heads/main/XSS2.png)
![XSS3](https://raw.githubusercontent.com/Yibux/task1/refs/heads/main/XSS3.png)

### Proponowane poprawki
1. Sanityzacja danych wejściowych - użycie bleach do całkowitego usunięcia wszelkich tagów HTML i atrybutów
2. Walidacja po stronie serwera - użycie wzorców regex, limitów długości. W przypadku niespełnienia warunków wyskakuje błąd na stronie użytkownika
3. Usunięcie filtra `| safe` - przeglądarka zawsze traktuje dane z bazy jako zwykły tekst do wyświetlenia, a nie jako kod HTML do wykonania

## Wynik poprawek
### Books
![XSS_poprawa1](https://raw.githubusercontent.com/Yibux/task1/refs/heads/main/XSS_poprawa1.png)
![XSS_poprawa2](https://raw.githubusercontent.com/Yibux/task1/refs/heads/main/XSS_poprawa2.png)
![XSS_poprawa3_book_edit](https://raw.githubusercontent.com/Yibux/task1/refs/heads/main/XSS_poprawa3_book_edit.png)

### Books
![XSS_poprawa1_customer](https://raw.githubusercontent.com/Yibux/task1/refs/heads/main/XSS_poprawa1_customer.png)
![XSS_poprawa2_customer](https://raw.githubusercontent.com/Yibux/task1/refs/heads/main/XSS_poprawa2_customer.png)
