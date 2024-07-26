import hashlib
import json
import operator

import ir_measures
import numpy as np
import sklearn.preprocessing
import smart_open

__version__ = "0.3.0"

DEFAULT_METRICS = [
    "P@1",
    "P@5",
    "P@10",
    "P@20",
    "Judged@10",
    "Judged@20",
    "Judged@50",
    "AP@100",
    "AP@1000",
    "nDCG@5",
    "nDCG@10",
    "nDCG@20",
    "Recall@100",
    "Recall@1000",
    "RR",
]


class TRECRun:
    def __init__(self, results):
        self._cache_hash = None

        if isinstance(results, dict):
            # use comprehension to ensure copy
            self.results = {
                str(qid): {str(docid): float(score) for docid, score in docscores.items()}
                for qid, docscores in results.items()
                if len(docscores) > 0
            }
        else:
            # is the path a JSON object?
            try:
                with open(results, "rt", encoding="utf-8") as f:
                    self.results = json.load(f)
                    return
            except json.JSONDecodeError:
                pass

            # is the path a TREC run file?
            self.results = {}
            with smart_open.open(results) as f:
                for line in f:
                    fields = line.strip().split()
                    if len(fields) > 0:
                        qid, _, docid, rank, score = fields[:5]
                        score = float(score)
                        self.results.setdefault(qid, {})

                        if docid in self.results[qid]:
                            score = max(score, self.results[qid][docid])
                        self.results[qid][docid] = score

            if not self.results:
                raise IOError("provided path contained no results: %s" % results)

    def _arithmetic_op(self, other, op):
        if isinstance(other, TRECRun):
            try:
                results = {
                    qid: {docid: op(score, other.results[qid][docid]) for docid, score in self.results[qid].items()}
                    for qid in self.results
                }
            except KeyError:
                raise ValueError(
                    "both TrecRuns must contain the same qids and docids; perhaps you should intersect or concat first?"
                )
        else:
            scalar = other
            results = {qid: {docid: op(score, scalar) for docid, score in self.results[qid].items()} for qid in self.results}

        return TRECRun(results)

    def add(self, other):
        return self._arithmetic_op(other, operator.add)

    def subtract(self, other):
        return self._arithmetic_op(other, operator.sub)

    def multiply(self, other):
        return self._arithmetic_op(other, operator.mul)

    def divide(self, other):
        return self._arithmetic_op(other, operator.truediv)

    def topk(self, k):
        """Return a new run containg the top-k results"""
        results = {}
        for qid, docscores in self.results.items():
            if len(docscores) > k:
                results[qid] = dict(sorted(docscores.items(), key=lambda x: x[1], reverse=True)[:k])
            else:
                results[qid] = docscores.copy()

        return TRECRun(results)

    def intersect(self, other):
        """Return a new run containing only the query-document pairs contained in other"""

        if not isinstance(other, TRECRun):
            raise NotImplementedError()

        shared_results = {
            qid: {docid: score for docid, score in self.results[qid].items() if docid in other.results[qid]}
            for qid in self.results.keys() & other.results.keys()
        }
        return TRECRun(shared_results)

    def qids(self):
        return set(self.results.keys())

    # def union_qids(self, other, shared_qids="disallow"):
    #     if not isinstance(other, TRECRun):
    #         raise NotImplementedError()

    #     if shared_qids == "disallow":
    #         if self.qids().intersection(other.qids()):
    #             raise ValueError("inputs share some qids but shared_qids='disallow'")

    #         new_results = deepcopy(self.results)
    #         new_results.update(deepcopy(other.results))
    #     else:
    #         raise NotImplementedError("only disallow is implemented")

    #     return TRECRun(new_results)

    def concat(self, other):
        # other = other.normalize(method="minmax")
        results = {qid: {docid: score for docid, score in self.results[qid].items()} for qid in self.results}
        new_results = {
            qid: {docid: score for docid, score in other.results[qid].items() if docid not in self.results[qid]}
            for qid in other.results
            if qid in self.results
        }

        for qid in new_results:
            mn, mx = min(other[qid].values()), max(other[qid].values())
            for docid, score in new_results[qid].items():
                results[qid][docid] = score - mx + mn - 1e-3

        return TRECRun(results)

    def difference(self, other):
        results = {
            qid: {docid: score for docid, score in self.results[qid].items() if docid not in other.results.get(qid, {})}
            for qid in self.results
        }
        return TRECRun(results)

    def normalize(self, method="rr"):
        """Normalize document scores"""

        normalization_funcs = {
            "minmax": sklearn.preprocessing.minmax_scale,
            "standard": sklearn.preprocessing.scale,
        }

        if method == "rr":
            sorted_results = {
                qid: sorted(
                    ((docid, score) for docid, score in self.results[qid].items()),
                    key=lambda x: x[1],
                    reverse=True,
                )
                for qid in self.results
            }
            results = {
                qid: {docid: 1 / (idx + 1) for idx, (docid, old_score) in enumerate(sorted_results[qid])}
                for qid in sorted_results
            }
        elif method in normalization_funcs:
            results = {qid: {} for qid in self.results}
            for qid in self.results:
                docids, scores = zip(*self.results[qid].items())
                results[qid] = dict(zip(docids, normalization_funcs[method](scores)))
        else:
            raise ValueError(f"unknown method: {method}")

        return TRECRun(results)

    def __contains__(self, k):
        return k in self.results

    def __getitem__(self, k):
        # TODO is it ok to NOT return a copy here?
        return self.results[k]

    def __and__(self, other):
        return self.intersect(other)

    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        return self.add(other)

    def __mul__(self, other):
        return self.multiply(other)

    def __rmul__(self, other):
        return self.multiply(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __rsub__(self, other):
        return (-self).add(other)

    def __truediv__(self, other):
        return self.divide(other)

    def __neg__(self):
        return self.multiply(-1)

    def __len__(self):
        return sum(len(x) for x in self.results.values())

    def __eq__(self, other):
        if isinstance(other, TRECRun):
            return self.results == other.results
        return NotImplemented

    def write_trec_run(self, outfn, tag="run"):
        """Save the run in TREC format"""

        preds = self.results
        count = 0
        with open(outfn, "wt") as outf:
            qids = sorted(preds.keys())
            for qid in qids:
                rank = 1
                for docid, score in sorted(preds[qid].items(), key=lambda x: x[1], reverse=True):
                    print(f"{qid} Q0 {docid} {rank} {score} {tag}", file=outf)
                    rank += 1
                    count += 1

    def write_json_run(self, outfn):
        """Save the run in json format"""

        with open(outfn, "wt", encoding="utf-8") as outf:
            json.dump(self.results, outf)

    def remove_unjudged_documents(self, qrels):
        """Return a new run with unjudged documents removed"""

        results = {
            qid: {docid: score for docid, score in docscores.items() if docid in qrels.get(qid, [])}
            for qid, docscores in self.results.items()
        }
        return TRECRun(results)

    def evaluate(
        self,
        qrels,
        metrics=DEFAULT_METRICS,
    ):
        """Evaluate the run using the provided qrels"""

        metrics = [ir_measures.parse_measure(metric) if isinstance(metric, str) else metric for metric in metrics]

        d = {}
        for val in ir_measures.iter_calc(metrics, qrels, self.results):
            d.setdefault(str(val.measure), {})[val.query_id] = val.value

        for metric in d:
            d[metric]["mean"] = np.mean(list(d[metric].values()))

        return d

    def cache_hash(self):
        """Compute a hash of the run"""

        if not self._cache_hash:
            self._cache_hash_json = json.dumps(self.results, sort_keys=True)
            self._cache_hash = hashlib.sha256(self._cache_hash_json.encode()).hexdigest()

        return self._cache_hash

    def aggregate_docids(self, docid_conversion_func):
        """Apply docid_conversion_func to each docid and take the max score when collisions occur.

        For example, use this to convert passage IDs to their corresponding doc IDs and use the max passage score as the doc score.
        """

        d = {}
        for qid, docscores in self.results.items():
            d[qid] = {}
            for docid, score in docscores.items():
                new_docid = docid_conversion_func(docid)
                d[qid][new_docid] = max(score, d[qid].get(new_docid, -999999))

        return TRECRun(d)
