
# Modelowanie Bezpiecznej Aplikacji Bankowej z Zasadami Domain Driven Design

## Opis Zadania
Celem tego zadania jest zamodelowanie wybranego fragmentu aplikacji bankowej zgodnie z zasadami Domain Driven Design (DDD). Skupiamy się na zarządzaniu kontem bankowym, realizacji przelewów, powiadomieniach oraz autoryzacji. Model obejmuje wybrane encje, agregaty oraz obiekty wartości, a także określa ich atrybuty i przyjęte założenia.

## Bounded Contexts
1. **Zarządzanie Kontem**:
   - Tworzenie i zarządzanie kontami bankowymi.
   - Obsługa klientów i ich danych osobowych.
2. **Przelewy**:
   - Realizacja przelewów między kontami.
   - Walidacja kwot i odbiorców.
3. **Powiadomienia**:
   - Obsługa powiadomień dla klientów za pomocą SMS, e-mail oraz aplikacji mobilnej.
   - Zarządzanie preferencjami powiadomień.
4. **Autoryzacja**:
   - Przechowywanie historii logowań klientów.
   - Śledzenie operacji związanych z kontami bankowymi.

## Model Agregatów i Encji
### Agregat: KontoBankowe
- **Encje**:
  - `KontoBankowe`
    - `numerKonta` (String, unikalny identyfikator konta w formacie IBAN)
    - `saldo` (Decimal, aktualne saldo konta)
    - `wlasciciel` (Referencja do encji Klient)
  - `Klient`
    - `id` (UUID, unikalny identyfikator klienta)
    - `imie` (Obiekt wartości: Imie)
    - `nazwisko` (Obiekt wartości: Nazwisko)
    - `adres` (Obiekt wartości: Adres)
- **Obiekty wartości**:
  - `Adres`
    - `ulica` (String)
    - `miasto` (String)
    - `kodPocztowy` (String)
  - `Imie`
    - `wartosc` (String, maksymalnie 50 znaków, tylko litery i myślniki)
  - `Nazwisko`
    - `wartosc` (String, maksymalnie 50 znaków, tylko litery i wybrane znaki specjalne)

### Agregat: Przelew
- **Encje**:
  - `Przelew`
    - `id` (UUID, unikalny identyfikator przelewu)
    - `zrodloKonto` (Referencja do `KontoBankowe`)
    - `doceloweKonto` (String, Numer konta bankowego w formacie IBAN)
    - `kwota` (Obiekt wartości: KwotaPrzelewu)
    - `opis` (Obiekt wartości: OpisPrzelewu)
    - `dataPrzelewu` (DateTime, data realizacji przelewu)
- **Obiekty wartości**:
  - `KwotaPrzelewu`
    - `wartosc` (Decimal)
    - `waluta` (String, np. "PLN", "EUR")
  - `OpisPrzelewu`
    - `opis` (String, maksymalnie 255 znaków, opcjonalny)
    - `adres` (String, maksymalnie 255 znaków, opcjonalny)

### Agregat: Powiadomienia
- **Encje**:
  - `Powiadomienie`
    - `id` (UUID, unikalny identyfikator powiadomienia)
    - `typ` (Obiekt wartości: TypPowiadomienia)
    - `tresc` (Obiekt wartości: TrescPowiadomienia)
    - `odbiorca` (Referencja do encji Klient)
    - `dataWyslania` (DateTime)
- **Obiekty wartości**:
  - `TrescPowiadomienia`
    - `wartosc` (String, maksymalnie 500 znaków)
  - `TypPowiadomienia` (Enum, wartości: SMS, Email, Push)

### Agregat: Autoryzacja
- **Encje**:
  - `HistoriaLogowan`
    - `id` (UUID, unikalny identyfikator wpisu)
    - `klient` (Referencja do encji Klient)
    - `dataLogowania` (DateTime)
    - `ip` (Obiekt wartości: IP, adres IP logowania)
  - `HistoriaOperacji`
    - `id` (UUID, unikalny identyfikator operacji)
    - `typOperacji` (Enum, np. Logowanie, Przelew, ZmianaDanych)
    - `dataOperacji` (DateTime)
    - `opis` (Obiekt wartości: OpisOperacji)
- **Obiekty wartości**:
  - `OpisOperacji`
    - `typOperacji` (Enum)
    - `wartosc` (String, maksymalnie 255 znaków)
  - `IP`
    - `ip` (String, zgodnie ze specyfikacją IPv4)

## Diagram Modelu
![Diagram Modelu](model.png)

## Przyjęte Założenia
| Encja/Obiekt Wartości  | Atrybut              | Typ Danych    | Opis/Założenia                                                                 |
|------------------------|----------------------|---------------|--------------------------------------------------------------------------------|
| `KontoBankowe`         | `numerKonta`        | String        | Musi być unikalny i zgodny z formatem IBAN.                                    |
|                        | `saldo`             | Decimal       | Musi być większe lub równe 0.                                                 |
| `Klient`               | `imie`              | Imie          | Maksymalnie 50 znaków, tylko litery i myślniki.                               |
|                        | `nazwisko`          | Nazwisko      | Maksymalnie 50 znaków, tylko litery, myślniki i apostrofy.                    |
| `Powiadomienie`        | `typ`               | Enum          | Akceptowane wartości: SMS, Email, Push.                                       |
|                        | `tresc`             | TrescPowiadomienia | Maksymalnie 500 znaków.                                                     |
| `HistoriaLogowan`      | `ip`                | String        | Musi być zgodny z formatem IPv4 lub IPv6.                                     |
| `HistoriaOperacji`     | `opis`              | OpisOperacji  | Maksymalnie 255 znaków.                                                       |

## Operacje
1. **Zarządzanie Kontem**:
   - Tworzenie nowego konta z przypisanym właścicielem.
   - Aktualizacja salda konta po realizacji przelewu.
2. **Przelewy**:
   - Tworzenie nowego przelewu po weryfikacji dostępności środków.
   - Aktualizacja sald kont źródłowego i docelowego.
3. **Powiadomienia**:
   - Wysyłanie powiadomień w zależności od preferencji klienta.
   - Zarządzanie historią powiadomień.
4. **Autoryzacja**:
   - Rejestrowanie każdego logowania klienta.
   - Przechowywanie historii operacji na kontach.

