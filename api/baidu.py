import base64
import json
import os
import urllib
import wave

import pyaudio
import requests
from fastapi.responses import FileResponse
from pydantic import BaseModel

# 密钥
# 语音技术
key1 = {'API_KEY': "llkOr5jXwWAIwhPhNP4HDCoG", 'SECRET_KEY': "lNd9vcztgWGwy4X0WyudOdVWqGhT2yr8"}
# 文本相似度
key2 = {'API_KEY': "pJtzkASZhNLpCA7RvrdSTSNs", 'SECRET_KEY': "EQKQULLDJdCvoxf9sPdXDjTOSMBXcQnt"}
# 文心一言
key_yiyan = {'API_KEY': "4SWaPszw4d5TFGUvsQxs2YrF", 'SECRET_KEY': "FJRTv9fmzvNRKM90Xrj58P4cvDFRLYfj"}


class Texts(BaseModel):
    text_a: str
    text_b: str


# 鉴权
def get_access_token(key):
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """

    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": key['API_KEY'], "client_secret": key['SECRET_KEY']}
    return str(requests.post(url, params=params).json().get("access_token"))


# 音频转文本
def audio_to_text(wav_filename):
    url = "https://vop.baidu.com/server_api"

    payload = json.dumps({
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": "J4nS6lEMroP5km4kWsbIal81gGhUthqp",
        "token": get_access_token(key1),
        "speech": get_file_content_as_base64(wav_filename, False),
        "len": os.path.getsize(wav_filename)
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    content = json.loads(response.text)

    if 'result' in content:
        return content['result'][0]
    else:
        return "No result found"


# 文本转音频
def text_to_audio(res_str, audio_path):
    url = "https://tsn.baidu.com/text2audio"

    data = {
        "tex": res_str,
        "tok": get_access_token(key1),
        "cuid": "7dnI1VxMnE7ignByRO8RnW7KMdc6fp7s",
        "ctp": 1,  # 客户端类型，web端固定值1
        "lan": "zh",  # 中文语言
        "spd": 5,  # 语速
        "pit": 5,  # 语调
        "vol": 5,  # 音量
        "per": 3,  # 男女声，4是度丫丫
        "aue": 3,  # 音频格式，3是mp3
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }

    response = requests.request("POST", url, headers=headers, data=data)

    text = response.content
    f = open(audio_path, "wb")
    f.write(text)
    f.close()


# 文本相似度
def get_text_similarity(text_1, text_2):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?charset=UTF-8&access_token=" + get_access_token(key2)

    payload = json.dumps({
        "text_1": text_1,
        "text_2": text_2
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    content = json.loads(response.text)

    if "score" in content:
        return content["score"]
    else:
        return "no score"


# 请求文心一言获取问题
def get_wenxin(prompt):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + get_access_token(key_yiyan)
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "top_p": 1,
        "penalty_score": 1.0
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    content = json.loads(response.text)
    if 'result' in content:
        return content['result']
    else:
        return "No result found"


# 请求文心一言获得问题和答案
def ask2wenxin(jobSelection: str, question_num: int, question_degree: str, job_stress: str):
    if job_stress == '':
        prompt = "我正在参加" + jobSelection + "岗位的面试，你作为本场首席面试官，模拟真实面试场景，确保问题的随机性和多样性。现在请直接对我提出一个以'问题：'开头的" + jobSelection + "方面的问题，并且问题的难度为" + question_degree + "，不需要作过多的解释，在问题后面给出以'答案：'开头的精简的参考答案。注意答案中不要包括中文冒号'：'。"
    else:
        prompt = "我正在参加" + jobSelection + "岗位的面试，你作为本场首席面试官，模拟真实面试场景，确保问题的随机性和多样性。现在请直接对我提出一个以'问题：'开头的" + jobSelection + "方面的问题，并且问题的难度为" + question_degree + "，不需要作过多的解释，在问题后面给出以'答案：'开头的精简的参考答案。注意答案中不要包括中文冒号'：'。最后请注意：" + job_stress
    first_set = set()
    q_a_dic = {}

    while True:
        result = get_wenxin(prompt)
        question = result.split("：")[1].split("答案")[0]
        answer = result.split("：")[2]
        q_a_dic[question] = answer
        first_set.add(question)

        if len(list(first_set)) == question_num:
            questionArr = list(first_set)
            break
    answerArr = []
    for i in range(question_num):
        answerArr.append(q_a_dic[questionArr[i]])

    return {'question': questionArr, 'answer': answerArr}


# 生成录音文件
def sound_record(filename):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("开始录音,请说话!")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束,请稍后!")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# 读取音频文件
def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


# 取出文本转语音
def text2audio(wav_name: str):
    return FileResponse(f'{wav_name}.mp3', media_type="audio/mpeg")


# 取出语音转文本
def audio2text(response: str):
    sound_record(f'{response}.wav')
    text = audio_to_text(f'{response}.wav')
    return {'result': text}


# 获取文本相似度
def text_similarity(text_1: str, text_2: str):
    result = get_text_similarity(text_1, text_2)
    return result


if __name__ == '__main__':
    pass
