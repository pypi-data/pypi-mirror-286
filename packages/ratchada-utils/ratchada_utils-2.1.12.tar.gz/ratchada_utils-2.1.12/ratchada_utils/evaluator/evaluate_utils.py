import deepcut
import jiwer
import pandas as pd
from tqdm import tqdm

from ..processor import EnglishTextNormalizer


def alignedPrint(steps: list, preds: list[str], actuals: list[str], score: float):
    """
    Print the result of comparing reference and hypothesis sentences in an aligned way.

    Args:
        steps (List[str]): The list of steps.
        preds (List[str]): The list of words produced by splitting the hypothesis sentence.
        actuals (List[str]): The list of words produced by splitting the reference sentence.
        score (float): The rate calculated based on edit distance.
    """
    print("REF:", end=" ")
    for i in range(len(steps)):
        if steps[i] == "i":
            count = 0
            for j in range(i):
                if steps[j] == "d":
                    count += 1
            index = i - count
            print(" " * (len(preds[index])), end=" ")
        elif steps[i] == "s":
            count1 = 0
            for j in range(i):
                if steps[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if steps[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(actuals[index1]) < len(preds[index2]):
                print(
                    actuals[index1] + " " * (len(preds[index2]) - len(actuals[index1])),
                    end=" ",
                )
            else:
                print(actuals[index1], end=" "),
        else:
            count = 0
            for j in range(i):
                if steps[j] == "i":
                    count += 1
            index = i - count
            print(actuals[index], end=" "),
    print("\nHYP:", end=" ")
    for i in range(len(steps)):
        if steps[i] == "d":
            count = 0
            for j in range(i):
                if steps[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(actuals[index])), end=" ")
        elif steps[i] == "s":
            count1 = 0
            for j in range(i):
                if steps[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if steps[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(actuals[index1]) > len(preds[index2]):
                print(
                    preds[index2] + " " * (len(actuals[index1]) - len(preds[index2])),
                    end=" ",
                )
            else:
                print(preds[index2], end=" ")
        else:
            count = 0
            for j in range(i):
                if steps[j] == "d":
                    count += 1
            index = i - count
            print(preds[index], end=" ")
    print("\nEVA:", end=" ")
    for i in range(len(steps)):
        if steps[i] == "d":
            count = 0
            for j in range(i):
                if steps[j] == "i":
                    count += 1
            index = i - count
            print("D" + " " * (len(actuals[index]) - 1), end=" ")
        elif steps[i] == "i":
            count = 0
            for j in range(i):
                if steps[j] == "d":
                    count += 1
            index = i - count
            print("I" + " " * (len(preds[index]) - 1), end=" ")
        elif steps[i] == "s":
            count1 = 0
            for j in range(i):
                if steps[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if steps[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(actuals[index1]) > len(preds[index2]):
                print("S" + " " * (len(actuals[index1]) - 1), end=" ")
            else:
                print("S" + " " * (len(preds[index2]) - 1), end=" ")
        else:
            count = 0
            for j in range(i):
                if steps[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(actuals[index])), end=" ")
    print(f"\nWER: {score}")


def get_step(preds: list[str], actuals: list[str], dp: list[list]) -> dict:
    """
    Get the list of steps in the process of dynamic programming.

    Args:
        preds (List[str]): The list of words produced by splitting the hypothesis sentence.
        actuals (List[str]): The list of words produced by splitting the reference sentence.
        dp (List[List[int]]): The matrix built when calculating the editing distance of preds and actuals.

    Returns:
        Dict[str, any]: A dictionary containing steps and error statistics.
    """
    x = len(preds)
    y = len(actuals)
    steps = []
    insertions, substitutions, deletions = 0, 0, 0
    inserted_words, deleted_words, substituted_words = [], [], []

    with tqdm(total=x + y, desc="Processing steps", unit="step") as pbar:
        while x > 0 or y > 0:
            if (
                x >= 1
                and y >= 1
                and dp[y][x] == dp[y - 1][x - 1]
                and actuals[y - 1] == preds[x - 1]
            ):
                steps.append("e")
                x -= 1
                y -= 1
            elif y >= 1 and dp[y][x] == dp[y - 1][x] + 1:
                steps.append("i")
                inserted_words.append(actuals[y - 1])
                insertions += 1
                y -= 1
            elif x >= 1 and y >= 1 and dp[y][x] == dp[y - 1][x - 1] + 1:
                steps.append("s")
                substituted_words.append((preds[x - 1], actuals[y - 1]))
                substitutions += 1
                x -= 1
                y -= 1
            else:
                steps.append("d")
                deleted_words.append(preds[x - 1])
                deletions += 1
                x -= 1
            pbar.update(1)

    return {
        "steps": steps[::-1],
        "insertions": insertions,
        "substitutions": substitutions,
        "deletions": deletions,
        "inserted_words": inserted_words,
        "substituted_words": substituted_words,
        "deleted_words": deleted_words,
    }


def isd(preds: list[str], actuals: list[str], debug: bool = False) -> tuple:
    """
    Calculate the edit distance and generate summary statistics.

    Args:
        preds (List[str]): The list of words from the hypothesis sentence.
        actuals (List[str]): The list of words from the reference sentence.
        debug (bool, optional): If True, print debug information. Defaults to False.

    Returns:
        Tuple[int, Dict[str, any], pd.DataFrame]: Edit distance, step information, and summary statistics.
    """
    dp = [[0 for _ in range(len(preds) + 1)] for _ in range(len(actuals) + 1)]

    for row in tqdm(range(len(dp)), desc="Measuring Result vs Truth"):
        for col in range(len(dp[0])):
            if row == 0 or col == 0:
                dp[row][col] = max(row, col)
                continue

            if preds[col - 1] != actuals[row - 1]:
                dp[row][col] = (
                    min(dp[row - 1][col], dp[row][col - 1], dp[row - 1][col - 1]) + 1
                )
            else:
                dp[row][col] = min(
                    dp[row - 1][col], dp[row][col - 1], dp[row - 1][col - 1]
                )

    step = get_step(preds, actuals, dp)
    columns = [
        "wer",
        "cer",
        "insertions",
        "deletions",
        "substitutions",
        "inserted_words",
        "deleted_words",
        "substituted_words",
    ]
    summary = pd.DataFrame(
        [
            [
                dp[-1][-1] / len(actuals),
                jiwer.cer(hypothesis="".join(preds), reference="".join(actuals)),
                step["insertions"],
                step["deletions"],
                step["substitutions"],
                step["inserted_words"],
                step["deleted_words"],
                step["substituted_words"],
            ]
        ],
        columns=columns,
    )
    if debug:
        alignedPrint(step["steps"], actuals, preds, dp[-1][-1] / len(actuals))
        print(summary)

    return (dp[-1][-1], step, summary)


def wer_th(pred: str, actual: str, **kwargs) -> float:
    """
    Calculate Word Error Rate for Thai text.

    Args:
        pred (str): The hypothesis text.
        actual (str): The reference text.
        **kwargs: Additional arguments to pass to the isd function.

    Returns:
        float: The Word Error Rate.
    """
    preds = deepcut.tokenize(pred)
    actuals = deepcut.tokenize(actual)
    err, step, _ = isd(preds, actuals, **kwargs)
    return err / len(actuals)


def wer_eng(pred: str, actual: str, **kwargs) -> float:
    """
    Calculate Word Error Rate for English text.

    Args:
        pred (str): The hypothesis text.
        actual (str): The reference text.
        **kwargs: Additional arguments to pass to the isd function.

    Returns:
        float: The Word Error Rate.
    """
    normalizer = EnglishTextNormalizer()
    pred = normalizer(pred)
    actual = normalizer(actual)

    preds = pred.split(" ")
    actuals = actual.split(" ")

    err, steps, _ = isd(preds, actuals, **kwargs)
    return err / len(actuals)


def cer_th(pred: str, actual: str):
    """
    Calculate Character Error Rate for Thai text.

    Args:
        pred (str): The hypothesis text.
        actual (str): The reference text.

    Returns:
        float: The Character Error Rate.
    """
    return jiwer.cer(hypothesis=pred, reference=actual)


def cer_eng(pred: str, actual: str):
    """
    Calculate Character Error Rate for English text.

    Args:
        pred (str): The hypothesis text.
        actual (str): The reference text.

    Returns:
        float: The Character Error Rate.
    """
    normalizer = EnglishTextNormalizer()
    pred = normalizer(pred)
    actual = normalizer(actual)
    return jiwer.cer(hypothesis=pred, reference=actual)


def evaluate(preds: list[str], actuals: list[str], debug: bool = False) -> pd.DataFrame:
    """
    Evaluate the predictions against the actual values.

    Args:
        preds (List[str]): The list of predicted words.
        actuals (List[str]): The list of actual words.
        debug (bool, optional): If True, print debug information. Defaults to False.

    Returns:
        pd.DataFrame: A summary of evaluation metrics.
    """
    _, _, summary = isd(preds, actuals)

    return summary


# if __name__ == "__main__":
#     wer_score = wer_eng(
#         "I went to go to market place place", "I want to go to the market", debug=True
#     )
