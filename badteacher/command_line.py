import teacher


def int_input(prompt, blank=False):
    while True:
        try:
            inp = input(prompt)
            if not (blank and inp == ""):
                inp = abs(int(inp))
                assert inp != 0
            return inp
        except ValueError:
            print("Error: input must be an integer!")
        except AssertionError:
            print("Error: input can't be 0.")


student_list = teacher.StudentList()
student_list.create_students(int_input("Select the number of students: "))
student_list.n_pages = int_input("How many pages are there in the book? ")
inp = int_input(
    "Is there any uninterrogable student? Write its index, otherwise press enter: ", True)
while True:
    if inp == "":
        break
    else:
        try:
            assert student_list.list[int(
                student_list.search_students(index=inp)[0])].interrogable
            student_list.list[int(student_list.search_students(
                index=inp)[0])].interrogable = False
        except AssertionError:
            print("Error: student already absent.")
        except IndexError:
            print("Error: couldn't find this student.")
        inp = int_input("Another one? ", True)
student_list.calculate()
print(student_list)
