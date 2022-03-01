import re


class sstr(str):
    def __init__(self, string: str) -> None:
        self = string

    def divide(self, sep, consider_escape: bool = False) -> list[str]:
        if consider_escape == True:
            template = "{0}.*?(?<!\\\\){1}"
        else:
            template = "{0}.*?{1}"
        if type(sep) is not list and type(sep) is not tuple:
            sep = [sep]
        sep = [s for s in sep if s is not None]
        if "" in sep:
            raise ValueError("empty separator")
        if sep == []:
            return [str(self)]
        pattern = ""
        for s in sep:
            if type(s) is list or type(s) is tuple:
                pattern += "|" + template.format(re.escape(s[0]), re.escape(s[1]))
            else:
                s = re.escape(s)
                pattern += "|" + template.format(s, s)
        pattern = "(" + pattern.lstrip("|") + ")"
        divided_data = re.split(pattern, self)
        if divided_data[-1] == "" and len(divided_data) > 1:
            divided_data.pop(-1)
        return divided_data

    def divide_and_classify(self, sep, consider_escape: bool = False) -> tuple[str, bool]:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        for data in divided_data:
            yield data, sstr.surroundedby(data, sep=sep)

    def endswith_multiple(self, sep) -> bool:
        template = ".*{0}$"
        if type(sep) is not list and type(sep) is not tuple:
            sep = [sep]
        sep = [s for s in sep if s is not None]
        pattern = ""
        for s in sep:
            if type(s) is list or type(s) is tuple:
                pattern += "|" + template.format(re.escape(s[1]))
            else:
                pattern += "|" + template.format(re.escape(s))
        pattern = "(" + pattern.lstrip("|") + ")"
        return re.fullmatch(pattern, self) != None

    def get_inner_parts(self, sep, consider_escape: bool = False) -> list[str]:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        for data in divided_data:
            if sstr.surroundedby(data, sep=sep) == False:
                divided_data.remove(data)
        return divided_data

    def get_outer_parts(self, sep, consider_escape: bool = False) -> list[str]:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        for data in divided_data:
            if sstr.surroundedby(data, sep=sep) == True:
                divided_data.remove(data)
        return divided_data

    def scount(self, sep, *args, consider_escape: bool = False) -> int:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        total_count = 0
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], sep=sep) == False:
                total_count += divided_data[i].count(*args)
        return total_count

    def sfind(self, sep, *args, consider_escape: bool = False) -> int:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        checked_length = 0
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], sep=sep) == False:
                result = divided_data[i].find(*args)
                if result == -1:
                    checked_length += len(divided_data[i])
                else:
                    return checked_length + result
            else:
                checked_length += len(divided_data[i])
        return -1

    def sindex(self, sep, *args, consider_escape: bool = False) -> int:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        checked_length = 0
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], sep=sep) == False:
                result = divided_data[i].find(*args)
                if result == -1:
                    checked_length += len(divided_data[i])
                else:
                    return checked_length + result
            else:
                checked_length += len(divided_data[i])
        raise ValueError("substring not found")

    def slower(self, sep, *args, consider_escape: bool = False) -> str:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], sep=sep) == False:
                divided_data[i] = divided_data[i].lower(*args)
        return "".join(divided_data)

    def sreplace(self, sep, *args, consider_escape: bool = False) -> str:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], sep=sep) == False:
                divided_data[i] = divided_data[i].replace(*args)
        return "".join(divided_data)

    def srfind(self, sep, *args, consider_escape: bool = False) -> int:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        unchecked_length = len(self)
        for i in reversed(range(len(divided_data))):
            unchecked_length -= len(divided_data[i])
            if sstr.surroundedby(divided_data[i], sep=sep) == False:
                result = divided_data[i].rfind(*args)
                if result != -1:
                    return unchecked_length + result
        return -1

    def srindex(self, sep, *args, consider_escape: bool = False) -> int:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        unchecked_length = len(self)
        for i in reversed(range(len(divided_data))):
            unchecked_length -= len(divided_data[i])
            if sstr.surroundedby(divided_data[i], sep=sep) == False:
                result = divided_data[i].rfind(*args)
                if result != -1:
                    return unchecked_length + result
        raise ValueError("substring not found")

    def ssplit(self, _sep, *args, consider_escape: bool = False) -> list[str]:
        divided_data = self.divide(sep=_sep, consider_escape=consider_escape)
        splitted_data = []
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], sep=_sep) == True:
                if len(splitted_data) == 0:
                    splitted_data.append(divided_data[i])
                else:
                    splitted_data[-1] += divided_data[i]
            else:
                partial_splitted_data = divided_data[i].split(*args)
                if len(splitted_data) > 0 and len(partial_splitted_data) > 0:
                    if sstr.endswith_multiple(splitted_data[-1], sep=_sep) == True:
                        splitted_data[-1] += partial_splitted_data.pop(0)
                splitted_data.extend(partial_splitted_data)
        return splitted_data

    def sswapcase(self, sep, *args, consider_escape: bool = False) -> str:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], sep=sep) == False:
                divided_data[i] = divided_data[i].swapcase(*args)
        return "".join(divided_data)

    def startswith_multiple(self, sep) -> bool:
        template = "^{0}.*"
        if type(sep) is not list and type(sep) is not tuple:
            sep = [sep]
        sep = [p for p in sep if p is not None]
        pattern = ""
        for p in sep:
            if type(p) is list or type(p) is tuple:
                pattern += "|" + template.format(re.escape(p[0]))
            else:
                pattern += "|" + template.format(re.escape(p))
        pattern = "(" + pattern.lstrip("|") + ")"
        return re.fullmatch(pattern, self) != None

    def stitle(self, sep, *args, consider_escape: bool = False) -> str:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], sep=sep) == False:
                divided_data[i] = divided_data[i].title(*args)
        return "".join(divided_data)

    def supper(self, sep, *args, consider_escape: bool = False) -> str:
        divided_data = self.divide(sep=sep, consider_escape=consider_escape)
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], sep=sep) == False:
                divided_data[i] = divided_data[i].upper(*args)
        return "".join(divided_data)

    def surroundedby(self, sep) -> bool:
        template = "{0}.*{1}"
        if type(sep) is not list and type(sep) is not tuple:
            sep = [sep]
        sep = [s for s in sep if s is not None]
        if "" in sep:
            raise ValueError("empty separator")
        pattern = ""
        for s in sep:
            if type(s) is list or type(s) is tuple:
                pattern += "|" + template.format(re.escape(s[0]), re.escape(s[1]))
            else:
                s = re.escape(s)
                pattern += "|" + template.format(s, s)
        pattern = "(" + pattern.lstrip("|") + ")"
        return re.fullmatch(pattern, self) != None
