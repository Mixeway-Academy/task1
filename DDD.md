# Security By Design - Zadanie 1 - Domain Driven Design


1. **Króki opis zadania**
Celem zadania było zamodelowanie fragmentu bezpiecznej aplikacji bankowej wykorzystując zasady Domain Driven Design. W ramach zadania zdefiniowano Bounded Contexts (KontoBankowe, Przelewy, Obligacje), a następnie określono Agregaty, Encje i Obiekty Wartości. Przygotowano także graficzną reprezentację modelu domeny. Na poniższym rysunku Agregaty oznaczono za pomocą okręgów, prostokąty reprezentują Encje, natomiast elipsy to Obiekty Wartości.

2. **Graficzna reprezentacja modelu**

<img width="2231" height="1231" alt="DDD drawio" src="https://github.com/user-attachments/assets/2aab4a26-3c95-4d18-8ca9-9fc3569bff24" />

3. **Opis części modelu i przyjęte założenia**

| Bounded Context  | Opis                                                                                          |
| ---------------- | --------------------------------------------------------------------------------------------- |
| **KontoBankowe** | Realizacja operacji związanych z podglądem aktualnego stanu swoich kont przez klientów banku. |
| **Przelewy**     | Realizacja operacji wysyłania i odbierania przelewów przez klientów banku.                    |
| **Obligacje**    | Realizacja operacji dotyczących zakupu i zarządzania obligacjami przez klientów banku.        |

---

**Agregaty**
- **WyświetlKontoBankowe**  
- **ZlećPrzelew**  
- **KupObligacje**  

---

**Encje i ich atrybuty**

| **Encja** | **Atrybut** | **Typ danych** | **Długość / Format** | **Akceptowane znaki** | **Przykład** |
|------------|--------------|----------------|-----------------------|-----------------------|---------------|
| **Klient** | NumerIDKlienta | INT | – | cyfry 0–9 | 42 |
|  | NumerKontaKlienta | STRING | 26 znaków (NRB) | A–Z, 0–9 | PL61109010140000071219812874 |
|  | ImięKlienta | STRING | max 30 znaków | A–Z, a–z, ąćęłńóśźż, ĄĆĘŁŃÓŚŹŻ, spacja, myślnik | Jan |
|  | NazwiskoKlienta | STRING | max 40 znaków | A–Z, a–z, ąćęłńóśźż, ĄĆĘŁŃÓŚŹŻ, spacja, myślnik | Kowalski |
| **Przelew** | NumerIDPrzelewu | INT | – | cyfry 0–9 | 4242 |
|  | NumerKontaNadawcy | STRING | 26 znaków (NRB) | A–Z, 0–9 | PL12109024025963568524326623 |
|  | NumerKontaOdbiorcy | STRING | 26 znaków (NRB) | A–Z, 0–9 | PL14109024023977234567655981 |
| **Obligacje** | NumerIDObligacji | INT | – | cyfry 0–9 | 424242 |
|  | CenaObligacji | DECIMAL(10,2) | – | cyfry 0–9, kropka dziesiętna | 1250.50 |
|  | TerminWykupu | DATE | YYYY-MM-DD | cyfry, znak „-” | 2025-12-31 |

---

**Obiekty wartości**

| **Obiekt wartości** | **Typ danych** | **Długość / Format** | **Akceptowane znaki** | **Przykład** |
|----------------------|----------------|----------------------|-----------------------|---------------|
| StanKontaKlienta | DECIMAL(12,2) | – | cyfry 0–9, kropka dziesiętna | 10500.75 |
| StanKontaKlientaDoPrzelewu | DECIMAL(12,2) | – | cyfry 0–9, kropka dziesiętna | 2500.00 |
| StanKontaKlientaDoZakupuObligacji | DECIMAL(12,2) | – | cyfry 0–9, kropka dziesiętna | 42000.00 |
| KwotaWychodzacegoPrzelewu | DECIMAL(10,2) | – | cyfry 0–9, kropka dziesiętna | 42.42 |
| LiczbaKupowanychObligacji | INT | – | cyfry 0–9 | 42 |



W modelu założono, że informacja o stanie konta będzie występowała w każdym z trzech kontekstów. Jednocześnie w każdym z nich będzie ona reprezentowana przez inny obiekt wartości, ponieważ w przypadku StanKontaKlienta chodzi o informację ile pieniędzy ma klient na koncie wyłącznie w celu informacyjnym w obszarze kontekstu KontoBankowe. Jednocześnie StanKontaKlientaDoPrzelewu i StanKontaKlientaDoZakupuObligacji (odpowiednio w kontekście Przelewy i Obligacje) będą pozwalać realizować cele związane z np. weryfikacją, czy klient ma wystarczająco środków do zlecenia przelewu lub zakupu obligacji.
