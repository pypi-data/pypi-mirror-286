import pyrs


def show(txt: str) -> None:
    pyrs.show(txt)


def par_counter(txt: str) -> dict[str, int]:
    return pyrs.par_counter(txt)


def counter(txt: str) -> dict[str, int]:
    return pyrs.counter(txt)