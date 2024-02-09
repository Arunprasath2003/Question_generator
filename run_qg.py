import argparse
from questiongenerator import QuestionGenerator
from questiongenerator import store_qa


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--answer_style",
        default="all",
        type=str,
        help="The desired type of answers. Choose from ['all', 'sentences', 'multiple_choice']",
    )
    parser.add_argument("--model_dir", type=str, default=None)
    parser.add_argument("--num_questions", type=int, default=10)
    parser.add_argument("--show_answers", dest="show_answers", action="store_true", default=True)
    parser.add_argument("--text_file", type=str, required=True)
    parser.add_argument("--use_qa_eval", dest="use_qa_eval", action="store_true", default=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    with open(args.text_file, 'r',encoding='utf-8',errors='replace') as file:
        text = file.read()

    qg = QuestionGenerator()
    qa_list = qg.generate(
        text,
        num_questions=10,
        answer_style=args.answer_style,
        use_evaluator=args.use_qa_eval
    )
    output_path='D:/8TH_SEM/question_generator/articles/output.txt'
    store_qa(qa_list, output_path)
