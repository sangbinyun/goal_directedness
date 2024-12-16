# llm based evaluation
from openai import OpenAI
import logging
from typing import List, Dict
import json
from collections import Counter
import string
import re
from prompt import PromptTemplate

class HotpotEvaluator:
    def __init__(self, openai_key: str):
        """Initialize evaluator with OpenAI key."""
        self.client = OpenAI(api_key=openai_key)
        self.prompt_template = PromptTemplate.hotpot_evaluation
        
        # Initialize counters and results storage
        self._reset_metrics()

    def _reset_metrics(self):
        """Reset all evaluation metrics."""
        self.total = 0
        self.yes_count = 0
        self.no_count = 0
        self.exact_match_count = 0
        self.total_f1 = 0
        self.total_precision = 0
        self.total_recall = 0
        self.results = {
            'id': [],
            'correctness': [],
            'response': [],
            'exact_match': [],
            'precision': [],
            'recall': [],
            'f1': []
        }

    def _normalize_answer(self, s: str) -> str:
        """Normalize answer string by removing articles, punctuation, and extra whitespace."""
        def remove_articles(text):
            return re.sub(r'\b(a|an|the)\b', ' ', text)
        
        def white_space_fix(text):
            return ' '.join(text.split())
        
        def remove_punc(text):
            exclude = set(string.punctuation)
            return ''.join(ch for ch in text if ch not in exclude)
        
        def lower(text):
            return text.lower()
        
        return white_space_fix(remove_articles(remove_punc(lower(s))))

    def _get_tokens(self, s: str) -> Counter:
        """Get token counts from a normalized string."""
        return Counter(self._normalize_answer(s).split())

    def _evaluate_exact_match(self, prediction: str, ground_truth: str) -> bool:
        """Check if prediction exactly matches ground truth after normalization."""
        return self._normalize_answer(prediction) == self._normalize_answer(ground_truth)    

    def _compute_f1(self, prediction: str, ground_truth: str) -> tuple:
        """
        Compute F1 score between prediction and ground truth.
        Returns (precision, recall, f1)
        """
        prediction_tokens = self._get_tokens(prediction)
        ground_truth_tokens = self._get_tokens(ground_truth)
        
        common = prediction_tokens & ground_truth_tokens
        num_same = sum(common.values())
        
        if num_same == 0:
            return 0, 0, 0
            
        precision = num_same / sum(prediction_tokens.values())
        recall = num_same / sum(ground_truth_tokens.values())
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        return precision, recall, f1

    def _evaluate_accuracy(self, question: str, correct_answer: str, model_answer: str) -> str:
        """Evaluate a single answer using GPT-4o."""
        prompt = self.prompt_template.format(
            question = question,
            correct_answer = correct_answer,
            predicted_answer = model_answer
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Evaluation failed: {e}")
            return "ERROR"

    def _evaluate_llm_correctness(self, question: str, correct_answer: str, model_answer: str) -> str:
        """Evaluate answer correctness using LLM."""
        result = self._evaluate_accuracy(question, correct_answer, model_answer)
        
        if 'yes' in result.lower():
            self.yes_count += 1
            return 'yes', result
        elif 'no' in result.lower():
            self.no_count += 1
            return 'no', result
        return 'N/A', result

    def calculate_metrics_answer(self, data: Dict) -> Dict:
        """
        Evaluate a dataset of hotpot QA pairs.
        
        Args:
            data: Dict with keys 'question', 'gt_answer' (correct), and 'answer' (model response) and values as lists
        
        Returns:
            Dict with evaluation metrics including accuracy and F1 scores
        """
        self.total = len(data['id'])


        for i in range(self.total):
            # Store question ID
            self.results['id'].append(data['id'][i])

            # LLM-based correctness evaluation
            correctness, result = self._evaluate_llm_correctness(
                data['question'][i],
                data['gt_answer'][i],
                data['answer'][i]
            )
            self.results['correctness'].append(correctness)
            self.results['response'].append(result)


            # Exact match evaluation
            is_exact_match = self._evaluate_exact_match(
                data['answer'][i],
                data['gt_answer'][i]
            )
            if is_exact_match:
                self.exact_match_count += 1
            self.results['exact_match'].append(is_exact_match)     


            # F1 score evaluation
            precision, recall, f1 = self._compute_f1(
                data['answer'][i],
                data['gt_answer'][i]
            )
            self.results['precision'].append(precision)
            self.results['recall'].append(recall)
            self.results['f1'].append(f1)
            self.total_precision += precision
            self.total_recall += recall
            self.total_f1 += f1

        return {
            # Accuracy
            'correct': self.yes_count,
            'incorrect': self.no_count,
            'accuracy': self.yes_count / self.total if self.total > 0 else 0,
            'correctness': self.results['correctness'],
            'response': self.results['response'],

            # Exact match
            'exact_matches': self.exact_match_count,
            'exact_match_ratio': self.exact_match_count / self.total if self.total > 0 else 0,
            'exact_match': self.results['exact_match'],

            # F1 scores
            'precision': self.results['precision'],
            'recall': self.results['recall'],
            'f1': self.results['f1'],
            'avg_precision': self.total_precision / self.total if self.total > 0 else 0,
            'avg_recall': self.total_recall / self.total if self.total > 0 else 0,
            'avg_f1': self.total_f1 / self.total if self.total > 0 else 0,            
        }

    def calculate_metrics_supporting_docs(self, data: Dict) -> Dict:
        """
        Calculate metrics for supporting document prediction accuracy.
        
        Args:
            data: Dict containing 'supporting_documents' (predicted) and 'supporting_facts' (ground truth)
        
        Returns:
            Dict with supporting document evaluation metrics
        """
        total_precision = 0
        total_recall = 0
        total_f1 = 0
        exact_matches = 0
        total = len(data['supporting_documents'])
        
        results = {
            'precision': [],
            'recall': [],
            'f1': [],
            'exact_match': []
        }
        
        for pred, truth in zip(data['supporting_documents'], data['supporting_facts']):
            # Convert to sets for easier computation
            pred_set = set(pred)
            truth_set = set(truth)
            
            # Calculate metrics
            if len(pred_set) == 0 and len(truth_set) == 0:
                precision = 1.0
                recall = 1.0
                f1 = 1.0
            elif len(pred_set) == 0 or len(truth_set) == 0:
                precision = 0.0
                recall = 0.0
                f1 = 0.0
            else:
                true_positives = len(pred_set.intersection(truth_set))
                precision = true_positives / len(pred_set)
                recall = true_positives / len(truth_set)
                f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            # Check for exact match
            is_exact_match = pred_set == truth_set
            
            # Store individual results
            results['precision'].append(precision)
            results['recall'].append(recall)
            results['f1'].append(f1)
            results['exact_match'].append(is_exact_match)
            
            # Update totals
            total_precision += precision
            total_recall += recall
            total_f1 += f1
            if is_exact_match:
                exact_matches += 1
        
        return {
            'precision': results['precision'],
            'recall': results['recall'],
            'f1': results['f1'],
            'exact_match': results['exact_match'],
            'avg_precision': total_precision / total if total > 0 else 0,
            'avg_recall': total_recall / total if total > 0 else 0,
            'avg_f1': total_f1 / total if total > 0 else 0,
            'exact_matches': exact_matches,
            'exact_match_ratio': exact_matches / total if total > 0 else 0
        }

if __name__ == "__main__":
    # Instantiate evaluator
    evaluator = HotpotEvaluator(openai_key = os.environ["OPENAI_API_KEY"])

    # Load states
    states = json.load(open(f'states/states_{ExperimentName}.json', 'r'))

    # Calculate metrics
    results = evaluator.calculate_metrics_answer(states)
    results_docs = evaluator.calculate_metrics_supporting_docs(states)

    # Save results
    json.dump(results, open(f'metrics/metrics_answer_{ExperimentName}.json', 'w'), indent = 4)
    json.dump(results_docs, open(f'metrics/metrics_docs_{ExperimentName}.json', 'w'), indent = 4)