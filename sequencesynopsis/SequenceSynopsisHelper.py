"""Contains Helper functions for running Sequence Synopsis."""

from collections import Counter


def lcs(str1, str2):
    """Finds the LongestCommonSubsequence between given sequences"""
    tbl = [[0 for p in range(len(str2) + 1)] for q in range(len(str1) + 1)]
    for i, char1 in enumerate(str1):
        for j, char2 in enumerate(str2):
            tbl[i + 1][j + 1] = tbl[i][j] + 1 if char1 == char2 else max(
                tbl[i + 1][j], tbl[i][j + 1])
    res = []
    i, j = len(str1), len(str2)
    while i and j:
        if tbl[i][j] == tbl[i - 1][j]:
            i -= 1
        elif tbl[i][j] == tbl[i][j - 1]:
            j -= 1
        else:
            res.append(str1[i - 1])
            i -= 1
            j -= 1
    return res[::-1]


def sortByFrequency(seqList1, seqList2, selectedEvents):
    """Sort the given list of events (selectedEvents) based on
    the number of times they are present in seqlist1 and seqlist2 combined"""
    counter = Counter()
    for item in (seqList1, seqList2):
        for seqs in item:
            for event in seqs.events:
                if event in selectedEvents:
                    counter[event] += 1
    #print(counter)
    return sorted(counter, key=counter.get, reverse=True)


def levenshtein(str1, str2):
    """Calculates levenshtein distance between two strings."""
    # From Wikipedia
    if len(str1) < len(str2):
        return levenshtein(str2, str1)

    # len(str1) >= len(str2)
    if len(str2) == 0:
        return len(str1)

    previousRow = range(len(str2) + 1)
    for i, char1 in enumerate(str1):
        currentRow = [i + 1]
        for j, char2 in enumerate(str2):
            # j+1 instead of j since previousRow and currentRow are one character longer
            insertions = previousRow[j + 1] + 1
            deletions = currentRow[j] + 1       # than str2
            substitutions = previousRow[j] + (char1 != char2)
            currentRow.append(min(insertions, deletions, substitutions))
        previousRow = currentRow
    # print(previousRow)
    return previousRow[-1]


def calcDist(seqs, pattern):
    """Calculates given distance between sequence and pattern."""
    total = levenshtein(seqs, pattern)
    return total

def calcAverage(posList1, posList2):
    """Calculates average position of an event"""
    return [(p1+p2)/2.0 for p1, p2 in zip(posList1, posList2)]
    