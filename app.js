const schedule = require('node-schedule');
const cron = require('node-cron');
const { exec } = require('child_process'); 
const path = require('path');
const express = require('express');

const app = express();
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

const fs = require('fs');

let data;

const translator = {
    '월요일': 'monday',
    '화요일': 'tuesday',
    '수요일': 'wednesday',
    '목요일': 'thursday',
    '금요일': 'friday',
    '오늘': 'today',
    '아침': 'breakfast',
    '점심': 'lunch',
    '저녁': 'dinner',
    '메뉴': 'today',
};

function getWeekDayString(num) {
    if (num == 1) return 'monday';
    if (num == 2) return 'tuesday';
    if (num == 3) return 'wednesday';
    if (num == 4) return 'thursday';
    if (num == 5) return 'friday';

    return 'friday';
}

function isDay(str) {
    if (str === '월요일' || str === '화요일' || str === '수요일' || str === '목요일' || str === '금요일' || str === '오늘') return true;
    return false;
}

function isMeal(str) {
    if (str === '아침' || str === '점심' || str === '저녁') return true;
    return false;
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

const dailyJob = schedule.scheduleJob('1 0 * * *', () => {
    console.log('매일 자정에 메뉴를 파싱')
    const jsonFile = fs.readFileSync('./menu.json', 'utf8');
    data = JSON.parse(jsonFile);

    const date = new Date();
    const dayNum = date.getDay();
    const dayStr = getWeekDayString(dayNum);

    data["today"] = data[dayStr];
});

app.post('/message', function (req, res) {

    const utterance = req.body.userRequest.utterance;
    let responseText = '';
    const quickReplies = [];

    let utteranceArray = utterance.split(' ');
    if (utteranceArray.length === 2) {
        responseText = data[translator[utteranceArray[0]]][translator[utteranceArray[1]]];
    }
    else if (utteranceArray.length === 1) {
        if (isDay(utteranceArray[0])) {
            responseText = "시간을 선택하세요";
            quickReplies.push({
                'label': '아침',
                'action': 'message',
                'messageText':  utteranceArray[0] + ' 아침'
            });
            quickReplies.push({
                'label': '점심',
                'action': 'message',
                'messageText': utteranceArray[0] + ' 점심'
            });
            quickReplies.push({
                'label': '저녁',
                'action': 'message',
                'messageText': utteranceArray[0] + ' 저녁'
            });
        }
        else {
            //exception cases 
            //just breakfast, lunch, dinner case for today
            if (isMeal(utteranceArray[0]))
                responseText = data['today'][translator[utteranceArray[0]]];
            //menu handling
            else {
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
        }
    }

    else {
        responseText = "잘못된 내용입니다."
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
