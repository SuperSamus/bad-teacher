class Student:
    index = 0
    interrogable = True
    pages = set()
    _percentage = 0

    def __init__(self, surname="", name=""):
        self.surname = surname
        self.name = name

    def get_name(self):
        return f"{self.surname}{' ' if self.name else ''}{self.name}"

    @property
    def percentage(self):
        return self._percentage/100

    @percentage.setter
    def percentage(self, percentage):
        self._percentage = round(percentage * 100)

    def calculate_percentage(self, n_pages, n_students, interrogable_students):
        if self.interrogable:
            self.percentage = len(self.pages) * n_students * \
                100 / n_pages / interrogable_students

    def __repr__(self):
        if self.surname or self.name:
            name = f"{self.get_name()} ({self.index})"
        else:
            name = f"No name, index {self.index}"
        if self.interrogable:
            status = "interrogable"
        else:
            status = "not interrogable"
        pg = f"{len(self.pages)} pages ({join_list(sorted(self.pages), ', ')})"
        return f"{name}, {status}, {self.percentage}%, {pg};"

    def __str__(self):
        if self.surname or self.name:
            name = f"{self.get_name()} ({self.index})"
        else:
            name = self.index
        pg = f"{len(self.pages)} pages ({join_list(sorted(self.pages), ', ')})"
        if self.interrogable:
            return f"{name}: {self.percentage}%, {pg};"
        else:
            return f"{name}: not interrogable;"


class StudentList:
    list = []
    n_pages = 0
    # the pages that will call an absent student or an out of range student
    invalid_pages = set()
    # the percentage to call an absent student or an out of range student
    _invalid_percentage = 0

    @property
    def invalid_percentage(self):
        return self._invalid_percentage/100

    @invalid_percentage.setter
    def invalid_percentage(self, percentage):
        self._invalid_percentage = round(percentage * 100)

    def create_students(self, number):
        self.list = [Student() for i in range(number)]
        self.update()

    def search_students(self, *args, **kwargs):
        search_list = set()
        for i in args:
            for s in self.list:
                if i in s.surname or i in s.name or i == s.index:
                    search_list.add(s.index-1)
        for key, value in kwargs.items():
            for s in self.list:
                exec(
                    f"if {value} == s.{key}:\n\tsearch_list.add(s.index-1)")
        return list(search_list)

    def update(self):
        self._sort_alphabetically()
        self._index_students()

    def _sort_alphabetically(self):
        self.list = sorted(self.list, key=lambda s: s.name)
        self.list = sorted(self.list, key=lambda s: s.surname)

    def _index_students(self):
        ind = 1
        for s in self.list:
            s.index = ind
            ind += 1

    def count_interrogable_students(self):
        interrogable_students = 0
        for s in self.list:
            if s.interrogable:
                interrogable_students += 1
        return interrogable_students

    def _calculate_student_pages(self):
        self.invalid_pages = set()  # resetting
        for s in self.list:
            s.pages = set()

        for p in range(1, self.n_pages+1):
            try:
                s = self.list[sum_digits(p)-1]
                assert s.interrogable
                s.pages.add(p)
            # absent students or out of range will go there
            except (AssertionError, IndexError):
                self.invalid_pages.add(p)

    def _calculate_student_percentage(self):
        self.invalid_percentage = 0  # resetting

        for s in self.list:
            try:
                assert s.interrogable
                s.calculate_percentage(self.n_pages, len(
                    self.list), self.count_interrogable_students())
            except AssertionError:
                self.invalid_percentage += len(self.invalid_pages) * \
                    100 / self.n_pages

    def calculate(self):
        self.update()
        self._calculate_student_pages()
        self._calculate_student_percentage()

    def __repr__(self):
        lst = join_list(self.list, ", ")
        i_per = f"invalid percentage = {self.invalid_percentage}%"
        i_pag = f"{len(self.invalid_pages)} pages:"\
            f" {join_list(sorted(self.invalid_pages), ', ')}"
        return f"{lst}, {i_per}, {i_pag}."

    def __str__(self):
        lst = join_list(self.list)
        i_per = f"Probability to call an uninterrogable student"\
            f" = {self.invalid_percentage}%"
        i_pag = f"{len(self.invalid_pages)} pages:"\
            f" {join_list(sorted(self.invalid_pages), ', ')}"
        return f"{lst}\n\n{i_per}, {i_pag}."


def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s


def join_list(lst, st="\n"):
    return st.join(str(i) for i in lst)
