import datetime
import os
from PIL import Image, ImageFont, ImageDraw
from orm_study.quiz.constants import CERTIFICATION_TTF_PATH, CERTIFICATION_IMG_PATH


def _load_font(fontsize) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(font=CERTIFICATION_TTF_PATH, size=fontsize)


def generate_certification_image(name, user_answers, process_time, save_path) -> None:
    """
    :param name: 이름
    :param user_answers: command.solve_quiz 함수의 반환값
    :param process_time: command.solve_quiz 함수의 실행 시간
    :param save_path: 시험 성적서 저장 위치
    :return: None
    """
    certification_img = Image.open(CERTIFICATION_IMG_PATH)
    date = datetime.datetime.now()

    width, height = certification_img.size
    out_img = ImageDraw.Draw(certification_img)
    title_font = _load_font(100)
    body_font = _load_font(24)

    candidate_score_msg = f"{user_answers.count(True)} / {len(user_answers)}"
    trying_time_msg = f"{int(process_time // 60 // 60)}h {int(process_time // 60 % 60)}m {process_time % 60:.2f}s"
    candidate_date_msg = f"{date.strftime('%m %d. %Y')}"
    pass_fail_msg = "PASS" if user_answers.count(True) / len(user_answers) * 100 >= 75 else "FAIL"

    out_img.text(xy=(width // 2, 460), text=name, fill=(59, 59, 59), font=title_font, anchor="mm")
    out_img.text(xy=(388, 1154), text=name, fill=(59, 59, 59), font=body_font)
    out_img.text(xy=(468, 1243), text=candidate_score_msg, fill=(59, 59, 59), font=body_font)
    out_img.text(xy=(405, 1333), text=trying_time_msg, fill=(59, 59, 59), font=body_font)
    out_img.text(xy=(893, 1154), text=candidate_date_msg, fill=(59, 59, 59), font=body_font)
    out_img.text(xy=(876, 1243), text=pass_fail_msg, fill=(59, 59, 59), font=body_font)

    try:
        file_name = f"certification-{date.strftime('%Y%m%d%H%M%S')}.png"
        certification_img.save(os.path.join(save_path, file_name))
    except Exception as e:
        raise Exception(e)
