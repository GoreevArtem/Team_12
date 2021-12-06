def all_eq(lst: list) -> list:
    max_len = max([len(i) for i in lst])
    return [i + "_"*(max_len - len(i)) for i in lst]

ls = ["a", 'aa', 'bbb', 'cc', 'eeeeee']
print(f"initial list \n {ls}", f"final list \n {all_eq(ls)}", sep="\n")
