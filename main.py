import datetime
import sqlite3
from random import randint

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.animation import Animation
from kivy.graphics.vertex_instructions import Ellipse, Rectangle
from kivy.graphics.context_instructions import Color
from kivy.clock import Clock
from kivy.core.window import Window
#Window.size = (393, 750)
Window.size = (432, 825)

weekdays = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}

monthes = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
           7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}

currency__currency_symbol = {"ruble" : "₽", "hryvnia" : "₴", "tenge" : "₸", "tugrik" : "₮",
                             "yuan" : "Ұ", "dollar" : "$", "euro" : "€", "pound_sterling" : "£"}

user_data = {"user_login": "", "user_password": "", "user_name": "", "date_of_birth": "", "no_working": "",
             "study_at_school": "", "study_at_university": "", "working": "", "personal_business": "",
             "other_work": "", "days_a_week_at_work": "", "hours_a_day_work": "", "minutes_travel_time_to_work": "",
             "minutes_travel_time_from_work": "", "minutes_for_self_education_per_day": "", "no_hobbies": "",
             "sport_hobby": "", "tourism_hobby": "", "dance_hobby": "", "hunting_hobby": "", "art_hobby": "",
             "vocals_hobby": "", "collecting_hobby": "", "programming_hobby": "", "construction_hobby": "",
             "walk_hobby": "", "shopping_hobby": "", "film_hobby": "", "video_games_hobby": "", "meditation_hobby": "",
             "other_hobby": "", "hours_a_week_for_hobbies": "", "hours_of_sleep": "", "no_time_wasters": "",
             "TV_addiction_time_waster": "", "internet_addiction_time_waster": "", "chatter_time_waster": "",
             "smoking_time_waster": "", "other_time_waster": "", "hours_on_a_weekday_for_time_wasters": "",
             "hours_on_a_day_off_for_time_wasters": "", "visit_store_once_a_week": "",
             "minutes_on_the_way_to_the_store": "", "minutes_to_visit_shop": "", "hours_per_week_per_family": "",
             "hours_per_week_for_pets": "", "hours_per_week_for_cleaning": "", "minutes_per_day_per_shower": "",
             "minutes_after_sleep": "", "minutes_before_sleep": "", "hours_a_day_for_cooking": "",
             "minutes_for_breakfast": "", "minutes_for_lunch": "", "minutes_for_dinner": "",
             "hours_per_month_per_hairdresser": "", "hours_per_month_for_beauty_workers": "",
             "hours_per_week_for_other_activities": "",
             
             "currency": "", "scholarship_per_month": "", "salary_per_month": "", "premiums_per_year": "",
             "premium_amount": "", "number_of_businesses": "", "net_income_from_business_per_month": "",
             "other_financial_receipts_per_month": "", "sports_funds_per_month": "", "tourism_funds_per_month": "",
             "dance_funds_per_month": "", "hunting_funds_per_month": "", "art_funds_per_month": "",
             "vocals_funds_per_month": "", "collecting_funds_per_month": "", "programming_funds_per_month": "",
             "construction_funds_per_month": "", "walk_funds_per_month": "", "shopping_funds_per_month": "",
             "film_funds_per_month": "", "video_games_funds_per_month": "", "meditation_funds_per_month": "",
             "funds_for_other_types_of_hobbies_per_month": "", "self_education_funds_per_month": "",
             "TV_funds_per_month": "", "internet_resources_funds_per_month": "", "smoking_funds_per_month": "",
             "funds_for_other_types_of_time_wasters_per_month": "", "grocery_shopping_allowance_per_week": "",
             "funds_for_shopping_at_a_household_store_per_week": "", "funds_for_a_hairdresser_per_month": "",
             "funds_for_other_beauty_workers_per_month": "", "internet_funds_per_month": "",
             "other_funds_per_month": "",
             
             "date_day": "", "date_month": "", "date_year": "", "time_hour": "", "time_minute": "", "time_second": ""}

days_have_passed = 0



def update_days_have_passed():
    global days_have_passed

    if user_data["user_login"]:
        now = datetime.datetime.now()

        registration_date = datetime.datetime.strptime(f"{user_data['date_day']}.{user_data['date_month']}.{user_data['date_year']}", "%d.%m.%Y")
        now_date = datetime.datetime.strptime(f"{now.day}.{now.month}.{now.year}", "%d.%m.%Y")

        days_have_passed = (now_date - registration_date).days + (now.second - user_data["time_second"]) \
                            / 86400 + (now.minute - user_data["time_minute"]) / 1440 \
                            + (now.hour - user_data["time_hour"]) / 24

def update_current_user(user_login):
    global user_data

    with sqlite3.connect('db.db') as db:
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users")
        all_info = cursor.fetchall()[1:]
        for data in all_info:
            if user_login == data[0]:
                current_data = data
                break
        else:
            return -1
        
        cursor.execute(f"""UPDATE users SET user_login = ?, user_password = ?, user_name = ?, date_of_birth = ?,
                           no_working = ?, study_at_school = ?, study_at_university = ?, working = ?,
                           personal_business = ?, other_work = ?, days_a_week_at_work = ?, hours_a_day_work = ?,
                           minutes_travel_time_to_work = ?, minutes_travel_time_from_work = ?,
                           minutes_for_self_education_per_day = ?, no_hobbies = ?, sport_hobby = ?, tourism_hobby = ?,
                           dance_hobby = ?, hunting_hobby = ?, art_hobby = ?, vocals_hobby = ?, collecting_hobby = ?,
                           programming_hobby = ?, construction_hobby = ?, walk_hobby = ?, shopping_hobby = ?,
                           film_hobby = ?, video_games_hobby = ?, meditation_hobby = ?, other_hobby = ?,
                           hours_a_week_for_hobbies = ?, hours_of_sleep = ?, no_time_wasters = ?,
                           TV_addiction_time_waster = ?, internet_addiction_time_waster = ?, chatter_time_waster = ?,
                           smoking_time_waster = ?, other_time_waster = ?, hours_on_a_weekday_for_time_wasters = ?,
                           hours_on_a_day_off_for_time_wasters = ?, visit_store_once_a_week = ?,
                           minutes_on_the_way_to_the_store = ?, minutes_to_visit_shop = ?,
                           hours_per_week_per_family = ?, hours_per_week_for_pets = ?,
                           hours_per_week_for_cleaning = ?, minutes_per_day_per_shower = ?, minutes_after_sleep = ?,
                           minutes_before_sleep = ?, hours_a_day_for_cooking = ?, minutes_for_breakfast = ?,
                           minutes_for_lunch = ?, minutes_for_dinner = ?, hours_per_month_per_hairdresser = ?,
                           hours_per_month_for_beauty_workers = ?, hours_per_week_for_other_activities = ?,
                           
                           currency = ?, scholarship_per_month = ?, salary_per_month = ?, premiums_per_year = ?,
                           premium_amount = ?, number_of_businesses = ?, net_income_from_business_per_month = ?,
                           other_financial_receipts_per_month = ?, sports_funds_per_month = ?,
                           tourism_funds_per_month = ?, dance_funds_per_month = ?, hunting_funds_per_month = ?,
                           art_funds_per_month = ?, vocals_funds_per_month = ?, collecting_funds_per_month = ?,
                           programming_funds_per_month = ?, construction_funds_per_month = ?,
                           walk_funds_per_month = ?, shopping_funds_per_month = ?, film_funds_per_month = ?,
                           video_games_funds_per_month = ?, meditation_funds_per_month = ?,
                           funds_for_other_types_of_hobbies_per_month = ?, self_education_funds_per_month = ?,
                           TV_funds_per_month = ?, internet_resources_funds_per_month = ?,
                           smoking_funds_per_month = ?, funds_for_other_types_of_time_wasters_per_month = ?,
                           grocery_shopping_allowance_per_week = ?,
                           funds_for_shopping_at_a_household_store_per_week = ?,
                           funds_for_a_hairdresser_per_month = ?, funds_for_other_beauty_workers_per_month = ?,
                           internet_funds_per_month = ?, other_funds_per_month = ?,
                           
                           date_day = ?, date_month = ?, date_year = ?, time_hour = ?, time_minute = ?,
                           time_second = ? WHERE rowid = 1""", current_data)

        db.commit()

        user_data_keys = list(user_data.keys())
        for i in range(len(user_data_keys)):
            user_data[user_data_keys[i]] = current_data[i]

def update_db_data():
    current_login = user_data["user_login"]

    current_data = []
    for key in user_data.keys():
        current_data.append(user_data[key])

    with sqlite3.connect('db.db') as db:
        cursor = db.cursor()
        
        cursor.execute(f"""UPDATE users SET user_login = ?, user_password = ?, user_name = ?, date_of_birth = ?,
                           no_working = ?, study_at_school = ?, study_at_university = ?, working = ?,
                           personal_business = ?, other_work = ?, days_a_week_at_work = ?, hours_a_day_work = ?,
                           minutes_travel_time_to_work = ?, minutes_travel_time_from_work = ?,
                           minutes_for_self_education_per_day = ?, no_hobbies = ?, sport_hobby = ?, tourism_hobby = ?,
                           dance_hobby = ?, hunting_hobby = ?, art_hobby = ?, vocals_hobby = ?, collecting_hobby = ?,
                           programming_hobby = ?, construction_hobby = ?, walk_hobby = ?, shopping_hobby = ?,
                           film_hobby = ?, video_games_hobby = ?, meditation_hobby = ?, other_hobby = ?,
                           hours_a_week_for_hobbies = ?, hours_of_sleep = ?, no_time_wasters = ?,
                           TV_addiction_time_waster = ?, internet_addiction_time_waster = ?, chatter_time_waster = ?,
                           smoking_time_waster = ?, other_time_waster = ?, hours_on_a_weekday_for_time_wasters = ?,
                           hours_on_a_day_off_for_time_wasters = ?, visit_store_once_a_week = ?,
                           minutes_on_the_way_to_the_store = ?, minutes_to_visit_shop = ?,
                           hours_per_week_per_family = ?, hours_per_week_for_pets = ?,
                           hours_per_week_for_cleaning = ?, minutes_per_day_per_shower = ?, minutes_after_sleep = ?,
                           minutes_before_sleep = ?, hours_a_day_for_cooking = ?, minutes_for_breakfast = ?,
                           minutes_for_lunch = ?, minutes_for_dinner = ?, hours_per_month_per_hairdresser = ?,
                           hours_per_month_for_beauty_workers = ?, hours_per_week_for_other_activities = ?,
                           
                           currency = ?, scholarship_per_month = ?, salary_per_month = ?, premiums_per_year = ?,
                           premium_amount = ?, number_of_businesses = ?, net_income_from_business_per_month = ?,
                           other_financial_receipts_per_month = ?, sports_funds_per_month = ?,
                           tourism_funds_per_month = ?, dance_funds_per_month = ?, hunting_funds_per_month = ?,
                           art_funds_per_month = ?, vocals_funds_per_month = ?, collecting_funds_per_month = ?,
                           programming_funds_per_month = ?, construction_funds_per_month = ?,
                           walk_funds_per_month = ?, shopping_funds_per_month = ?, film_funds_per_month = ?,
                           video_games_funds_per_month = ?, meditation_funds_per_month = ?,
                           funds_for_other_types_of_hobbies_per_month = ?, self_education_funds_per_month = ?,
                           TV_funds_per_month = ?, internet_resources_funds_per_month = ?,
                           smoking_funds_per_month = ?, funds_for_other_types_of_time_wasters_per_month = ?,
                           grocery_shopping_allowance_per_week = ?,
                           funds_for_shopping_at_a_household_store_per_week = ?,
                           funds_for_a_hairdresser_per_month = ?, funds_for_other_beauty_workers_per_month = ?,
                           internet_funds_per_month = ?, other_funds_per_month = ?,
                           
                           date_day = ?, date_month = ?, date_year = ?, time_hour = ?, time_minute = ?,
                           time_second = ? WHERE user_login = '{current_login}' AND rowid > 1""", current_data)

        db.commit()


class LoginScreen(Screen):
    started = False

    def on_parent(self, *args):
        if not self.started:
            self.old_window_size = list(Window.size)
            self.big_ellipse_radius = Window.size[0]

            with self.canvas.before:
                Color(0, .9, 1, 1)

                self.big_ellipse = Ellipse(pos = (Window.size[0] * .5 - self.big_ellipse_radius, Window.size[1]),
                                    size = (2 * self.big_ellipse_radius, 2 * self.big_ellipse_radius))

                anim = Animation(pos = (self.big_ellipse.pos[0], self.big_ellipse.pos[1] - Window.size[1] * .35),
                                duration = 2, t = "in_out_cubic")
                anim.start(self.big_ellipse)

                self.points = []
                self.making_stars = Clock.schedule_interval(self.make_stars, 1/10)
            self.started = True

        else:
            with self.canvas.before:
                self.big_ellipse = Ellipse(pos = (Window.size[0] * .5 - self.big_ellipse_radius,
                                                  Window.size[1] - Window.size[1] * .35),
                                           size = (2 * self.big_ellipse_radius, 2 * self.big_ellipse_radius))
            self.on_size()
    
    def on_size(self, *args):
        self.big_ellipse_radius = Window.size[0]
        self.big_ellipse.pos = (Window.size[0] * .5 - self.big_ellipse_radius,
                                Window.size[1] - Window.size[1] * .35)
        self.big_ellipse.size = (2 * self.big_ellipse_radius, 2 * self.big_ellipse_radius)

        self.new_window_size = list(Window.size)
        difference_of_window_size = [self.new_window_size[0] / self.old_window_size[0],
                                    self.new_window_size[1] / self.old_window_size[1]]
        for point in self.points:
            point.pos = [point.pos[0] * difference_of_window_size[0], point.pos[1] * difference_of_window_size[1]]

        self.old_window_size = self.new_window_size

    def make_stars(self, *args):
        with self.canvas.before:
            new_point = Ellipse(pos = [self.big_ellipse.pos[0] + self.big_ellipse_radius,
                                self.big_ellipse.pos[1] + self.big_ellipse_radius], size = (1, 1))
            self.points.append(new_point)
            if len(self.points) >= 1500:
                self.making_stars.cancel()

            anim = Animation(pos = (randint(0, Window.size[0]), (randint(0, Window.size[1]))), duration = 3)
            anim.start(new_point)

    def clear_canvas(self):
        self.canvas.before.remove(self.big_ellipse)

    def log_in(self):
        login = self.ids.login.text
        password = self.ids.password.text

        if not login or not password:
            return False

        with sqlite3.connect('db.db') as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users")

            all_info = cursor.fetchall()
            if len(all_info) == 1:
                return False

            for data in all_info[1:]:
                if data[0] == login:
                    if data[1] == password:
                        update_current_user(login)
                        return True
                    else:
                        return False



class RegistrationTimeScreen(Screen):
    started = False

    def on_parent(self, *args):
        if not self.started:
            self.old_window_size = list(Window.size)

            with self.canvas.before:
                Color(1, 1, 0, 1)
                self.points = []
                self.making_stars = Clock.schedule_interval(self.make_stars, 1)
            self.started = True

        else:
            self.ids.state.color = 1, 1, 0, 1
            self.ids.state.text = "Время"

    def make_stars(self, *args):
        with self.canvas.before:
            new_point = Ellipse(pos = [randint(0, Window.size[0]), Window.size[1]], size = (1, 1))
            self.points.append(new_point)
            if len(self.points) >= 61:
                self.canvas.before.remove(self.points[0])
                self.points = self.points[1:]

            anim = Animation(pos = (randint(0, Window.size[0]), -1), duration = 60)
            anim.start(new_point)

    def write_data(self):
        global user_data

        if not self.ids.user_name.text:
            return False
        user_data["user_name"] = self.ids.user_name.text

        if len(self.ids.date_of_birth.text.split(".")) != 3:
            return False
        user_data["date_of_birth"] = self.ids.date_of_birth.text

        work_bool = True
        for work_type in ("no_working", "study_at_school", "study_at_university",
                          "working", "personal_business", "other_work"):
            if self.ids[work_type].active:
                work_bool = False
                break
        if work_bool:
            return False
        for work_type in ("no_working", "study_at_school", "study_at_university",
                          "working", "personal_business", "other_work"):
            user_data[work_type] = int(self.ids[work_type].active)

        if not self.ids.days_a_week_at_work.text:
            return False
        user_data["days_a_week_at_work"] = self.ids.days_a_week_at_work.text

        if not self.ids.hours_a_day_work.text:
            return False
        user_data["hours_a_day_work"] = self.ids.hours_a_day_work.text

        if not self.ids.minutes_travel_time_to_work.text:
            return False
        user_data["minutes_travel_time_to_work"] = self.ids.minutes_travel_time_to_work.text

        if not self.ids.minutes_travel_time_from_work.text:
            return False
        user_data["minutes_travel_time_from_work"] = self.ids.minutes_travel_time_from_work.text

        if not self.ids.minutes_for_self_education_per_day.text:
            return False
        user_data["minutes_for_self_education_per_day"] = self.ids.minutes_for_self_education_per_day.text

        hobby_bool = True
        for hobby in ("no_hobbies", "sport_hobby", "tourism_hobby", "dance_hobby", "hunting_hobby",
                      "art_hobby", "vocals_hobby", "collecting_hobby", "programming_hobby",
                      "construction_hobby", "walk_hobby", "shopping_hobby", "film_hobby",
                      "video_games_hobby", "meditation_hobby", "other_hobby"):
            if self.ids[hobby].active:
                hobby_bool = False
                break
        if hobby_bool:
            return False
        for hobby in ("no_hobbies", "sport_hobby", "tourism_hobby", "dance_hobby", "hunting_hobby",
                      "art_hobby", "vocals_hobby", "collecting_hobby", "programming_hobby",
                      "construction_hobby", "walk_hobby", "shopping_hobby", "film_hobby",
                      "video_games_hobby", "meditation_hobby", "other_hobby"):
            user_data[hobby] = int(self.ids[hobby].active)

        if not self.ids.hours_a_week_for_hobbies.text:
            return False
        user_data["hours_a_week_for_hobbies"] = self.ids.hours_a_week_for_hobbies.text

        if not self.ids.hours_of_sleep.text:
            return False
        user_data["hours_of_sleep"] = self.ids.hours_of_sleep.text

        time_waster_bool = True
        for time_waster in ("no_time_wasters", "TV_addiction_time_waster",
                            "internet_addiction_time_waster", "chatter_time_waster",
                            "smoking_time_waster", "other_time_waster"):
            if self.ids[time_waster].active:
                time_waster_bool = False
                break
        if time_waster_bool:
            return False
        for time_waster in ("no_time_wasters", "TV_addiction_time_waster",
                            "internet_addiction_time_waster", "chatter_time_waster",
                            "smoking_time_waster", "other_time_waster"):
            user_data[time_waster] = int(self.ids[time_waster].active)

        if not self.ids.hours_on_a_weekday_for_time_wasters.text:
            return False
        user_data["hours_on_a_weekday_for_time_wasters"] = self.ids.hours_on_a_weekday_for_time_wasters.text

        if not self.ids.hours_on_a_day_off_for_time_wasters.text:
            return False
        user_data["hours_on_a_day_off_for_time_wasters"] = self.ids.hours_on_a_day_off_for_time_wasters.text

        if not self.ids.visit_store_once_a_week.text:
            return False
        user_data["visit_store_once_a_week"] = self.ids.visit_store_once_a_week.text

        if not self.ids.minutes_on_the_way_to_the_store.text:
            return False
        user_data["minutes_on_the_way_to_the_store"] = self.ids.minutes_on_the_way_to_the_store.text

        if not self.ids.minutes_to_visit_shop.text:
            return False
        user_data["minutes_to_visit_shop"] = self.ids.minutes_to_visit_shop.text

        if not self.ids.hours_per_week_per_family.text:
            return False
        user_data["hours_per_week_per_family"] = self.ids.hours_per_week_per_family.text

        if not self.ids.hours_per_week_for_pets.text:
            return False
        user_data["hours_per_week_for_pets"] = self.ids.hours_per_week_for_pets.text

        if not self.ids.hours_per_week_for_cleaning.text:
            return False
        user_data["hours_per_week_for_cleaning"] = self.ids.hours_per_week_for_cleaning.text

        if not self.ids.minutes_per_day_per_shower.text:
            return False
        user_data["minutes_per_day_per_shower"] = self.ids.minutes_per_day_per_shower.text

        if not self.ids.minutes_after_sleep.text:
            return False
        user_data["minutes_after_sleep"] = self.ids.minutes_after_sleep.text

        if not self.ids.minutes_before_sleep.text:
            return False
        user_data["minutes_before_sleep"] = self.ids.minutes_before_sleep.text

        if not self.ids.hours_a_day_for_cooking.text:
            return False
        user_data["hours_a_day_for_cooking"] = self.ids.hours_a_day_for_cooking.text

        if not self.ids.minutes_for_breakfast.text:
            return False
        user_data["minutes_for_breakfast"] = self.ids.minutes_for_breakfast.text

        if not self.ids.minutes_for_lunch.text:
            return False
        user_data["minutes_for_lunch"] = self.ids.minutes_for_lunch.text

        if not self.ids.minutes_for_dinner.text:
            return False
        user_data["minutes_for_dinner"] = self.ids.minutes_for_dinner.text

        if not self.ids.hours_per_month_per_hairdresser.text:
            return False
        user_data["hours_per_month_per_hairdresser"] = self.ids.hours_per_month_per_hairdresser.text

        if not self.ids.hours_per_month_for_beauty_workers.text:
            return False
        user_data["hours_per_month_for_beauty_workers"] = self.ids.hours_per_month_for_beauty_workers.text

        if not self.ids.hours_per_week_for_other_activities.text:
            return False
        user_data["hours_per_week_for_other_activities"] = self.ids.hours_per_week_for_other_activities.text


        return True

class RegistrationMoneyScreen(Screen):
    started = False
    
    def on_parent(self, *args):
        if not self.started:
            self.old_window_size = list(Window.size)

            with self.canvas.before:
                Color(1, 1, 0, 1)
                self.points = []
                self.making_stars = Clock.schedule_interval(self.make_stars, 1)
            self.started = True

        else:
            self.ids.state.color = 1, 1, 0, 1
            self.ids.state.text = "Финансы"

    def make_stars(self, *args):
        with self.canvas.before:
            new_point = Ellipse(pos = [randint(0, Window.size[0]), 0], size = (1, 1))
            self.points.append(new_point)
            if len(self.points) >= 61:
                self.canvas.before.remove(self.points[0])
                self.points = self.points[1:]

            anim = Animation(pos = (randint(0, Window.size[0]), Window.size[1] + 1), duration = 60)
            anim.start(new_point)

    def write_data(self):
        global user_data

        for currency in ("currency_ruble", "currency_hryvnia", "currency_tenge", "currency_tugrik",
                         "currency_yuan", "currency_dollar", "currency_euro", "currency_pound_sterling"):
            if self.ids[currency].active:
                user_data["currency"] = currency[9:]
                break

        if user_data["study_at_school"] or user_data["study_at_university"]:
            if not self.ids.scholarship_per_month.text:
                return False
            user_data["scholarship_per_month"] = self.ids.scholarship_per_month.text
        else:
            user_data["scholarship_per_month"] = "0"

        if user_data["working"]:
            if not self.ids.salary_per_month.text:
                return False
            user_data["salary_per_month"] = self.ids.salary_per_month.text

            if not self.ids.premiums_per_year.text:
                return False
            user_data["premiums_per_year"] = self.ids.premiums_per_year.text

            if not self.ids.premium_amount.text:
                return False
            user_data["premium_amount"] = self.ids.premium_amount.text
        else:
            user_data["salary_per_month"] = "0"
            user_data["premiums_per_year"] = "0"
            user_data["premium_amount"] = "0"

        if user_data["personal_business"]:
            if not self.ids.number_of_businesses.text:
                return False
            user_data["number_of_businesses"] = self.ids.number_of_businesses.text

            if not self.ids.net_income_from_business_per_month.text:
                return False
            user_data["net_income_from_business_per_month"] = self.ids.net_income_from_business_per_month.text
        else:
            user_data["number_of_businesses"] = "0"
            user_data["net_income_from_business_per_month"] = "0"

        if not self.ids.other_financial_receipts_per_month.text:
            return False
        user_data["other_financial_receipts_per_month"] = self.ids.other_financial_receipts_per_month.text

        if user_data["sport_hobby"]:
            if not self.ids.sports_funds_per_month.text:
                return False
            user_data["sports_funds_per_month"] = self.ids.sports_funds_per_month.text
        else:
            user_data["sports_funds_per_month"] = "0"

        if user_data["tourism_hobby"]:
            if not self.ids.tourism_funds_per_month.text:
                return False
            user_data["tourism_funds_per_month"] = self.ids.tourism_funds_per_month.text
        else:
            user_data["tourism_funds_per_month"] = "0"

        if user_data["dance_hobby"]:
            if not self.ids.dance_funds_per_month.text:
                return False
            user_data["dance_funds_per_month"] = self.ids.dance_funds_per_month.text
        else:
            user_data["dance_funds_per_month"] = "0"

        if user_data["hunting_hobby"]:
            if not self.ids.hunting_funds_per_month.text:
                return False
            user_data["hunting_funds_per_month"] = self.ids.hunting_funds_per_month.text
        else:
            user_data["hunting_funds_per_month"] = "0"

        if user_data["art_hobby"]:
            if not self.ids.art_funds_per_month.text:
                return False
            user_data["art_funds_per_month"] = self.ids.art_funds_per_month.text
        else:
            user_data["art_funds_per_month"] = "0"

        if user_data["vocals_hobby"]:
            if not self.ids.vocals_funds_per_month.text:
                return False
            user_data["vocals_funds_per_month"] = self.ids.vocals_funds_per_month.text
        else:
            user_data["vocals_funds_per_month"] = "0"

        if user_data["collecting_hobby"]:
            if not self.ids.collecting_funds_per_month.text:
                return False
            user_data["collecting_funds_per_month"] = self.ids.collecting_funds_per_month.text
        else:
            user_data["collecting_funds_per_month"] = "0"

        if user_data["programming_hobby"]:
            if not self.ids.programming_funds_per_month.text:
                return False
            user_data["programming_funds_per_month"] = self.ids.programming_funds_per_month.text
        else:
            user_data["programming_funds_per_month"] = "0"

        if user_data["construction_hobby"]:
            if not self.ids.construction_funds_per_month.text:
                return False
            user_data["construction_funds_per_month"] = self.ids.construction_funds_per_month.text
        else:
            user_data["construction_funds_per_month"] = "0"

        if user_data["walk_hobby"]:
            if not self.ids.walk_funds_per_month.text:
                return False
            user_data["walk_funds_per_month"] = self.ids.walk_funds_per_month.text
        else:
            user_data["walk_funds_per_month"] = "0"

        if user_data["shopping_hobby"]:
            if not self.ids.shopping_funds_per_month.text:
                return False
            user_data["shopping_funds_per_month"] = self.ids.shopping_funds_per_month.text
        else:
            user_data["shopping_funds_per_month"] = "0"

        if user_data["film_hobby"]:
            if not self.ids.film_funds_per_month.text:
                return False
            user_data["film_funds_per_month"] = self.ids.film_funds_per_month.text
        else:
            user_data["film_funds_per_month"] = "0"

        if user_data["video_games_hobby"]:
            if not self.ids.video_games_funds_per_month.text:
                return False
            user_data["video_games_funds_per_month"] = self.ids.video_games_funds_per_month.text
        else:
            user_data["video_games_funds_per_month"] = "0"

        if user_data["meditation_hobby"]:
            if not self.ids.meditation_funds_per_month.text:
                return False
            user_data["meditation_funds_per_month"] = self.ids.meditation_funds_per_month.text
        else:
            user_data["meditation_funds_per_month"] = "0"

        if user_data["other_hobby"]:
            if not self.ids.funds_for_other_types_of_hobbies_per_month.text:
                return False
            user_data["funds_for_other_types_of_hobbies_per_month"] = self.ids.funds_for_other_types_of_hobbies_per_month.text
        else:
            user_data["funds_for_other_types_of_hobbies_per_month"] = "0"

        if int(user_data["minutes_for_self_education_per_day"]):
            if not self.ids.self_education_funds_per_month.text:
                return False
            user_data["self_education_funds_per_month"] = self.ids.self_education_funds_per_month.text
        else:
            user_data["self_education_funds_per_month"] = "0"

        if user_data["TV_addiction_time_waster"]:
            if not self.ids.TV_funds_per_month.text:
                return False
            user_data["TV_funds_per_month"] = self.ids.TV_funds_per_month.text
        else:
            user_data["TV_funds_per_month"] = "0"

        if user_data["internet_addiction_time_waster"]:
            if not self.ids.internet_resources_funds_per_month.text:
                return False
            user_data["internet_resources_funds_per_month"] = self.ids.internet_resources_funds_per_month.text
        else:
            user_data["internet_resources_funds_per_month"] = "0"

        if user_data["smoking_time_waster"]:
            if not self.ids.smoking_funds_per_month.text:
                return False
            user_data["smoking_funds_per_month"] = self.ids.smoking_funds_per_month.text
        else:
            user_data["smoking_funds_per_month"] = "0"

        if user_data["other_time_waster"]:
            if not self.ids.funds_for_other_types_of_time_wasters_per_month.text:
                return False
            user_data["funds_for_other_types_of_time_wasters_per_month"] = self.ids.funds_for_other_types_of_time_wasters_per_month.text
        else:
            user_data["funds_for_other_types_of_time_wasters_per_month"] = "0"
            
        if not self.ids.grocery_shopping_allowance_per_week.text:
            return False
        user_data["grocery_shopping_allowance_per_week"] = self.ids.grocery_shopping_allowance_per_week.text
            
        if not self.ids.funds_for_shopping_at_a_household_store_per_week.text:
            return False
        user_data["funds_for_shopping_at_a_household_store_per_week"] = self.ids.funds_for_shopping_at_a_household_store_per_week.text
            
        if not self.ids.funds_for_a_hairdresser_per_month.text:
            return False
        user_data["funds_for_a_hairdresser_per_month"] = self.ids.funds_for_a_hairdresser_per_month.text
            
        if not self.ids.funds_for_other_beauty_workers_per_month.text:
            return False
        user_data["funds_for_other_beauty_workers_per_month"] = self.ids.funds_for_other_beauty_workers_per_month.text
            
        if not self.ids.internet_funds_per_month.text:
            return False
        user_data["internet_funds_per_month"] = self.ids.internet_funds_per_month.text
            
        if not self.ids.other_funds_per_month.text:
            return False
        user_data["other_funds_per_month"] = self.ids.other_funds_per_month.text


        return True

class RegistrationConfirmScreen(Screen):
    started = False

    def on_parent(self, *args):
        if not self.started:
            self.old_window_size = list(Window.size)
            self.big_ellipse_radius = Window.size[0]

            with self.canvas.before:
                Color(1, .8, 0, 1)

                self.big_ellipse = Ellipse(pos = (Window.size[0] * .5 - self.big_ellipse_radius, Window.size[1]),
                                    size = (2 * self.big_ellipse_radius, 2 * self.big_ellipse_radius))

                anim = Animation(pos = (self.big_ellipse.pos[0], self.big_ellipse.pos[1] - Window.size[1] * .35),
                                duration = 2, t = "in_out_cubic")
                anim.start(self.big_ellipse)

                self.points = []
                self.making_stars = Clock.schedule_interval(self.make_stars, 1/10)
            self.started = True

        else:
            with self.canvas.before:
                self.big_ellipse = Ellipse(pos = (Window.size[0] * .5 - self.big_ellipse_radius,
                                                  Window.size[1] - Window.size[1] * .35),
                                           size = (2 * self.big_ellipse_radius, 2 * self.big_ellipse_radius))
            self.on_size()
    
    def on_size(self, *args):
        self.big_ellipse_radius = Window.size[0]
        self.big_ellipse.pos = (Window.size[0] * .5 - self.big_ellipse_radius,
                                Window.size[1] - Window.size[1] * .35)
        self.big_ellipse.size = (2 * self.big_ellipse_radius, 2 * self.big_ellipse_radius)

        self.new_window_size = list(Window.size)
        difference_of_window_size = [self.new_window_size[0] / self.old_window_size[0],
                                    self.new_window_size[1] / self.old_window_size[1]]
        for point in self.points:
            point.pos = [point.pos[0] * difference_of_window_size[0], point.pos[1] * difference_of_window_size[1]]

        self.old_window_size = self.new_window_size

    def make_stars(self, *args):
        with self.canvas.before:
            new_point = Ellipse(pos = [self.big_ellipse.pos[0] + self.big_ellipse_radius,
                                self.big_ellipse.pos[1] + self.big_ellipse_radius], size = (1, 1))
            self.points.append(new_point)
            if len(self.points) >= 1500:
                self.making_stars.cancel()

            anim = Animation(pos = (randint(0, Window.size[0]), (randint(0, Window.size[1]))), duration = 3)
            anim.start(new_point)

    def clear_canvas(self):
        self.canvas.before.remove(self.big_ellipse)

    def complete_registration(self):
        if not self.ids.new_login.text or not self.ids.new_password.text or not self.ids.confirm_new_password.text:
            return False
        if self.ids.new_password.text != self.ids.confirm_new_password.text:
            return False

        user_data["user_login"] = self.ids.new_login.text
        user_data["user_password"] = self.ids.new_password.text

        now = datetime.datetime.now()
        user_data["date_day"] = now.day
        user_data["date_month"] = now.month
        user_data["date_year"] = now.year
        user_data["time_hour"] = now.hour
        user_data["time_minute"] = now.minute
        user_data["time_second"] = now.second

        inputs = []
        for key in user_data.keys():
            inputs.append(user_data[key])

        try:
            with sqlite3.connect('db.db') as db:
                cursor = db.cursor()
                cursor.execute(f"INSERT INTO users VALUES({'?, ' * 96}?)", inputs)
                db.commit()
            update_current_user(self.ids.new_login.text)

            return True
        except:
            return False

class CurrentTimeAndMoneyScreen(Screen):
    started = False

    def on_parent(self, *args):
        if not self.started:
            self.old_window_size = list(Window.size)
            self.big_ellipse_radius = Window.size[1]

            with self.canvas.before:
                Color(0, .855, .95, 1)

                self.big_ellipse = Ellipse(pos = (-self.big_ellipse_radius * 2, Window.size[1] * .5 - self.big_ellipse_radius),
                                    size = (2 * self.big_ellipse_radius, 2 * self.big_ellipse_radius))

                anim = Animation(pos = (-self.big_ellipse_radius * 2 + Window.size[0] * .35, self.big_ellipse.pos[1]),
                                duration = 2, t = "in_out_cubic")
                anim.start(self.big_ellipse)

            Clock.schedule_interval(self.main_loop, .1)
            self.started = True

        else:
            with self.canvas.before:
                self.big_ellipse = Ellipse(pos = (-self.big_ellipse_radius * 2 + Window.size[0] * .35,
                                                  self.big_ellipse.pos[1]),
                                           size = (2 * self.big_ellipse_radius, 2 * self.big_ellipse_radius))
            self.on_size()

    def main_loop(self, *args):
        now = datetime.datetime.now()

        if 6 <= now.hour <= 11:
            greeting = "Доброе утро"
        elif 12 <= now.hour <= 17:
            greeting = "Добрый день"
        elif 18 <= now.hour <= 21:
            greeting = "Добрый вечер"
        elif (22 <= now.hour <= 23) or (0 <= now.hour <= 5):
            greeting = "Доброй ночи"

        self.ids.greeting.text = greeting + f", {user_data['user_name']}"
        self.ids.date.text = weekdays[now.weekday()] + ", [color=00e5ff][b]" + str(now.day) + "[/color][/b] " +  monthes[now.month]

        if user_data["currency"] != "ruble":
            self.ids.income.font_name = "data/fonts/Lato.ttf"
        else:
            self.ids.income.font_name = "Roboto"

        money_plus = (user_data["scholarship_per_month"] + user_data["salary_per_month"] \
                     + user_data["premiums_per_year"] * user_data["premium_amount"] / 12 + user_data["net_income_from_business_per_month"] \
                     + user_data["other_financial_receipts_per_month"]) / 30 * days_have_passed

        money_minus = ((user_data["sports_funds_per_month"] + user_data["tourism_funds_per_month"] + user_data["dance_funds_per_month"] + \
                      user_data["hunting_funds_per_month"] + user_data["art_funds_per_month"] + user_data["vocals_funds_per_month"] \
                      + user_data["collecting_funds_per_month"] + user_data["programming_funds_per_month"] \
                      + user_data["construction_funds_per_month"] + user_data["walk_funds_per_month"] + user_data["shopping_funds_per_month"] \
                      + user_data["film_funds_per_month"] + user_data["video_games_funds_per_month"] + user_data["meditation_funds_per_month"] \
                      + user_data["funds_for_other_types_of_hobbies_per_month"] + user_data["self_education_funds_per_month"] \
                      + user_data["TV_funds_per_month"] + user_data["internet_resources_funds_per_month"] + user_data["smoking_funds_per_month"] \
                      + user_data["funds_for_other_types_of_time_wasters_per_month"] + user_data["funds_for_a_hairdresser_per_month"] \
                      + user_data["funds_for_other_beauty_workers_per_month"] + user_data["internet_funds_per_month"] \
                      + user_data["other_funds_per_month"]) / 30 + (user_data["grocery_shopping_allowance_per_week"] \
                      + user_data["funds_for_shopping_at_a_household_store_per_week"]) / 7) * days_have_passed

        profitable_activity = (user_data["days_a_week_at_work"] / 7) * (user_data["hours_a_day_work"]) * days_have_passed

        self.ids.income.text = str(round(money_plus - money_minus, 2)) \
                               + "[color=002e33]" + currency__currency_symbol[user_data["currency"]] + "[/color]"
        self.ids.profitable_activity.text = str(int(profitable_activity)) + "[color=002e33]" + " ч." + "[/color]"
    
    def on_size(self, *args):
        self.big_ellipse_radius = Window.size[1]
        self.big_ellipse.pos = (-self.big_ellipse_radius * 2 + Window.size[0] * .35,
                                Window.size[1] * .5 - self.big_ellipse_radius)
        self.big_ellipse.size = (2 * self.big_ellipse_radius, 2 * self.big_ellipse_radius)

        self.new_window_size = list(Window.size)
        difference_of_window_size = [self.new_window_size[0] / self.old_window_size[0],
                                    self.new_window_size[1] / self.old_window_size[1]]

        self.old_window_size = self.new_window_size


class CurrentMoneyScreen(Screen):
    started = False

    def on_parent(self, *args):
        if not self.started:
            with self.ids.cash_flow_canvas.canvas:
                Color(0, 1, 0, 1)
                self.income_rectangle = Rectangle(pos = self.ids.cash_flow_canvas.pos, size = self.ids.cash_flow_canvas.size)

                Color(1, 0, 0, 1)
                self.expenses_rectangle = Rectangle(pos = self.ids.cash_flow_canvas.pos, size = self.ids.cash_flow_canvas.size)

                Color(1, 1, 0, 1)
                self.cash_flow_rectangle = Rectangle(pos = self.ids.cash_flow_canvas.pos, size = self.ids.cash_flow_canvas.size)

            Clock.schedule_interval(self.main_loop, .1)
            self.started = True

    def main_loop(self, *args):
        if user_data["currency"] != "ruble":
            for ident in self.ids:
                self.ids[ident].font_name = "data/fonts/Lato.ttf"
        else:
            for ident in self.ids:
                self.ids[ident].font_name = "Roboto"

        money_income = (user_data["scholarship_per_month"] + user_data["salary_per_month"] \
                     + user_data["premiums_per_year"] * user_data["premium_amount"] / 12 + user_data["net_income_from_business_per_month"] \
                     + user_data["other_financial_receipts_per_month"]) / 30
        money_plus = money_income * days_have_passed

        money_expenses = (user_data["sports_funds_per_month"] + user_data["tourism_funds_per_month"] + user_data["dance_funds_per_month"] + \
                      user_data["hunting_funds_per_month"] + user_data["art_funds_per_month"] + user_data["vocals_funds_per_month"] \
                      + user_data["collecting_funds_per_month"] + user_data["programming_funds_per_month"] \
                      + user_data["construction_funds_per_month"] + user_data["walk_funds_per_month"] + user_data["shopping_funds_per_month"] \
                      + user_data["film_funds_per_month"] + user_data["video_games_funds_per_month"] + user_data["meditation_funds_per_month"] \
                      + user_data["funds_for_other_types_of_hobbies_per_month"] + user_data["self_education_funds_per_month"] \
                      + user_data["TV_funds_per_month"] + user_data["internet_resources_funds_per_month"] + user_data["smoking_funds_per_month"] \
                      + user_data["funds_for_other_types_of_time_wasters_per_month"] + user_data["funds_for_a_hairdresser_per_month"] \
                      + user_data["funds_for_other_beauty_workers_per_month"] + user_data["internet_funds_per_month"] \
                      + user_data["other_funds_per_month"]) / 30 + (user_data["grocery_shopping_allowance_per_week"] \
                      + user_data["funds_for_shopping_at_a_household_store_per_week"]) / 7
        money_minus = money_expenses * days_have_passed

        cash_flow = money_income - money_expenses

        with self.ids.cash_flow_canvas.canvas:
            if money_income > money_expenses:
                self.income_rectangle.size = self.ids.cash_flow_canvas.size[0] / 2, self.ids.cash_flow_canvas.size[1]
                self.income_rectangle.pos = (self.ids.cash_flow_canvas.pos[0] + self.ids.cash_flow_canvas.size[0] / 2,
                                             self.ids.cash_flow_canvas.pos[1])

                self.expenses_rectangle.size = self.income_rectangle.size[0] * (money_expenses / money_income), self.ids.cash_flow_canvas.size[1]
                self.expenses_rectangle.pos = self.income_rectangle.pos[0] - self.expenses_rectangle.size[0], self.income_rectangle.pos[1]

                self.cash_flow_rectangle.size = self.income_rectangle.size[0] - self.expenses_rectangle.size[0], self.income_rectangle.size[1]
                self.cash_flow_rectangle.pos = self.income_rectangle.pos

            elif money_income < money_expenses:
                self.expenses_rectangle.size = self.ids.cash_flow_canvas.size[0] / 2, self.ids.cash_flow_canvas.size[1]
                self.expenses_rectangle.pos = self.ids.cash_flow_canvas.pos

                self.income_rectangle.size = self.expenses_rectangle.size[0] * (money_income / money_expenses), self.ids.cash_flow_canvas.size[1]
                self.income_rectangle.pos = (self.ids.cash_flow_canvas.pos[0] + self.ids.cash_flow_canvas.size[0] / 2,
                                             self.ids.cash_flow_canvas.pos[1])

                self.cash_flow_rectangle.size = self.expenses_rectangle.size[0] - self.income_rectangle.size[0], self.expenses_rectangle.size[1]
                self.cash_flow_rectangle.pos = self.income_rectangle.pos[0] - self.cash_flow_rectangle.size[0], self.expenses_rectangle.pos[1]

            else:
                self.expenses_rectangle.size = self.ids.cash_flow_canvas.size[0] / 2, self.ids.cash_flow_canvas.size[1]
                self.expenses_rectangle.pos = self.ids.cash_flow_canvas.pos

                self.income_rectangle.size = self.ids.cash_flow_canvas.size[0] / 2, self.ids.cash_flow_canvas.size[1]
                self.income_rectangle.pos = (self.ids.cash_flow_canvas.pos[0] + self.ids.cash_flow_canvas.size[0] / 2,
                                             self.ids.cash_flow_canvas.pos[1])

                self.cash_flow_rectangle.size = 0, 0
                self.cash_flow_rectangle.pos = self.income_rectangle.pos
                

        self.ids.income.text = str(round(money_income * 30, 2)) + currency__currency_symbol[user_data["currency"]]
        self.ids.expenses.text = str(round(money_expenses * 30, 2)) + currency__currency_symbol[user_data["currency"]]
        self.ids.cash_flow.text = str(round((cash_flow) * 30, 2)) + currency__currency_symbol[user_data["currency"]]

        scholarship_plus = user_data["scholarship_per_month"] / 30 * days_have_passed
        self.ids.scholarship.text = str(round(scholarship_plus, 2)) \
                                    + currency__currency_symbol[user_data["currency"]] + f"\n({round(scholarship_plus / money_plus * 100, 2)}%)"

        salary_plus = user_data["salary_per_month"] / 30 * days_have_passed
        self.ids.salary.text = str(round(salary_plus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(salary_plus / money_plus * 100, 2)}%)"

        premiums_plus = user_data["premiums_per_year"] * user_data["premium_amount"] / 360 * days_have_passed
        self.ids.premiums.text = str(round(premiums_plus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(premiums_plus / money_plus * 100, 2)}%)"

        business_plus = user_data["net_income_from_business_per_month"] / 30 * days_have_passed
        self.ids.business.text = str(round(business_plus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(business_plus / money_plus * 100, 2)}%)"

        other_financial_receipts_plus = user_data["other_financial_receipts_per_month"] / 30 * days_have_passed
        self.ids.other_financial_receipts.text = str(round(other_financial_receipts_plus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(other_financial_receipts_plus / money_plus * 100, 2)}%)"



        sport_minus = user_data["sports_funds_per_month"] / 30 * days_have_passed
        self.ids.sport.text = str(round(sport_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(sport_minus / money_minus * 100, 2)}%)"

        tourism_minus = user_data["tourism_funds_per_month"] / 30 * days_have_passed
        self.ids.tourism.text = str(round(sport_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(tourism_minus / money_minus * 100, 2)}%)"

        dance_minus = user_data["dance_funds_per_month"] / 30 * days_have_passed
        self.ids.dance.text = str(round(dance_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(dance_minus / money_minus * 100, 2)}%)"

        hunting_minus = user_data["hunting_funds_per_month"] / 30 * days_have_passed
        self.ids.hunting.text = str(round(hunting_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(hunting_minus / money_minus * 100, 2)}%)"

        art_minus = user_data["art_funds_per_month"] / 30 * days_have_passed
        self.ids.art.text = str(round(art_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(art_minus / money_minus * 100, 2)}%)"

        vocal_minus = user_data["vocals_funds_per_month"] / 30 * days_have_passed
        self.ids.vocal.text = str(round(vocal_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(vocal_minus / money_minus * 100, 2)}%)"

        collecting_minus = user_data["collecting_funds_per_month"] / 30 * days_have_passed
        self.ids.collecting.text = str(round(collecting_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(collecting_minus / money_minus * 100, 2)}%)"

        programming_minus = user_data["programming_funds_per_month"] / 30 * days_have_passed
        self.ids.programming.text = str(round(programming_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(programming_minus / money_minus * 100, 2)}%)"

        construction_minus = user_data["construction_funds_per_month"] / 30 * days_have_passed
        self.ids.construction.text = str(round(construction_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(construction_minus / money_minus * 100, 2)}%)"

        walk_minus = user_data["walk_funds_per_month"] / 30 * days_have_passed
        self.ids.walk.text = str(round(walk_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(walk_minus / money_minus * 100, 2)}%)"

        shopping_minus = user_data["shopping_funds_per_month"] / 30 * days_have_passed
        self.ids.shopping.text = str(round(shopping_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(shopping_minus / money_minus * 100, 2)}%)"

        film_minus = user_data["film_funds_per_month"] / 30 * days_have_passed
        self.ids.film.text = str(round(film_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(film_minus / money_minus * 100, 2)}%)"

        video_games_minus = user_data["video_games_funds_per_month"] / 30 * days_have_passed
        self.ids.video_games.text = str(round(video_games_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(video_games_minus / money_minus * 100, 2)}%)"

        meditation_minus = user_data["meditation_funds_per_month"] / 30 * days_have_passed
        self.ids.meditation.text = str(round(meditation_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(meditation_minus / money_minus * 100, 2)}%)"

        other_types_of_hobbies_minus = user_data["funds_for_other_types_of_hobbies_per_month"] / 30 * days_have_passed
        self.ids.other_types_of_hobbies.text = str(round(other_types_of_hobbies_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(other_types_of_hobbies_minus / money_minus * 100, 2)}%)"

        self_education_minus = user_data["self_education_funds_per_month"] / 30 * days_have_passed
        self.ids.self_education.text = str(round(self_education_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(self_education_minus / money_minus * 100, 2)}%)"

        TV_minus = user_data["TV_funds_per_month"] / 30 * days_have_passed
        self.ids.TV.text = str(round(TV_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(TV_minus / money_minus * 100, 2)}%)"

        internet_resources_minus = user_data["internet_resources_funds_per_month"] / 30 * days_have_passed
        self.ids.internet_resources.text = str(round(internet_resources_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(internet_resources_minus / money_minus * 100, 2)}%)"

        smoking_minus = user_data["smoking_funds_per_month"] / 30 * days_have_passed
        self.ids.smoking.text = str(round(smoking_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(smoking_minus / money_minus * 100, 2)}%)"

        other_types_of_time_wasters_minus = user_data["funds_for_other_types_of_time_wasters_per_month"] / 30 * days_have_passed
        self.ids.other_types_of_time_wasters.text = str(round(other_types_of_time_wasters_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] \
                                 + f"\n({round(other_types_of_time_wasters_minus / money_minus * 100, 2)}%)"

        hairdresser_minus = user_data["funds_for_a_hairdresser_per_month"] / 30 * days_have_passed
        self.ids.hairdresser.text = str(round(hairdresser_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(hairdresser_minus / money_minus * 100, 2)}%)"

        other_beauty_workers_minus = user_data["funds_for_other_beauty_workers_per_month"] / 30 * days_have_passed
        self.ids.other_beauty_workers.text = str(round(other_beauty_workers_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(other_beauty_workers_minus / money_minus * 100, 2)}%)"

        internet_minus = user_data["internet_funds_per_month"] / 30 * days_have_passed
        self.ids.internet.text = str(round(internet_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(internet_minus / money_minus * 100, 2)}%)"

        grocery_shopping_minus = user_data["grocery_shopping_allowance_per_week"] / 7 * days_have_passed
        self.ids.grocery_shopping.text = str(round(grocery_shopping_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(grocery_shopping_minus / money_minus * 100, 2)}%)"

        shopping_at_a_household_store_minus = user_data["funds_for_shopping_at_a_household_store_per_week"] / 7 * days_have_passed
        self.ids.shopping_at_a_household_store.text = str(round(shopping_at_a_household_store_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] \
                                 + f"\n({round(shopping_at_a_household_store_minus / money_minus * 100, 2)}%)"

        other_funds_minus = user_data["other_funds_per_month"] / 30 * days_have_passed
        self.ids.other_funds.text = str(round(other_funds_minus, 2)) \
                                 + currency__currency_symbol[user_data["currency"]] + f"\n({round(other_funds_minus / money_minus * 100, 2)}%)"

class CurrentTimeScreen(Screen):
    started = False

    def on_parent(self, *args):
        if not self.started:
            Clock.schedule_interval(self.main_loop, .1)
            self.started = True

    def main_loop(self, *args):
        hours_have_passed = days_have_passed * 24
        self.ids.hours_have_passed.text = str(round(hours_have_passed, 2)) + " ч."

        profitable_activity = user_data["days_a_week_at_work"] / 7 * (user_data["hours_a_day_work"] \
        + (user_data["minutes_travel_time_to_work"] + user_data["minutes_travel_time_from_work"]) / 60) * days_have_passed
        self.ids.work_time.text = str(round(profitable_activity, 2)) + " ч." + f"\n({round(profitable_activity / hours_have_passed * 100, 2)}%)"

        self_education = user_data["minutes_for_self_education_per_day"] / 60 * days_have_passed
        self.ids.self_education.text = str(round(self_education, 2)) + " ч." + f"\n({round(self_education / hours_have_passed * 100, 2)}%)"

        hobby = user_data["hours_a_week_for_hobbies"] / 7 * days_have_passed
        self.ids.hobby.text = str(round(hobby, 2)) + " ч." + f"\n({round(hobby / hours_have_passed * 100, 2)}%)"

        sleep = user_data["hours_of_sleep"] * days_have_passed
        self.ids.sleep.text = str(round(sleep, 2)) + " ч." + f"\n({round(sleep / hours_have_passed * 100, 2)}%)"

        family = user_data["hours_per_week_per_family"] / 7 * days_have_passed
        self.ids.family.text = str(round(family, 2)) + " ч." + f"\n({round(family / hours_have_passed * 100, 2)}%)"

        pets = user_data["hours_per_week_for_pets"] / 7 * days_have_passed
        self.ids.pets.text = str(round(pets, 2)) + " ч." + f"\n({round(pets / hours_have_passed * 100, 2)}%)"

        time_wasters = (user_data["hours_on_a_day_off_for_time_wasters"] * 5 + user_data["hours_on_a_weekday_for_time_wasters"] * 2) \
                       / 7 * days_have_passed
        self.ids.time_wasters.text = str(round(time_wasters, 2)) + " ч." + f"\n({round(time_wasters / hours_have_passed * 100, 2)}%)"

        shops = user_data["visit_store_once_a_week"] * (user_data["minutes_on_the_way_to_the_store"] / 30 + user_data["minutes_to_visit_shop"] / 60)\
                / 7 * days_have_passed
        self.ids.shops.text = str(round(shops, 2)) + " ч." + f"\n({round(shops / hours_have_passed * 100, 2)}%)"

        cleaning = user_data["hours_per_week_for_cleaning"] / 7 * days_have_passed
        self.ids.cleaning.text = str(round(cleaning, 2)) + " ч." + f"\n({round(cleaning / hours_have_passed * 100, 2)}%)"

        shower = user_data["minutes_per_day_per_shower"] / 60 * days_have_passed
        self.ids.shower.text = str(round(shower, 2)) + " ч." + f"\n({round(shower / hours_have_passed * 100, 2)}%)"

        after_sleep = user_data["minutes_after_sleep"] / 60 * days_have_passed
        self.ids.after_sleep.text = str(round(after_sleep, 2)) + " ч." + f"\n({round(after_sleep / hours_have_passed * 100, 2)}%)"

        before_sleep = user_data["minutes_before_sleep"] / 60 * days_have_passed
        self.ids.before_sleep.text = str(round(before_sleep, 2)) + " ч." + f"\n({round(before_sleep / hours_have_passed * 100, 2)}%)"

        cooking = user_data["hours_a_day_for_cooking"] * days_have_passed
        self.ids.cooking.text = str(round(cooking, 2)) + " ч." + f"\n({round(cooking / hours_have_passed * 100, 2)}%)"

        meal = (user_data["minutes_for_breakfast"] + user_data["minutes_for_lunch"] + user_data["minutes_for_dinner"]) / 60 * days_have_passed
        self.ids.meal.text = str(round(meal, 2)) + " ч." + f"\n({round(meal / hours_have_passed * 100, 2)}%)"

        hairdresser = user_data["hours_per_month_per_hairdresser"] / 30 * days_have_passed
        self.ids.hairdresser.text = str(round(hairdresser, 2)) + " ч." + f"\n({round(hairdresser / hours_have_passed * 100, 2)}%)"

        beauty_sphere = user_data["hours_per_month_for_beauty_workers"] / 30 * days_have_passed
        self.ids.beauty_sphere.text = str(round(beauty_sphere, 2)) + " ч." + f"\n({round(beauty_sphere / hours_have_passed * 100, 2)}%)"

        other = user_data["hours_per_week_for_other_activities"] / 7 * days_have_passed
        self.ids.other.text = str(round(other, 2)) + " ч." + f"\n({round(other / hours_have_passed * 100, 2)}%)"

        free_time = hours_have_passed - profitable_activity - self_education - hobby - sleep - family - pets \
                    - time_wasters - shops - cleaning - shower - after_sleep - before_sleep - cooking - meal - hairdresser - beauty_sphere - other
        self.ids.free_time.text = str(round(free_time, 2)) + " ч." + f"\n({round(free_time / hours_have_passed * 100, 2)}%)"

        if free_time > 0:
            self.ids.free_time.color = 0, 1, 0, 1
        elif free_time < 0:
            self.ids.free_time.color = 1, 0, 0, 1
        else:
            self.ids.free_time.color = 1, 1, 1, 1

class SettingsScreen(Screen):
    pass

class PersonalDataSettingsScreen(Screen):
    def on_parent(self, *args):
        Clock.schedule_once(self.fill_data, .1)

    def fill_data(self, *args):
        self.ids.state.color = 0, .9, 1, 1
        self.ids.state.text = "Общие данные"

        self.ids.user_name.text = user_data['user_name']
        self.ids.date_of_birth.text = user_data['date_of_birth']

        for work_type in ("no_working", "study_at_school", "study_at_university",
                          "working", "personal_business", "other_work"):
            if user_data[work_type]:
                self.ids[work_type].active = True

        for hobby in ("no_hobbies", "sport_hobby", "tourism_hobby", "dance_hobby", "hunting_hobby",
                      "art_hobby", "vocals_hobby", "collecting_hobby", "programming_hobby",
                      "construction_hobby", "walk_hobby", "shopping_hobby", "film_hobby",
                      "video_games_hobby", "meditation_hobby", "other_hobby"):
            if user_data[hobby]:
                self.ids[hobby].active = True

        for time_waster in ("no_time_wasters", "TV_addiction_time_waster",
                            "internet_addiction_time_waster", "chatter_time_waster",
                            "smoking_time_waster", "other_time_waster"):
            if user_data[time_waster]:
                self.ids[time_waster].active = True

    def write_data(self):
        global user_data

        if not self.ids.user_name.text:
            return False

        if len(self.ids.date_of_birth.text.split(".")) != 3:
            return False

        work_bool = True
        for work_type in ("no_working", "study_at_school", "study_at_university",
                          "working", "personal_business", "other_work"):
            if self.ids[work_type].active:
                work_bool = False
                break
        if work_bool:
            return False

        hobby_bool = True
        for hobby in ("no_hobbies", "sport_hobby", "tourism_hobby", "dance_hobby", "hunting_hobby",
                      "art_hobby", "vocals_hobby", "collecting_hobby", "programming_hobby",
                      "construction_hobby", "walk_hobby", "shopping_hobby", "film_hobby",
                      "video_games_hobby", "meditation_hobby", "other_hobby"):
            if self.ids[hobby].active:
                hobby_bool = False
                break
        if hobby_bool:
            return False

        time_waster_bool = True
        for time_waster in ("no_time_wasters", "TV_addiction_time_waster",
                            "internet_addiction_time_waster", "chatter_time_waster",
                            "smoking_time_waster", "other_time_waster"):
            if self.ids[time_waster].active:
                time_waster_bool = False
                break
        if time_waster_bool:
            return False

        user_data["user_name"] = self.ids.user_name.text
        user_data["date_of_birth"] = self.ids.date_of_birth.text

        for work_type in ("no_working", "study_at_school", "study_at_university",
                          "working", "personal_business", "other_work"):
            user_data[work_type] = int(self.ids[work_type].active)

        for hobby in ("no_hobbies", "sport_hobby", "tourism_hobby", "dance_hobby", "hunting_hobby",
                      "art_hobby", "vocals_hobby", "collecting_hobby", "programming_hobby",
                      "construction_hobby", "walk_hobby", "shopping_hobby", "film_hobby",
                      "video_games_hobby", "meditation_hobby", "other_hobby"):
            user_data[hobby] = int(self.ids[hobby].active)

        for time_waster in ("no_time_wasters", "TV_addiction_time_waster",
                            "internet_addiction_time_waster", "chatter_time_waster",
                            "smoking_time_waster", "other_time_waster"):
            user_data[time_waster] = int(self.ids[time_waster].active)

        update_db_data()
        update_current_user(user_data["user_login"])


        return True

class TimeDataSettingsScreen(Screen):
    def on_parent(self, *args):
        Clock.schedule_once(self.fill_data, .1)

    def fill_data(self, *args):
        self.ids.state.color = 0, .9, 1, 1
        self.ids.state.text = "Данные о времени"
        for key in user_data.keys():
            if key in self.ids:
                self.ids[key].text = str(user_data[key])

    def write_data(self):
        global user_data

        if not self.ids.days_a_week_at_work.text:
            return False
        if not self.ids.hours_a_day_work.text:
            return False
        if not self.ids.minutes_travel_time_to_work.text:
            return False
        if not self.ids.minutes_travel_time_from_work.text:
            return False
        if not self.ids.minutes_for_self_education_per_day.text:
            return False
        if not self.ids.hours_a_week_for_hobbies.text:
            return False
        if not self.ids.hours_of_sleep.text:
            return False
        if not self.ids.hours_on_a_weekday_for_time_wasters.text:
            return False
        if not self.ids.hours_on_a_day_off_for_time_wasters.text:
            return False
        if not self.ids.visit_store_once_a_week.text:
            return False
        if not self.ids.minutes_on_the_way_to_the_store.text:
            return False
        if not self.ids.minutes_to_visit_shop.text:
            return False
        if not self.ids.hours_per_week_per_family.text:
            return False
        if not self.ids.hours_per_week_for_pets.text:
            return False
        if not self.ids.hours_per_week_for_cleaning.text:
            return False
        if not self.ids.minutes_per_day_per_shower.text:
            return False
        if not self.ids.minutes_after_sleep.text:
            return False
        if not self.ids.minutes_before_sleep.text:
            return False
        if not self.ids.hours_a_day_for_cooking.text:
            return False
        if not self.ids.minutes_for_breakfast.text:
            return False
        if not self.ids.minutes_for_lunch.text:
            return False
        if not self.ids.minutes_for_dinner.text:
            return False
        if not self.ids.hours_per_month_per_hairdresser.text:
            return False
        if not self.ids.hours_per_month_for_beauty_workers.text:
            return False
        if not self.ids.hours_per_week_for_other_activities.text:
            return False

        user_data["days_a_week_at_work"] = self.ids.days_a_week_at_work.text
        user_data["hours_a_day_work"] = self.ids.hours_a_day_work.text
        user_data["minutes_travel_time_to_work"] = self.ids.minutes_travel_time_to_work.text
        user_data["minutes_travel_time_from_work"] = self.ids.minutes_travel_time_from_work.text
        user_data["minutes_for_self_education_per_day"] = self.ids.minutes_for_self_education_per_day.text
        user_data["hours_a_week_for_hobbies"] = self.ids.hours_a_week_for_hobbies.text
        user_data["hours_of_sleep"] = self.ids.hours_of_sleep.text
        user_data["hours_on_a_weekday_for_time_wasters"] = self.ids.hours_on_a_weekday_for_time_wasters.text
        user_data["hours_on_a_day_off_for_time_wasters"] = self.ids.hours_on_a_day_off_for_time_wasters.text
        user_data["visit_store_once_a_week"] = self.ids.visit_store_once_a_week.text
        user_data["minutes_on_the_way_to_the_store"] = self.ids.minutes_on_the_way_to_the_store.text
        user_data["minutes_to_visit_shop"] = self.ids.minutes_to_visit_shop.text
        user_data["hours_per_week_per_family"] = self.ids.hours_per_week_per_family.text
        user_data["hours_per_week_for_pets"] = self.ids.hours_per_week_for_pets.text
        user_data["hours_per_week_for_cleaning"] = self.ids.hours_per_week_for_cleaning.text
        user_data["minutes_per_day_per_shower"] = self.ids.minutes_per_day_per_shower.text
        user_data["minutes_after_sleep"] = self.ids.minutes_after_sleep.text
        user_data["minutes_before_sleep"] = self.ids.minutes_before_sleep.text
        user_data["hours_a_day_for_cooking"] = self.ids.hours_a_day_for_cooking.text
        user_data["minutes_for_breakfast"] = self.ids.minutes_for_breakfast.text
        user_data["minutes_for_lunch"] = self.ids.minutes_for_lunch.text
        user_data["minutes_for_dinner"] = self.ids.minutes_for_dinner.text
        user_data["hours_per_month_per_hairdresser"] = self.ids.hours_per_month_per_hairdresser.text
        user_data["hours_per_month_for_beauty_workers"] = self.ids.hours_per_month_for_beauty_workers.text
        user_data["hours_per_week_for_other_activities"] = self.ids.hours_per_week_for_other_activities.text

        update_db_data()
        update_current_user(user_data["user_login"])


        return True

class MoneyDataSettingsScreen(Screen):
    def on_parent(self, *args):
        Clock.schedule_once(self.fill_data, .1)

    def fill_data(self, *args):
        self.ids.state.color = 0, .9, 1, 1
        self.ids.state.text = "Данные о финансах"

        for currency in ("ruble", "hryvnia", "tenge", "tugrik",
                         "yuan", "dollar", "euro", "pound_sterling"):
            if user_data["currency"] == currency:
                self.ids["currency_"+currency].active = True
                break

        for key in user_data.keys():
            if key in self.ids:
                self.ids[key].text = str(user_data[key])

    def write_data(self):
        global user_data

        for currency in ("currency_ruble", "currency_hryvnia", "currency_tenge", "currency_tugrik",
                         "currency_yuan", "currency_dollar", "currency_euro", "currency_pound_sterling"):
            if self.ids[currency].active:
                user_data["currency"] = currency[9:]
                break

        if not self.ids.scholarship_per_month.text:
            return False
        if not self.ids.salary_per_month.text:
            return False
        if not self.ids.premiums_per_year.text:
            return False
        if not self.ids.premium_amount.text:
            return False
        if not self.ids.number_of_businesses.text:
            return False
        if not self.ids.net_income_from_business_per_month.text:
            return False
        if not self.ids.other_financial_receipts_per_month.text:
            return False
        if not self.ids.sports_funds_per_month.text:
            return False
        if not self.ids.tourism_funds_per_month.text:
            return False
        if not self.ids.dance_funds_per_month.text:
            return False
        if not self.ids.hunting_funds_per_month.text:
            return False
        if not self.ids.art_funds_per_month.text:
            return False
        if not self.ids.vocals_funds_per_month.text:
            return False
        if not self.ids.collecting_funds_per_month.text:
            return False
        if not self.ids.programming_funds_per_month.text:
            return False
        if not self.ids.construction_funds_per_month.text:
            return False
        if not self.ids.walk_funds_per_month.text:
            return False
        if not self.ids.shopping_funds_per_month.text:
            return False
        if not self.ids.film_funds_per_month.text:
            return False
        if not self.ids.video_games_funds_per_month.text:
            return False
        if not self.ids.meditation_funds_per_month.text:
            return False
        if not self.ids.funds_for_other_types_of_hobbies_per_month.text:
            return False
        if not self.ids.self_education_funds_per_month.text:
            return False
        if not self.ids.TV_funds_per_month.text:
            return False
        if not self.ids.internet_resources_funds_per_month.text:
            return False
        if not self.ids.smoking_funds_per_month.text:
            return False
        if not self.ids.funds_for_other_types_of_time_wasters_per_month.text:
            return False
        if not self.ids.grocery_shopping_allowance_per_week.text:
            return False
        if not self.ids.funds_for_shopping_at_a_household_store_per_week.text:
            return False
        if not self.ids.funds_for_a_hairdresser_per_month.text:
            return False
        if not self.ids.funds_for_other_beauty_workers_per_month.text:
            return False
        if not self.ids.internet_funds_per_month.text:
            return False
        if not self.ids.other_funds_per_month.text:
            return False

        user_data["scholarship_per_month"] = self.ids.scholarship_per_month.text
        user_data["salary_per_month"] = self.ids.salary_per_month.text
        user_data["premiums_per_year"] = self.ids.premiums_per_year.text
        user_data["premium_amount"] = self.ids.premium_amount.text
        user_data["number_of_businesses"] = self.ids.number_of_businesses.text
        user_data["net_income_from_business_per_month"] = self.ids.net_income_from_business_per_month.text
        user_data["other_financial_receipts_per_month"] = self.ids.other_financial_receipts_per_month.text
        user_data["sports_funds_per_month"] = self.ids.sports_funds_per_month.text
        user_data["tourism_funds_per_month"] = self.ids.tourism_funds_per_month.text
        user_data["dance_funds_per_month"] = self.ids.dance_funds_per_month.text
        user_data["hunting_funds_per_month"] = self.ids.hunting_funds_per_month.text
        user_data["art_funds_per_month"] = self.ids.art_funds_per_month.text
        user_data["vocals_funds_per_month"] = self.ids.vocals_funds_per_month.text
        user_data["collecting_funds_per_month"] = self.ids.collecting_funds_per_month.text
        user_data["programming_funds_per_month"] = self.ids.programming_funds_per_month.text
        user_data["construction_funds_per_month"] = self.ids.construction_funds_per_month.text
        user_data["walk_funds_per_month"] = self.ids.walk_funds_per_month.text
        user_data["shopping_funds_per_month"] = self.ids.shopping_funds_per_month.text
        user_data["film_funds_per_month"] = self.ids.film_funds_per_month.text
        user_data["video_games_funds_per_month"] = self.ids.video_games_funds_per_month.text
        user_data["meditation_funds_per_month"] = self.ids.meditation_funds_per_month.text
        user_data["funds_for_other_types_of_hobbies_per_month"] = self.ids.funds_for_other_types_of_hobbies_per_month.text
        user_data["self_education_funds_per_month"] = self.ids.self_education_funds_per_month.text
        user_data["TV_funds_per_month"] = self.ids.TV_funds_per_month.text
        user_data["internet_resources_funds_per_month"] = self.ids.internet_resources_funds_per_month.text
        user_data["smoking_funds_per_month"] = self.ids.smoking_funds_per_month.text
        user_data["funds_for_other_types_of_time_wasters_per_month"] = self.ids.funds_for_other_types_of_time_wasters_per_month.text
        user_data["grocery_shopping_allowance_per_week"] = self.ids.grocery_shopping_allowance_per_week.text
        user_data["funds_for_shopping_at_a_household_store_per_week"] = self.ids.funds_for_shopping_at_a_household_store_per_week.text
        user_data["funds_for_a_hairdresser_per_month"] = self.ids.funds_for_a_hairdresser_per_month.text
        user_data["funds_for_other_beauty_workers_per_month"] = self.ids.funds_for_other_beauty_workers_per_month.text
        user_data["internet_funds_per_month"] = self.ids.internet_funds_per_month.text
        user_data["other_funds_per_month"] = self.ids.other_funds_per_month.text

        update_db_data()
        update_current_user(user_data["user_login"])


        return True

class ChangePasswordScreen(Screen):
    def on_parent(self, *args):
        Clock.schedule_once(self.fill_data, .1)

    def fill_data(self, *args):
        self.ids.state.color = 0, .9, 1, 1
        self.ids.state.text = "Изменение пароля"

    def clear_text_inputs(self):
        self.ids.old_password.text = ""
        self.ids.new_password.text = ""
        self.ids.confirm_new_password.text = ""

    def write_data(self):
        global user_data

        if not self.ids.old_password.text or not self.ids.new_password.text or not self.ids.confirm_new_password.text:
            return False

        if self.ids.old_password.text != user_data["user_password"]:
            return False

        if self.ids.new_password.text != self.ids.confirm_new_password.text:
            return False

        user_data["user_password"] = self.ids.new_password.text

        update_db_data()
        update_current_user(user_data["user_login"])


        return True



class AppScreenManager(ScreenManager):
    pass

class mainApp(App):
    def database_init(self):
        global user_data

        with sqlite3.connect('db.db') as db:
            cursor = db.cursor()
            try:
                cursor.execute("""CREATE TABLE users (user_login TEXT, user_password TEXT, user_name TEXT,
                                date_of_birth TEXT, no_working INT, study_at_school INT, study_at_university INT,
                                working INT, personal_business INT, other_work INT, days_a_week_at_work INT,
                                hours_a_day_work FLOAT, minutes_travel_time_to_work FLOAT,
                                minutes_travel_time_from_work FLOAT, minutes_for_self_education_per_day FLOAT,
                                no_hobbies INT, sport_hobby INT, tourism_hobby INT, dance_hobby INT,
                                hunting_hobby INT, art_hobby INT, vocals_hobby INT, collecting_hobby INT,
                                programming_hobby INT, construction_hobby INT, walk_hobby INT, shopping_hobby INT,
                                film_hobby INT, video_games_hobby INT, meditation_hobby INT, other_hobby INT,
                                hours_a_week_for_hobbies FLOAT, hours_of_sleep FLOAT, no_time_wasters INT,
                                TV_addiction_time_waster INT, internet_addiction_time_waster INT,
                                chatter_time_waster INT, smoking_time_waster INT, other_time_waster INT,
                                hours_on_a_weekday_for_time_wasters FLOAT,
                                hours_on_a_day_off_for_time_wasters FLOAT, visit_store_once_a_week INT,
                                minutes_on_the_way_to_the_store FLOAT, minutes_to_visit_shop FLOAT,
                                hours_per_week_per_family FLOAT, hours_per_week_for_pets FLOAT,
                                hours_per_week_for_cleaning FLOAT, minutes_per_day_per_shower FLOAT,
                                minutes_after_sleep FLOAT, minutes_before_sleep FLOAT,
                                hours_a_day_for_cooking FLOAT, minutes_for_breakfast FLOAT,
                                minutes_for_lunch FLOAT, minutes_for_dinner FLOAT,
                                hours_per_month_per_hairdresser FLOAT, hours_per_month_for_beauty_workers FLOAT,
                                hours_per_week_for_other_activities FLOAT,

                                currency TEXT, scholarship_per_month FLOAT, salary_per_month FLOAT,
                                premiums_per_year FLOAT, premium_amount FLOAT, number_of_businesses INT,
                                net_income_from_business_per_month FLOAT, other_financial_receipts_per_month FLOAT,
                                sports_funds_per_month FLOAT, tourism_funds_per_month FLOAT,
                                dance_funds_per_month FLOAT, hunting_funds_per_month FLOAT,
                                art_funds_per_month FLOAT, vocals_funds_per_month FLOAT,
                                collecting_funds_per_month FLOAT, programming_funds_per_month FLOAT,
                                construction_funds_per_month FLOAT, walk_funds_per_month FLOAT,
                                shopping_funds_per_month FLOAT, film_funds_per_month FLOAT,
                                video_games_funds_per_month FLOAT, meditation_funds_per_month FLOAT,
                                funds_for_other_types_of_hobbies_per_month FLOAT,
                                self_education_funds_per_month FLOAT, TV_funds_per_month FLOAT,
                                internet_resources_funds_per_month FLOAT, smoking_funds_per_month FLOAT,
                                funds_for_other_types_of_time_wasters_per_month FLOAT,
                                grocery_shopping_allowance_per_week FLOAT,
                                funds_for_shopping_at_a_household_store_per_week FLOAT,
                                funds_for_a_hairdresser_per_month FLOAT,
                                funds_for_other_beauty_workers_per_month FLOAT, internet_funds_per_month FLOAT,
                                other_funds_per_month FLOAT,
                                
                                date_day INT, date_month INT, date_year INT, time_hour INT, time_minute INT,
                                time_second INT)""")
                cursor.execute(f"INSERT INTO users VALUES({'?, ' * 96}?)",
                                ("", "", "", "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            except:
                cursor.execute("SELECT * FROM users")
                current_data = cursor.fetchall()
                if len(current_data) == 1:
                    return
                update_current_user(current_data[0][0])

                cursor.execute("SELECT * FROM users")
                current_data = cursor.fetchall()[0]

                user_data_keys = list(user_data.keys())
                for i in range(len(user_data_keys)):
                    user_data[user_data_keys[i]] = current_data[i]

            db.commit()

    def main_loop(self, *args):
        update_days_have_passed()

    def build(self):
        self.database_init()
        Clock.schedule_interval(self.main_loop, .1)


if __name__ == "__main__":
    mainapp = mainApp()
    mainapp.run()