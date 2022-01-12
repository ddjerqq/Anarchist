class A:
    def __init__(self, *args) -> None:
        print("init a")

class B(A):
    def __init__(self, *args) -> None:
        super().__init__(self, *args)
        print("init b")

a = A("a parameter")

b = B("b parameter")

