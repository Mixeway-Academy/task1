import os
import tempfile

import pytest
from project import app, db


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.mark.parametrize("book_name", [
    "The Mystery of the Old Manor",
    "Starlight Ventures: A Cosmic Journey",
    "Ech4234oes of the Past: Memories Revisited",
    "Guardia243 - 23ns of the Realm (Part II)",
    "Whispers in the Wind: A Tale of Courage",
    "Chronicles of t-1)(-:he Ancient Times",
    "Beyond the Horizon: Exploring New Worlds",
    "The Last Stand: Heroes Unite",
    "Secrets of the Enchanted Forest",
    "Journey to the Center (A Sci-Fi Odyssey)"
])
def test_book_name_accepts_valid_values(client, book_name):
    response = client.post("/books/create",
                           json={"name": book_name, "author": "xxx", "year_published": 2023,
                                 "book_type": "xxx"},
                           follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.parametrize("book_name", [
    "<script>alert('Is book name still compromised?')</script>"
    "<image/src/onerror=prompt(8)>",
    "<img/src/onerror=prompt(8)>",
    "<image src/onerror=prompt(8)>",
    "<img src/onerror=prompt(8)>",
    "<image src =q onerror=prompt(8)>",
    "<img src =q onerror=prompt(8)>",
    "</scrip</script>t><img src =q onerror=prompt(8)>",
    "<script\x20type=\"text/javascript\">javascript:alert(1);</script>",
    "<script\x3Etype=\"text/javascript\">javascript:alert(1);</script>",
    "<script\x0Dtype=\"text/javascript\">javascript:alert(1);</script>",
    "<script\x09type=\"text/javascript\">javascript:alert(1);</script>",
    "<script\x0Ctype=\"text/javascript\">javascript:alert(1);</script>",
    "<script\x2Ftype=\"text/javascript\">javascript:alert(1);</script>",
    "<script\x0Atype=\"text/javascript\">javascript:alert(1);</script>",
    "'`\"><\\x3Cscript>javascript:alert(1)</script>",
    "'`\"><\\x00script>javascript:alert(1)</script>",
    "<img src=1 href=1 onerror=\"javascript:alert(1)\"></img>",
    "<audio src=1 href=1 onerror=\"javascript:alert(1)\"></audio>",
    "<video src=1 href=1 onerror=\"javascript:alert(1)\"></video>"])
def test_book_name_rejects_invalid_values(client, book_name):
    with pytest.raises(ValueError):
        client.post("/books/create",
                    json={"name": book_name, "author": "xxx", "year_published": 2023,
                          "book_type": "xxx"},
                    follow_redirects=True)
