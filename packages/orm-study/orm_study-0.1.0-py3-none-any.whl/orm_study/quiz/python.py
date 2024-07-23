import random
from typing import Optional
from dataclasses import dataclass
from rich import print
from orm_study.quiz.command import fetch_quiz, solve_quiz, display_results
from orm_study.quiz.constants import CHAPTER_CHOICE, CHAPTER

Select = str | int


@dataclass(slots=True)
class PythonQuiz:
    chapter: str
    quiz_list: list


class PythonQuizSelector:
    def show(self) -> None:
        print(CHAPTER_CHOICE)

    def select_quiz_by_chapter(self, chapter: Select, _type: Select) -> PythonQuiz:
        """
        _type: 객관식, 주관식, 혼합형 중에 선택
         - 1: 객관식
         - 2: 주관식
         - 3: 혼합형
        """
        chapter = self._cast_type(chapter)
        _type = self._cast_type(_type)

        if chapter not in CHAPTER:
            raise ValueError("존재하지 않는 챕터입니다.")
        if _type not in ["1", "2", "3"]:
            raise ValueError("존재하지 않는 유형입니다.")

        quiz_list = fetch_quiz(chapter, _type)
        return PythonQuiz(chapter=chapter, quiz_list=quiz_list)

    def _cast_type(self, _type: Select) -> str:
        if isinstance(_type, int):
            _type = str(_type)
        return _type


class PythonQuizManager:
    def __init__(self, python_quiz: PythonQuiz) -> None:
        self.python_quiz = python_quiz

    def solve(self, quiz_num: Optional[int] = None) -> None:
        quizes = self.python_quiz.quiz_list
        if quiz_num:
            quizes = random.sample(quizes, quiz_num)
        answer_list, process_time = solve_quiz(quizes)
        display_results(self.python_quiz.chapter, answer_list)

    def show(self, only_quiz: bool = False, quiz_num: Optional[int] = None) -> None:
        """
        퀴즈만 보여주거나, 정답도 함께 보여줄 수 있습니다.
        """
        ...
