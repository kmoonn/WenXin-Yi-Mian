let start_button = document.querySelector("#start-record");
const timer = document.getElementById('timer');
const question = document.getElementById('question');
const nextBtn = document.getElementById('next');
const videoStream = document.getElementById('video-stream')
const audioPlayer = document.getElementById('audioPlayer')

start_button.disabled = true;// 按钮初始化为禁止状态
nextBtn.disabled = true;// 按钮初始化为禁止状态

let timer_duration = parseInt(questionsNum) * 5 * 60; // 计时器10分钟
let questions = ['问题已准备就绪，可点击开始面试'];
let timeLeft = parseInt(questionsNum) * 60 * 5;
let timerInterval;

let currentQuestionIndex;

let question_number = 0;

let recorder; // 存储录音的MediaRecorder对象
let chunks = []; // 存储录音数据的数组


const videoConstraints = {
    width: { ideal: 640 },
    height: { ideal: 480 }
};



let localStream;

async function startCamera() {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ video: videoConstraints});
        videoStream.srcObject = localStream;
        videoStream.play();

    } catch (error) {
        console.error('Error accessing the camera:', error);
    }
}

function stopCamera() {
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
        videoStream.srcObject = null;
    }
}

videoStream.addEventListener('play', () => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = videoStream.width;
    canvas.height = videoStream.height;

    const sendInterval = 1000; // Set an appropriate interval for sending frames (in milliseconds)

    setInterval(() => {
        context.drawImage(videoStream, 0, 0, canvas.width, canvas.height);
        const frameData = canvas.toDataURL('image/jpeg');

        // console.log(frameData)

        fetch('/process_frame', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ frame: frameData }),
        })
        .then(response => response.json())
        .then(data => {
            // console.log(data);
        })
        .catch(error => {
            console.error('Error processing frame:', error);
        });
    }, sendInterval);
});

// 摄像头
// async function startCamera() {
//     fetch('start')
//         .then(response => response.text())
//         .then(message => console.log(message));
//     videoStream.style.visibility = 'visible'
//     videoStream.src = "videofeed";
// }
//
//
// function stopCamera() {
//     fetch('stop')
//         .then(response => response.text())
//         .then(message => console.log(message));
//     videoStream.src = "";
//     videoStream.style.visibility = 'hidden'
// }



// 录音
function startRecording() {
    try {
        recorder = new Recorder({
            sampleBits: 16, // 采样位数，支持 8 或 16，默认是16
            sampleRate: 16000, // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
            numChannels: 1, // 声道，支持 1 或 2， 默认是1
        })
        Recorder.getPermission().then(
            () => {
                console.log("开始录音");
                recorder.start();
            },
            (error) => {
                alert("请允许使用麦克风")
                console.log(error)
            }
        )
    } catch (error) {
        console.log(error);
    }
}

function stopRecording() {
    recorder.stop();
    const wavBlob = recorder.getWAVBlob();
    const formData = new FormData();
    const newbolb = new Blob([wavBlob], {type: 'audio/wav'});

    formData.append('file', newbolb, 'audio' + question_number + '.wav');

    fetch('/upload-audio/' + question_number, {method: 'POST', body: formData})
        .then(response => response.json())
        .then(data => {
            console.log(data); // 打印服务器返回的数据
            question_number += 1; // 切换到下一个问题
            // resolve(); // Promise的解析函数调用
        })
        .catch(error => {
            console.error(error);
            // resolve();
        })
}

function startTimer() {
    // 每秒执行一次计时器回调函数
    timerInterval = setInterval(() => {
        timeLeft--;
        timer.style.width = `${(timeLeft / timer_duration) * 100}%`;
        if (timeLeft <= 0) {
            stopCamera();
            window.location.href = "/Video_Test_Results";
        }
    }, 1000);
}


fetch('Questions', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        jobSelection: jobSelection,
        questionDegree: questionDegree,
        questionsNum: questionsNum,
        jobStress: jobStress
    })
})
    .then(response => response.json())
    .then(data => {

        // 将服务器返回的问题数据追加到questions数组中
        questions = questions.concat(data);

        console.log(questions) // 打印问题数

        showQuestion(0); // 展示第一个问题

        start_button.disabled = false;
    });

async function showQuestion(index) {
    if (index < questions.length) {
        question.textContent = questions[index];
        currentQuestionIndex = index;

        fetch('get_audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({question_id: currentQuestionIndex, question: questions[currentQuestionIndex]})
        })
            .then(response => response.blob())
            .then(blob => {
                const objectUrl = URL.createObjectURL(blob);
                audioPlayer.src = objectUrl;
                audioPlayer.play();
            })
            .catch(error => console.error('Error fetching audio:', error))

    } else {
        stopCamera();
        nextBtn.disabled = true
        question.textContent = "恭喜你，完成本次面试" + "\n" + "结果正在处理中，请稍等..."
        await new Promise(r => setTimeout(r, 1000)); // 等待1秒钟
        window.location.href = "/Video_Test_Results"; // 跳转到测试结果页面
    }
}

nextBtn.addEventListener('click', async () => {
    audioPlayer.pause();
    await stopRecording(); // 停止录音
    // recorder.stop(); // 停止录音器
    chunks = []; // 重置录音数据
    showQuestion(currentQuestionIndex + 1); // 展示下一个问题
    startRecording(); // 开始录音下一个问题的回答
});

start_button.addEventListener('click', async function () {
    await startCamera(); // 启动摄像头
    startTimer(); // 启动计时器
    showQuestion(1); // 展示第一个问题
    startRecording(); // 开始录音
    nextBtn.disabled = false; // 启用"下一步"按钮
    start_button.disabled = true; // 禁用"开始录制"按钮
});