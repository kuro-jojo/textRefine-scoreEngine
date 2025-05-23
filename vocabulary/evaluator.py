from typing import Set
from spacy.language import Language
from vocabulary.models import VocabularyResult
from vocabulary.sophistication_checker import SophisticationChecker
from vocabulary.precision_checker import PrecisionChecker
from vocabulary.diversity_calculator import LexicalDiversityCalculator
from vocabulary.constants import (
    LEXICAL_DIVERSITY_WEIGHT,
    SOPHISTICATION_WEIGHT,
    PRECISION_WEIGHT,
)


class VocabularyEvaluator:
    """
    Evaluates the vocabulary quality of a given text based on:
    - Lexical Diversity (TTR)
    - Word Sophistication (word frequency distribution)
    - Word Precision (usage and stylistic issues)
    """

    def __init__(self, nlp: Language, lang: str = "en-US"):
        # Initialize all the necessary checkers for each component
        self.lexical_diversity_checker = LexicalDiversityCalculator(nlp=nlp)
        self.sophistication_checker = SophisticationChecker(nlp=nlp)
        self.precision_checker = PrecisionChecker(nlp=nlp, lang=lang)

    def evaluate(
        self, text: str, replacement_words: Set[tuple[str, str]] = set()
    ) -> VocabularyResult:
        """
        Perform vocabulary evaluation on the given text, aggregating scores from
        lexical diversity, word sophistication, and precision.

        Args:
            text: Input text to analyze.
            replacement_words: Set of replacement words to include in the sophistication check.

        Returns:
            VocabularyResult: Combined result of all three components.
        """
        # Step 1: Compute Lexical Diversity (TTR)
        lexical_diversity_score = self.lexical_diversity_checker.compute(text)

        # Step 2: Compute Word Sophistication
        sophistication_result = self.sophistication_checker.evaluate(
            text, replacement_words
        )

        # Step 3: Compute Word Precision
        precision_result = self.precision_checker.evaluate(text)

        # Combining all three component scores
        combined_score = (
            lexical_diversity_score.ttr * LEXICAL_DIVERSITY_WEIGHT
            + sophistication_result.score * SOPHISTICATION_WEIGHT
            + precision_result.score * PRECISION_WEIGHT
        )

        # Return the aggregated result
        return VocabularyResult(
            score=round(combined_score, 3),
            sophistication=sophistication_result,
            precision=precision_result,
            lexical_diversity=lexical_diversity_score,
        )
