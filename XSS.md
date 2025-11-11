**Przykłady wystąpień podatności XSS:**
![Udokumentowany wynik podatności XSS, przykład 1 - Jan Konarski](XSS_1.png "XSS_Vulnerability_1")
![Udokumentowany wynik podatności XSS, przykład 2 - Jan Konarski](XSS_2.png "XSS_Vulnerability_2")
**Przykłady wstrzyknięć:**
```
- <BODY ONLOAD=alert(’XSS’)>
- <script>alert(1)</script>
- <div style="font-family:'foo&#10;;color:red;';">LOL
- <svg><script ?>alert(1)
- I kilka innych, niektóre tworzą iframe'y, których trudno się pozbyć, w tym wypadku administrator musi usunąć rekord z bazy danych aplikacji.
```

Sposób rozwiązania podatności dla aplikacji do wypożyczania książek:
- Sprawdzenie długości ciągu znakowego dla pól formularza.
- Wykorzystanie zapytania Regex, w celu eliminacji znaków specjalnych pozwalających na wykonanie kodu HTML'owego.
- Wykorzystanie funkcji, które potraktują kod jako tekst.
