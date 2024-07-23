class TransCompiler:
    def __init__(self, code :str):
        self.code = code
        self.map = {
            "+": "ヤハッ",
            "-": "アァ...",
            ".": "ッテコト..?",
            "<" : "ウワァ..." ,
            ">" : "ヒャハー...!",
            "[" : "ウゥ...",
            "]" : "泣いちゃった..!",
            "," :"なんだもう朝かと",
        }

    def compile(self):
        result = ""
        for c in self.code:
            result += self.map[c]

        return result
