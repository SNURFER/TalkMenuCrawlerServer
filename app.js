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

const job = schedule.scheduleJob('30 24 * * 6,7', () => {
    runPyScript();
    console.log('매주 토, 일 자정에 수행');
});

app.use(express.urlencoded({ extended: false }));
app.use(express.json());

app.get('/keyboard', (req, res) => {
    const fs = require('fs');

    const jsonFile = fs.readFileSync('./menu.json', 'utf8');
    console.log(jsonFile);
    const data = JSON.parse(jsonFile);

    res.json(data);
});

app.get('/monday', (req, res) => {
    const fs = require('fs');

    const jsonFile = fs.readFileSync('./menu.json', 'utf8');
    console.log(jsonFile);
    const data = JSON.parse(jsonFile);

    res.json(data["monday"]);
});

app.get('/tuesday', (req, res) => {
    const fs = require('fs');

    const jsonFile = fs.readFileSync('./menu.json', 'utf8');
    console.log(jsonFile);
    const data = JSON.parse(jsonFile);

    res.json(data["tuesday"]);
});

app.get('/wednesday', (req, res) => {
    const fs = require('fs');

    const jsonFile = fs.readFileSync('./menu.json', 'utf8');
    console.log(jsonFile);
    const data = JSON.parse(jsonFile);

    res.json(data["wednesday"]);
});

app.get('/thursday', (req, res) => {
    const fs = require('fs');

    const jsonFile = fs.readFileSync('./menu.json', 'utf8');
    console.log(jsonFile);
    const data = JSON.parse(jsonFile);

    res.json(data["thursday"]);
});

app.get('/friday', (req, res) => {
    const fs = require('fs');

    const jsonFile = fs.readFileSync('./menu.json', 'utf8');
    console.log(jsonFile);
    const data = JSON.parse(jsonFile);

    res.json(data["friday"]);
});

app.listen(3000, () => console.log('node on 3000'));
