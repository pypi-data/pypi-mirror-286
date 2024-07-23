from transcompiler import TransCompiler


class Token:
    PLUS = "+"
    MINUS = "-"
    DOT = "."
    KAMMA = ","
    LEFT = "<"
    RIGHT = ">"
    LEFT_PARAM = "["
    RIGHT_PARAM = "]"


class Tokenizer:

    def __init__(self, code :str):
        self.tc_map = TransCompiler(code).map
        self.code = code
        self.map = {
            self.tc_map["+"] : Token.PLUS,
            self.tc_map["."] : Token.DOT,
            self.tc_map["<"] : Token.LEFT,
            self.tc_map[">"] : Token.RIGHT,
            self.tc_map["["] : Token.LEFT_PARAM,
            self.tc_map["]"] : Token.RIGHT_PARAM,
            self.tc_map[","] : Token.KAMMA,
            self.tc_map["-"] : Token.MINUS,
        }


    def tokenize(self) -> list[str]:
        tokenes : list[str] = []
        tmp = ""
        for c in self.code:
            tmp += c
            if tmp in self.tc_map.values():
                tokenes.append(self.map[tmp])
                tmp = ""
        return tokenes