import csv, json
import math
from web_crawler import facebookapi as fbapi
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

RegisteredData_path = '/Users/jasmine/PycharmProjects/HW2/registered_data.json'

# Global variable
student_data = dict()

def class_participation_by_userid(student_ID, type):  # 抓出「課程參與度統計」學生學號和統計項目
    Course_Participation_path = '/Users/jasmine/PycharmProjects/HW2/Course_Participation.csv'
    with open(Course_Participation_path, newline='')as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            if row['ID'] == student_ID:
                if row[type] == '' or row[type] == ' ':
                    row[type] = 0
                return row[type]


def all_students_class_participation(type):  # 抓出「課程參與度統計」單一統計項目的次數加總
    Course_Participation_path = '/Users/jasmine/PycharmProjects/HW2/Course Participation.csv'
    with open(Course_Participation_path, newline='')as csvfile:
        rows = csv.DictReader(csvfile)
        total = 0
        for row in rows:
            if row[type] != '':
                total += float(row[type])
        return total


def linebot_answer_time(student_ID):  # 抓出學生在linebot回答問題的次數
    linebotdata_path = '/Users/jasmine/PycharmProjects/HW2/linebot_questions_and_answers.json'
    with open(linebotdata_path, 'r') as f:
        data = json.load(f)
        answer_time = 0
        question_list = ['question1', 'question2', 'question3']
        for i in question_list:
            if student_ID in data[i]['reply']:
                answer_time += 1
        return answer_time


def linebot_question_time(student_ID):  # 抓出學生在linebot問問題的次數
    linebotdata_path = '/Users/jasmine/PycharmProjects/HW2/linebot_questions.json'
    with open(linebotdata_path, 'r') as f:
        data = json.load(f)
        question_time = 0
        if student_ID in data:
            question_time += 1

        return question_time


def change_id_to_facebook_name(student_ID):
    FB_ID_path = '/Users/jasmine/PycharmProjects/HW2/FB_ID.csv'
    with open(FB_ID_path, newline='')as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            if row['\ufeff學號'] == student_ID:
                return row['臉書名稱']


def get_fb_information_by_student_ID(facebook_information, student_ID):
    facebook_name = change_id_to_facebook_name(student_ID)
    if facebook_name in facebook_information:
        return facebook_information[facebook_name]
    return 0


def get_quartile(score_data, n):  # 找出四分位數
    if n < 1 or n > 3:
        return False
    score_data.sort()
    position = (len(score_data) + 1) * n / 4
    pos_integer = int(math.modf(position)[1])
    pos_decimal = position - pos_integer
    quartile = score_data[pos_integer - 1] + (score_data[pos_integer] - score_data[pos_integer - 1]) * pos_decimal
    return quartile


def get_interact_in_class(student_ID):
    interact1 = linebot_answer_time(student_ID)
    interact2 = linebot_question_time(student_ID)
    interact3 = class_participation_by_userid(student_ID, '上課發言次數')
    interact4 = get_fb_information_by_student_ID(fbapi.get_all_posts_all_user_comments_times(dataset), student_ID)
    interact_in_class = float(interact1) + float(interact2) + float(interact3) + float(interact4)
    return interact_in_class


def get_dedication_in_the_course(student_ID):
    dedication1 = class_participation_by_userid(student_ID, '自主學習python 的時數')
    dedication1_2 = class_participation_by_userid(student_ID, 'Final project 小組討論時數')
    dedication2 = class_participation_by_userid(student_ID, '現場問老師問題次數')
    dedication3 = class_participation_by_userid(student_ID, '現場問TA問題次數')
    dedication4 = class_participation_by_userid(student_ID, '私訊問助教問題次數')
    dedication5 = class_participation_by_userid(student_ID, 'TA Time 參加次數')
    dedication6 = class_participation_by_userid(student_ID, '老師office hour 次數')
    dedication_in_the_course_a = float(dedication1) + float(dedication1_2)
    dedication_in_the_course_b = float(dedication2) + float(dedication3) + float(dedication4) + float(
        dedication5) + float(dedication6)
    return dedication_in_the_course_a, dedication_in_the_course_b


def get_everyones_grade(grade_type):
    Course_Participation_path = '/Users/jasmine/PycharmProjects/HW2/Course_Participation.csv'
    with open(Course_Participation_path, newline='')as csvfile:
        rows = csv.DictReader(csvfile)
        id_list = []
        grade_list = []
        for row in rows:
            id_list.append(row['ID'])
        for id in id_list:
            grade_list.append(grade_type(id))
    return grade_list


def grade_calculator(student_ID):
    # 上課聽講認真程度(attentiveness_of_the_lecture) 10%
    attendance = class_participation_by_userid(student_ID, '來上課的次數')
    attentiveness = class_participation_by_userid(student_ID, '上課認真程度的自評(1-10分)')
    point1 = 0.1 * float(attendance) * float(attentiveness)
    if point1 > 10:
        point1 = 10

    # 課程中的互動程度 5%
    interact_in_class = get_interact_in_class(student_ID)
    score_data2 = get_everyones_grade(get_interact_in_class)
    point2 = 0
    if 1 <= interact_in_class < get_quartile(score_data2, 1):
        point2 = 2
    elif get_quartile(score_data2, 1) <= interact_in_class < get_quartile(score_data2, 2):
        point2 = 3
    elif get_quartile(score_data2, 2) <= interact_in_class < get_quartile(score_data2, 3):
        point2 = 4
    elif get_quartile(score_data2, 3) <= interact_in_class:
        point2 = 5

    #  對課程python付出程度 5%
    dedication_in_the_course = list(get_dedication_in_the_course(student_ID))
    score_data3 = get_everyones_grade(get_dedication_in_the_course)
    score_data3 = [[item[0] for item in score_data3], [item[1] for item in score_data3]]
    point3_list = []
    for i in range(2):
        if 1 <= dedication_in_the_course[i] < get_quartile(score_data3[i], 1):
            point3_list.append(2)
        elif get_quartile(score_data3[i], 1) <= dedication_in_the_course[i] < get_quartile(score_data3[i], 2):
            point3_list.append(3)
        elif get_quartile(score_data3[i], 2) <= dedication_in_the_course[i] < get_quartile(score_data3[i], 3):
            point3_list.append(4)
        elif get_quartile(score_data3[i], 3) <= dedication_in_the_course[i]:
            point3_list.append(5)
    if point3_list == []:
        point3 = 0
    else:
        point3 = max(point3_list)

    # BONUS +1%
    taking_notes = class_participation_by_userid(student_ID, '共筆協作篇數')
    helping_others = class_participation_by_userid(student_ID, '協助同學python 次數')
    playing = class_participation_by_userid(student_ID, '跟老師打桌遊的次數')
    clubhouse = class_participation_by_userid(student_ID, '上Cloubhouse 參與次數')
    if int(taking_notes) or int(helping_others) or int(playing) or int(clubhouse) >= 1:
        bonus_point = 1
    else:
        bonus_point = 0

    # final score
    final_score = point1 + point2 + point3 + bonus_point
    if final_score >= 20:
        final_score = 20

    return final_score


def student_grade():
    FB_ID_path = '/Users/jasmine/PycharmProjects/HW2/FB_ID.csv'
    with open(FB_ID_path, newline='')as csvfile:
        rows = csv.DictReader(csvfile)
        student_id_data = {}
        for row in rows:
            student_id_data[row['\ufeff學號']] = grade_calculator(row['\ufeff學號'])
        return student_id_data

if __name__ == '__main__':
    dataset = fbapi.get_json_from_cloud(date='0511')
    data = fbapi.get_all_posts_all_user_comments_times(dataset=dataset)
    print(grade_calculator("F34086074"))
    print(student_grade())

