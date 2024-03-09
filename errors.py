class ParsingError(Exception):
    def __init__(self, msg):
        self.msg = msg


class CompileError(Exception):
    def __init__(self, msg):
        self.msg = msg
