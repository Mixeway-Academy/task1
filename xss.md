# Zadanie 2 - Weryfikacja danych wejściowych

## Opis podatności
Znaleziono podatność typu **Stored Cross-Site Scripting (XSS)** w aplikacji "Flask Book Library". Podatność umożliwiała wstrzyknięcie złośliwego kodu JavaScript poprzez formularz dodawania nowej książki (pole "Title"), który był następnie przechowywany w bazie danych i wykonywanyza każdym razem gdy przechodzi się do zakładki z książkami.

## Sposób odtworzenia
Podatność można było odtworzyć w formularzu dodawania książki, wpisując w pole tytułu kod:
`"><script>alert(1)</script>`

## Zaproponowana poprawka
Poprawka polega na sanitacji danych wejściowych bezpośrednio w backendzie aplikacji, przed ich zapisaniem w bazie danych. W tym celu wykorzystano bibliotekę `bleach`, która czyści dane wejściowe z potencjalnie niebezpiecznych tagów HTML i atrybutów.

### Zmiany w kodzie (views.py):
W funkcjach `create_book` oraz `edit_book` w pliku `project/books/views.py` dodano sanitację wszystkich pól przyjmujących dane od użytkownika:

```python
# Przykład sanitacji w create_book:
sanitized_name = bleach.clean(data['name'])
new_book = Book(name=sanitized_name, ...)
```

Dzięki temu, nawet jeśli użytkownik spróbuje wstrzyknąć tag `<script>`, zostanie on usunięty lub przefiltrowany przed zapisem, co eliminuje zagrożenie XSS.

Prawdopodobnie podatność XSS dotyczy również pól Author jak i innych zakładek, natomiast skupiłem się tylko na jednej jako przykład.