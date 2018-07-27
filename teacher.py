import operator


class Student:

    def __init__(self, surname="", name=""):
        self.surname = surname
        self.name = name
        self.index = 0
        self.probability = 0
        self.accounted = True
        self.pages = tuple()

    def getName(self):
        return f"{self.surname}{' ' if self.name else ''}{self.name}"

    def __repr__(self):
        return f"{f'{self.name()} ({self.index})' if self.surname or self.name else f'No name, index {self.index}'}, {'accounted' if self.accounted else 'absent'}, {self.probability}%, {len(self.pages)} pages ({', '.join(self.pages)})"

    def __str__(self):
        return f"{f'{self.name()} ({self.index})' if self.surname or self.name else f'{self.index}'}: {self.probability}%, {len(self.pages)} pages ({', '.join(self.pages)})" if self.accounted else "Absent"


class StudentList:
    def __init__(self):
        self.list = []

    def update(self):
        self.sortAlphabetically()
        self.indexStudents()

    def createStudents(self, number):
        self.list = [Student() for i in range(number)]
        self.update()

    def sortAlphabetically(self):
        self.list = sorted(sorted(
            self.list, key=lambda student: student.name), key=lambda student: student.surname)

    def indexStudents(self):
        ind = 1
        for i in self.list:
            i.index = ind
            ind += 1

    def calculatePages(self, nPages):
        for i in range(1, nPages+1):
            self.list[sumDigits(i)-1].pages.append(i)

    def __repr__(self):
        return ', '.join([str(i) for i in self.list])

    def __str__(self):
        return '\n'.join([str(i) for i in self.list])


def sumDigits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s


studentList = StudentList()
