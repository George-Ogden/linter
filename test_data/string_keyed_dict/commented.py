a = {  # noqa: string-keyed-dict
    "A": True,
}

b = {  # noqa
    "B": True,
}

c = {  # random comment
    "C": False,
}

d = {
    "D": False,
}

e = {"e": {"E": True}}  # noqa:string-keyed-dict

f = {  # noqa:string-keyed-dict-fail
    "F": False,
}

g = {
    "G": False,  # noqa
}  # in the wrong place

h = {
    "h": False,  # in the wrong place again
}  # noqa
