import base64
import codecs
import logging
import random

import tiktoken
from cryptography.fernet import Fernet

from prompt_hacker import constant
from prompt_hacker.generator import CombinationBase64Decoder, DisemvowelDecoder
from prompt_hacker.interface import StringConverter


class Base64Convertor:
    def encode(self, plain_txt: str) -> str:
        return base64.b64encode(plain_txt.encode("UTF-8")).decode("utf-8")

    def decode(self, encoded: str) -> str:
        return base64.b64decode(encoded.encode("ascii")).decode("UTF-8")

    def advanced_decode(self, encoded: str) -> str:
        return CombinationBase64Decoder().decode(encoded)


class Obfuscationer:
    def __init__(self, method: str) -> None:
        self.method = method
        match method:
            case "leetspeak":
                obfuscater: StringConverter = LeetSpeakConverter()
            case "rot13":
                obfuscater = Rot13Converter()
            case "disemvowel":
                obfuscater = DisemvowelConverter()
            case "hex":
                obfuscater = HexConverter()
            case _:
                raise ValueError(
                    "invalid method, choose between {'leetspeak', 'rot13', 'disemvowel'}",
                )
        self.obfuscater = obfuscater

    def models(self) -> list[str]:
        return ["leetspeak", "rot13", "disemvowel", "hex"]

    def encode(self, string: str) -> str:
        return self.obfuscater.encode(string)

    def decode(self, encoded: str) -> str:
        return self.obfuscater.decode(encoded)


class DisemvowelConverter(StringConverter):
    def encode(self, string: str) -> str:
        for r in "aeiouAEIOU":
            string = string.replace(r, "")
        return string

    def decode(self, string: str) -> str:
        logging.warning(
            "Originally, decoding of disemvowel is not possible. Accordingly, decoding will proceed with prediction through LLM.",
        )
        return DisemvowelDecoder().decode(string)


class Rot13Converter(StringConverter):
    def encode(self, string: str) -> str:
        return codecs.encode(string, "rot_13")

    def decode(self, encoded: str) -> str:
        return codecs.decode(encoded, "rot_13")


class LeetSpeakConverter(StringConverter):
    def __init__(self, random_seed: int = 1337, encode_ratio: float = 1.0) -> None:
        random.seed(random_seed)
        self.encode_ratio = encode_ratio
        self.char_map: dict[str, list[str]] = {
            "a": ["4", "@", "/-\\", "^"],
            "b": ["I3", "8", "13", "|3"],
            "c": ["[", "{", "<", "("],
            "d": [")", "|)", "[)", "|>"],
            "e": ["3", "[-"],
            "f": ["|=", "ph", "|#", "/="],
            "g": ["&", "6", "(_+]", "9", "C-", "gee"],
            "h": ["#", "/-/", "[-]", "]-[", ")-(", "(-)", ":-:", "|-|", "}{"],
            "i": ["1", "[]", "!", "|", "eye", "3y3", "]["],
            "j": [",_|", "_|", "._|", "._]", ",_]", "]"],
            "k": [">|", "|<", "/<", "1<", "|c", "|(", "|{"],
            "l": ["1", "7", "|_", "|"],
            "m": ["/\\/\\", "/V\\", "JVI", "[V]", "[]V[]", "|\\/|", "^^"],
            "n": ["^/", "|\\|", "/\\/", r"[\]", "<\\>", "{\\}", "|V", "/V"],
            "o": ["0", "Q", "()", "oh", "[]"],
            "p": ["|*", "|o", "?", "|^", "[]D"],
            "q": ["(_,)", "()_", "2", "O_"],
            "r": ["12", "|`", "|~", "|?", "/2", "|^", "Iz", "|9"],
            "s": ["$", "5", "z", "ehs", "es"],
            "t": ["7", "+", "-|-", "']['", '"|"', "~|~"],
            "u": ["|_|", "(_)", "V", "L|"],
            "v": ["\\/", "|/", "\\|"],
            "w": ["\\/\\/", "VV", "\\N", "'//", "\\\\'", "\\^/", "\\X/"],
            "x": ["><", ">|<", "}{", "ecks"],
            "y": ["j", "`/", "\\|/", "\\//"],
            "z": ["2", "7_", "-/_", "%", ">_", "~/_", r"-\_", "-|_"],
        }
        self.encoder = {
            alphabet: random.choice(candidates)
            for alphabet, candidates in self.char_map.items()
        }

        decoder = {v: k for k, v in self.encoder.items()}
        self.sorted_decoder = dict(
            sorted(decoder.items(), key=lambda x: len(x[0]), reverse=True),
        )

    def encode(self, string: str) -> str:
        encoded = ""
        for char in string:
            if char.lower() in self.char_map and random.random() <= self.encode_ratio:
                leet_replacement = self.encoder[char.lower()]
                encoded += leet_replacement
            else:
                encoded += char
        return encoded

    def decode(self, encoded: str, decoded: str = "") -> str:
        reduced = False
        for code, char in self.sorted_decoder.items():
            if encoded.startswith(code):
                decoded += char
                encoded = encoded[len(code) :]
                reduced = True
                break
        if not reduced:
            decoded += encoded[0]
            encoded = encoded[1:]

        if len(encoded):
            return self.decode(encoded, decoded)
        else:
            return decoded


class FermetConverter(StringConverter):
    def __init__(self) -> None:
        super().__init__()
        self.cipher_suite = Fernet(constant.FERMET_KEY)

    def encode(self, string: str) -> str:
        return self.cipher_suite.encrypt(string.encode("utf-8")).decode("utf-8")

    def decode(self, encoded: str) -> str:
        return self.cipher_suite.decrypt(encoded.encode("utf-8")).decode("utf-8")


class TikTokenTrucator:
    def __init__(self, max_length):
        self.max_length = max_length
        self.enc = tiktoken.encoding_for_model(constant.MODEL_NM)

    def truncate(self, text):
        return self.enc.decode(self.enc.encode(text)[: self.max_length])
        return self.enc.decode(self.enc.encode(text)[: self.max_length])


class HexConverter:
    def encode(self, txt):
        return txt.encode().hex()

    def decode(self, txt):
        return bytes.fromhex(txt).decode("utf-8")
