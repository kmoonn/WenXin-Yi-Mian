import base64
import os
import secrets
import string
from datetime import datetime, timedelta

import bcrypt
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, session, redirect, url_for, Response
from werkzeug.utils import secure_filename

from api import baidu
from db import mongodb

current_directory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


# 随机 Secret Key
def generate_secret_key(length=32):
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(characters) for _ in range(length))
    return secret_key


# 生成一个 64 字符长度的随机 Secret Key
# secret_key = generate_secret_key(64)
# print(secret_key)
app.secret_key = "40LER3oA_{esZ:c^s[B=[O<afGL[d<!vhhG[)P0['w|EWC^PR<z|>Y^9'`gPJ[82"

app.config['SESSION_TYPE'] = 'filesystem'
app.permanent_session_lifetime = timedelta(days=7)  # 设置生命周期为7天

# 相似度列表
similarities = []
# 问题数组
Questions_Arr = []
# 正确答案数组
Correct_Answer_Arr = []
# 用户答案
User_Answers = []
# 模拟面试详细信息
All_Video_Details = []
# 模拟笔试详细信息
All_Text_Details = []

UPLOAD_FOLDER = current_directory + '\\' + 'db\\uploads'
QUESTION_AUDIO = current_directory + '\\' + 'db\\questions'
ALLOWED_EXTENSIONS = {'ogg', 'wav', 'mp3'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['QUESTION_AUDIO'] = QUESTION_AUDIO


@app.route('/')
def index():
    """
    Render the main page.
    """
    global similarities
    global Questions_Arr
    global Correct_Answer_Arr
    global User_Answers
    global All_Text_Details

    similarities = []
    Questions_Arr = []
    Correct_Answer_Arr = []
    User_Answers = []
    All_Text_Details = []

    global All_Video_Details

    All_Video_Details = []
    return render_template('index.html')


@app.route('/ToLogin')
def ToLogin():
    # 登录
    return render_template('Login.html')


@app.route('/ToRegister')
def ToRegister():
    return render_template('Register.html')


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password'].encode('utf-8')

        user = mongodb.get_colleciton('user').find_one({'email': useremail})

        if user and bcrypt.checkpw(password, user['password']):
            if 'message' in session:
                session.pop('message')
            if user.get('role') == 'admin':
                session['role'] = 'admin'
            session['useremail'] = useremail
            session['username'] = user.get('username')
            return redirect(url_for('home'))
        else:
            session['message'] = "账号或密码错误，请重试"
    return redirect(url_for('ToLogin'))


@app.route('/Logout')
def Logout():
    session.pop('useremail')
    return redirect(url_for('home'))


# 待写
@app.route('/Change_User_Info')
def Change_User_Info():
    return ""


@app.route('/Change_User_Image')
def Change_User_Image():
    return ""


@app.route('/Register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password']
    if not useremail or not password:
        session['message'] = '邮箱和密码不为空'
        return redirect(url_for('ToRegister'))
    if mongodb.get_colleciton('user').find_one({'email': useremail}):
        session['message'] = '邮箱已经注册'
        return redirect(url_for('ToRegister'))
    mongodb.add_user('', useremail, password, 'user')
    session['message'] = '注册成功，可以登录啦'
    return redirect(url_for('ToLogin'))


@app.route('/home')
def home():
    global similarities
    global Questions_Arr
    global Correct_Answer_Arr
    global User_Answers
    global All_Text_Details

    similarities = []
    Questions_Arr = []
    Correct_Answer_Arr = []
    User_Answers = []
    All_Text_Details = []

    global All_Video_Details

    All_Video_Details = []
    return render_template('index.html')


@app.route('/Instructions_Text')
def Instructions_Text():
    """
    Render the instructions for the text test.
    """
    global similarities
    global Questions_Arr
    global Correct_Answer_Arr
    global User_Answers
    global All_Text_Details

    similarities = []
    Questions_Arr = []
    Correct_Answer_Arr = []
    User_Answers = []
    All_Text_Details = []

    global All_Video_Details

    All_Video_Details = []
    return render_template('Instructions_Text.html')


@app.route('/Instructions_Video')
def Instructions_Video():
    """
    Render the instructions for the video test.
    """
    global similarities
    global Questions_Arr
    global Correct_Answer_Arr
    global User_Answers
    global All_Text_Details

    similarities = []
    Questions_Arr = []
    Correct_Answer_Arr = []
    User_Answers = []
    All_Text_Details = []

    global All_Video_Details

    All_Video_Details = []
    return render_template('Instructions_Video.html')


@app.route('/Text_Test', methods=['GET', 'POST'])
def Text_Test():
    """
    模拟笔试页面
    """
    if request.method == 'POST':
        job_selection = request.form['jobSelection']
        question_degree = request.form['questionDegree']
        questions_num = request.form['questionsNumSelect']
        job_stress = request.form['jobStress']

    return render_template('Text_Test.html', jobSelection=job_selection, questionDegree=question_degree,
                           questionsNum=questions_num, jobStress=job_stress)


@app.route('/Text_Test_Results')
def Text_Test_Results():
    """
    Render the text test results page.
    """
    return render_template('Text_Test_Results.html')


@app.route('/Text_Test_Result_Record/<int:Qindex>')
def Text_Test_Result_Record(Qindex):
    useremail = session['useremail']
    All_Record_Results = get_results(useremail)
    for result in All_Record_Results:
        if (result[0] == Qindex):
            text_result_data = result[3]
            return render_template('Text_Test_Record_Results.html', text_result_data=text_result_data)
    # else:
    #     return redirect(url_for("home"))


@app.route('/Video_Test_Result_Record/<int:Qindex>')
def Video_Test_Result_Record(Qindex):
    useremail = session['useremail']
    All_Record_Results = get_results(useremail)
    for result in All_Record_Results:
        if (result[0] == Qindex):
            video_result_data = result[3]
            return render_template('Video_Test_Record_Results.html', video_result_data=video_result_data)
    # else:
    #     return redirect(url_for("home"))


@app.route('/Video_Test', methods=['GET', 'POST'])
def Video_Test():
    """
    模拟面试页面
    """
    # 前端参数字典
    if request.method == 'POST':
        job_selection = request.form['jobSelection']
        question_degree = request.form['questionDegree']
        questions_num = request.form['questionsNumSelect']
        job_stress = request.form['jobStress']

    return render_template('Video_Test.html', jobSelection=job_selection, questionDegree=question_degree,
                           questionsNum=questions_num, jobStress=job_stress)


@app.route('/Video_Test_Results')
def Video_Test_Results():
    """
    Render the video test results page.
    """
    return render_template('Video_Test_Results.html')


@app.route('/Personal_Center')
def Personal_Center():
    return render_template('Personal_Center.html')


@app.route('/Brief_Info')
def Brief_Info():
    """
    Render the video test results page.
    """
    return render_template('Brief_Info.html')


@app.route('/Pro_Doc')
def Pro_Doc():
    """
    Render the video test results page.
    """
    return render_template('Pro_Doc.html')


@app.route('/Prompt')
def Prompt():
    """
    Render the video test results page.
    """
    return render_template('Prompt.html')


@app.route('/Main_Page')
def Main_Page():
    """
    Render the video test results page.
    """
    return render_template('Main_Page.html')


@app.route('/favicon.ico')
def favicon():
    """
    Serve the favicon.
    """
    return send_from_directory(os.path.join(app.root_path, 'static'), '/assets/img/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# 返回问题列表
@app.route('/Questions', methods=['POST'])
def Text_Questions():
    """
    得到10个问题及答案，并返回，数组格式
    """

    global Questions_Arr
    global Correct_Answer_Arr

    data = request.get_json()
    job_selection = data.get('jobSelection')
    question_degree = data.get('questionDegree')
    question_num = int(float(data.get('questionsNum')))
    job_stress = data.get('jobStress')

    # 二代
    question_dic = baidu.ask2wenxin(job_selection, question_num, question_degree, job_stress)
    Questions_Arr = question_dic["question"]
    Correct_Answer_Arr = question_dic["answer"]

    return Questions_Arr


# 返回答案
@app.route('/Text_Answers/<int:Qindex>', methods=['POST'])
def text_answers(Qindex):
    """
    Receive and process user answers for text questions.
    """
    global All_Text_Details
    global Questions_Arr
    global Correct_Answer_Arr

    answer = request.data.decode('utf-8')
    temp_list = []
    temp_list.append(Questions_Arr[Qindex])
    temp_list.append(Correct_Answer_Arr[Qindex])
    temp_list.append(answer)
    temp_list.append(baidu.get_text_similarity(str(answer), str(Correct_Answer_Arr[Qindex])))
    All_Text_Details.append(temp_list)
    return jsonify(answer)


# 允许上传的文件格式
def allowed_file(filename):
    """
    Check if the file extension is allowed.
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 上传语音
@app.route('/upload-audio/<int:Qindex>', methods=['POST'])
def upload_audio(Qindex):
    """
    上传音频文件，以及处理
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # 语音转文字
        text = baidu.audio_to_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        global Questions_Arr
        global Correct_Answer_Arr
        global All_Video_Details
        Similarity = baidu.get_text_similarity(str(text), str(Correct_Answer_Arr[Qindex]))
        temp_list = []
        temp_list.append(Questions_Arr[Qindex])
        temp_list.append(Correct_Answer_Arr[Qindex])
        temp_list.append(text)
        temp_list.append(Similarity)
        All_Video_Details.append(temp_list)
        return jsonify({'success': text}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400


# 模拟面试结果返回二维数组
@app.route('/video_results')
def video_results():
    temp_Emotion_Counts = emotion_counts
    temp_Results = All_Video_Details
    temp_Emotion_Counts['angry'] = emotion_counts['angry'] * 0.2
    temp_Emotion_Counts['disgust'] = emotion_counts['disgust'] * 0.2
    temp_Emotion_Counts['fear'] = emotion_counts['fear'] * 0.2
    temp_Emotion_Counts['happy'] = emotion_counts['happy'] * 1.3
    temp_Emotion_Counts['sad'] = emotion_counts['sad'] * 0.2
    temp_Emotion_Counts['neutral'] = emotion_counts['neutral'] * 1
    temp_Emotion_Counts['no_face'] = 0

    new_temp = []
    new_temp.append(temp_Results)
    new_temp.append(list(temp_Emotion_Counts.values()))

    if 'useremail' in session:
        mongodb.add_video_result(session['useremail'], datetime.now().strftime("%Y-%m-%d %H:%M"), new_temp)
    return jsonify(new_temp)


# 模拟笔试结果
@app.route('/text_results')
def text_results():
    if 'useremail' in session:
        mongodb.add_text_result(session['useremail'], datetime.now().strftime("%Y-%m-%d %H:%M"), All_Text_Details)
    # All_Text_Details_temp = []
    All_Text_Details_temp = All_Text_Details

    return jsonify(All_Text_Details_temp)


def get_results(useremail):
    results = []
    i = 0
    text_results = mongodb.get_text_result_list(useremail)
    video_results = mongodb.get_video_result_list(useremail)
    for text_result in text_results:
        text_result_temp = []
        text_result_temp.append(i)
        text_result_temp.append('模拟笔试')
        text_result_temp.append(text_result['created_at'])
        text_result_temp.append(text_result['data'])
        results.append(text_result_temp)
        i = i + 1
    for video_result in video_results:
        video_result_temp = []
        video_result_temp.append(i)
        video_result_temp.append('模拟面试')
        video_result_temp.append(video_result['created_at'])
        video_result_temp.append(video_result['data'])
        results.append(video_result_temp)
        i = i + 1
    return results


@app.route('/Get_Results')
def Get_Reults():
    useremail = session['useremail']

    results = get_results(useremail)

    session['All_Record_Results'] = results
    session.permanent = True
    session.modified = True
    print(session['All_Record_Results'])
    return jsonify(results)


# 生成视频帧的函数
def generate_frames():
    global camera  # 引用全局摄像头变量

    while True:
        if camera is not None:
            success, frame = camera.read()  # 从摄像头读取一帧
            if not success:
                break
        else:
            break

        ret, buffer = cv2.imencode('.jpg', frame)  # 将帧编码为JPEG格式
        frame_copy = frame
        frame = buffer.tobytes()  # 将帧转换为字节形式
        # 将帧转换为灰度图像，以便进行人脸检测
        output_filename = "newoutput.jpg"
        cv2.imwrite(output_filename, frame_copy)
        gray = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)
        #  针对每个检测到的人脸执行以下操作
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # 针对每个检测到的人脸执行以下操作
        for (x, y, w, h) in faces:
            # 提取人脸区域
            face = frame_copy[y:y + h, x:x + w]
            # 如果存在人脸
            if len(face) > 0:
                try:
                    # 使用DeepFace库分析人脸，提取主要情绪
                    result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=True)
                    if result[0]['dominant_emotion'] is not None:
                        # 根据分析结果更新对应情绪的计数
                        emotion_counts[result[0]['dominant_emotion']] += 1
                    else:
                        print('no_emotion')
                except ValueError as err:
                    emotion_counts['no_face'] += 1
            else:
                emotion_counts['no_face'] += 1
        yield (b'--frame\r\n'  # 发送一个分隔符标记，表示新的视频帧开始
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 发送视频帧数据


@app.route('/videofeed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global emotion_counts

    data = request.json
    if 'frame' in data:
        frame_data = data['frame']

        # print(frame_data)

        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        # print(frame_bytes)

        nparr = np.frombuffer(frame_bytes, np.uint8)

        # print(nparr)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # print(frame)

        output_filename = "output.jpg"
        cv2.imwrite(output_filename, frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # print(gray)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # print("faces===========")
        # print(len(faces))
        for (x, y, w, h) in faces:
            face = frame[y:y + h, x:x + w]
            if len(face) > 0:
                print(face)
                try:
                    result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=True)
                    if result[0]['dominant_emotion'] is not None:
                        print(result[0]['dominant_emotion'])
                        emotion_counts[result[0]['dominant_emotion']] += 1
                    else:
                        print('no_emotion')
                except ValueError as err:
                    emotion_counts['no_face'] += 1
            else:
                emotion_counts['no_face'] += 1

        return jsonify({'emotion_counts': emotion_counts}), 200
    else:
        return jsonify({'error': 'No frame data provided.'}), 400


# 开始
@app.route('/start')
def start():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        return '摄像头开启'
    else:
        return '摄像头已开启'


@app.route('/stop')
def stop():
    global camera
    if camera is not None:
        camera.release()
        camera = None
        camera = cv2.VideoCapture(0)
    return '摄像头停止'


# 得到问题语言
@app.route('/get_audio', methods=['POST', 'GET'])
def get_audio():
    if request.method == 'POST':
        data = request.get_json()
        question_id = data.get('question_id')
        question = data.get('question')

        question_audio = os.path.join(app.config['QUESTION_AUDIO'], f"question{question_id}.mp3")

        baidu.text_to_audio(question, question_audio)

    return send_file(question_audio, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
