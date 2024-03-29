# Question_generator

The goal of Question Generation is to generate a valid and fluent question according to a given passage and the target answer. Question Generation can be used in many scenarios, such as automatic tutoring systems, improving the performance of Question Answering models and enabling chatbots to lead a conversation. The system is built using pretrained models from [HuggingFace Transformers](https://github.com/huggingface/transformers). There are two models: the question generator itself, and the QA evaluator which ranks and filters the question-answer pairs based on their acceptability.


- [question generator training and validation data](https://huggingface.co/datasets/iarfmoose/question_generator)
- [qa evaluator training and validation data](https://huggingface.co/datasets/iarfmoose/qa_evaluator)

## Usage


```
pip install -r requirements.txt -qq
python run_qg.py --text_file articles/twitter_hack.txt
```

This will generate 10 question-answer pairs of mixed style (full-sentence and multiple choice) based on the article specified in `--text_file` and print them to the console. For more information see the qg_commandline_example notebook.

The `QuestionGenerator` class can also be instantiated and used like this:

```python
from questiongenerator import QuestionGenerator
qg = QuestionGenerator()
qg.generate(text, num_questions=10)
```

This will generate 10 questions of mixed style and return a list of dictionaries containing question-answer pairs. In the case of multiple choice questions, the answer will contain a list of dictionaries containing the answers and a boolean value stating if the answer is correct or not. The output can be easily printed using the `print_qa()` function. For more information see the question_generation_example notebook.

### Choosing the number of questions

The desired number of questions can be passed as a command line argument using `--num_questions` or as an argument when calling `qg.generate(text, num_questions=20`. If the chosen number of questions is too large, then the model may not be able to generate enough. The maximum number of questions will depend on the length of the input text, or more specifically the number of sentences and named entities containined within text. Note that the quality of some of the outputs will decrease for larger numbers of questions, as the QA Evaluator ranks generated questions and returns the best ones.

### Answer styles

The system can generate questions with full-sentence answers (`'sentences'`), questions with multiple-choice answers (`'multiple_choice'`), or a mix of both (`'all'`). This can be selected using the `--answer_style` or `qg.generate(answer_style=<style>)` arguments.

## Models

### Question Generator

The question generator model takes a text as input and outputs a series of question and answer pairs. The answers are sentences and phrases extracted from the input text. The extracted phrases can be either full sentences or named entities extracted using [spaCy](https://spacy.io/). Named entities are used for multiple-choice answers. The wrong answers will be other entities of the same type found in the text. The questions are generated by concatenating the extracted answer with the full text (up to a maximum of 512 tokens) as context in the following format:

```
answer_token <extracted answer> context_token <context>
```

The concatenated string is then encoded and fed into the question generator model. The model architecture is `t5-base`. The pretrained model was finetuned as a sequence-to-sequence model on a dataset made up several well-known QA datasets ([SQuAD](https://rajpurkar.github.io/SQuAD-explorer/), [RACE](http://www.cs.cmu.edu/~glai1/data/race/), [CoQA](https://stanfordnlp.github.io/coqa/), and [MSMARCO](https://microsoft.github.io/msmarco/)). The datasets were restructured by concatenating the answer and context fields into the previously mentioned format. The concatenated answer and context was then used as an input for training, and the question field became the targets.


### QA Evaluator

The QA evaluator takes a question answer pair as an input and outputs a value representing its prediction about whether the input was a valid question and answer pair or not. The model is `bert-base-cased` with a sequence classification head. The pretrained model was finetuned on the same data as the question generator model, but the context was removed. The question and answer were concatenated 50% of the time. In the other 50% of the time a corruption operation was performed (either swapping the answer for an unrelated answer, or by copying part of the question into the answer). The model was then trained to predict whether the input sequence represented one of the original QA pairs or a corrupted input.

The input for the QA evaluator follows the format for `BertForSequenceClassification`, but using the question and answer as the two sequences. It is the following format:

```
[CLS] <question> [SEP] <answer [SEP]
```
