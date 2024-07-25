import re
import jieba
import langid
import textstat

from typing import List, Tuple
from hanziconv import HanziConv
from nltk.tokenize import WordPunctTokenizer


from dingo.model.model import Model
from dingo.model.rule.util import normalize, base_rps_frac_chars_in_dupe_ngrams, get_stop_words, split_paragraphs, TextSlice
from dingo.model.rule.base import BaseRule, ResModel


@Model.rule_register('QUALITY_SIGNAL_COMPLETENESS', ['default','sft','pretrain','benchmark'])
class CommonColonEnd(BaseRule):
    """check whether the last char is ':'"""

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        if len(input_data[0]) <= 0:
            return res
        if input_data[0][-1] == ':':
            res.error_status = True
            res.error_reason = 'Ends with a colon.'
        return res


@Model.rule_register('QUALITY_SIGNAL_EFFECTIVENESS', ['default','sft','pretrain','benchmark'])
class CommonContentNull(BaseRule):
    """check whether content is null"""

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        count = len(input_data[0].strip())
        if count == 0:
            res.error_status = True
            res.error_reason = 'Content is empty.'
        return res


@Model.rule_register('QUALITY_SIGNAL_SIMILARITY', ['default','sft','pretrain','benchmark'])
class CommonDocRepeat(BaseRule):
    """check whether content repeats"""

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        repeat_score = base_rps_frac_chars_in_dupe_ngrams(6, input_data[0])
        if repeat_score >= 80:
            res.error_status = True
            res.error_reason = 'Repeatability of text is too high, with ratio： ' + str(repeat_score)
        return res


@Model.rule_register('QUALITY_SIGNAL_RELEVANCE', ['default','sft','pretrain','benchmark'])
class CommonHtmlEntity(BaseRule):
    """check whether content has html entity"""

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        entities = [
            "nbsp",
            "lt",
            "gt",
            "amp",
            "quot",
            "apos",
            "hellip",
            "ndash",
            "mdash",
            "lsquo",
            "rsquo",
            "ldquo",
            "rdquo",
        ]
        full_entities_1 = [f"&{entity}；" for entity in entities]
        full_entities_2 = [f"&{entity};" for entity in entities]
        full_entities_3 = [f"＆{entity};" for entity in entities]
        full_entities_4 = [f"＆{entity}；" for entity in entities]
        full_entities = (
                full_entities_1 + full_entities_2 + full_entities_3 + full_entities_4
        )
        # half_entity_1 = [f"{entity}；" for entity in entities]
        half_entity_2 = [f"＆{entity}" for entity in entities]
        half_entity_3 = [f"&{entity}" for entity in entities]
        # half_entity_4 = [f"{entity};" for entity in entities]
        half_entities = half_entity_2 + half_entity_3
        # maked_entities = [f"{entity}" for entity in entities]
        all_entities = full_entities + half_entities

        pattern = '|'.join(all_entities)
        matches = re.findall(pattern, input_data[0])
        if matches:
            res.error_status = True
            res.error_reason = matches
        return res


@Model.rule_register('QUALITY_SIGNAL_SECURITY', ['default','sft','pretrain','benchmark'])
class CommonLicenseKey(BaseRule):
    """check if the content contains license key"""
    pattern = "|".join(
        [
            "[A-Z0-9]{47}",
            "[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}",
            "[A-Z0-9]{4}-\d{8}-[A-Z0-9]{4}",
        ]
    )

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        match = re.search(cls.pattern, input_data[0], re.I)
        if match:
            res.error_status = True
            res.error_reason = "Contain license key."
        return res


@Model.rule_register('QUALITY_SIGNAL_FLUENCY', ['default','sft','pretrain','benchmark'])
class CommonNoPunc(BaseRule):
    """check whether content has paragraph without punctuations"""

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        paragraphs = input_data[0].split('\n')
        max_word_count = 0
        for paragraph in paragraphs:
            if len(paragraph) == 0:
                continue
            sentences = re.split(r'[-–.!?,;•、。！？，；·]', paragraph)
            for sentence in sentences:
                words = sentence.split()
                word_count = len(words)
                if word_count > max_word_count:
                    max_word_count = word_count
        text_stat_res = textstat.flesch_reading_ease(input_data[0])
        if int(max_word_count) > 56 and text_stat_res < 20:
            res.error_status = True
            res.error_reason = 'Paragraph without punctuation.'
        return res


@Model.rule_register('QUALITY_SIGNAL_RELEVANCE', ['default','sft','pretrain','benchmark'])
class CommonSpecialCharacter(BaseRule):
    pattern = r"[�□]|\{\/U\}"

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        matches = re.findall(cls.pattern, input_data[0])
        if matches:
            res.error_status = True
            res.error_reason = matches
        return res


@Model.rule_register("QUALITY_SIGNAL_RELEVANCE", ['zh_all'])
class CommonWatermark(BaseRule):
    """check whether english prompt produce chinese prediction"""
    key_list = []

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        res = ResModel()
        assert len(input_data) == 1
        matches = re.findall('|'.join(cls.key_list), input_data[0])
        if matches:
            res.error_status = True
            res.error_reason = matches
        return res


@Model.rule_register("QUALITY_SIGNAL_COMPLETENESS", ['en_all','pretrain'])
class CommonWordNumber(BaseRule):
    """check whether the number of word in [50, 100000] """

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        normalized_content = normalize(input_data[0])
        normalized_words = tuple(normalized_content.split())
        num_normalized_words = len(normalized_words)
        if num_normalized_words >= 50 and num_normalized_words < 100000:
            pass
        else:
            res.error_status = True
            res.error_reason = "The number of word is: " + str(num_normalized_words)
        return res


@Model.rule_register('QUALITY_SIGNAL_EFFECTIVENESS', ['en_all','pretrain'])
class CommonMeanWordLength(BaseRule):
    """check whether the mean length of word in [3, 10] """

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        normalized_content = normalize(input_data[0])
        normalized_words = tuple(normalized_content.split())
        num_normalized_words = len(normalized_words)
        if num_normalized_words == 0:
            return res

        num_chars = float(sum(map(len, normalized_words)))
        mean_length = num_chars / num_normalized_words
        mean_length = round(mean_length, 2)
        if mean_length >= 3 and mean_length < 10:
            pass
        else:
            res.error_status = True
            res.error_reason = "The mean length of word is: " + str(mean_length)
        return res


@Model.rule_register('QUALITY_SIGNAL_EFFECTIVENESS', ['en_all','sft','pretrain','benchmark'])
class CommonSymbolWordRatio(BaseRule):
    """check whether the ratio of symbol / word is > 0.1"""
    key_list = ["#", "...", "…"]

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        raw_content = input_data[0]
        raw_words = tuple(WordPunctTokenizer().tokenize(raw_content))
        num_raw_words = len(raw_words)
        if num_raw_words == 0:
            return res

        num_words = num_raw_words
        num_symbols = float(sum(
            raw_content.count(x) for x in cls.key_list
        ))

        ratio = num_symbols / num_words
        if ratio > 0.4:
            res.error_status = True
            res.error_reason = "The ratio of symbol / word is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_SIGNAL_EFFECTIVENESS", ['en_all','pretrain'])
class CommonAlphWords(BaseRule):
    """check whether the ratio of words that contain at least one alphabetic character > 0.8 """

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        raw_content = input_data[0]
        raw_words = tuple(WordPunctTokenizer().tokenize(raw_content))
        num_raw_words = len(raw_words)
        if num_raw_words == 0:
            return res

        ALPH_REGEX = re.compile(r"[a-zA-Z]")
        num_words = num_raw_words
        num_words_with_alpha = float(sum(
            int(ALPH_REGEX.search(word) is not None)
            for word in raw_words
        ))
        ratio = num_words_with_alpha / num_words
        if ratio > 0.8:
            pass
        else:
            res.error_status = True
            res.error_reason = "The ratio of words that contain at least one alphabetic character is: " + str(ratio)
        return res


@Model.rule_register('QUALITY_SIGNAL_EFFECTIVENESS', ['pretrain'])
class CommonStopWord(BaseRule):
    """check whether the ratio of stop word > 2"""

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        raw_content = input_data[0]
        raw_words = tuple(WordPunctTokenizer().tokenize(raw_content))
        num_raw_words = len(raw_words)
        if num_raw_words == 0:
            return res

        STOP_WORDS = get_stop_words("en")
        num_stop_words = sum(
            map(lambda w: w in STOP_WORDS, raw_words)
        )
        ratio = num_stop_words / num_raw_words
        if ratio > 0.4:
            res.error_status = True
            res.error_reason = "The ratio of stop words is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_SIGNAL_COMPLETENESS", ['pretrain'])
class CommonSentenceNumber(BaseRule):
    """check whether the number of sentence > 3 """

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        raw_content = input_data[0]

        SENT_PATTERN = re.compile(r'\b[^.!?]+[.!?]*', flags=re.UNICODE)
        num_sentence = len(SENT_PATTERN.findall(raw_content))
        if num_sentence <= 3:
            res.error_status = True
            res.error_reason = "The number of sentence is: " + str(num_sentence)
        return res


@Model.rule_register("QUALITY_SIGNAL_UNDERSTANDABILITY", [])
class CommonCurlyBracket(BaseRule):
    """check whether content contains curly bracket: { or } """
    pattern = "[{}]"

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        matches = re.findall(cls.pattern, input_data[0])
        if matches:
            res.error_status = True
            res.error_reason = matches
        return res


@Model.rule_register("QUALITY_SIGNAL_UNDERSTANDABILITY", ['pretrain'])
class CommonCapitalWords(BaseRule):
    """check whether capital words ratio > 0.1 """

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        raw_content = input_data[0]
        raw_words = tuple(WordPunctTokenizer().tokenize(raw_content))
        num_raw_words = len(raw_words)
        if num_raw_words == 0:
            return res

        num_words = num_raw_words
        num_capital_words = sum([word.isupper() for word in raw_words])
        print(num_capital_words)
        ratio = num_capital_words / num_words
        if ratio > 0.1:
            res.error_status = True
            res.error_reason = "The ratio of capital words is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_SIGNAL_EFFECTIVENESS", ['sft','pretrain','benchmark'])
class CommonLoremIpsum(BaseRule):
    """check whether the ratio of lorem ipsum < 3e-08 """

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        normalized_content = normalize(input_data[0])
        num_normalized_content = len(normalized_content)
        if num_normalized_content == 0:
            return res

        SEARCH_REGEX = re.compile(r"lorem ipsum", re.IGNORECASE)
        num_occurrences = len(SEARCH_REGEX.findall(normalized_content))
        ratio = num_occurrences / num_normalized_content
        if ratio > 3e-08:
            res.error_status = True
            res.error_reason = "The ratio of lorem ipsum is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_SIGNAL_UNDERSTANDABILITY", ['pretrain'])
class CommonUniqueWords(BaseRule):
    """check whether the ratio of unique words > 0.1"""

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        normalized_content = normalize(input_data[0])
        normalized_words = tuple(normalized_content.split())
        num_normalized_words = len(normalized_words)
        if num_normalized_words == 0:
            return res

        num_words = num_normalized_words
        num_unique_words = len(set(normalized_words))
        ratio = num_unique_words / num_words
        if ratio > 0.1:
            pass
        else:
            res.error_status = True
            res.error_reason = "The ratio of unique words is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_SIGNAL_EFFECTIVENESS", ['pretrain'])
class CommonCharNumber(BaseRule):
    """check whether the number of char > 200 """
    threshold = 200

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        text = input_data[0]
        text = text.strip()
        text = text.replace(" ", "")
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        num_char = len(text)
        if num_char < cls.threshold:
            res.error_status = True
            res.error_reason = "The number of char is: " + str(num_char)
        return res


@Model.rule_register("QUALITY_SIGNAL_UNDERSTANDABILITY", ['sft','pretrain','benchmark'])
class CommonLineStartWithBulletpoint(BaseRule):
    """check whether lines start with bulletpoint. """
    key_list = [
        "\u2022",  # bullet point
        "\u2023",  # triangular bullet point
        "\u25B6",  # black right pointing triangle
        "\u25C0",  # black left pointing triangle
        "\u25E6",  # white bullet point
        "\u25A0",  # black square
        "\u25A1",  # white square
        "\u25AA",  # black small square
        "\u25AB",  # white small square
        "\u2013",  # en dash
    ]

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        raw_content = input_data[0]
        raw_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=lambda x: x, remove_empty=True
        )
        num_lines = len(raw_lines)
        if num_lines == 0:
            return res

        num_occurrences = sum([line.text.lstrip().startswith(tuple(cls.key_list)) for line in raw_lines])
        ratio = num_occurrences / num_lines
        if ratio > 0.9:
            res.error_status = True
            res.error_reason = "The ratio of lines start with bulletpoint is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_SIGNAL_COMPLETENESS", ['sft','pretrain','benchmark'])
class CommonLineEndWithEllipsis(BaseRule):
    """check whether lines end with ellipsis. """
    key_list = ["...", "…"]

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        raw_content = input_data[0]
        raw_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=lambda x: x, remove_empty=True
        )
        num_lines = len(raw_lines)
        if num_lines == 0:
            return res

        num_occurrences = sum([line.text.rstrip().endswith(tuple(cls.key_list)) for line in raw_lines])
        ratio = num_occurrences / num_lines
        if ratio > 0.3:
            res.error_status = True
            res.error_reason = "The ratio of lines end with ellipsis is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_SIGNAL_COMPLETENESS", ['pretrain'])
class CommonLineEndWithTerminal(BaseRule):
    """check whether lines end with terminal punctuation mark. """
    key_list = [".", "!", "?", "”", "\""]

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        raw_content = input_data[0]
        raw_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=lambda x: x, remove_empty=True
        )
        num_lines = len(raw_lines)
        if num_lines == 0:
            return res

        num_occurrences = sum([line.text.rstrip().endswith(tuple(cls.key_list)) for line in raw_lines])
        ratio = num_occurrences / num_lines
        if ratio < 0.6:
            res.error_status = True
            res.error_reason = "The ratio of lines end with terminal punctuation mark is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_SIGNAL_EFFECTIVENESS", ['sft','pretrain','benchmark'])
class CommonLineWithJavascript(BaseRule):
    """check whether line with the word Javascript. """

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        assert len(input_data) == 1
        res = ResModel()
        raw_content = input_data[0]
        normalized_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=normalize, remove_empty=True
        )
        num_lines = len(normalized_lines)
        if num_lines == 0:
            return res

        num_occurrences = sum(['javascript' in line.text for line in normalized_lines])
        num_not_occur = num_lines - num_occurrences
        if num_not_occur < 3 and num_lines > 3:
            res.error_status = True
            res.error_reason = "The lines with the word Javascript is: " + str(num_occurrences)
        return res


if __name__ == '__main__':
    content = "DNA stands for deoxyribonucleic acid."
    tmp = CommonCapitalWords().eval([content])
    print(tmp)