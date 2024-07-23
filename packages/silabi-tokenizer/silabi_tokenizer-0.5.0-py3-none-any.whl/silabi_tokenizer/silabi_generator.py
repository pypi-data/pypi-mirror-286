import json


class SilabiVocabGenerator:
    """
    Tokenizes text on kiswahili syllables
    """

    silabis = [
        "mbwa",
        "mbwe",
        "mbwi",
        "ndwa",
        "ndwe",
        "ndwi",
        "ngwa",
        "ngwe",
        "ngwi",
        "njwa",
        "njwe",
        "njwi",
        "nywa",
        "nywe",
        "shwa",
        "shwe",
        "shwi",
        "chwa",
        "chwe",
        "chwi",
        "pwa",
        "pwe",
        "pwi",
        "pwo",
        "swa",
        "swe",
        "swi",
        "twa",
        "twe",
        "twi",
        "zwa",
        "zwe",
        "zwi",
        "cha",
        "che",
        "chi",
        "cho",
        "chu",
        "dha",
        "dhe",
        "dhi",
        "dho",
        "dhu",
        "gha",
        "ghe",
        "ghi",
        "gho",
        "ghu",
        "kha",
        "khe",
        "kho",
        "khu",
        "mba",
        "mbe",
        "mbi",
        "mbo",
        "mbu",
        "nda",
        "nde",
        "ndi",
        "ndo",
        "ndu",
        "nga",
        "nge",
        "ngi",
        "ngo",
        "ngu",
        "ng’a",
        "ng’e",
        "ng’o",
        "nja",
        "nje",
        "nji",
        "njo",
        "nju",
        "nya",
        "nye",
        "nyi",
        "nyo",
        "nyu",
        "sha",
        "she",
        "shi",
        "sho",
        "shu",
        "tha",
        "the",
        "thi",
        "tho",
        "thu",
        "vya",
        "vye",
        "vyo",
        "bwa",
        "bwe",
        "bwi",
        "gwa",
        "gwe",
        "gwi",
        "jwa",
        "jwe",
        "jwi",
        "kwa",
        "kwe",
        "kwi",
        "lwa",
        "lwe",
        "lwi",
        "mwa",
        "mwe",
        "mwi",
        "nza",
        "nze",
        "nzi",
        "nzo",
        "nzu",
        "ba",
        "be",
        "bi",
        "bo",
        "bu",
        "da",
        "de",
        "di",
        "do",
        "du",
        "fa",
        "fe",
        "fi",
        "fo",
        "fu",
        "ga",
        "ge",
        "gi",
        "go",
        "gu",
        "ha",
        "he",
        "hi",
        "ho",
        "hu",
        "ja",
        "je",
        "ji",
        "jo",
        "ju",
        "ka",
        "ke",
        "ki",
        "ko",
        "ku",
        "la",
        "le",
        "li",
        "lo",
        "lu",
        "ma",
        "me",
        "mi",
        "mo",
        "mu",
        "na",
        "ne",
        "ni",
        "no",
        "nu",
        "pa",
        "pe",
        "pi",
        "po",
        "pu",
        "ra",
        "re",
        "ri",
        "ro",
        "ru",
        "sa",
        "se",
        "si",
        "so",
        "su",
        "ta",
        "te",
        "ti",
        "to",
        "va",
        "ve",
        "vi",
        "vo",
        "vu",
        "wa",
        "we",
        "wi",
        "wo",
        "wu",
        "ya",
        "ye",
        "yi",
        "yo",
        "yu",
        "vu",
        "za",
        "ze",
        "zi",
        "zo",
        "zu",
        "a",
        "e",
        "i",
        "o",
        "u",
    ]

    def __init__(self, vocab_prefix="swahili") -> None:
        self.vocab_prefix = vocab_prefix
        self.lookup = {}

    def generate_silabi_lookup(self):
        """
        Populates the lookup table with unknown,bos,eos,pad tokens
        Adds the utf-8 bytes to the lookup table
        Adds the silabis with capital letter, whitespace permutations
        """
        # add special tokens
        self.lookup["<unk>"] = 0
        self.lookup["<s>"] = 1
        self.lookup["<s/>"] = 2
        self.lookup["<pad>"] = 3

        # add utf-8 byte fallback tokens
        special_tokens_length = len(self.lookup)
        byte_values = list(range(256))
        for index, value in enumerate(byte_values):
            self.lookup[f"<0x{value:02x}>"] = index + special_tokens_length

        # add silabis and their permutation to the lookup
        counter = len(self.lookup)
        index = 0
        while index < len(self.silabis):
            silabi = self.silabis[index]
            capital_silabi = silabi.capitalize()
            whitespace_silabi = f"_{silabi}"
            whitespace_silabi_capital = f"_{capital_silabi}"

            permutations = [
                silabi,
                capital_silabi,
                whitespace_silabi,
                whitespace_silabi_capital,
            ]
            for permutation in permutations:
                self.lookup[permutation] = counter + 1
                counter += 1

            index += 1

        return self.lookup

    def write_to_file(self, file_path="swahili_vocab.json"):
        with open(file_path, "w") as f:
            json.dump(self.lookup, f, indent=4, ensure_ascii=False)


