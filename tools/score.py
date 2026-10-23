"""Scoring helpers: accuracy, per type precision and recall, confusion matrix, calibration table."""


def accuracy(truth, predicted):
    if not truth:
        return 0.0
    return sum(1 for t, p in zip(truth, predicted) if t == p) / len(truth)


def per_label(truth, predicted, labels):
    rows = {}
    for label in labels:
        tp = sum(1 for t, p in zip(truth, predicted) if t == label and p == label)
        fp = sum(1 for t, p in zip(truth, predicted) if t != label and p == label)
        fn = sum(1 for t, p in zip(truth, predicted) if t == label and p != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        rows[label] = {"precision": precision, "recall": recall, "support": tp + fn}
    return rows


def confusion(truth, predicted, labels):
    matrix = {t: {p: 0 for p in labels} for t in labels}
    for t, p in zip(truth, predicted):
        if t in matrix and p in matrix[t]:
            matrix[t][p] += 1
    return matrix


def calibration(truth, predicted, confidences, bins=(0.0, 0.5, 0.7, 0.8, 0.9, 0.95, 1.01)):
    """Group answers by confidence. For an honest model, the share right in each group is close to the confidence."""
    rows = []
    for low, high in zip(bins[:-1], bins[1:]):
        idx = [i for i, c in enumerate(confidences) if low <= c < high]
        if not idx:
            continue
        right = sum(1 for i in idx if truth[i] == predicted[i])
        mean_conf = sum(confidences[i] for i in idx) / len(idx)
        rows.append({"range": "%.2f to %.2f" % (low, min(high, 1.0)), "answers": len(idx),
                     "mean_confidence": mean_conf, "share_right": right / len(idx)})
    return rows


def review_split(truth, predicted, confidences, threshold):
    """What happens if everything below the confidence threshold goes to a person."""
    auto = [i for i, c in enumerate(confidences) if c >= threshold]
    human = [i for i, c in enumerate(confidences) if c < threshold]
    auto_acc = (sum(1 for i in auto if truth[i] == predicted[i]) / len(auto)) if auto else 0.0
    return {"threshold": threshold, "automatic": len(auto), "to_a_person": len(human),
            "automatic_accuracy": auto_acc}
