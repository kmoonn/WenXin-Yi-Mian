let questions = [];
let userAnswers = [];
let currentQuestionIndex = 0;
let timeLeft = 180;
let timerInterval;
const inputBox = document.getElementById('input-box')
const questionText = document.getElementById('question-text');
const answerInput = document.getElementById('answer-input');
const submitBtn = document.getElementById('submit-btn');
// const timer = document.querySelector('.timer');
const timer = document.getElementById('timer');

inputBox.style.visibility = "hidden";

let Question_number = 0;
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
    // body: JSON.stringify(paramsDic)
})
    .then(response => response.json())
    .then(data => {
        questions = questions.concat(data);
        console.log(questions)
        questionText.innerHTML = "请注意：可以开始答题啦！<br>每题有3分钟时间作答<br>按<i style='color: #0fb1ff'>enter</i>键开始答题";
    })
    .catch(error => console.error(error));

// Start the timer
function startTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerInterval = setInterval(() => {
        timeLeft--;
        timer.style.width = `${(timeLeft / 180) * 100}%`;
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            userAnswers.push('timeout');
            checkAnswer()
            // currentQuestionIndex++;
            // if (currentQuestionIndex < questions.length) {
            //   resetTimer();
            //   startTimer();
            //   showQuestion();
            // } else {
            //   window.location.href = "/Text_Test_Results";
            // }
        }
    }, 1000);
}

// Reset the timer
function resetTimer() {
    timeLeft = 180;
    timer.style.width = '100%';
}

// Handle form submission
submitBtn.addEventListener('click', (e) => {
    e.preventDefault();
    checkAnswer();
});

answerInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
        checkAnswer();
    }
});
let first_enter = 0
window.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && first_enter == 0) {
        console.log(1)
        first_enter = 1
        resetTimer();
        startTimer();
        showQuestion();
        inputBox.style.visibility = "visible";
    }
})

function showQuestion() {
    questionText.innerText = questions[currentQuestionIndex];
    answerInput.value = '';
}

function checkAnswer() {
    const userAnswer = answerInput.value;
    answerInput.value = ''; // Clear the answer input field
    currentQuestionIndex++;

    // Send the user's answer to the server
    fetch('Text_Answers/' + Question_number, {
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain'
        },
        body: userAnswer
    })
        .then(response => {
            if (response.ok) {

                console.log(response);
                Question_number += 1;
            } else {
                console.error('Failed to submit answer.');
            }

            // Check if there are more questions to show
            if (currentQuestionIndex < questions.length) {
                resetTimer();
                startTimer();
                showQuestion();
            } else {
                window.location.href = "/Text_Test_Results";
            }
        })
        .catch(error => console.error(error));
}

