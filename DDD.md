# Domain Driven Design – Aplikacja Bankowa

## Opis Zadania
Celem zadania jest zamodelowanie fragmentu aplikacji bankowej przy użyciu zasad Domain Driven Design (DDD). Zadanie koncentruje się na dwóch aspektach – Zarządzanie Kontem oraz Przelewy.

## Diagram Modelu
![Model](https://github.com/gzub04/TBO-task1/blob/main/model.png)

## Konteksty, Agregaty, Encje i Obiekty Wartości


### Kontekst KontoBankowe
**Agregat Konto**
- **IdKonta** - Unikalny identyfikator konta (UUID)
- **Numer rachunku** - Numer rachunku bankowego, spełniający standardy IBAN (String)
- **Saldo** - Aktualne saldo konta wyrażone jako liczba (numeric)
- **Waluta** - Kod waluty konta, np. "PLN" (String)

**Encja Klient**
- **IdKlienta** - Unikalny identyfikator klienta (UUID)
- **DaneOsobowe** - Dane osobowe klienta (DaneOsobowe)
- **Adres** - Adres zamieszkania klienta (Adres)

**Value Object DaneOsobowe**
- **Imie** - Imię klienta (String)
- **Nazwisko** - Nazwisko klienta (String)
- **DataUrodzenia** - Data urodzenia klienta w formacie YYYY-MM-DD (Date)

### Kontekst Przelew
**Agregat Przelew**
- **IdPrzelewu** - Unikalny identyfikator przelewu (UUID)
- **NumerKontaNadawcy** - Numer konta bankowego nadawcy przelewu (String)
- **NumerKontaOdbiorcy** - Numer konta bankowego odbiorcy przelewu (String)
- **Kwota** - Kwota do przelania, obejmująca wartość i walutę (Kwota)

**Agregat Kwota**
- **KwotaPrzelewu** - Wartość kwoty przelewu, dodatnia liczba zmiennoprzecinkowa (numeric)
- **Waluta** - Kod waluty przelewu, np. "PLN" (String)
