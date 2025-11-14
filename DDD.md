## Opis zadania
Celem zadania jest zaprojektowanie fragmentu bezpiecznej aplikacji bankowej z wykorzystaniem zasad Domain Driven Design (DDD).
Skupiono się na kontekście Zarządzania Kontem i Przelewami.
Model został uproszczony do kilku kluczowych agregatów, encji i obiektów wartości, z naciskiem na czytelność oraz oddzielenie logiki domenowej od infrastruktury.

## Diagram modelu
![DDD_diagram](https://raw.githubusercontent.com/Yibux/task1/refs/heads/main/DDD_diagram.png)

## Bounded Context
1. Zarządzanie kontem
2. Przelewy bankowe

## Agregaty
### Konto bankowe
| Nazwa | Typ | Opis | Ograniczenia |
|-------|-----|------|--------------|
| id | String | Identyfikator konta bankowego | Unikalny, UUID |
| numerKonta | NumerKonta | Numer rachunku bankowego | Zgodnie z ograniczeniami encji NumerKonta |
| saldo | Saldo | Środki na koncie | Zgodnie z ograniczeniami obiektu wartości Saldo |
| status | Enum | Status konta (aktywny, zablokowany, zamknięty) | Tylko dozwolone wartości enum |
| wlasciciel | Klient | Właściciel konta | Zgodnie z ograniczeniami encji Klient |

### Przelew
| Nazwa | Typ | Opis | Ograniczenia |
|-------|-----|------|--------------|
| id | String | Identyfikator przelewu | Unikalny, UUID |
| data | DateTime | Data i godzina zlecenia przelewu | Nie może być w przyszłości |
| kontoDocelowe | KontoBankowe | Konto odbiorcy przelewu | Zgodnie z ograniczeniami agregatu KontoBankowe |
| kontoZrodlowe | KontoBankowe | Konto, z którego wykonany jest przelew | Zgodnie z ograniczeniami agregatu KontoBankowe |
| kwota | KwotaPrzelewu | Kwota do przelania | > 0, waluta zgodna z kontem źródłowym |
| status | Enum | Status przelewu (zlecony, zrealizowany, anulowany) | Tylko dozwolone wartości enum |
| tytul | String | Tytuł przelewu | Maks. 140 znaków |

Poprawny format IBAN: 2 litery, 2 cyfry kontrolne, 24 cyfry numeru konta
## Encje
### Klient
| Nazwa | Typ | Opis | Ograniczenia |
|-------|-----|------|--------------|
| id | String | Identyfikator klienta | Unikalny, UUID |
| adres | Adres | Adres klienta | Zgodnie z obiektem wartości Adres |
| imie | String | Imię klienta | Może składać się z liter oraz `-` - maks. 100 znaków |
| nazwisko | String | Nazwisko klienta | Może składać się z liter oraz `-` - maks. 100 znaków |
| email | String | Email klienta | Musi być poprawnym adresem e-mail, unikalny |
| telefon | String | Numer telefonu klienta | Format międzynarodowy, np. +48XXXXXXXXX |
 
## Obiekty Wartości
### Adres
| Nazwa | Typ | Opis | Ograniczenia |
|-------|-----|------|--------------|
| ulica       | String | Ulica i numer budynku | Maks. 100 znaków, znaki alfanumeryczne i `-` |
| miasto | String | Miasto | Maks. 50 znaków, litery i `-` |
| kodPocztowy | String | Kod pocztowy | Format `XX-XXX` |
| kraj | String | Kraj | Maks. 50 znaków, litery |

### KwotaPrzelewu
| Nazwa | Typ | Opis | Ograniczenia |
|-------|-----|------|--------------|
| wartosc | Decimal | Kwota pieniężna przelewu | > 0.00 |
| waluta | Enum | Waluta przelewu np. (PLN, EUR, USD) | Musi być zgodna z kontem źródłowym, wartościami enum |

### Saldo
| Nazwa | Typ | Opis | Ograniczenia |
|-------|-----|------|--------------|
| wartosc | Decimal | Kwota pieniężna salda | >= 0.00 |
| waluta | Enum | Waluta salda konta bakowego np. (PLN, EUR, USD) | Zgodna z wartościami enum |