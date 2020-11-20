var express = require('express');
var router = express.Router();
const app = express();
const path = require('path')
const mysql = require("mysql2");
const crypto = require('crypto');
const multer = require("multer");
const multiparty = require('multiparty')
const axios = require('axios')
const utf8 = require('utf8');

var bodyParser = require('body-parser')
var urlencodedParser = bodyParser.urlencoded({ extended: false })

const pool = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    database: 'ais',
    password: 'admin'
});

var file = ""
var description = ""
var id = ""
var guests = []


const storage = multer.diskStorage({
    destination: function(req, file, cb) {
        cb(null, './public/images')
    },
    filename: function(req, file, cb) {
        cb(null, file.originalname)
    }
});
const upload = multer({ storage: storage });

const GuestsController = require('./../controllers/GuestsController')

//***************************/ API BLOCK *****************************//

var id = ""

router.get('/api/more_event/:id', async function(req, res) {
    var event = []
    pool.query('select * from events_table where id = ?', [req.params.id], function(err, data) {
        if (err) throw err;
        if (data) {
            event = data
            pool.query('select * from sub_events where event_id = ?', [data[0].id], function(err, data) {
                res.send({ data: data, event: event })
            })
        }
    })
})

router.get('/api/auth/:id', async function(req, res) {

    var user = []
    pool.query("select * from users where user_id=?", [req.params.id],
        function(err, data) {
            if (err) throw err;
            if (data.length > 0) {
                user = data[0]
                pool.query("update users set isLoggedIn = true where user_id=?", [req.params.id],
                    function(err, data) {
                        if (err) throw err;
                    });

                res.setHeader('Access-Control-Allow-Origin', '*');
                res.setHeader('Access-Control-Allow-Headers', 'origin, content-type, accept');
                console.log(user)
                res.send(user)
            } else {
                res.send({ id: '000', last_name: 'Гость', name: 'Гость', second_name: '', isLoggedIn: false })
            }
        });
})

router.get('/api/guests/:id', async function(req, res) {
    var guests = []
    var main_event = []
    var isLoad = false
    var guests = []
    var main_event = []

    pool.query('select * from users where event_id = ?', [req.params.id], function(err, data) {
            if (data.length > 0) {
                guests = data
                pool.query('select * from main_events where id = ?', [req.params.id], function(err, data) {
                    if (data.length > 0) {
                        main_event = data
                        res.send({ guests: guests, main_event: main_event })
                    }
                })
            }
        })
        // pool.query('select user_id, event_id from user_event where event_id = ?', [req.params.id], function(err, data) {
        //     if (data.length > 0) {
        //       data.forEach(user => {
        //           pool.query('select * from users where id = ? and isActive = 1', [user.user_id], function(err, data) {
        //               if (data[0]) {
        //                   guests.push(data[0])
        //               }
        //           })
        //           pool.query('select * from main_events where id = ?', [req.params.id], function(err, data) {
        //               if (err) throw err;
        //               main_event = data
        //               isLoad = true
        //           })
        //       })
        //     } else {
        //       pool.query('select * from main_events where id = ?', [req.params.id], function(err, data) {
        //           if (err) throw err;
        //           res.send({event: data})
        //       })
        //     }
        // })

    var myVar = setTimeout(function() {
        if (isLoad) {
            res.send({
                guests: guests,
                event: main_event[0]
            })
        }
    }, 100)
})

router.get('/api/guests_today', async function(req, res) {
    var guests_id = []
    var guests = []
    var main_ids = []
    var isLoad = false

    // main_ids.forEach(event => {
    // pool.query('select user_id from user_event where event_id = 113', function(err,data) {
    //     if (err) throw err;
    //     data.forEach(user => {
    //       console.log(user)
    pool.query('select * from users where event_id = 113', function(err, data) {
            if (err) throw err;
            res.send(data)
        })
        // })
        // })
        // })

    // setTimeout(function() {
    //     if (isLoad) {
    //         res.send(guests)
    //     }
    // }, 300)
})

router.get('/api/getUsers', async function(req, res) {
    pool.query("select * from users where event_id = 113",
        function(err, data) {
            if (data) {
                res.send(data)
                return data
            } else {
                return "Error!"
            }
        }
    );
})

router.get('/api/deleteUsers', async function(req, res) {
    pool.query('delete from users where isActive = 1', function(err, data) {
        if (err) {
            res.send(err)
        }
        res.send("Success")
    })
})

router.post('/api/upload', async function(req, res) {
    let storage = multer.diskStorage({
        destination: function(req, file, cb) {
            cb(null, './uploads')
        },

        filename: function(req, file, cb) {
            cb(null, file.originalname)
        }
    });

    const uploadFile = multer({ storage: storage }).single('file');
    const gc = new GuestsController()

    await uploadFile(req, res, async function(err) {
        if (err) {
            return res.send(err);
        }
        res.send(await gc.index(req.file, pool))
    })
});

router.post('/api/uploadEvents', async function(req, res) {
    let storage = multer.diskStorage({
        destination: function(req, file, cb) {
            cb(null, './uploads')
        },

        filename: function(req, file, cb) {
            cb(null, file.originalname)
        }
    });

    const uploadFile = multer({ storage: storage }).single('file');
    const gc = new GuestsController(pool)

    await uploadFile(req, res, async function(err) {
        if (err) {
            return res.send(err);
        }
        res.send(await gc.events(req.file, pool))
    })
});

router.get('/api/recentEvents', async function(req, res) {

    var isLoad = false
    var mainEvents = []
    var count = 0

    pool.query("select * from main_events where timeStop > CURDATE()",
        function(err, data) {
            console.log(data)
            if (err) throw err;
            if (data.length > 0) {
                for (let i = 0; i < data.length; i++) {
                    mainEvents.push({
                        id: data[i].id,
                        mainTitle: data[i].title,
                        mainDesc: data[i].description,
                        mainTimeStart: data[i].timeStart,
                        mainTimeStop: data[i].timeStop,
                        image: data[i].image,
                        events: []
                    })
                    pool.query('select * from events_table where timeStop > ? order by timeStart asc limit 3', [new Date(Date.now())], function(err, data) {
                        if (err) throw err;
                        if (data) {
                            count += data.length
                            for (let j = 0; j < data.length; j++) {
                                mainEvents[i].events.push({
                                    id: data[j].id,
                                    main_id: data[j].main_id,
                                    title: data[j].title,
                                    description: data[j].description,
                                    timeStart: data[j].timeStart,
                                    timeStop: data[j].timeStop,
                                    place: data[j].place,
                                    isBig: data[j].isBig,
                                    subevents: []
                                })
                                pool.query('select * from sub_events where event_id = ?', [data[j].id], function(err, data) {
                                    if (err) console.log(err)
                                    for (let k = 0; k < data.length; k++) {
                                        mainEvents[i].events[j].subevents.push({
                                            subTitle: data[k].title,
                                            subTimeStart: data[k].timeStart,
                                            subTimeStop: data[k].timeStop,
                                        })
                                    }
                                })
                            }
                        }
                    })
                    isLoad = true
                }
            } else {
                console.log('No data')
                res.send()
            }
        });

    var myVar = setTimeout(function() {
        if (isLoad) {
            res.send(mainEvents)
        }
    }, 300)
})

router.post('/api/createEvent', urlencodedParser, async function(req, res) {
    const event = req.body.data
    pool.query("insert into events (title, big_event_title, description, timeStart, timeStop, place, big_event_id, image) values (?,?,?,?,?,?,?,?)", [event.title, event.big_event_title, event.description, event.timeStart, event.timeStop, event.place, "1", event.image],
        function(err, data) {
            if (data) {
                res.send(data)
                return data
            } else {
                return "Error!"
            }
        });
})

router.get('/api/getEvents', async function(req, res) {
    var isLoad = false
    var mainEvents = []
    pool.query("select * from main_events",
        function(err, data) {
            console.log(data)
            if (data.length == 0) {
                res.send({ result: "Empty" })
            }
            for (let i = 0; i < data.length; i++) {
                mainEvents.push({
                    id: data[i].id,
                    mainTitle: data[i].title,
                    mainDesc: data[i].description,
                    mainTimeStart: data[i].timeStart,
                    mainTimeStop: data[i].timeStop,
                    image: data[i].image,
                    events: []
                })
                pool.query('select * from events_table where main_id = ?', [data[i].id], function(err, data) {
                    for (let j = 0; j < data.length; j++) {
                        mainEvents[i].events.push({
                            title: data[j].title,
                            description: data[j].description,
                            timeStart: data[j].timeStart,
                            timeStop: data[j].timeStop,
                            place: data[j].place,
                            isBig: data[j].isBig,
                            subevents: []
                        })
                        pool.query('select * from sub_events where event_id = ?', [data[j].id], function(err, data) {
                            for (let k = 0; k < data.length; k++) {
                                mainEvents[i].events[j].subevents.push({
                                    subTitle: data[k].title,
                                    subTimeStart: data[k].timeStart,
                                    subTimeStop: data[k].timeStop,
                                })
                            }
                            isLoad = true
                        })
                    }
                })
            }
            // } else {
            //     return "Error!"
            // }
        });
    var myVar = setTimeout(function() {
        if (isLoad) {
            res.send(mainEvents)
        }
    }, 300)
})

router.get('/api/getCustomEvent/:id', async function(req, res) {
    var guests = ''
    pool.query('select id from users where event_id = ?', [req.params.id], async function(err, data) {
        guests = data
    })

    pool.query("select id, description, image from main_events where id =?", [req.params.id], function(err, data) {
        if (!err) {
            res.send({
                data: data,
                guests: guests
            })
        } else {
            res.send("Error" + err)
        }
    })
})

router.get('/api/getSingleEvent/:id', async function(req, res) {
    var isLoad = false
    var mainEvents = []
    var guests = []

    pool.query('select user_id from user_event where event_id = ?', [req.params.id], function(err, data) {
        for (let i = 0; i < data.length; i++) {
            pool.query('select * from users where id = ?', [data[i].user_id], function(err, data) {
                guests.push(data)
            })
        }
    })

    pool.query("select * from main_events where id = ?", [req.params.id],
        function(err, data) {
            if (data) {
                for (let i = 0; i < data.length; i++) {
                    mainEvents.push({
                        id: req.params.id,
                        mainTitle: data[i].title,
                        mainDesc: data[i].description,
                        mainTimeStart: data[i].timeStart,
                        mainTimeStop: data[i].timeStop,
                        image: data[i].image,
                        guests: guests,
                        events: []
                    })
                    pool.query('select * from events_table where main_id = ?', [data[i].id], function(err, data) {
                        for (let j = 0; j < data.length; j++) {
                            mainEvents[i].events.push({
                                title: data[j].title,
                                description: data[j].description,
                                timeStart: data[j].timeStart,
                                timeStop: data[j].timeStop,
                                place: data[j].place,
                                isActive: 0,
                                isBig: data[j].isBig,
                                subevents: []
                            })
                            pool.query('select * from sub_events where event_id = ?', [data[j].id], function(err, data) {
                                for (let k = 0; k < data.length; k++) {
                                    mainEvents[i].events[j].subevents.push({
                                        subTitle: data[k].title,
                                        subTimeStart: data[k].timeStart,
                                        subTimeStop: data[k].timeStop,
                                        isActive: 0,
                                    })
                                }
                                isLoad = true
                            })
                        }
                    })
                }
            } else {
                return "Error!"
            }
        });
    var myVar = setTimeout(function() {
        if (isLoad) {
            res.json(mainEvents)
        }
    }, 500)
})

router.post('/api/createFeedback', async function(req, res) {
    const subject = req.body.subject
    const body = req.body.body
    const user_id = req.body.user_id
    pool.query("insert into feedback (id, user_id, subject, body) values (?, ?,?,?)", [new Date(), user_id, subject, body], function(err, data) {
        if (!err) {
            res.send("Success")
        } else {
            console.log(err)
            res.send("Error" + err)
        }
    })
})

router.post('/api/getPlace', async function(req, res) {
    console.log(req.body.guests)
    axios.post('http://10.100.0.1:8080/api/v1.0/placing', {
            guests: req.body.guests,
            user: req.body.user
        })
        .then(result => {
            res.send(result.data)
        })
        .catch(err => {
            res.send("Ошибка загрузки изображения")
        })
})

router.post('/api/updateEvent', upload.single('file'), async function(req, res) {

    try {
        var fileName = req.file.originalname
    } catch (err) {
        try {
            var fileName = await JSON.parse(req.body.data).image
        } catch (err) {
            res.send(err)
            return
        }
    }
    description = await JSON.parse(req.body.data).title
    guests = await JSON.parse(req.body.guests)
    id = await req.body.id

    pool.query('update main_events set description = ?, image = ? where id = ?', [description, fileName, id], function(err, data) {
        if (err) {
            console.log(err)
            res.send(err)
        }
        res.send("Success")
    })

    if (guests) {
        guests.forEach(g => {
            pool.query('insert into user_event (user_id, event_id) values (?,?)', [g, id])
        })
    }
})

router.get('/api/deleteEvent/:id', async function(req, res) {
    var eventId = ''
    var mainId = req.params.id
    try {
        pool.query('delete from main_events where id = ?', [mainId], function(err, data) {
            pool.query('select id from events_table where main_id = ?', [mainId], function(err, data) {

                data.forEach(d => {
                    pool.query('delete from sub_events where event_id = ?', [d.id], function(err, data) {})
                })
                pool.query('delete from events_table where main_id = ?', [req.params.id], function(err, data) {})
            })
        })
    } catch (e) {
        res.send("Error " + e)
    }
    res.send("Success")
})

//*******************************************************************//

module.exports = router;