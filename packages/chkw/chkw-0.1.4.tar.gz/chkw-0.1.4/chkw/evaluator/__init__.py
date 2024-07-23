from tokenizer import Token


class Evaluator:
    def __init__(self, tokenes: list[str]):
        self.tokenes = tokenes
        self.memory = [0 for n in range(100000)]
        self.p = 0
        self.now_token_position = 0
        self.corresponding_params = []

    def eval(self):
        self.set_corresponding_params()
        while True:

            if self.now_token_position >= len(self.tokenes):
                break
            t = self.tokenes[self.now_token_position]
            if t == Token.PLUS:
                self.memory[self.p] += 1
                self.now_token_position +=1
                continue
            if t == Token.MINUS:
                self.memory[self.p] -= 1
                self.now_token_position +=1
                continue
            if t == Token.LEFT:
                self.p -= 1
                self.now_token_position += 1
                continue
            if t == Token.RIGHT:
                self.p += 1
                self.now_token_position += 1
                continue
            if t == Token.LEFT_PARAM:

                if self.memory[self.p] == 0:
                    for cp in self.corresponding_params:
                        if cp[0] == self.now_token_position:
                            self.now_token_position = cp[1]
                            break
                else:
                    self.now_token_position+=1
                continue
            if t == Token.RIGHT_PARAM:
                if self.memory[self.p] == 0:
                    self.now_token_position+=1
                else:
                    for cp in self.corresponding_params:
                        if cp[1] == self.now_token_position:
                            self.now_token_position = cp[0]
                            break
                continue
            if t == Token.DOT:
                print(chr(self.memory[self.p]), end="")
                self.now_token_position += 1
                continue




    def set_corresponding_params(self):
        for i, t in enumerate(self.tokenes):
            if t == Token.LEFT_PARAM:
                self.get_position_corresponding_param(i)




    def get_position_corresponding_param(self, pos):
        left_param_pos = pos
        depth = 0
        while pos:
            if pos >= len(self.tokenes) :
                return -1
            t = self.tokenes[pos]
            if t == Token.LEFT_PARAM:
                depth += 1
            if t == Token.RIGHT_PARAM:
                depth -= 1
                if depth == 0:
                    self.corresponding_params.append((left_param_pos, pos))
                    return pos
            pos += 1
