# Zadanie 1 – Domain Driven Design

## Opis zadania

Celem zadania jest zamodelowanie fragmentu bezpiecznej aplikacji bankowej z wykorzystaniem zasad Domain Driven Design. Model obejmuje trzy konteksty ograniczone (Bounded Context): **Uwierzytelnienie**, **Zarządzanie Kontem** oraz **Przelewy**. W każdym kontekście wyodrębniono agregaty (Użytkownik, Klient, KontoBankowe, Przelew) oraz obiekty wartości (np. Adres, Kwota, NumerRachunku), które pilnują poprawności danych już w momencie ich tworzenia. Konteksty komunikują się ze sobą wyłącznie przez identyfikatory i zdarzenia, dzięki czemu np. dane uwierzytelniające nigdy nie trafiają do modułu przelewów.

## Model

![Model DDD](model.png)

**Legenda:** żółte – agregaty (Aggregate Root, encje z tożsamością), zielone – obiekty wartości (bez tożsamości, niemodyfikowalne), linia przerywana – relacja po identyfikatorze, numerowane strzałki – integracja między kontekstami.

## Bounded Contexts

| Kontekst | Odpowiedzialność | Agregaty |
|---|---|---|
| Uwierzytelnienie | Logowanie, weryfikacja hasła, blokowanie konta po nieudanych próbach | Użytkownik |
| Zarządzanie Kontem | Dane klienta, otwieranie/blokowanie rachunków, księgowanie salda | Klient, KontoBankowe |
| Przelewy | Zlecanie i realizacja przelewów, walidacja danych przelewu | Przelew |

## Encje i agregaty – atrybuty i założenia

### Użytkownik (agregat, kontekst: Uwierzytelnienie)

| Atrybut | Typ | Założenia |
|---|---|---|
| idUżytkownika | UUID | Generowany przez system, niezmienny |
| login | Login | Unikalny w systemie |
| hasłoHash | HashHasła | Hasło nigdy nie jest przechowywane jawnie |
| idKlienta | UUID | Referencja do Klienta (tylko identyfikator) |
| liczbaNieudanychPrób | int | 0–3 |
| zablokowany | bool | `true` po 3 nieudanych próbach logowania |

### Klient (agregat, kontekst: Zarządzanie Kontem)

| Atrybut | Typ | Założenia |
|---|---|---|
| idKlienta | UUID | Generowany przez system, niezmienny |
| imię | string | 2–50 znaków, tylko litery (w tym polskie), `-` i spacja |
| nazwisko | string | 2–50 znaków, j.w. |
| pesel | PESEL | Unikalny, poprawna suma kontrolna |
| adres | Adres | Obiekt wartości – zmiana adresu = podmiana całego obiektu |
| dataUtworzenia | Date | Nie może być z przyszłości |

### KontoBankowe (agregat, kontekst: Zarządzanie Kontem)

| Atrybut | Typ | Założenia |
|---|---|---|
| numer | NumerRachunku | Identyfikator konta, unikalny |
| idKlienta | UUID | Właściciel; jeden klient może mieć wiele kont (1:N) |
| saldo | Kwota | Nie może spaść poniżej 0 (brak debetu) |
| status | StatusKonta | `AKTYWNE`, `ZABLOKOWANE`, `ZAMKNIĘTE` |
| limitDzienny | Kwota | Domyślnie 10 000 PLN, > 0 |
| dataOtwarcia | Date | Ustawiana przy otwarciu, niezmienna |

### Przelew (agregat, kontekst: Przelewy)

| Atrybut | Typ | Założenia |
|---|---|---|
| idPrzelewu | UUID | Generowany przez system |
| rachunekNadawcy | NumerRachunku | Musi należeć do zalogowanego klienta |
| rachunekOdbiorcy | NumerRachunku | Musi być różny od rachunku nadawcy |
| kwota | KwotaPrzelewu | Patrz obiekt wartości |
| tytuł | TytułPrzelewu | Patrz obiekt wartości |
| status | StatusPrzelewu | Zmiany tylko w dozwolonej kolejności |
| dataZlecenia | DateTime | Ustawiana przez system (UTC) |

## Obiekty wartości – formaty danych

| Obiekt wartości | Format / ograniczenia | Przykład |
|---|---|---|
| Login | 5–30 znaków, `[a-zA-Z0-9._]` | `jan.kowalski` |
| HashHasła | Hash bcrypt/argon2; hasło źródłowe min. 12 znaków, w tym wielka litera, cyfra i znak specjalny | `$argon2id$...` |
| PESEL | Dokładnie 11 cyfr + poprawna cyfra kontrolna | `44051401458` |
| Adres | ulica 1–100 zn., nrDomu 1–10 zn., kodPocztowy `NN-NNN`, miasto 2–50 zn., kraj kod ISO 3166 (2 litery) | `Długa 5, 00-001 Warszawa, PL` |
| Kwota | decimal, 2 miejsca po przecinku, waluta ISO 4217 (`PLN`, `EUR`) | `1250.00 PLN` |
| NumerRachunku | IBAN: `PL` + 26 cyfr, poprawna suma kontrolna | `PL61109010140000071219812874` |
| KwotaPrzelewu | > 0,00 i ≤ 100 000,00; 2 miejsca po przecinku; waluta `PLN` lub `EUR` | `200.00 PLN` |
| TytułPrzelewu | 1–140 znaków, bez znaków sterujących i HTML (`<`, `>`) | `Czynsz listopad` |
| StatusPrzelewu | `UTWORZONY` → `ZATWIERDZONY` → `ZREALIZOWANY` lub `ODRZUCONY` | `ZATWIERDZONY` |

Wszystkie obiekty wartości są **niemodyfikowalne** i walidowane w konstruktorze – nie da się utworzyć obiektu z niepoprawnymi danymi.

## Operacje i integracja między kontekstami

| Nr | Skąd → Dokąd | Operacja | Opis |
|---|---|---|---|
| 1 | Uwierzytelnienie → Zarządzanie Kontem | `ZalogowanoUżytkownika(idKlienta)` | Przekazywany jest tylko identyfikator klienta – bez loginu i hasła |
| 2 | Uwierzytelnienie → Przelewy | Weryfikacja tokenu sesji | Przelew można zlecić tylko z ważną sesją (token wygasa po 15 min bezczynności) |
| 3 | Przelewy → Zarządzanie Kontem | `ObciążKonto(nadawca, kwota)`, `UznajKonto(odbiorca, kwota)` | Konto sprawdza status `AKTYWNE`, saldo i limit dzienny |
| 4 | Zarządzanie Kontem → Przelewy | Zdarzenie `ŚrodkiZaksięgowane` lub `BrakŚrodków` | Przelew zmienia status na `ZREALIZOWANY` albo `ODRZUCONY` |

### Przykładowy przebieg przelewu

1. Klient loguje się (Uwierzytelnienie) – otrzymuje token sesji.
2. Klient tworzy `Przelew` – status `UTWORZONY`; obiekty wartości walidują kwotę, IBAN i tytuł.
3. Klient zatwierdza przelew – status `ZATWIERDZONY`.
4. Kontekst Przelewy wysyła polecenie obciążenia do kontekstu Zarządzanie Kontem.
5. `KontoBankowe` sprawdza reguły (saldo ≥ kwota, limit dzienny, konto aktywne) i publikuje zdarzenie.
6. Przelew otrzymuje status `ZREALIZOWANY` lub `ODRZUCONY`.

## Reguły biznesowe (niezmienniki agregatów)

- Saldo konta nigdy nie może być ujemne.
- Z zablokowanego lub zamkniętego konta nie można wykonać przelewu.
- Suma przelewów z jednego konta w ciągu dnia nie może przekroczyć `limitDzienny`.
- Zrealizowanego lub odrzuconego przelewu nie można już zmienić.
- Użytkownik jest blokowany po 3 nieudanych próbach logowania.
- Agregaty odwołują się do siebie tylko przez identyfikatory, a nie przez bezpośrednie referencje do obiektów.
