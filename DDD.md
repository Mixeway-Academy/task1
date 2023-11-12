Projekt ten przedstawia fragment systemu bankowego, zaprojektowanego zgodnie z zasadami Domain Driven Design, ze szczególnym uwzględnieniem aspektów bezpieczeństwa. Skupia się na trzech głównych encjach: Osoba, KontoBankowe i Przelew, które są ze sobą powiązane i reprezentują kluczowe funkcje bankowości. Diagram relacji encji wizualizuje strukturę i zależności między tymi encjami, podkreślając ich atrybuty i relacje. Dodatkowo, tabela szczegółowo opisuje każdą encję i jej atrybuty, wraz z wymaganiami bezpieczeństwa, takimi jak ograniczenia długości, format danych i zabezpieczenia przed typowymi zagrożeniami cybernetycznymi. Całość projektu ma na celu zapewnienie klarownego i bezpiecznego modelu danych, który może być wykorzystany w rzeczywistym systemie bankowym.

![d-MPu8KA5W](https://github.com/ppopiolek/task1/assets/56610497/b55a7e36-7bb5-40e4-9613-171301df4c85)

| Encja         | Atrybut         | Opis | Wymagania |
|---------------|-----------------|------|-------------------------|
| Osoba         | ID              | Unikalny identyfikator osoby | Ciąg cyfr, dokładnie 10 znaków, bez możliwości sekwencji powtarzających się cyfr |
|               | Imie            | Imię osoby | Ciąg znaków alfabetycznych, 2-50 znaków, bez znaków specjalnych |
|               | Nazwisko        | Nazwisko osoby | Ciąg znaków alfabetycznych, 2-50 znaków, bez znaków specjalnych |
|               | Email           | Adres email osoby | Walidacja formatu email, maksymalnie 100 znaków, zabezpieczenie przed SQL injection |
|               | Telefon         | Numer telefonu osoby | Tylko cyfry, 9-15 znaków, bez możliwości wprowadzenia kodów krajowych |
|               | DataUrodzenia   | Data urodzenia osoby | Format daty YYYY-MM-DD, walidacja zakresu dat |
|               | Adres           | Adres zamieszkania osoby | Ciąg znaków, maksymalnie 200 znaków, zabezpieczenie przed XSS |
| KontoBankowe  | NumerKonta      | Numer konta bankowego | Ciąg cyfr, dokładnie 26 znaków, zgodność ze standardem IBAN |
|               | Saldo           | Saldo konta | Liczba zmiennoprzecinkowa, zakres od -1e+6 do 1e+6, zabezpieczenie przed manipulacją salda |
|               | TypKonta        | Typ konta bankowego | Predefiniowane wartości, np. 'Oszczędnościowe', 'Rozliczeniowe', bez możliwości wprowadzania danych z zewnątrz |
| Przelew       | IDPrzelewu      | Unikalny identyfikator przelewu | Ciąg cyfr, dokładnie 20 znaków, generowany losowo, bez możliwości predykcji |
|               | Kwota           | Kwota przelewu | Liczba zmiennoprzecinkowa, zakres od 0.01 do 1e+5, walidacja przeciwko manipulacji kwotą |
|               | Tytul           | Tytuł przelewu | Ciąg znaków, maksymalnie 100 znaków |
|               | DataPrzelewu    | Data wykonania przelewu | Format daty i czasu YYYY-MM-DD HH:MM:SS, walidacja zakresu dat i czasu |
