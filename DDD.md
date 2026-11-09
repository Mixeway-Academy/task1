# Zadanie 1 – Modelowanie Domain-Driven Design dla systemu bankowego

## 1. Opis zadania
Celem zadania jest zamodelowanie wybranego, bezpiecznego fragmentu aplikacji bankowej z wykorzystaniem zasad Domain-Driven Design (DDD). Projekt koncentruje się na wydzieleniu dedykowanego kontekstu biznesowego (Bounded Context) oraz zamodelowaniu w nim kluczowych agregatów, encji i obiektów wartości. Model eliminuje zbędne powiązania danych, kładąc nacisk na reguły integralności transakcji, poprawność kwot i formatów rachunków.


## 2. Zdefiniowanie Bounded Context

W ramach architektury całego systemu bankowego zidentyfikowano następujące konteksty:
* **Uwierzytelnianie:** logowanie, sesja użytkownika, uwierzytelnianie dwuskładnikowe.
* **Dane Klientów:** zarządzanie danymi osobowymi klientów, w tym imię, nazwisko, PESEL, adres zamieszkania.
* **Przelewy:** stan rachunków, weryfikacja środków oraz przeprowadzanie transakcji finansowych.

Do dalszego szczegółowego modelowania wybrano **Przelewy**.

## 3. Schemat modelu dziedzinowego

Poniższy diagram przedstawia relacje pomiędzy elementami wewnątrz wybranego kontekstu:

![Model DDD - Przelewy](model.png)


## 4. Przyjęte założenia, formaty danych i reguły biznesowe

Poniższa tabela przedstawia szczegółową specyfikację encji, agregatów i obiektów wartości, oraz nałożone na nie ograniczenia reguł domenowych.

| Element | Typ DDD | Atrybuty i typy danych | Formaty i reguły biznesowe |
| :--- | :--- | :--- | :--- |
| **Przelew** | Agregat | • `id`: UUID<br>• `od`: NumerRachunku<br>• `do`: NumerRachunku<br>• `kwota`: Kwota | • Rachunek nadawcy (`od`) i rachunek odbiorcy (`do`) nie mogą być tożsame.<br>• Kwota przelewu musi być większa od zera.<br>• Zlecenie przelewu jest niezmienne po zatwierdzeniu. |
| **KontoBankowe** | Agregat | • `id`: UUID<br>• `numerRachunku`: NumerRachunku<br>• `saldo`: Kwota | • Saldo konta nie może spaść poniżej 0.<br>• Rachunek jest jednawalutowy – waluta salda musi być zgodna z walutą przypisaną do konta. |
| **Klient** | Encja | • `id`: UUID<br>•`konta`: List\<UUID\> | • W tym kontekście modeluje jedynie powiązanie właściciela z kontem.<br>• Klient może posiadać jedno lub wiele Kont Bankowych. |
| **NumerRachunku** | Obiekt Wartości | • `numer`: String | • Format polskiego standardu NRB (dokładnie 26 cyfr). |
| **Kwota** | Obiekt Wartości | • `wartosc`: Decimal<br>• `waluta`: String | • Wartość nieujemna, zaokrąglana ściśle do 2 miejsc po przecinku.<br>• Waluta w standardzie ISO 4217 (np. `PLN`, `EUR`, `USD`).<br>• Zabezpieczenie przed operacjami na różnych walutach (np. dodawanie PLN do EUR wymaga przejścia przez zewnętrzny kantor). |

---

## 5. Scenariusz transakcji

1. **Inicjalizacja:** Zalogowany `Klient` zgłasza chęć wykonania przelewu z jego `KontaBankowego`.
2. **Weryfikacja reguł:**
   - Sprawdzana jest poprawność obiektów wartości: format `NumerRachunku` odbiorcy oraz czy `Kwota` > 0.
   - Agregat `KontoBankowe` weryfikuje swój niezmiennik: czy bieżące `saldo` pozwala na pokrycie wnioskowanej kwoty.
3. **Modyfikacja stanu:**
   - Agregat `KontoBankowe` nadawcy pomniejsza swoje saldo o zadaną kwotę.
   - Zostaje utworzony i utrwalony nowy agregat `Przelew` powiązany z numerami rachunków nadawcy i odbiorcy.

