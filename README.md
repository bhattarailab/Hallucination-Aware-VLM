# Hallucination Aware Hallucination-Aware Multimodal Benchmark for Gastrointestinal Image Analysis with Large Vision Language Models #

**Paper Available: https://arxiv.org/pdf/2505.07001**


## Contributions ##
* Multimodal image-text GI dataset, with VLM-generated descriptive responses, expert-labeled tags identifying hallucinated sentences, and their corresponding corrections.

* Extensive evaluation of state-of-the-art VLMs using both existing and proposed LLM-assisted evaluation metrics.

* Hallucination-aware fine-tuning shown to improve robustness compared to standard fine-tuning.


## About dataset ###
We used publicly available [Kvasir-v2](https://datasets.simula.no/kvasir/) images to generate medical reports using ChatGPT-4o, which were then reviewed by experts to identify and correct medical hallucinations. Our dataset not only provides the corrected responses of the vision-language model (VLM) but also includes sentence-level hallucination tags, offering additional insights into how the VLM hallucinates.

![Data annotation pipeline](Images/data_pipeline_with_stats.png)



## About Evaluation Metircs ##

While several metrics such as BLEU, ROUGE, and METEOR are commonly used to evaluate the similarity between ground-truth texts and generated texts, they are often limited by context-length dependence, insensitivity to subtle semantic differences, and an inability to assess factual accuracy. We propose two LLM-assited metrics that use GPT4o's strong overall textual and semantic understanding to assess the similarity between ground-truth and generated outputs:

* **Report Similarity (R-Sim):**  Rates coarse-level semantic similarity between the ground-truth and VLM responses on a scale of 1 to 5 (worst to best), using ChatGPT-4o
prompted to assess similarity with a focus on GI endoscopy and 12 diagnostic
questions.

* **Question Answering Accuracy Score (QAAS):** Objectively
measures accuracy by comparing VLM responses to 12 ground-truth Q&A pairs,
with ChatGPT-4o handling synonyms and similar phrasing.


## Hallucination-aware finetuning ##

Instead of instruction finetuning VLM models with the objective of generating ground-truth texts, we have used instruction finetuning to first detect hallucinated sentences in the default pretrained VLM response, followed by correcting the response. We used standard LORA for parameter efficient finetuning.

![Hal-aware finetuning](Images/hal-aware.png)


## Benchmarks ##

We evaluate our hallucination-aware fine-tuning strategy across various open-source VLMs and consistently demonstrate improved performance across multiple evaluation metrics.

![Benchmark Table](Images/MICCAI_benchmark_table.png)

![Fine-grained results](Images/category_comp.png)



***Information: We will soon release the dataset and evaluation code ....***


