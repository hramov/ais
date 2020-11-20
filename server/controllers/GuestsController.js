'use strict'

const xlsx = require('node-xlsx');
const crypto = require('crypto');
var QRCode = require('qrcode')
var fs = require('fs-extra');
const zip = require('zip-a-folder');
const mysql = require('mysql2/promise');
const utf8 = require('utf8');
// const base_url = 'http://10.0.0.109:3000'
const base_url_front = 'http://10.0.0.109:8080'
var mainEvCount = 0;
var evCount = 0;




class GuestsController {

    constructor() {}

    index(file, pool) {

        const pathDir = './uploads/' + (new Date().getDate() + 1)

        if (!fs.existsSync(pathDir)) {
            fs.mkdirSync(pathDir);
        }

        var user = {}
        const data = xlsx.parse('./uploads/' + file.originalname);

        data.forEach(d => {
            d.data.forEach(async user => {
                if (user[0] === '№ п/п') return;
                const u = {
                    id: user[0],
                    last_name: user[1],
                    name: user[2],
                    second_name: user[3],
                    status: user[4],
                    isActive: user[5],
                    organization: user[6],
                    user_id: crypto.createHmac('sha256', String(new Date()) + Math.random()).digest('hex'),
                    event_id: user[7]
                }

                console.log("Начинаю запись в базу")

                pool.query('INSERT INTO users (last_name, name, second_name, status, isActive, organization, isLoggedIn, user_id, event_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [u.last_name, u.name, u.second_name, u.status, u.isActive, u.organization, false, u.user_id, u.event_id])

                pool.query('insert into user_event (user_id, event_id) values (?,?)', [u.id, u.event_id])

                const pathQR = String(pathDir + '/' + u.id + '_' + u.last_name + u.name + u.second_name + '.png');
                console.log(pathQR)

                QRCode.toFile(
                    pathQR, [{ data: process.env.BASE_URL + '/#/user/' + u.user_id }],
                )
            })
        })

        zip.zip(pathDir, './public/data' + new Date().getDate() + '.zip');
        return String('/data' + new Date().getDate() + '.zip')
    }

    async events(file, pool) {

        const connection = await mysql.createConnection({
            host: 'localhost',
            user: "root",
            database: "ais",
            password: "admin"
        });

        const data = xlsx.parse('./uploads/' + file.originalname)

        console.log(JSON.stringify(data))
        var eventDate = "";
        var eventDateStop = "";

        try {
            for (let i = 0; i < data[0].data.length; i++) {
                console.log("Начинаю обработку")
                if (data[0].data[i][0] === '!') {
                    console.log("Main event")
                    var pattern = /(\d{2})\.(\d{2})\.(\d{4})/;
                    var timeStart = new Date(data[0].data[i][2].replace(pattern, '$3-$2-$1'));
                    var timeStop = new Date(data[0].data[i][3].replace(pattern, '$3-$2-$1'));
                    try {
                        await connection.execute('INSERT INTO main_events (title, timeStart, timeStop) VALUES (?,?,?)', [data[0].data[i][1], timeStart, timeStop])
                        mainEvCount = await connection.execute("select id from main_events order by id desc limit 1")
                    } catch (err) {
                        console.log("Bad value")
                    }

                    console.log(mainEvCount[0])
                    mainEvCount = mainEvCount[0][0].id
                } else if (data[0].data[i][0] === '-') {
                    console.log(data[0].data[i])
                    var pattern = /(\d{2})\.(\d{2})\.(\d{4})/;

                    var timeStart = new Date(data[0].data[i][2].replace(pattern, '$3-$2-$1') + " " + data[0].data[i][4]);
                    eventDate = timeStart.toLocaleDateString();
                    console.log(timeStart)
                    var timeStop = new Date(data[0].data[i][3].replace(pattern, '$3-$2-$1') + " " + data[0].data[i][5]);
                    eventDateStop = timeStop.toLocaleDateString();


                    try {
                        await connection.execute('INSERT INTO events_table (main_id, title, timeStart, timeStop, place, isBig) VALUES (?,?,?,?,?,?)', [mainEvCount, data[0].data[i][1], timeStart, timeStop, data[0].data[i][6], data[0].data[i][7]])
                        evCount = await connection.execute("select id from events_table order by id desc limit 1")
                        evCount = evCount[0][0].id
                    } catch (err) {
                        console.log(err)
                    }
                } else if (data[0].data[i][0] === '/') {
                    var pattern = /(\d{2})\.(\d{2})\.(\d{4})/;

                    var timeStart = new Date(eventDate.replace(pattern, '$3-$2-$1') + " " + data[0].data[i][4]);
                    var timeStop = new Date(eventDate.replace(pattern, '$3-$2-$1') + " " + data[0].data[i][5]);

                    await console.log(timeStart)

                    try {
                        await connection.execute('INSERT INTO sub_events (event_id, title, timeStart, timeStop, place) VALUES (?,?,?,?,?)', [evCount, data[0].data[i][1], timeStart, timeStop, data[0].data[i][6]])
                    } catch (err) {
                        console.log(err + " " + data[0].data[i][1])
                    }
                }
            }
        } catch (e) {
            console.log(e)
            return "Error!" + e
        }
        return "Success"
    }
}

module.exports = GuestsController