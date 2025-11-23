import pytest
from datetime import datetime, timedelta
from project.books.models import Book
from project.customers.models import Customer
from project.loans.models import Loan

# Valid data tests
@pytest.mark.parametrize("name,author", [
    ("Pan Tadeusz", "Adam Mickiewicz"),
    ("LÓD", "Jacek Dukaj"),
    ("12345", "Autor123"),
    ("Żółta Łódź", "Łukasz Nowak"),
])
def test_valid_book_creation(name, author):
    book = Book(name=name, author=author, year_published=1890, book_type="5days")
    assert book.name == name
    assert book.author == author
    assert book.status == "available"


# Not valid data tests
@pytest.mark.parametrize("name,author", [
    ("<script>alert(1)</script>", "Autor"),          
    ("Book", "<b>Autor</b>"),      
    ("Book!", "Autor"),            
    ("Book@", "Autor"),  
    ("", "<script>alert(1)</script>"),                 
])
def test_invalid_book_creation(name, author):
    with pytest.raises(ValueError):
        Book(name=name, author=author, year_published=2020, book_type="2days")

# Valid data tests
@pytest.mark.parametrize("name,city", [
    ("Jan Kowalski", "Warszawa"),
    ("Anna Nowak123", "Kraków"),
    ("Żaneta Łęcka", "Łódź"),
    ("Michał Żółć", "Gdańsk"),
])
def test_valid_customer_creation(name, city):
    customer = Customer(name=name, city=city, age=30)
    assert customer.name == name
    assert customer.city == city
    assert customer.age == 30


# Not valid data tests
@pytest.mark.parametrize("name,city", [
    ("<script>", "Warszawa"), 
    ("Jan", "<b>Łódź</b>"), 
    ("Jan!", "Warszawa"),      
    ("Jan", "Gdańsk@"),     
    ("", "Poznań"),    
    ("Ewa", ""), 
])
def test_invalid_customer_creation(name, city):
    with pytest.raises(ValueError):
        Customer(name=name, city=city, age=25)

@pytest.mark.parametrize("customer_name,book_name", [
    ("Jan Kowalski", "Pan Tadeusz"),
    ("Anna Żółć", "Lalka"),
    ("Michał123", "Solaris 2"),
    ("Łukasz Nowak", "Wiedźmin"),
])
def test_valid_loan_creation(customer_name, book_name):
    loan_date = datetime.now()
    return_date = loan_date + timedelta(days=7)

    loan = Loan(
        customer_name=customer_name,
        book_name=book_name,
        loan_date=loan_date,
        return_date=return_date,
        original_author="Adam Mickiewicz",
        original_year_published=1834,
        original_book_type="5days"
    )

    assert loan.customer_name == customer_name
    assert loan.book_name == book_name
    assert loan.original_author == "Adam Mickiewicz"
    assert loan.original_year_published == 1834
    assert loan.original_book_type == "5days"
    assert isinstance(loan.loan_date, datetime)
    assert isinstance(loan.return_date, datetime)

# Not valid data tests
@pytest.mark.parametrize("customer_name,book_name", [
    ("<script>alert(1)</script>", "Lalka"),        
    ("Jan", "<script>alert(1)</script>"),           
    ("Jan!", "Solaris"),          
    ("Jan", "Book@"),          
    ("", "Pan Tadeusz"),  
    ("Ewa", ""),   
])
def test_invalid_loan_creation(customer_name, book_name):
    loan_date = datetime.now()
    return_date = loan_date + timedelta(days=7)

    with pytest.raises(ValueError):
        Loan(
            customer_name=customer_name,
            book_name=book_name,
            loan_date=loan_date,
            return_date=return_date,
            original_author="Adam Mickiewicz",
            original_year_published=1834,
            original_book_type="5days"
        )