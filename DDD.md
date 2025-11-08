# Zadanie 1 - Domain Driven Design

## Cel: Celem zadania jest zamodelowanie fragmentu bezpiecznej aplikacji bankowej z wykorzystaniem zasad Domain Driven Design (DDD)

Wybranym obszarem jest obsługa przelewów bankowych oraz wymiany walut.
Model skupia się na kluczowych encjach takich jak Klient, Przelew, WymianaWalut, obiektach wartości takich jak `wyswietlKontoBankowe()`, `zaktualizujKontoBankowe()`, `wykonajPrzelew()` i `wykonajWymiane()` oraz agregatach WyświetlKontoBankowe, ZlećPrzelew i ZlećWymianeWalut.
Przedstawiony model nie stanowi pełnego systemu bankowego, a jedynie uporządkowany fragment pokazujący zależności i zasady projektowe DDD.


## Diagram koncepcyjny modelu DDD


<img width="4478" height="2395" alt="Rysunek 3" src="https://github.com/user-attachments/assets/6140612a-fe53-4c19-b4b4-67ec2d1d737b" />



Na diagramie obiekt wartości `wyswietlKontoBankowe()` jest zaznaczony na środku 3 kontekstów:
- Konta Bankowe
- Przelewy
- Wymiany Walut
  
Ma to symbolizować, że Użytkownik ma mieć dostęp do wszystkich 3 paneli za pomocą tego obiektu.


## Założenia projektowe i specyfikacja

| Typ obiektu | Nazwa | Opis
|--------------|--------|------------------
| Agregat | WyświetlKontoBankowe | Odpowiada za wyświetlanie konta bankowego
| Agregat | ZlećPrzelew | Odpowiada za zlecenia przelewu
| Agregat | ZlećWymianeWalut | Odpowiada za zlecenia wymiany walut

| Typ obiektu | Nazwa | Kluczowe atrybuty | Typ danych / format | Opis / ograniczenia |
|--------------|--------|------------------|----------------------|---------------------|
| Encja | Klient | id_klienta: UUID, imie: String, nazwisko: String, adres: Adres | UUID; tekst | Każdy klient ma unikalny identyfikator i powiązany adres. |
| Encja | Przelew | id_przelewu: UUID, nadawca: KontoBankowe, odbiorca: KontoBankowe, kwota: Kwota, data_zlecenia: Date | UUID; Decimal | Odpowiada za pełny cykl życia przelewu. |
| Encja | WymianaWalut | id_wymiany: UUID, nadawca: KontoBankowe, kwota: Kwota, data_zlecenia: Date, kurs: Kurs, waluta_nadawcy: Enum[PLN, EUR, USD], waluta_do_nabycia: Enum[PLN, EUR, USD] | UUID; Decimal | Odpowiada za pełny cykl życia operacji wymiany walut. |


| Typ obiektu | Operacja | Opis | Integracja z innymi kontekstami |
|-----------|------|-------------------|----------------------------------|
| Obiekt wartości | `wyswietlKontoBankowe()` | Wyświetla główny panel konta bankowego | Integracja z kontekstem **Konto Bankowe**, **Przelewy** i **Wymiany Walut**. |
| Obiekt wartości | `zaktualizujKontoBankowe()` | Aktualizuje stan Konta Bankowego | Aktualizuje dane w kontekście **Konto Bankowe** |
| Obiekt wartości | `wykonajPrzelew()` | Wykonuje przelew i aktualizuje ekran główny konta nadawcy. | Integracja z kontekstem **Przelewy** |
| Obiekt wartości | `wykonajWymiane()` | Wykonuje operację przewalutowania środków, aktualizuje ekran główny konta nadawcy. | Integracja z kontekstem **Wymiany Walut** |











