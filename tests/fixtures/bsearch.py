import string

books = string.ascii_uppercase
books = list(books)


def bsearch(book, shelf):
    start = 0
    end = len(books) - 1

    while end >= start:
        halfway = (start + end) // 2

        guess = shelf[halfway]

        if guess == book:
            return halfway

        elif guess > book:
            end = halfway - 1

        elif guess < book:
            start = halfway + 1


g = bsearch("Q", books)
