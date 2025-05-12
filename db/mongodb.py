import bcrypt
import pymongo


# 连接MongoDB
def get_client():
    uri = "mongodb://localhost:27017/yimian"
    client = pymongo.MongoClient(uri)
    return client


def get_colleciton(collection):
    db = get_client().yimian
    collection = db[collection]
    return collection


# 创建用户类
class User:
    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role


# 笔试记录类
class TextResult:
    def __init__(self, email, created_at, data):
        self.email = email
        self.created_at = created_at
        self.data = data


# 面试记录类
class VideoResult:
    def __init__(self, email, created_at, data):
        self.email = email
        self.created_at = created_at
        self.data = data


# 添加用户
def add_user(username, email, password, role):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username, email, hashed_password, role)
    get_colleciton('user').insert_one(new_user.__dict__)


# 添加笔试、面试记录
def add_text_result(email, created_at, data):
    new_text_result = TextResult(email, created_at, data)
    get_colleciton('text_result').insert_one(new_text_result.__dict__)


def add_video_result(email, created_at, data):
    new_video_result = VideoResult(email, created_at, data)
    get_colleciton('video_result').insert_one(new_video_result.__dict__)


# 查询笔试、面试记录
def get_text_result_list(email):
    text_results = get_colleciton('text_result').find({'email': email})
    return list(text_results)


def get_video_result_list(email):
    video_results = get_colleciton('video_result').find({'email': email})
    return list(video_results)


# 查询用户是否存在
def check_user_exists(email):
    user = get_colleciton('user').find_one({'email': email})
    return user is not None


def save_text_result():
    return ""


def save_video_result():
    return ""


def print_user():
    users = get_colleciton('user').find()
    for user in users:
        print(user)


def print_text_result(email):
    text_results = get_colleciton('text_result').find({'email': email})
    print(list(text_results))
    for text_result in text_results:
        print(text_result)


def print_video_result(email):
    video_results = get_colleciton('video_result').find_one({'email': email})
    print(video_results)


if __name__ == '__main__':
    print(get_text_result_list('3453863492@qq.com'))
