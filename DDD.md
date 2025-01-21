# Domain driven design

## Cel zadania 
 Celem zadania jest zamodelowanie fragmentu bezpiecznej aplikacji bankowej wykorzystując zasady Domain Driven Design.
 
## Definiowanie kontekstów encji i obiektów wartości
W ramach zadania rozważono 3 przykładowe konteksty:
- Przelewy (kontekst w ramach którego realizowane są transfery środków)
- Zarządzanie kontem (kontekst obsługi danych i konta klienta)
- Autoryzacja (kontekst realizujący zadania bezpieczeństwa operacji)

### Konteks przelewy
- Agregat: Operacja
	- Encja: Przelew (Atrybuty: IdOperacji; Kwota; Nadawca; Odbiorca; TimeStamp)
	- Obiekt wartości: Kwota (Atrybuty: Watość; Waluta)
	- Obiekt wartości: TimeStamp (Atrybuty: Data; Godzina)
	- Obiekt wartości: Nadawca (Atrybuty: IdKlienta; NumerKonta)
	- Obiekt wartości: Odbiorca (Atrybuty: IdKlienta; NumerKonta)

### Kontekst Zarządzanie kontem
- Agregat: KontoBankowe
	- Encja: Konto (Atrybuty: NumerKonta; IdKlienta; Saldo)
	- Obiekt wartości: Saldo (Atrybuty: Kwota; Waluta)
	- Encja: Klient (Atrybuty: IdKlienta; DaneOsobowe; DaneKontaktowe)
	- Obiekt wartości: DaneOsobowe (Atrybuty: Imie; Nazwisko; Pesel)
	- Obiekt wartości: DaneKontaktowe (Atrybuty: NrTelefonu; Email; Adres)
	- Obiekt wartości: Adres (Atrybuty: Miasto; Ulica; NrBudynku; NrLokalu; KodPocztowy)
	
### Kontekst Autoryzacja
- Agregat Sesja
	- Encja: Sesja (Atrybuty: IdSesji; IdKlienta; TokenSesji; Status; CzasRozpoczęcia; CzasZakończenia)
	
## Założenia
- Przelew: Nadawca i Odbiorca wskazują na rózne konta bankowe
- Kwota: większa od zera w obsługiwanej walucie
- Konto: Numer konta unikalny i zgodny z formatem IBAN
- Dane Osobowe: wszystkie pola wypełnione; Imie i Nazwisko składają się wyłącznie z liter i myślników; PESEL prawidłowy ze względu na format
- Adres: Kod pocztowy we własciwym formacie; Jedynie pole NrLokalu może pozostać puste dla budynków niepodzielonych na unikalnie numerowane lokale 