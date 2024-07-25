from typing import Any, Dict

from sklearn.metrics import roc_auc_score

from pureml_evaluate.metrics.metric_base import MetricBase


class ROC_AUC(MetricBase):

    name: Any = "roc_auc"
    input_type: Any = "float"
    output_type: Any = None
    kwargs: Dict = {}

    def parse_data(self, data):

        return data

    # def compute(self, references, predictions=None, prediction_scores=None, average="macro", sample_weight=None,
    #             max_fpr=None, multi_class="raise", labels=None, **kwargs):

    #     if prediction_scores is None and predictions is None:
    #         score = None
    #     elif predictions is None:
    #         score = roc_auc_score(y_true=references, y_score=prediction_scores, average=average, sample_weight=sample_weight,
    #                             multi_class=multi_class, max_fpr=max_fpr, labels=labels)
    #         score = float(score)
    #     elif prediction_scores is None:
    #         score = roc_auc_score(y_true=references, y_score=predictions, average=average, sample_weight=sample_weight,
    #                             multi_class=multi_class, max_fpr=max_fpr, labels=labels)
    #         score = float(score)

    #     score = {
    #         self.name : score
    #         }
    def compute(
        self,
        references,
        predictions=None,
        prediction_scores=None,
        average="macro",
        sample_weight=None,
        max_fpr=None,
        multi_class="raise",
        labels=None,
        **kwargs
    ):

        if "kwargs" in kwargs and "average" in kwargs["kwargs"]:
            average = kwargs["kwargs"]["average"]
            # prediction_scores = kwargs['kwargs']['prediction_scores']
            multi_class = "ovo"

        if prediction_scores is None and predictions is None:
            score = None
        elif predictions is None:
            score = roc_auc_score(
                y_true=references,
                y_score=prediction_scores,
                average=average,
                sample_weight=sample_weight,
                multi_class=multi_class,
                max_fpr=max_fpr,
                labels=labels,
            )
            score = float(score)

        elif prediction_scores is None:
            score = roc_auc_score(
                y_true=references,
                y_score=predictions,
                average=average,
                sample_weight=sample_weight,
                multi_class=multi_class,
                max_fpr=max_fpr,
                labels=labels,
            )
            score = float(score)

        score = {self.name: {"value": score}}

        return score

    # return score
