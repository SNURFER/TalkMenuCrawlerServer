const schedule = require('node-schedule');
const cron = require('node-cron');
const { exec } = require('child_process'); 
const path = require('path');
const express = require('express');

const app = express();

function runPyScript(){
    return new Promise((resolve, reject) => {
        const pyBinPath = path.join(__dirname, '.venv/bin/python');
        exec(pyBinPath + ' test.py', (err, stdout, stderr) => {
            if(err) reject(err);
            resolve(stdout);
        });
    });
}

const job = schedule.scheduleJob('1 * * * * *', () => {
    runPyScript();
    console.log('매 1분에 실행');
});
// runPyScript();

//test

app.use(express.urlencoded({ extended: false }));
app.use(express.json());

app.get('/keyboard', (req, res) => {
    const fs = require('fs');

    const jsonFile = fs.readFileSync('./menu.json', 'utf8');
    console.log(jsonFile);
    const data = JSON.parse(jsonFile);

    res.json(data);
});

app.listen(3000, () => console.log('node on 3000'));
