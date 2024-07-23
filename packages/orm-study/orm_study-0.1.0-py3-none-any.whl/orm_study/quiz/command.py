import random
import typer
from typing import List, Tuple, Annotated
from typer import Typer
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print
from orm_study.quiz.constants import CHAPTER, TYPE, EXAM_CHOICE, CHAPTER_CHOICE, TYPE_CHOICE
from orm_study.quiz.reader import get_chapter, parse_content
from orm_study.quiz.certification import generate_certification_image
from orm_study.quiz.decorator import TimeTrace

app = Typer()


def fetch_quiz(chapter_input: str, type_input: str) -> List[Tuple[str, str]]:
    """
    :param chapter_input: chapter_input ∈ CHAPTER
    :param type_input: type_input ∈ TYPE
    :raises:`typer.Exit`: chapter_input not in CHAPTER or type_input not in TYPE
    :return: quiz_answer_set
    """
    try:
        quiz_txt = get_chapter(chapter_number=chapter_input, _type=type_input)
    except ValueError as msg:
        print(msg)
        raise typer.Exit(code=1)
    else:
        quizes, answers = parse_content(quiz_txt)
        quiz_answer_set = list(zip(quizes, answers))
        random.shuffle(quiz_answer_set)

        return quiz_answer_set


def fetch_exam() -> List[Tuple[str, str]]:
    """
    :return: quiz_answer_set
    """
    quiz_txt = []

    for chapter_number in CHAPTER:
        for type_input in TYPE:
            quiz_raw = get_chapter(chapter_number, type_input)
            if quiz_raw not in quiz_txt:
                quiz_txt.append(quiz_raw)

    quizes, answers = parse_content("".join(quiz_txt))
    quiz_answer_set = list(zip(quizes, answers))
    random.shuffle(quiz_answer_set)

    return quiz_answer_set


def select_exam_mode() -> bool:
    print(Panel(EXAM_CHOICE, title="시험 모드", title_align="center"))
    chapter_input = Prompt.ask("[white bold]시험 모드에 도전하시겠습니까?")

    if chapter_input.upper() == "Y":
        return True

    return False


def select_chapter() -> str:
    print(Panel(CHAPTER_CHOICE, title="챕터 선택", title_align="center"))
    chapter_input = Prompt.ask("[white bold]도전할 문제의 챕터를 선택해주세요 ")

    if chapter_input not in CHAPTER:
        print("[red bold]존재하지 않는 챕터입니다.")
        raise typer.Exit()

    return chapter_input


def select_quiz_type() -> str:
    print(Panel(TYPE_CHOICE, title="문제 유형 선택", title_align="center"))

    while True:
        type_input = Prompt.ask("[white bold]도전할 문제의 유형을 선택해주세요 ")
        if type_input not in TYPE:
            print("[red bold]존재하지 않는 유형입니다.")
        else:
            break

    return type_input


def select_quiz_num(max_num: int, min_num: int = 1) -> int:
    """
    :param max_num: 최대 문제 수
    :param min_num: 최소 문제 수, 기본값은 1 입니다.
    :return: min_num 이상, max_num 이하의 정수
    """
    while True:
        msg = f"[white bold]문항 수를 선택해주세요. ({min_num} ~ {max_num}개)"
        quiz_num = Prompt.ask(msg)
        if not quiz_num:
            return max_num
        elif int(quiz_num) > max_num:
            print("[red bold]최대 문항 수를 넘을 수 없습니다.ㅠㅠ")
        elif int(quiz_num) < min_num:
            print(f"[red bold]최소 {min_num}개 이상 선택해야 합니다.")
        else:
            return int(quiz_num)


@TimeTrace
def solve_quiz(quiz_answer_set: List[Tuple[str, str]]) -> List[bool]:
    user_answers = []
    for i, (quiz, answer) in enumerate(quiz_answer_set, start=1):
        print(Panel(f"[blue bold]문제 {i}{quiz}", title_align="center"))
        user_input = Prompt.ask("[white bold] 정답을 입력해주세요")
        user_answers.append(user_input == answer)
        print()
    return user_answers


def display_results(chapter_input: str, user_answers: List[bool]):
    print(f"[green bold]챕터 {chapter_input} 퀴즈 결과")
    print(f"[blue bold]총 {len(user_answers)}문제 중 {user_answers.count(True)}문제를 맞추셨습니다.")


@app.command(help="파이썬 퀴즈를 시작합니다.")
def start(
    time_check: Annotated[bool, typer.Option(help="퀴즈 타이머 추가")] = False,
    name: Annotated[str, typer.Argument(help="이름을 입력해주세요")] = "익명",
):
    print(f"[green bold]안녕하세요, {name}님! 파이썬 퀴즈를 시작합니다.")
    exam_mode_on = select_exam_mode()
    quiz_answer_set = quiz_num = chapter_input = type_input = None

    # TODO: select_exam_mode 함수를 지우고 새로운 커멘드 exam을 사용할 수 있도록 분리된 함수로 작성해야 합니다.
    if exam_mode_on:
        quiz_answer_set = fetch_exam()
        quiz_num = select_quiz_num(len(quiz_answer_set), min_num=15)
    else:
        chapter_input = select_chapter()
        type_input = select_quiz_type()
        quiz_answer_set = fetch_quiz(chapter_input, type_input)
        quiz_num = select_quiz_num(len(quiz_answer_set))
        print(f"[green bold]챕터 {chapter_input}: {CHAPTER[chapter_input]}\n")

    quiz_answer_set = quiz_answer_set[:quiz_num]
    user_answers, process_time = solve_quiz(quiz_answer_set)

    if time_check:
        print(f"[red bold]소요 시간: {process_time:.2f}초")

    if exam_mode_on:
        print("[red bold]시험 종료")
        save_path = "./"

        # TODO: 이미지 세이브 위치를 변경할 수 있어야 합니다.
        generate_certification_image(name, user_answers, process_time, save_path)
        print(f"인증서가 다음 위치에 저장되었습니다. {save_path}")
    else:
        display_results(chapter_input, user_answers)


if __name__ == "__main__":
    app()
