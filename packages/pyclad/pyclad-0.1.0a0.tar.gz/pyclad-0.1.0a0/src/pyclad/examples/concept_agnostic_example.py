import pathlib

from pyclad.callbacks.evaluation.matrix_evaluation import MatrixMetricEvaluationCallback
from pyclad.callbacks.evaluation.time_evaluation import TimeEvaluationCallback
from pyclad.data.readers.concepts_readers import read_dataset_from_npy
from pyclad.metrics.base.roc_auc import RocAuc
from pyclad.metrics.continual.average_continual import ContinualAverage
from pyclad.metrics.continual.backward_transfer import BackwardTransfer
from pyclad.metrics.continual.forward_transfer import ForwardTransfer
from pyclad.models.classical.isolation_forest import IsolationForestAdapter
from pyclad.output.json_writer import JsonOutputWriter
from pyclad.scenarios.concept_agnostic_scenario import concept_agnostic_scenario
from pyclad.strategies.baselines.cumulative import CumulativeStrategy

if __name__ == "__main__":
    data_loader = read_dataset_from_npy(
        pathlib.Path("resources/nsl-kdd_random_anomalies_5_concepts_1000_per_cluster.npy"), dataset_name="NSL-KDD-R"
    )
    strategy = CumulativeStrategy(IsolationForestAdapter())
    callbacks = [
        MatrixMetricEvaluationCallback(
            base_metric=RocAuc(),
            metrics=[ContinualAverage(), BackwardTransfer(), ForwardTransfer()],
        ),
        TimeEvaluationCallback(),
    ]
    concept_agnostic_scenario(data_loader, strategy=strategy, callbacks=callbacks, batch_size=64)

    output_writer = JsonOutputWriter(pathlib.Path("output.json"))
    output_writer.write([data_loader, strategy, *callbacks])
