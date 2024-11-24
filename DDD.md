W ramach zadania zostały zdefiniowane dwa konteksty:
- zarządzanie kontem bankowym
- uwierzytelnienie

## Diagram

![[diagram.png]]

## Zarządzanie kontem bankowym

**Agregat: Konto Bankowe**
- numerKonta (String)
	- ograniczony do 26 cyfr, nazywany także numerem rachunku
- IBAN (String)
	- ograniczony do 28 znaków składa się z przedrostka krajowego banku (np. PL) oraz numeru rachunku
- sadlo (Double)
	- wartość nie może być ujemna (założyłem że nie są to konta debetowe)
- Waluta (Enum)
	- wartość atrybutu ograniczona do listy oznaczeń walut, tj. EUR, PLN, USD, GBP itp. 
**Operacje:**
- otworzenie konta bankowego


**Encja: Klient**
- idKlienta (String) - unikalny identyfikator klienta
	- stała długość 12 znaków
	- możliwe są tylko cyfry
- imię (String)
	- długość: 2-60 znaków
	- możliwe jedynie znaki alfabetyczne z rozszerzeniem na znaki diakrytyczne
- Nazwisko (String)
	- długość: 2-60 znaków
	- możliwe jedynie znaki alfabetyczne z rozszerzeniem na znaki diakrytyczne
- Email (String)
	- długość: 3-254 znaków
	- format zgodny z określonymi RFC: 3696, 1123, 4291, 5321, 5322
- PESEL (String)
	- długość: 11 znaków
	- możliwe są tylko cyfry
**Operacje:**
- utworzenie klienta
- aktualizacja dokumentu tożsamości
- aktualizacja adresu


**Obiekt wartości: Adres**
- ulica (String)
	- długość: do 254 znaków
	- możliwe jedynie znaki alfabetyczne z rozszerzeniem na znaki diakrytyczne
- numerBudynku (String)
	- długość: 1-10 znaków
	- możliwe jedynie znaki alfanumeryczne
- numerMieszkania (String)
	- długość: 1-10 znaków
	- możliwe jedynie znaki alfanumeryczne
- kodPocztowy (String)
	- długość: 1-10 znaków
	- możliwe jedynie znaki alfanumeryczne
- kraj (Enum)
	- wybór ograniczony do listy krajów na świecie


**Obiekt wartości: DokumentTożsamości**
- typDokumentu (Enum)
	- wybór ograniczony do typu dokumentu: paszport, dowód osobisty
- numerDokumentu (String)
	- długość: 9 znaków
	- możliwe jedynie znaki alfanumeryczne
- dataWygaśnięcia (Date)

## Uwierzytelnienie

**Agregat: Użytkownik**
- idKlienta (String) - wartość powiązana z klientem, z którym użytkownik jest powiązany
	- tała długość 12 znaków
	- możliwe są tylko cyfry
- statusKonta (Enum)
	- ograniczenie do wartości: AKTYWNE, NIEAKTYWNE, ZABLOKOWANE
- metoda2FA (Enum)
	- ograniczenie do wartości: SMS, TOTP, FIDO2
- aktywnaSesja (TokenSesji) - zalogowana sesja (jeśli taka istnieje)
**Operacje:**
- logowanie użytkownika
- wylogowywanie użytkownika
- reset hasła użytkownika


**Encja: TokenSesji**
- idSesji (String)
	- format UUID
- token (String) - wygenerowany token sesji
- dataUtworzenia (Date)
- dataWygaśnięcia (Date)
- adresIP (String)
	- format zgodny z ipv4: xxx.xxx.xxx.xxx
**Operacje:**
- unieważnienie tokenu sesji


**Obiekt Wartości: Hasło**
- wartość (String) - pole zawierające hash hasła
	- hash hasła musi być generowany zgodnie z wytycznymi bezpieczeństwa NIST
- dataUtworzenia (Date)
- dataOstatniejZmiany (Date)
- wymuszenieZmiany (Bool) - flaga do ustawienia w przypadku wymuszonego resetu hasła dla użytkownika

## Możliwe integracje

- dla każdego użytkownika tworzony jest jeden użytkownik pozwalający na uwierzytelnienie w bankowości internetowej
- dla danego klienta może zostać zresetowane hasło przez pracownika banku, co powoduje ustawienie flagi w obiekcie hasła