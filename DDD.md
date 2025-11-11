#Mateusz Węcławski TBO
Celem projektu jest zamodelowanie fragmentu systemu bankowego zgodnie z zasadami **Domain Driven Design (DDD)**.  
Model obejmuje dwa konteksty: **Zarządzanie Kontem** oraz **Przelewy**, pozwalające na tworzenie klientów, prowadzenie rachunków i inicjowanie przelewów.  
Celem jest zaprezentowanie zależności pomiędzy encjami, agregatami oraz obiektami wartości w bezpiecznym modelu domenowym.



1. Konteksty w odrębie systemu bankowego
   - Zarządzanie Kontem - odpowiada za m.in. rejestrację użytkownika, zarządzanie saldem
   - Przelewy - odpowiada za inicjowanie i walidację wykonywania przelewów między kontami
   - Uwierzytelnianie - odpowiada za logowanie i weryfikację użytkownika

2. Modelowanie Agregatów, Encji i Obiektów Wartości
   - Agregat KontoBankowe:
     - Encje:
         - KontoBankowe (główna encja)
         - Klient (zawiera m.in. jego dane osobowe)
     - Value Objects:
          - Saldo (reprezentuje ilość środków klienta)
          - Numer konta
    - Agregat Przelew:
      - Encje:
          - Przelew (główna encja, identyfikowalny transfer pieniędzy)
      - Value Objects:
          - Kwota przelewu
          - Numer konta odbiorcy przelewu
          - Numer konta nadawcy przelewu
         
3. Szczegółowy opis encji i value objects:
   - Konto Bankowe:
       - Klient_id
       - Saldo (value object)
       - Numer_Konta (numer konta jest jednoczesnie id konta gdyż jest unikalne)
   - Klient:
        - Numer posiadanego konta
        - Dane Osobowe
        - Dane Adresowe (value object) 
        - Dane kontaktowe (value object) 
    - Dane Osobowe:
         - Imie (string min. 3 znaki, max 30 znaków, bez cyfr)
         - Nazwisko (string min. 3 znaki, max 30 znaków, bez cyfr)
         - Data urodzenia (data, walidacja: użytkownik musi mieć minimum 18 lat *w tym banku nie ma kont dla dzieci*)
         - Płeć (mężczyzna/kobieta)
         - Pesel (string, 11 cyfr, walidacja peselu na podstawie m.in płci i daty urodzenia)
    - Dane Adresowe:
         - ulica (string min. 3 znaki, max 40 znaków, dodatkowa walidacja czy taki adres faktycznie istnieje, np API google maps albo urzędu) 
         - miasto (string min. 3 znaki, max 40 znaków, dodatkowa walidacja czy taka miejscowość faktycznie istnieje, np API google maps albo urzędu) 
         - kod pocztowy (string w formacie "cyfra cyfra - cyfra cyfra cyfra", dodatkowa weryfikacja po api czy dany kod pocztowy pasuje pod dane miasto i ulicę)
    - Dane Kontaktowe:
         - e-mail (string, dozwolone cyfry i litery, musi być w formacie "X@'strona.com/pl'")
         - nr telefonu (9 cyfr)
    - Przelew:
         - Nadawca_id (int, 26 cyfr, tu brak walidacji bo automatycznie system pobiera od uzytkownika) 
         - Odbiorca_id (int, 26 cyfr, dodatkowa walidacja czy taki numer istnieje)
         - Kwota_przelewu (Decimal, kwota m.in 1 zł, max w zależnośći od tego jaki limit ma ustawiony nadawca oraz od aktualnego salda)
         - Data_realizacji_przelewu (format daty, data musi być w przyszłości, lub jeśli przelew natychmiastowy to data dzisiejsza)
         - Tytuł_przelewu (i cyfry i litery, min. 5 znaków, max 40)



<img width="756" height="301" alt="Untitled Diagram drawio" src="https://github.com/user-attachments/assets/9ed8d9f4-f4a1-4362-9a26-72f93951a1c6" />
