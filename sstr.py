import re
from typing import SupportsIndex


class sstr(str):
    def __init__(self, string: str) -> None:
        self = string

    def divide(self, enclosure=None, consider_escape: bool = False) -> list[str]:
        if consider_escape == True:
            template = "{0}.*?(?<!\\\\){1}"
        else:
            template = "{0}.*?{1}"
        if type(enclosure) is not list and type(enclosure) is not tuple:
            enclosure = [enclosure]
        enclosure = [e for e in enclosure if e is not None]
        if "" in enclosure:
            raise ValueError("empty enclosure")
        if enclosure == []:
            return [str(self)]
        pattern = ""
        for e in enclosure:
            if type(e) is list or type(e) is tuple:
                pattern += "|" + template.format(re.escape(e[0]), re.escape(e[1]))
            else:
                e = re.escape(e)
                pattern += "|" + template.format(e, e)
        pattern = "(" + pattern.lstrip("|") + ")"
        divided_data = re.split(pattern, self)
        if divided_data[-1] == "" and len(divided_data) > 1:
            divided_data.pop(-1)
        return divided_data

    def divide_and_classify(self, enclosure=None, consider_escape: bool = False) -> tuple[str, bool]:
        divided_data = self.divide(enclosure, consider_escape)
        for data in divided_data:
            yield data, sstr.surroundedby(data, enclosure)

    def endswith_multiple(self, enclosure=None) -> bool:
        template = ".*{0}$"
        if type(enclosure) is not list and type(enclosure) is not tuple:
            enclosure = [enclosure]
        enclosure = [e for e in enclosure if e is not None]
        if "" in enclosure:
            raise ValueError("empty enclosure")
        if enclosure == []:
            return False
        pattern = ""
        for e in enclosure:
            if type(e) is list or type(e) is tuple:
                pattern += "|" + template.format(re.escape(e[1]))
            else:
                pattern += "|" + template.format(re.escape(e))
        pattern = "(" + pattern.lstrip("|") + ")"
        return re.fullmatch(pattern, self) != None

    def get_inner_parts(self, enclosure=None, consider_escape: bool = False) -> list[str]:
        divided_data = self.divide(enclosure, consider_escape)
        for data in divided_data:
            if sstr.surroundedby(data, enclosure) == False:
                divided_data.remove(data)
        return divided_data

    def get_outer_parts(self, enclosure=None, consider_escape: bool = False) -> list[str]:
        divided_data = self.divide(enclosure, consider_escape)
        for data in divided_data:
            if sstr.surroundedby(data, enclosure) == True:
                divided_data.remove(data)
        return divided_data

    def scount(self, *args, enclosure=None, consider_escape: bool = False, **kwargs) -> int:
        divided_data = self.divide(enclosure, consider_escape)
        total_count = 0
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], enclosure) == False:
                total_count += divided_data[i].count(*args, **kwargs)
        return total_count

    def sfind(self, *args, enclosure=None, consider_escape: bool = False, **kwargs) -> int:
        divided_data = self.divide(enclosure, consider_escape)
        checked_length = 0
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], enclosure) == True:
                checked_length += len(divided_data[i])
            else:
                result = divided_data[i].find(*args, **kwargs)
                if result == -1:
                    checked_length += len(divided_data[i])
                else:
                    return checked_length + result
        return -1

    def sindex(self, *args, enclosure=None, consider_escape: bool = False, **kwargs) -> int:
        divided_data = self.divide(enclosure, consider_escape)
        checked_length = 0
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], enclosure) == True:
                checked_length += len(divided_data[i])
            else:
                result = divided_data[i].find(*args, **kwargs)
                if result == -1:
                    checked_length += len(divided_data[i])
                else:
                    return checked_length + result
        raise ValueError("substring not found")

    def slower(self, *args, enclosure=None, consider_escape: bool = False, **kwargs) -> str:
        divided_data = self.divide(enclosure, consider_escape)
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], enclosure) == False:
                divided_data[i] = divided_data[i].lower(*args, **kwargs)
        return "".join(divided_data)

    def sreplace(self, *args, enclosure=None, consider_escape: bool = False, **kwargs) -> str:
        divided_data = self.divide(enclosure, consider_escape)
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], enclosure) == False:
                divided_data[i] = divided_data[i].replace(*args, **kwargs)
        return "".join(divided_data)

    def srfind(self, *args, enclosure=None, consider_escape: bool = False, **kwargs) -> int:
        divided_data = self.divide(enclosure, consider_escape)
        unchecked_length = len(self)
        for i in list(reversed(range(len(divided_data)))):
            unchecked_length -= len(divided_data[i])
            if sstr.surroundedby(divided_data[i], enclosure) == False:
                result = divided_data[i].rfind(*args, **kwargs)
                if result != -1:
                    return unchecked_length + result
        return -1

    def srindex(self, *args, enclosure=None, consider_escape: bool = False, **kwargs) -> int:
        divided_data = self.divide(enclosure, consider_escape)
        unchecked_length = len(self)
        for i in list(reversed(range(len(divided_data)))):
            unchecked_length -= len(divided_data[i])
            if sstr.surroundedby(divided_data[i], enclosure) == False:
                result = divided_data[i].rfind(*args, **kwargs)
                if result != -1:
                    return unchecked_length + result
        raise ValueError("substring not found")

    def srsplit(self, *args, enclosure=None, consider_escape: bool = False, maxsplit: SupportsIndex = -1, **kwargs) -> list[str]:
        divided_data = list(reversed(self.divide(enclosure=enclosure, consider_escape=consider_escape)))
        splitted_data = []
        for i in range(len(divided_data)):
            if maxsplit != -1:
                if len(splitted_data) == maxsplit + 1:
                    splitted_data[-1] = "".join(list(reversed(divided_data[i:]))) + splitted_data[-1]
                    break
            if sstr.surroundedby(divided_data[i], enclosure=enclosure) == True:
                if len(splitted_data) > 0:
                    splitted_data[-1] = divided_data[i] + splitted_data[-1]
                else:
                    splitted_data.append(divided_data[i])
            else:
                if maxsplit == -1:
                    maxsplit_argument = -1
                else:
                    maxsplit_argument = maxsplit + 1 - len(splitted_data)
                partial_splitted_data = list(reversed(divided_data[i].rsplit(maxsplit=maxsplit_argument, *args, **kwargs)))
                if len(splitted_data) > 0:
                    splitted_data[-1] = partial_splitted_data.pop(0) + splitted_data[-1]
                else:
                    if maxsplit != -1:
                        if len(partial_splitted_data) > maxsplit_argument:
                            partial_splitted_data[-2] = partial_splitted_data[-1] + kwargs["enclosure"] + partial_splitted_data[-2]
                            partial_splitted_data.pop(-1)
                splitted_data = list(reversed(partial_splitted_data)) + splitted_data
        return splitted_data

    def ssplit(self, *args, enclosure=None, consider_escape: bool = False, maxsplit: SupportsIndex = -1, **kwargs) -> list[str]:
        divided_data = self.divide(enclosure=enclosure, consider_escape=consider_escape)
        splitted_data = []
        for i in range(len(divided_data)):
            if maxsplit != -1:
                if len(splitted_data) == maxsplit + 1:
                    splitted_data[-1] = splitted_data[-1] + "".join(divided_data[i:])
                    break
            if sstr.surroundedby(divided_data[i], enclosure=enclosure) == True:
                if len(splitted_data) > 0:
                    splitted_data[-1] = splitted_data[-1] + divided_data[i]
                else:
                    splitted_data.append(divided_data[i])
            else:
                if maxsplit == -1:
                    maxsplit_argument = -1
                else:
                    maxsplit_argument = maxsplit + 1 - len(splitted_data)
                partial_splitted_data = divided_data[i].split(maxsplit=maxsplit_argument, *args, **kwargs)
                if len(splitted_data) > 0:
                    splitted_data[-1] = splitted_data[-1] + partial_splitted_data.pop(0)
                else:
                    if maxsplit != -1:
                        if len(partial_splitted_data) > maxsplit_argument:
                            partial_splitted_data[-2] = partial_splitted_data[-2] + kwargs["enclosure"] + partial_splitted_data[-1]
                            partial_splitted_data.pop(-1)
                splitted_data = splitted_data + partial_splitted_data
        return splitted_data

    def sswapcase(self, *args, enclosure=None, consider_escape: bool = False, **kwargs) -> str:
        divided_data = self.divide(enclosure, consider_escape)
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], enclosure) == False:
                divided_data[i] = divided_data[i].swapcase(*args, **kwargs)
        return "".join(divided_data)

    def startswith_multiple(self, enclosure=None) -> bool:
        template = "^{0}.*"
        if type(enclosure) is not list and type(enclosure) is not tuple:
            enclosure = [enclosure]
        enclosure = [e for e in enclosure if e is not None]
        if "" in enclosure:
            raise ValueError("empty enclosure")
        if enclosure == []:
            return False
        pattern = ""
        for e in enclosure:
            if type(e) is list or type(e) is tuple:
                pattern += "|" + template.format(re.escape(e[0]))
            else:
                pattern += "|" + template.format(re.escape(e))
        pattern = "(" + pattern.lstrip("|") + ")"
        return re.fullmatch(pattern, self) != None

    def stitle(self, *args, enclosure=None, consider_escape: bool = False, **kwargs) -> str:
        divided_data = self.divide(enclosure, consider_escape)
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], enclosure) == False:
                divided_data[i] = divided_data[i].title(*args, **kwargs)
        return "".join(divided_data)

    def supper(self, *args, enclosure=None, consider_escape: bool = False, **kwargs) -> str:
        divided_data = self.divide(enclosure, consider_escape)
        for i in range(len(divided_data)):
            if sstr.surroundedby(divided_data[i], enclosure) == False:
                divided_data[i] = divided_data[i].upper(*args, **kwargs)
        return "".join(divided_data)

    def surroundedby(self, enclosure=None) -> bool:
        template = "{0}.*{1}"
        if type(enclosure) is not list and type(enclosure) is not tuple:
            enclosure = [enclosure]
        enclosure = [e for e in enclosure if e is not None]
        if "" in enclosure:
            raise ValueError("empty enclosure")
        if enclosure == []:
            return False
        pattern = ""
        for e in enclosure:
            if type(e) is list or type(e) is tuple:
                pattern += "|" + template.format(re.escape(e[0]), re.escape(e[1]))
            else:
                e = re.escape(e)
                pattern += "|" + template.format(e, e)
        pattern = "(" + pattern.lstrip("|") + ")"
        return re.fullmatch(pattern, self) != None
