# Potwierdzenie podatności XSS

## Książki

Na stronie `http://localhost:5000/books/` można wprowadzić kod JavaScript w polach nazwy i autora książki:

![Kod JavaScript w polach nazwy i autora książki]({88070C59-4936-460F-A495-8B48EDB2B0CA}.png)

Po zapisaniu danych i odświeżeniu strony pojawiają się okna z komunikatami `1` i `2`:

![Komunikat 1 po odświeżeniu listy książek]({EE5A9CA3-F06C-4D17-AC15-5DA81C0E1A17}.png)
![Komunikat 2 po odświeżeniu listy książek]({F78A26A2-83AB-4EC2-8E23-9837D3FEA488}.png)

## Klienci

Na stronie `http://localhost:5000/customers/` można wprowadzić kod JavaScript w polach imienia i miasta:

![Kod JavaScript w polach imienia i miasta]({FD853E47-B3FF-421D-A74A-4A74FB989CF0}.png)

Po zapisaniu danych i odświeżeniu strony pojawiają się okna z komunikatami `3` i `4`:

![Komunikat 3 po odświeżeniu listy klientów]({343B3017-CBCB-4C07-A9C6-C8A7110B7FC9}.png)
![Komunikat 4 po odświeżeniu listy klientów]({B08AD939-D146-416F-BC66-C8FA984EE474}.png)

## Wypożyczenia

Na stronie `http://localhost:5000/loans/` można wybrać klienta i książkę, których nazwy zawierają wcześniej zapisany kod JavaScript:

![Wybór klienta i książki zawierających kod JavaScript]({BF92D595-28E5-456A-892F-BFF2440703A0}.png)

Po zapisaniu wypożyczenia i odświeżeniu strony pojawiają się okna z komunikatami `3` i `1`:

![Komunikat 3 po odświeżeniu listy wypożyczeń]({FC563CBC-7D7F-4A84-B481-0E252AACCFA9}.png)
![Komunikat 1 po odświeżeniu listy wypożyczeń]({3831E229-EB57-4461-814D-2AD2AB0E7957}.png)

Kod pozostaje zapisany w bazie i wykonuje się przy ponownym wyświetleniu danych. Jest to podatność persistent XSS. Powyższe screenshoty przedstawiają działanie aplikacji przed wprowadzeniem poprawki.
