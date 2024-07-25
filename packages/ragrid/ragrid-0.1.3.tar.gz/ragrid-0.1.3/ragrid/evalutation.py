import pandas as pd
import os
from ragrid.library_exceptions import DocumentExtractorError,InvalidFilePath,LibraryError
import logging
# Get the logger for deepeval
logger = logging.getLogger('deepeval')
# Set the logging level to ERROR to suppress INFO, DEBUG, and WARNING messages
logger.setLevel(logging.ERROR)
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    SummarizationMetric,
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    HallucinationMetric,
    BiasMetric,
    ToxicityMetric,
    GEval
)
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics.ragas import RagasMetric

class EvaluationMetric:
    def __init__(self, csv_path=None, **kwargs):
        default_attributes = {
            "Create_CSV": True,
            "Contextual_precision_Score": True,
            "contextual_recall_score": True,
            "Contextual_relevancy_score": True,
            "Contextual Reason": True,
            "Contextual Recall": True,
            "Contextual Relevancy": True,
            "Correctness_Score": True,
            "Correctness_Reason": True,
            "Summarization_Score": True,
            "Summarization_Reason": True,
            "Answer_Relevancy_Score": True,
            "Answer_Relevancy_Reason": True,
            "Faithfulness_Score": True,
            "Faithfulness_Reason": True,
            "Hallucination_Score": True,
            "Hallucination_Reason": True,
            "Bias_Score": True,
            "Bias_Reason": True,
            "Toxicity_Score": True,
            "Toxicity_Reason": True,
            "Ragas_Score": True
        }
        self.attributes = default_attributes
        self.attributes.update(kwargs)

        if self.attributes.get("Create_CSV"):
            self.csv_path = 'relevance_scores.csv'
        else:
            self.csv_path = csv_path

    def evaluation_metrics_function(self, user_query, llm_response, retriever):
        if not isinstance(retriever, list):
            raise TypeError("Retriever must be a list.")    
        
        try:
            test_case = LLMTestCase(
                input=user_query,
                actual_output=llm_response,
                expected_output="",
                retrieval_context=retriever,
                context=retriever
            )

            metrics = {
                "Contextual_precision_Score": ContextualPrecisionMetric(),
                "contextual_recall_score": ContextualRecallMetric(),
                "Contextual_relevancy_score": ContextualRelevancyMetric(),
                "Correctness_Score": GEval(
                    name="Correctness",
                    criteria="Determine whether the actual output is factually correct based on the expected output.",
                    evaluation_steps=[
                        "Check whether the facts in 'actual output' contradicts any facts in 'expected output'",
                        "You should also heavily penalize omission of detail",
                        "Vague language, or contradicting OPINIONS, are OK"
                    ],
                    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
                ),
                "Summarization_Score": SummarizationMetric(
                    threshold=0.5,
                    model="gpt-4",
                    assessment_questions=[
                        "Is the coverage score based on a percentage of 'yes' answers?",
                        "Does the score ensure the summary's accuracy with the source?",
                        "Does a higher score mean a more comprehensive summary?"
                    ]
                ),
                "Answer_Relevancy_Score": AnswerRelevancyMetric(
                    threshold=0.7,
                    model="gpt-4",
                    include_reason=True
                ),
                "Faithfulness_Score": FaithfulnessMetric(
                    threshold=0.7,
                    model="gpt-4",
                    include_reason=True
                ),
                "Hallucination_Score": HallucinationMetric(threshold=0.5),
                "Bias_Score": BiasMetric(threshold=0.5),
                "Toxicity_Score": ToxicityMetric(threshold=0.5),
                "Ragas_Score": RagasMetric(threshold=0.5, model="gpt-3.5-turbo")
            }

            results = {
                "User Query": [user_query],
                "LLM Response": [llm_response]
            }

            for key, metric in metrics.items():
                if self.attributes.get(key):
                    metric.measure(test_case)
                    results[key] = [metric.score]
                    reason_key = key.replace("Score", "Reason")
                    if self.attributes.get(reason_key):
                        results[reason_key] = [metric.reason]

            df = pd.DataFrame(results)

            if not os.path.isfile(self.csv_path):
                df.to_csv(self.csv_path, index=False)
            else:
                df.to_csv(self.csv_path, mode='a', header=False, index=False)

        except FileNotFoundError:
            raise InvalidFilePath()
        except pd.errors.EmptyDataError:
            raise DocumentExtractorError()
        except Exception as e:
            raise LibraryError(f"An unexpected error occurred: {str(e)}")