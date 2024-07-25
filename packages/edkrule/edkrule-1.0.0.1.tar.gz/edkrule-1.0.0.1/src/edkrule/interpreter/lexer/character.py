class Character:
    @staticmethod
    def iscolon(char: str):
        return char == ":"

    @staticmethod
    def isalpha(char: str):
        return char.isalpha()

    @staticmethod
    def isdigit(char: str):
        return char.isdigit()

    @staticmethod
    def isplus(char: str): return char == "+"

    @staticmethod
    def isminus(char: str): return char == "-"

    @staticmethod
    def isdivide(char: str): return char == "/"

    @staticmethod
    def ismultiply(char: str): return char == "*"

    @staticmethod
    def isgreat(char: str): return char == ">"

    @staticmethod
    def isless(char: str): return char == "<"

    @staticmethod
    def isdollor(char: str): return char == "$"

    @staticmethod
    def isleftparentheses(char: str): return char == "("

    @staticmethod
    def isrightparentheses(char: str): return char == ")"

    @staticmethod
    def isassign(char: str): return char == "="

    @staticmethod
    def isexclamationpoint(char: str): return char == "!"

    @staticmethod
    def ist(char: str): return char == "t"

    @staticmethod
    def isr(char: str): return char == "r"

    @staticmethod
    def isu(char: str): return char == "u"

    @staticmethod
    def ise(char: str): return char == "e"

    @staticmethod
    def isf(char: str): return char == "f"

    @staticmethod
    def isa(char: str): return char == "a"

    @staticmethod
    def isl(char: str): return char == "l"

    @staticmethod
    def iss(char: str): return char == "s"

    @staticmethod
    def ise(char: str): return char == "e"

    @staticmethod
    def isdot(char: str): return char == "."

    @staticmethod
    def iscomma(char: str): return char == ","

    @staticmethod
    def isstar(char: str): return char == "*"

    @staticmethod
    def isblank(char: str): return char.isspace()

    @staticmethod
    def isand(char: str): return char == "&"

    @staticmethod
    def isL(char: str): return char == "|"

    @staticmethod
    def isquestion(char: str): return char == "?"

    @staticmethod
    def isdoublequotation(char): return char == "\""

    @staticmethod
    def issinglequotation(char): return char == "\'"

    @staticmethod
    def isseparators(char):
        return Character.isblank(char) or \
               Character.isrightparentheses(char) or \
               Character.isand(char) or \
               Character.isL(char) or Character.iscomma(char)

    @staticmethod
    def iskeyword(char):
        """
        是否是保留字段的开头
        :param char:
        :type char:
        :return:
        :rtype:
        """
        return Character.ist(char) or Character.isf(char)

    @staticmethod
    def isoperate(char):
        """
        是否是操作符或运算符
        :param char:
        :type char:
        :return:
        :rtype:
        """
        return char in ["+", "-", "*", "/", "%", "&", "|", "=", ">", "<", "!"]
