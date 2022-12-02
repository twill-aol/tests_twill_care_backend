import datetime as dt
import random
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


TIME_START = str(dt.datetime.now().strftime("%Y%m%d%H%M"))[2:]


class MainCase(BaseCase):

    # response = MainCase.signup()
    user_id = ""
    email = ""
    password = "Password+1"
    cookies = {}
    access_token = {}

    @classmethod
    def cookies_construction(self):
        response_get_phpsessid = MyRequests.get('/')
        # if bool(response_get_phpsessid.cookies["PHPSESSID"]):
        try:
            phpsesid = response_get_phpsessid.cookies["PHPSESSID"]
            self.cookies["PHPSESSID"] = phpsesid
        except:
            pass
        response_get_sessionid = MyRequests.get('/signup/')
        # if response_get_sessionid.cookies["sessionid"]:
        try:
            sessionid = response_get_sessionid.cookies["sessionid"]
            self.cookies["sessionid"] = sessionid
        except:
            pass
        return self.cookies

    @classmethod
    def login_method(self):
        json_data = {  # логин
            "email": self.email,
            "password": self.password,
        }
        response = MyRequests.post('https://auth.stage-twill.health/api/public/auth/?client_id=gAAAAABg0ekJj1wog3OxuvZe7Ff7JVxJkX53lLG0unWlePRpI_wHb3LUE3NapCFNxwyZzHr3RqD0BoC_YdlEXOErpD8LXmmYzw%3D%3D', json=json_data)
        self.access_token = BaseCase.response_to_json(response)["access_token"]
        return self.access_token

    @classmethod
    def generate_names(self):
        first_names = (
            "Patrick",
            "Ethan",
            "Kevin",
            "Justin",
            "Matthew",
            "William",
            "Christopher",
            "Anthony",
            "Ryan",
            "Michael",
            "Nicholas",
            "David",
            "Alex",
            "James",
            "Josh",
            "Dillon",
            "Brandon",
            "Philip",
            "Fred",
            "Tyler",
            "Caleb",
            "Thomas",
            "Aaron",
            "Brad",
            "Emilу",
            "Hannah",
            "Natalie",
            "Sophia",
            "Ella",
            "Madison",
            "Sydney",
            "Anna",
            "Taylor",
            "Isabella",
            "Kayla",
            "Victoria",
            "Elizabeth",
            "Ashley",
            "Rachel",
            "Alexis",
            "Julia",
            "Samantha",
            "Haley",
            "Olivia",
            "Sarah",
            "Jessica",
            "Ava",
            "Kaitlyn",
            "Katherine"
        )
        last_names = (
            "Hampton",
            "Hudson",
            "Jordan",
            "Stewart",
            "Johnson",
            "Brown",
            "Walker",
            "Hall",
            "White",
            "Wilson",
            "Thompson",
            "Moore",
            "Taylor",
            "Anderson",
            "Smith",
            "Jackson",
            "Harris",
            "Martin",
            "Young",
            "Hernandez",
            "Garcia",
            "Davis",
            "Miller",
            "Martinez",
            "Robinson",
            "Clark",
            "Rodrigues",
            "Lewis",
            "Lee",
            "Allen",
            "King",
            "Aaronson",
            "Cave",
            "Carter",
            "Watson"
        )
        names = f"{random.choice(first_names)} {random.choice(last_names)}"
        return names

    @classmethod
    def signup(self, email=None):
        dynamic_part = f'oleynik+bot{TIME_START}'
        domain = 'alarstudios.com'
        if email is None:
            email = f"{dynamic_part}@{domain}"
        signup_data = {
            "email": email,
            "username": f"Bot{TIME_START}",
            "password": self.password,
            "postal": "11111",
            "gender": "male",
            "date_of_birth": '2000-10-10',
            "first_name": f"Bot{TIME_START}",
            "last_name": f"AQABot{TIME_START}",
        }
        MainCase.cookies_construction()
        response = MyRequests.post("/api/v2/user/", json=signup_data, cookies=self.cookies)

        Assertions.assert_code_status(response, 200)
        # Assertions.assert_json_has_keys(
        #     response,
        #     [
        #         "user_id",
        #         "user",
        #         "is_redirected",
        #         "original_url",
        #         "origin_referral_id",
        #         "env",
        #         "access_token",
        #     ],
        # )
        self.user_id = BaseCase.response_to_json(response)["user"]["id"]
        self.email = BaseCase.response_to_json(response)["user"]["email"]
        # MainCase.login_method()

        self.access_token = BaseCase.response_to_json(response)["access_token"]
        return self.user_id, self.email, self.cookies, self.access_token

    @classmethod
    def signup_router(self, email=None):
        if self.user_id != "":
            print('►')
            return self.user_id, self.email, self.cookies, self.access_token
        else:
            print('►►►')
            return self.signup(email)

    @classmethod
    def finder_text(self, content, flag, board):
        find_id_position = content.find(flag) + len(flag)
        text = ""
        for symbol in content[find_id_position:]:
            if symbol != board:
                text += symbol
            else:
                break
        return text

    @classmethod
    def good_phrases(self):
        phrases = (
            "Be happy",
            "Everything will be alright",
            "Let's make this world a kinder place",
            "Nothing is impossible",
            "Believe in the dream",
            "You can do more",
            "Just do it",
            "Smile and everything will work out",
            "Focus on your breath",
            "Feel the fluidity",
            "We are all connected",
            "Happiness comes from within",
            "Our heart is full",
            "Focus on your breath",
            "Concentrate the mind on the present moment",
            "Humility, infinity, integrity, liberty, majesty, synergy",
            "Don't give up",
            "Be an example",
            "Stand on the side of the light",
            "God is everywhere",
        )
        phrase = random.choice(phrases)
        return phrase
