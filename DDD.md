Zadanie polegało na stworzeniu fragmentu modelu systemu bankowego zgodnie z zasadami
Domain Driven Design. Wyróżnione zostały trzy konteksty - Zarządzanie Kontem, Uwierzytelnianie
oraz Przelewy. Pierwszy z nich odpowiada za dane klienta oraz jego konta bankowe (saldo, operacje
na koncie). Uwierzytelnianie opisuje elementy potrzebne do zalogowania użytkownika w systemie.
Z kolei kontekst Przelewy odpowiada za zlecanie przelewów z konta klienta na wskazany rachunek.

![Model DDD](DDD.png)

+ Kontekst Zarządzanie Kontem

Agregaty: Klient, KontoBankowe

| Encja/Value Object | Atrybut         | Format danych                                                  |
|--------------------|-----------------|----------------------------------------------------------------|
| Klient             | imię            | string, 2-50 znaków, litery (także polskie), spacja, myślnik   |
| Klient             | nazwisko        | string, 2-50 znaków, litery, spacja, myślnik, apostrof         |
| Klient             | pesel           | string, 11 cyfr, poprawna suma kontrolna                       |
| Klient             | email           | string, do 254 znaków, format lokalna@domena                   |
| Adres              | ulica           | string, 2-80 znaków, litery, cyfry, spacja, kropka i myślnik   |
| Adres              | nrDomu          | string, 1-4 cyfry i opcjonalnie litera (np. 12A)               |
| Adres              | kodPocztowy     | string, 6 znaków, 2 cyfry połączone "-" z 3 cyframi            |
| Adres              | miasto          | string, 2-50 znaków, litery, spacja, myślnik                   |
| Adres              | kraj            | string, 2 wielkie litery (kod ISO, np. PL)                     |
| KontoBankowe       | numerRachunku   | VO NumerRachunku                                               |
| KontoBankowe       | idWłaściciela   | UUID istniejącego klienta                                      |
| KontoBankowe       | saldo           | Decimal, 2 cyfry po przecinku, nie może być mniejsze od 0      |
| KontoBankowe       | status          | AKTYWNE, ZABLOKOWANE lub ZAMKNIĘTE                             |
| Operacja           | typ             | OBCIĄŻENIE lub UZNANIE                                         |
| Operacja           | kwota           | Decimal, 2 cyfry po przecinku, większa od 0                    |

+ Kontekst Uwierzytelnianie

Agregat: Użytkownik

| Encja/Value Object | Atrybut           | Format danych                                                       |
|--------------------|-------------------|---------------------------------------------------------------------|
| Użytkownik         | login             | string, 6-32 znaki, małe litery, cyfry, kropka, myślnik             |
| Użytkownik         | idKlienta         | UUID istniejącego klienta                                           |
| Użytkownik         | nieudaneLogowania | int, po 5 nieudanych próbach status zmienia się na ZABLOKOWANY      |
| Użytkownik         | status            | AKTYWNY lub ZABLOKOWANY                                             |
| HashHasła          | algorytm          | string, Argon2id lub bcrypt                                         |
| HashHasła          | hash              | string, hasło nie jest zapisywane jawnie, przy ustawianiu 12-128 znaków |

+ Kontekst Przelewy

Agregat: Przelew

| Encja/Value Object | Atrybut         | Format danych                                                 |
|--------------------|-----------------|---------------------------------------------------------------|
| Przelew            | rachunekNadawcy | VO NumerRachunku, konto musi należeć do zlecającego           |
| Przelew            | dataZlecenia    | DateTime, ustawiana przez system                              |
| Przelew            | status          | ZLECONY, ZREALIZOWANY lub ODRZUCONY                           |
| TytułPrzelewu      | tekst           | string, 1-140 znaków, litery, cyfry, spacja oraz . , - / : ( ) |
| KwotaPrzelewu      | wartość         | Decimal, 2 cyfry po przecinku, od 0,01 do 100 000,00          |
| KwotaPrzelewu      | waluta          | PLN, EUR lub USD                                              |
| Odbiorca           | nazwa           | string, 2-70 znaków, litery, cyfry, spacja, kropka, myślnik   |
| Odbiorca           | numerRachunku   | VO NumerRachunku, inny niż rachunek nadawcy                   |
| NumerRachunku      | wartość         | string, "PL" i 26 cyfr (IBAN), poprawna suma kontrolna        |

Wszystkie identyfikatory (idKlienta, idKonta, idPrzelewu itd.) to UUID generowane przez system.
Konteksty odwołują się do siebie wyłącznie za pomocą identyfikatorów (linie kropkowane na diagramie).
Zlecenie przelewu powoduje obciążenie konta nadawcy - jeśli brakuje środków lub konto jest
zablokowane, przelew otrzymuje status ODRZUCONY. W żadnym polu tekstowym nie są dozwolone znaki
`<`, `>`, `"`, `` ` ``, `{`, `}`, ponieważ nie są potrzebne w żadnym z nich.
