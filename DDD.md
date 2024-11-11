# DDD 4 banking

Zadanie miało na celu zmodelowanie fragmentu bezpiecznej aplikacji bankowej wykorzystując zasady DDD. W zadaniu skupiono się na zidentyfikowaniu 2 kluczowych bounded contextów - zarządzanie kontem bankowym oraz realizacji przelewów oraz odpowiednich agregatów, encji i obiektów, wspierających podstawowe działanie modelowanej aplikacji. Określono również odpowiednie założenia i ograniczenia zaprojektowanych elementów systemu.

## Bounded Contexty
### Zarządzanie kontem bankowym

kontekst obsługujący funkcje związane z kontem bankowym, np. zakładanie konta, sprawdzanie salda, aktualizacja ilości środków

### Realizacja przelewów

kontekst odpowiadający za realizację przelewów między kontami, w tym: tworzenie, weryfikacja i zatwierdzanie przelewów


## Agregaty, encje i value objects

### Agregaty i encje
* **BankAccount**
    * agregat
    * reprezentuje konto bankowe
    * zawiera encje tj. **Client** oraz value object **Balance** 

* **MoneyTransfer**
    * agregat
    * inicjowanie i zatwierdzanie przelewów między kontami
    * zawiera value object **TransferAmount** oraz encje **Sender** i **Recipient**

### Value objects
* **Balance** - aktualne saldo na danym koncie
* **TransferAmount** - kwota przelewu
* **Address** - value object pwoiązany z **Client** entity, informacja kontaktowa


![diagram](./Diagram%20bez%20tytułu.png)

## Przyjęte założenia i ograniczenia

| Obiekt | Atrybuty | Opis Założenia |
|-|-|-|
| BankAccount | accountNumber, balance, Client | Unikalny numer konta (np. IBAN - 28 znakow); właściciel jako encja (Client) |
| MoneyTransfer | transferId, date, status, sender, recipient | Każdy przelew ma unikalne ID; kwota jako value object (TransferAmount); data i odbiorca/nadawca |
| Client | clientId, name, address | Identyfikator klienta, dane osobowe, adres jako obiekt wartości (Address) |
| TransferAmount | value, currency | Kwota przelewu > 0; waluta zgodna z walutą konta (w przypadku "konta" wielowalutowego, z klientem zostaje powiązane nowe konto (BankAccount) z nową walutą) |
| Address | coutnryCode, city, postalCode, street, houseNumber | Weryfikacja formatu kodu pocztowego (postalCode); Wybór kodu państwa z listy (enumeracja) |
