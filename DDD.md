# 1. Opis projektu
Stworzony został projekt aplikacji zarządzającej bankowością zgodnie z zachowaniem zasad _Domain Driven Design_. Projekt ma na celu podzielenie konkretnych komponentów na konteksty biznesowe oraz
uwzględniać ma mechanizmy bezpieczeństwa zapobiegające przed atakami wstrzykującymi dane takimi jak XSS lub SQL Injection. Głównymi 

# 2. Model aplikacji
<img width="4088" height="2608" alt="image" src="https://github.com/user-attachments/assets/e55763fd-e5ff-42fd-b5c1-eee1c0f1dc85" />

# 3. Założenia

| Kontekst | Obiekt | Atrybuty | Funkcje | 
| ----- | ----- | ----- | ----- | 
| **Bank Accounts** | Account | <br>• **AccountID:** UUID (unikalny ciąg znaków)<br>• **AccountName:** String (tylko znaki a-z, A-Z, 0-9)<br>• **Currency:** Enum (przyjmuje tylko 3 duże litery, np. PLN, USD)<br>• **AccountNumber:** String (tylko cyfry, przyjmuje dokładnie 26 znaków dla IBAN)<br>• **Balance:** Decimal (liczba zmiennoprzecinkowa) | _depositFunds(), withdrawFunds()_ | 
| **Bank Accounts** | Client | <br>• **ClientID:** UUID<br>• **FirstName, LastName:** String (tylko litery: a-z, A-Z + ą-ź)<br>• **Pesel:** String (dokładnie 11 cyfr oraz walidacja sumy kontrolnej)<br>• **PhoneNumber:** String (cyfry, opcjonalnie znak _+_ na początku)<br>• **Email:** String (walidacja formatu @ + .) | _updateData(), blockClient()_ | 
| **Bank Accounts** | Address | <br>• **AddressID:** UUID<br>• **Country, City:** String (tylko litery a-z, A-Z)<br>• **Street:** String (litery i cyfry)<br>• **Apartment:** String (litery i cyfry)<br>• **PostalCode:** String (format xx-xxx) | _updateAddress()_ | 
| **Transfers** | Transfer | <br>• **TransferID, TargetAccountID:** UUID<br>• **TransferName:** String (litery, cyfry, znaki specjalne, zakazane: @<>/\)<br>• **TransferAmount:** Decimal (wartość dodatnia)<br>• **Currency:** Enum (3 litery) | _initiateTransfer(), rejectTransfer()_ | 
| **Cards** | Card | <br>• **CardID, AccountID:** UUID<br>• **ExpirationDate:** String (specyficzny format MM/YY)<br>• **State:** INT (cyfra oznaczająca dany stan karty np. 1-active) | _blockCard(), activateCard()_ | 
| **Products** | Product, Offer | <br>• **ProductID, OfferID:** UUID<br>• **ProductName, OfferDescription:** String (dowolne znaki tekstowe. należy użyć Sanitizera)<br>• **ExpireDate:** DateTime (data w przyszłości) | createProduct(), changeOfferDescription() | 
