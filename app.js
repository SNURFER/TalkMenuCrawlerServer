const schedule = require('node-schedule');
const cron = require('node-cron');
const { exec } = require('child_process'); 
const path = require('path');
const express = require('express');

const app = express();

function getWeekDayString(num) {
    if (num == 1) return 'monday';
    if (num == 2) return 'tuesday';
    if (num == 3) return 'wednesday';
    if (num == 4) return 'thursday';
    if (num == 5) return 'friday';

    return 'friday';
}

function runPyScript(){
    return new Promise((resolve, reject) => {
        const pyBinPath = path.join(__dirname, '.venv/bin/python');
        exec(pyBinPath + ' test.py', (err, stdout, stderr) => {
            if(err) reject(err);
            resolve(stdout);
        });
    });
}

const job = schedule.scheduleJob('30 24 * * 6,7', () => {
    runPyScript();
    console.log('매주 토, 일 자정에 수행');
});

app.use(express.urlencoded({ extended: false }));
app.use(express.json());

app.post('/message', function (req, res) {
    const fs = require('fs');
    const jsonFile = fs.readFileSync('./menu.json', 'utf8');
    const data = JSON.parse(jsonFile);

    const date = new Date();
    const dayNum = date.getDay();
    const dayStr = getWeekDayString(dayNum);

    const question = req.body.userRequest.utterance;
    let responseText = '';
    const quickReplies = [];

    if (question == "오늘" || question == "메뉴") {
        responseText = "시간을 선택하세요";
        quickReplies.push({
            'label': '아침',
            'action': 'message',
            'messageText': '아침'
        });
        quickReplies.push({
            'label': '점심',
            'action': 'message',
            'messageText': '점심'
        });
        quickReplies.push({
            'label': '저녁',
            'action': 'message',
            'messageText': '저녁'
        });
    }

    if (question == "아침" || question == "오늘 아침") {
        responseText = data[dayStr]["breakfast"];
    }
    if (question == "점심" || question == "오늘 점심") {
        responseText = data[dayStr]["lunch"];
    }
    if (question == "저녁" || question == "오늘 저녁") {
        responseText = data[dayStr]["dinner"];
    }

    if (question == "월요일") {
        responseText = "시간을 선택하세요";
        quickReplies.push({
            'label': '아침',
            'action': 'message',
            'messageText': '월요일 아침'
        });
        quickReplies.push({
            'label': '점심',
            'action': 'message',
            'messageText': '월요일 점심'
        });
        quickReplies.push({
            'label': '저녁',
            'action': 'message',
            'messageText': '월요일 저녁'
        });
    }
    if (question == "월요일 아침") {
        responseText = data["monday"]["breakfast"];
    }
    if (question == "월요일 점심") {
        responseText = data["monday"]["lunch"];
    }
    if (question == "월요일 저녁") {
        responseText = data["monday"]["dinner"];
    }


    if (question == "화요일") {
        responseText = "시간을 선택하세요";
        quickReplies.push({
            'label': '아침',
            'action': 'message',
            'messageText': '화요일 아침'
        });
        quickReplies.push({
            'label': '점심',
            'action': 'message',
            'messageText': '화요일 점심'
        });
        quickReplies.push({
            'label': '저녁',
            'action': 'message',
            'messageText': '화요일 저녁'
        });
    }
    if (question == "화요일 아침") {
        responseText = data["tuesday"]["breakfast"];
    }
    if (question == "화요일 점심") {
        responseText = data["tuesday"]["lunch"];
    }
    if (question == "화요일 저녁") {
        responseText = data["tuesday"]["dinner"];
    }


    if (question == "수요일") {
        responseText = "시간을 선택하세요";
        quickReplies.push({
            'label': '아침',
            'action': 'message',
            'messageText': '수요일 아침'
        });
        quickReplies.push({
            'label': '점심',
            'action': 'message',
            'messageText': '수요일 점심'
        });
        quickReplies.push({
            'label': '저녁',
            'action': 'message',
            'messageText': '수요일 저녁'
        });
    }
    if (question == "수요일 아침") {
        responseText = data["wednesday"]["breakfast"];
    }
    if (question == "수요일 점심") {
        responseText = data["wednesday"]["lunch"];
    }
    if (question == "수요일 저녁") {
        responseText = data["wednesday"]["dinner"];
    }

    if (question == "목요일") {
        responseText = "시간을 선택하세요";
        quickReplies.push({
            'label': '아침',
            'action': 'message',
            'messageText': '목요일 아침'
        });
        quickReplies.push({
            'label': '점심',
            'action': 'message',
            'messageText': '목요일 점심'
        });
        quickReplies.push({
            'label': '저녁',
            'action': 'message',
            'messageText': '목요일 저녁'
        });
    }
    if (question == "목요일 아침") {
        responseText = data["thursday"]["breakfast"];
    }
    if (question == "목요일 점심") {
        responseText = data["thursday"]["lunch"];
    }
    if (question == "목요일 저녁") {
        responseText = data["thursday"]["dinner"];
    }

    if (question == "금요일") {
        responseText = "시간을 선택하세요";
        quickReplies.push({
            'label': '아침',
            'action': 'message',
            'messageText': '금요일 아침'
        });
        quickReplies.push({
            'label': '점심',
            'action': 'message',
            'messageText': '금요일 점심'
        });
        quickReplies.push({
            'label': '저녁',
            'action': 'message',
            'messageText': '금요일 저녁'
        });
    }
    if (question == "금요일 아침") {
        responseText = data["friday"]["breakfast"];
    }
    if (question == "금요일 점심") {
        responseText = data["friday"]["lunch"];
    }
    if (question == "금요일 저녁") {
        responseText = data["friday"]["dinner"];
    }

    const responseBody = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'simpleText': {
                        'text': responseText 
                    }
                }
            ],
            'quickReplies': quickReplies
        }
    };

    res.status(200).send(responseBody);
});

app.listen(3000, () => console.log('node on 3000'));
