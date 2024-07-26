# RATCHADA_UTILS: EVALUATOR PACKAGE
#
# COPYRIGHT (C) 2024 RATCHADA UTILS PROJECT
# AUTHOR:   TM-BEST-CHOKULKET
#           TM-ZOON-PATCHARAWIWATPONG
# URL: <https://thinkingmachin.es/>
# LICENSE: see LICENSE for futher info

"""
RATCHADA EVALUATOR PACKAGE:
Text evaluation metrics for Thai and English languages.

This module provides functions to calculate Word Error Rate (WER) and
Character Error Rate (CER) for Thai and English text.

evaluate: perform simple evaluation measured between prediction and actual results
isd: similar to evaluate, but give more concise information on each prediction and actuals with Status tagged
    isd: Insertion-Substitution-Deletetion
"""

from .evaluate_utils import evaluate, isd, simple_evaluator
