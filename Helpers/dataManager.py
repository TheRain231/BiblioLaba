import methods.methods as sql


class Book:
    id = 0
    title = ""
    author = ""
    authorSurname = ""
    genre = ""
    publisher = ""
    description = ""
    image = ""
    count = 0


class DataManager:
    def __init__(self):
        self.booksDictionary: dict[int, Book] = {}
        self.selectedBook = 1

        self.createTable()

    def getSelectedBook(self) -> int:
        return self.selectedBook

    def selectBook(self, value: int):
        self.selectedBook = value

    def insertNewBook(self, title: str, authorName: str, image: str, description: str, genre: str,
                      publishngHouseLabel: str, clientLogin: str = "1", clientPassword: str = "2",
                      count: int = 1, authorSurName: str = ""):
        sql.InsertNewBook(title, authorName, authorSurName, image, description, genre, publishngHouseLabel, clientLogin,
                          clientPassword, count)
        self.loadData()

    def createTable(self):
        sql.CreateDB()
        sql.CreateTables()
        sql.CreateFuncs()
        sql.CreateTriggers()

    def loadData(self):
        genreDictionary = {}
        authorDictionary = {}
        publisherDictionary = {}

        booksData = sql.TakeDataBook()
        genreData = sql.TakeDataGenre()
        authorData = sql.TakeDataAuthor()
        publisherData = sql.TakeDataPublishingHouse()

        for genre in genreData:
            genreDictionary[genre[0]] = genre[1]
        for author in authorData:
            authorDictionary[author[0]] = author[1:]
        for publisher in publisherData:
            publisherDictionary[publisher[0]] = publisher[1]

        for book in booksData:
            print(book)
            bookT = Book()
            bookT.title = book[1]
            bookT.image = book[2]
            bookT.description = book[3]
            bookT.count = book[8]

            bookT.author, bookT.authorSurname = authorDictionary[book[4]]
            bookT.genre = genreDictionary[book[5]]
            bookT.publisher = publisherDictionary[book[6]]

            self.booksDictionary[book[0]] = bookT
