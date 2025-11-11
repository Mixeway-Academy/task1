**Opis Zadania:**
- Niniejsze zadania miało na celu przedstawić założenia modelu Domain Driven Design dla fragmentu aplikacji bankowej. Schemat zawarty poniżej obrazuje zależności między agregatami, encjami i obiektami wartości dla dziedziny (bounding context) uwierzytelniania użytkowników. Zilustrowany fragment pokazuje przepływ informacji od utworzenia konta użytkownika, przypisania mu roli, aż po podjęcie się próby zalogowania do serwisu i zarejestrowania daty udanego zalogowania do banku online.
![diagram przedstawiający schemat Domain Driven Design dla zadania 01. Tworzenie bezpiecznego oprogramowania - Jan Konarski](DDD_Diagram.png "Diagram")

**Przyjęte założenia / Integracje:**
- W przypadku Bounding Contextu dla Uwierzytelniania, zakładamy, że każdy klient w banku przy rejestracji uzyskuje swoje konto użytkownika.
- Z racji na to, w przypadku pojawienia się kontekstu Klientów, istniałaby relacja Klienci Banku -> Uwierzytelnianie (Klient-Użytkownik)
- Każdy zarejestrowany użytkownik otrzymuje swoją rolę składającą się z: Typu (np. Klient / Pracownik), uprawnień oraz encji opisującej ID Roli w bazie.
- Agregat Logowania rejestruje wszystkie podjęte przez użytkowników (udane) zalogowania. Innymi słowy, sprawdzamy kto się zalogował i kiedy.
- Autoryzacja jest agregatem, który w sposób logiczny łączy ze sobą: Dane logującego się użytkownika, jego uprawnienia oraz timestamp zalogowania się do serwisu.
- Autoryzacja posiada również licznik podjętych prób logowania, po którego przekroczeniu (np. 3) system podejmuje kolejnych prób zalogowania użytkownika do chwili odblokowania konta.
- Autoryzacja integrowałaby się z Bounding Contextem dla Stanu Konta użytkownika, bądź Transakcji. Po udanym uwierzytelnieniu, użytkownik uzyskiwałby dostęp do wyświetlania swoich funduszy i wykonywania transakcji.
