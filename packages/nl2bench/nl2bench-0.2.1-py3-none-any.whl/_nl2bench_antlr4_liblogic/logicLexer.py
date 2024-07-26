# Generated from logic.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\t")
        buf.write("\'\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\6")
        buf.write("\7\35\n\7\r\7\16\7\36\3\b\6\b\"\n\b\r\b\16\b#\3\b\3\b")
        buf.write("\2\2\t\3\3\5\4\7\5\t\6\13\7\r\b\17\t\3\2\4\5\2\62;C\\")
        buf.write("c|\5\2\13\f\17\17\"\"\2(\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3")
        buf.write("\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2")
        buf.write("\2\3\21\3\2\2\2\5\23\3\2\2\2\7\25\3\2\2\2\t\27\3\2\2\2")
        buf.write("\13\31\3\2\2\2\r\34\3\2\2\2\17!\3\2\2\2\21\22\7*\2\2\22")
        buf.write("\4\3\2\2\2\23\24\7+\2\2\24\6\3\2\2\2\25\26\7-\2\2\26\b")
        buf.write("\3\2\2\2\27\30\7`\2\2\30\n\3\2\2\2\31\32\7#\2\2\32\f\3")
        buf.write("\2\2\2\33\35\t\2\2\2\34\33\3\2\2\2\35\36\3\2\2\2\36\34")
        buf.write("\3\2\2\2\36\37\3\2\2\2\37\16\3\2\2\2 \"\t\3\2\2! \3\2")
        buf.write("\2\2\"#\3\2\2\2#!\3\2\2\2#$\3\2\2\2$%\3\2\2\2%&\b\b\2")
        buf.write("\2&\20\3\2\2\2\5\2\36#\3\b\2\2")
        return buf.getvalue()


class logicLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    LPAREN = 1
    RPAREN = 2
    OR = 3
    XOR = 4
    NOT = 5
    INPUT = 6
    WHITESPACE = 7

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'+'", "'^'", "'!'" ]

    symbolicNames = [ "<INVALID>",
            "LPAREN", "RPAREN", "OR", "XOR", "NOT", "INPUT", "WHITESPACE" ]

    ruleNames = [ "LPAREN", "RPAREN", "OR", "XOR", "NOT", "INPUT", "WHITESPACE" ]

    grammarFileName = "logic.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


