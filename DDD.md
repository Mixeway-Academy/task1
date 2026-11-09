## Zadanie 1 - Domain Driven Design
### Opis zadania

Celem zadania jest zamodelowanie wybranego fragmentu bezpiecznej aplikacji bankowej zgodnie z podejściem Domain Driven Design (DDD). Projekt skupia się na procesie zlecenia i realizacji przelewu, ograniczając model do kilku najważniejszych agregatów i encji, aby zaprezentować podstawowe zależności oraz założenia bezpieczeństwa.

### 1. Zdefiniowane Bounded Contexts

W obrębie wybranego fragmentu systemu zidentyfikowano następujące konteksty:

*   **Zarządzanie Kontem:** Odpowiada za cykl życia konta bankowego (np. status aktywny/zablokowany) oraz przechowywanie podstawowych danych właściciela rachunku.
*   **Realizacja Przelewów:** Kontekst operacyjny obsługujący logikę biznesową zlecania transakcji, walidacji dostępnych środków i weryfikacji poprawności danych przelewu.
*   **Uwierzytelnianie i Autoryzacja:** Kontekst bezpieczeństwa weryfikujący tożsamość użytkownika oraz jego uprawnienia do dysponowania konkretnym kontem bankowym przed zatwierdzeniem operacji.

### 2. Modelowanie Agregatów, Encji i Obiektów Wartości 

#### Kontekst 1: Zarządzanie Kontem 

**Agregaty:**
*   **KontoBankowe**
    *   Odpowiada za informacje o rachunku bankowym, jego status i powiązanie z właścicielem. 
    *   Kluczowe operacje: otwarcie konta, blokada konta, pobranie salda.

**Encje:**
*   **KontoBankowe**
    *   Korzeń agregatu KontoBankowe. Pilnuje, aby stan rachunku (np. saldo) zawsze był spójny i zgodny z regułami biznesowymi.
*   **Klient**
    *   Odpowiada za podstawowe dane klienta (imię, nazwisko, identyfikator), będącego właścicielem rachunku.

**Obiekty Wartości:**
*   **Adres**
    *   Zawiera szczegóły dotyczące adresu klienta (ulica, miasto, kod pocztowy).
*   **DaneKontaktowe**
    *   Zawiera bezpieczne kanały kontaktu z klientem (adres e-mail, zweryfikowany numer telefonu do powiadomień SMS).

---

#### Kontekst 2: Realizacja Przelewów

**Agregaty:**
*   **Przelew**
    *   Zarządza procesem transferu środków. Gwarantuje, że nie można zmienić kwoty ani odbiorcy po zainicjowaniu transakcji.
    *   Kluczowe operacje: inicjalizacja przelewu, autoryzacja przelewu, realizacja (lub anulowanie/odrzucenie).

**Encje:**
*   **Przelew**
    *   Korzeń agregatu Przelew. Przechowuje dane o transakcji, w tym identyfikator nadawcy, datę operacji i aktualny status (np. PENDING, COMPLETED).

**Obiekty Wartości:**
*   **KwotaPrzelewu**
    *   Reprezentuje kwotę transferu oraz jej walutę. Zawiera logikę weryfikującą, czy kwota jest wartością dodatnią (zabezpieczenie przed manipulacją).
*   **NumerKonta**
    *   Ściśle sformatowany identyfikator rachunku odbiorcy i nadawcy (np. zgodny ze standardem IBAN), walidowany przy utworzeniu obiektu.

---

#### Kontekst 3: Uwierzytelnianie i Autoryzacja 

**Agregaty:**
*   **Uzytkownik (System User)**
    *   Odpowiada za bezpieczeństwo dostępu do systemu. Niezależny od encji Klient, chroni system przed nieautoryzowanym dostępem.
    *   Kluczowe operacje: logowanie, wylogowanie, zablokowanie profilu po nieudanych próbach logowania.

**Encje:**
*   **Uzytkownik**
    *   Korzeń agregatu. Posiada unikalny identyfikator logowania, który po udanym uwierzytelnieniu jest mapowany na identyfikator Klienta.

**Obiekty Wartości:**
*   **DaneLogowania**
    *   Przechowuje bezpieczne dane uwierzytelniające, takie jak hash hasła oraz sól kryptograficzna, nigdy nie przechowuje hasła jawnym tekstem.
*   **TokenSesji**
    *   Generowany po udanym logowaniu. Zawiera informacje o dacie wygaśnięcia sesji oraz jej unikalnym identyfikatorze, służy do autoryzacji operacji (np. zlecenia przelewu).
 
### 3. Zdefiniowane założenia i atrybuty

W celu zapewnienia bezpieczeństwa i spójności danych, przyjęto rygorystyczne założenia dotyczące formatów i ograniczeń dla poszczególnych encji oraz obiektów wartości (Value Objects). Wszystkie obiekty wartości są niemutowalne (immutable).

| Element (Typ) | Atrybuty | Typ danych | Ograniczenia i walidacja (Bezpieczeństwo) |
| :--- | :--- | :--- | :--- |
| **KontoBankowe** (Encja) | `idKonta` <br> `numerKonta` <br> `saldo` <br> `status` | UUID <br> *NumerKonta* <br> *KwotaPrzelewu* <br> Enum | `status` przyjmuje tylko wartości: `AKTYWNE`, `ZABLOKOWANE`, `ZAMKNIETE`. Operacje zmiany salda możliwe tylko w statusie `AKTYWNE`. |
| **Klient** (Encja) | `idKlienta` <br> `imie` <br> `nazwisko` <br> `pesel` | UUID <br> String <br> String <br> String | `imie` i `nazwisko` wolne od znaków specjalnych, `pesel` musi zawierać dokładnie 11 cyfr i przechodzić walidację sumy kontrolnej. |
| **Adres** (VO) | `ulica` <br> `miasto` <br> `kodPocztowy` | String <br> String <br> String | `kodPocztowy` musi być zgodny z wyrażeniem regularnym. |
| **DaneKontaktowe** (VO) | `email` <br> `telefon` | String <br> String | `email` walidowany RFC 5322. `telefon` w formacie międzynarodowym. |
| **Przelew** (Encja) | `idPrzelewu` <br> `kontoNadawcy` <br> `kontoOdbiorcy` <br> `kwota` <br> `status` <br> `data`| UUID <br> *NumerKonta* <br> *NumerKonta* <br> *KwotaPrzelewu* <br> Enum <br> DataTime| `kontoNadawcy` i `kontoOdbiorcy` nie mogą być takie same. `status`: `ZAINICJOWANY`, `AUTORYZOWANY`, `ZREALIZOWANY`, `ODRZUCONY`; `data` musi być datą bieżącą lub przyszłą. |
| **KwotaPrzelewu** (VO) | `wartosc` <br> `waluta` | BigDecimal <br> String | `wartosc` musi być **ściśle większa od 0.00**. `waluta` musi być zgodna ze standardem ISO 4217 (np. 3 litery: `PLN`, `EUR`). |
| **NumerKonta** (VO) | `numer` | String | Format IBAN lub standardowy NRB (26 cyfr). Przy tworzeniu obiektu automatycznie weryfikowana jest suma kontrolna (Modulo 97). |
| **Uzytkownik** (Encja) | `idUzytkownika` <br> `login` | UUID <br> String | `login` musi mieć min. 8 znaków (alfanumeryczne). |
| **DaneLogowania** (VO) | `hashHasla` <br> `sol` | String <br> String | Hasła nigdy nie są przechowywane jawnym tekstem. `hashHasla` to wynik silnej funkcji (np. Argon2id lub bcrypt). |
| **TokenSesji** (VO) | `tokenID` <br> `dataWygasniecia` | String (JWT) <br> DateTime | `dataWygasniecia` nie może być dłuższa niż np. 15 minut od wydania. Wykonanie operacji (przelew) sprawdza czy token jest nadal ważny. |
