import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);
import axios from 'axios'

export default new Vuex.Store({

    state: {
        user: JSON.parse(localStorage.getItem('user') || '[]'),
        guests: JSON.parse(localStorage.getItem('guests') || '[]'),
        users: JSON.parse(localStorage.getItem('users') || '[]'),
        recEvents: JSON.parse(localStorage.getItem('rec_events') || '[]'),
        events: JSON.parse(localStorage.getItem('events') || '[]'),
        getUrl: 'http://localhost:5000/',
        place: '',
        guests_today: JSON.parse(localStorage.getItem('guests_today') || '[]'),
        now: '',
        subnow: '',
        more_event: JSON.parse(localStorage.getItem('more_event') || '[]'),
        more_subevent: JSON.parse(localStorage.getItem('more_subevent') || '[]'),
    },

    mutations: {
        add_user(state, data) {
            state.user = data
        },

        resetBar(state, data) {
            state.now = data
        },
        updateBar(state, data) {
            state.now = data
        },
        updateSubBar(state, data) {
            state.subnow = data
        },
        getGuests(state, data) {
            state.guests = data
            console.log(state.guests)
        },
        getUsers(state, data) {
            state.users = data
        },
        getEvents(state, data) {
            state.events = data
        },
        getRecentEvents(state, events) {
            state.recEvents = events
        },

        getPlace(state, place) {
            state.place = place
        },
        guests_today(state, guests) {
            state.guests_today = guests
        },
        get_more_event(state, data) {
            state.more_event = data
        },
        get_more_subevent(state, data) {
            state.more_subevent = data
        }
    },

    actions: {

        async updateBar({ commit }, data) {
            var now = new Date(Date.now()).getTime()
            var start = new Date(data[0]).getTime()
            var stop = new Date(data[1]).getTime()
            var result = ((now - start) / (stop - start)) * 100
            commit('updateBar', result)

            if (stop < now) {
                if (result < 100) {
                    return 0
                } else {
                    console.log(1)
                    return 1
                }
            }
        },

        async updateSubBar({ commit }, data) {
            var now = new Date(Date.now()).getTime()
            var start = new Date(data[0]).getTime()
            var stop = new Date(data[1]).getTime()
            var result = ((now - start) / (stop - start)) * 100
            commit('updateSubBar', result)
        },

        async getUsers({ commit }) {
            return new Promise((resolve, reject) => {
                axios.get(this.state.getUrl + 'api/getUsers')
                    .then(resp => {
                        if (resp.data) {
                            commit('getUsers', resp.data)
                            localStorage.setItem('users', JSON.stringify(resp.data))
                            resolve(resp)
                        }
                    })
                    .catch(err => {
                        localStorage.removeItem('users')
                        reject(err)
                    })
            })
        },

        async login({ commit }, id) {
            return new Promise((resolve, reject) => {
                axios.get(this.state.getUrl + 'api/auth/' + id)
                    .then(resp => {
                        if (resp.data) {
                            console.log(resp.data)
                            resp.data.isLoggedIn = true
                            localStorage.setItem('user', JSON.stringify(resp.data))
                            commit('add_user', resp.data)
                            resolve(resp)
                        }
                    })
                    .catch(err => {
                        console.log(err)
                        localStorage.removeItem('user')
                        reject(err)
                    })
            })
        },

        async getGuests({ commit }, id) {
            return new Promise((resolve, reject) => {
                axios.get(this.state.getUrl + 'api/guests/' + id)
                    .then(resp => {
                        if (resp.data) {
                            commit('getGuests', resp.data)
                            localStorage.setItem('guests', JSON.stringify(resp.data))
                            resolve(resp)
                        } else {
                            resolve('На данное мероприятие никто не зарегистрировался')
                        }
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },

        async updateUser(id) {
            axios({ url: this.state.getUrl + 'api/setLog/' + id, method: 'GET' })
                .then(resp => {
                    if (resp.data) {
                        console.log("Success!", resp.data)
                    }
                })
        },

        async getRecentEvents({ commit }) {
            // if (!localStorage.getItem('rec_events')) {
            return new Promise((resolve, reject) => {
                    axios.get(this.state.getUrl + 'api/recentEvents')
                        .then(res => {
                            commit('getRecentEvents', res.data)
                            localStorage.setItem('rec_events', JSON.stringify(res.data))
                            resolve(res.data)
                        })
                        .catch(err => {
                            reject(err)
                        })
                })
                // } else {
                //   return this.state.recEvents
                // }
        },

        async getEvents({ commit }) {
            if (!localStorage.getItem('events')) {
                return new Promise((resolve, reject) => {
                    axios.get(this.state.getUrl + 'api/getEvents')
                        .then(res => {
                            commit('getEvents', res.data)
                            localStorage.setItem('events', JSON.stringify(res.data))
                            resolve(res.data)
                        })
                        .catch(err => {
                            reject(err)
                        })
                })
            } else {
                return this.state.events
            }
        },

        // async createEvent(data) {
        //     console.log(data)
        //     await axios.post(this.state.getUrl + 'api/createEvent', { data: data })
        //         .then(res => {
        //             console.log(res)
        //         })
        // },

        async guests_today({ commit }) {
            if (!localStorage.getItem('guests_today')) {
                await axios.get(this.state.getUrl + 'api/guests_today')
                    .then(res => {
                        console.log(res)
                        commit('guests_today', res.data)
                        localStorage.setItem('guests_today', JSON.stringify(res.data))
                    })
            } else {
                return this.state.guests_today
            }
        },

        async get_more_event({ commit }, id) {
            if (!localStorage.getItem('more_event') || !localStorage.getItem('more_subevent')) {
                await axios.get(this.state.getUrl + 'api/more_event/' + id)
                    .then(res => {
                        console.log(res.data)
                        commit('get_more_subevent', res.data.data)
                        commit('get_more_event', res.data.event)
                        localStorage.setItem('more_event', JSON.stringify(res.data))
                        localStorage.setItem('more_subevents', JSON.stringify(res.data))
                    })
            } else {
                return this.state.more_event
            }
        }
    },

    getters: {

        isAdmin: state => {
            if (state.user.isActive == 0) {
                return true
            } else {
                return false
            }
        },
        getUser: state => {
            return state.user
        },

        guestsGetter: state => {
            if (state.guests) {
                state.guests.guests.forEach(guest => {
                    guest.name_all = guest.last_name + ' ' + guest.name + ' ' + guest.second_name
                })
                return state.guests
            }
        },

        getRecentEventss: state => {
            return state.recEvents
        },

        getUrl: state => state.getUrl,

        getUsers: state => state.users,

        placeGetter: state => state.place,
        guests_today: state => {
            state.guests_today.forEach(guest => {
                guest.name_all = guest.last_name + ' ' + guest.name + ' ' + guest.second_name
            })
            return state.guests_today
        },

        getEvents: state => state.events,

        getNow: state => state.now,
        getSubNow: state => state.subnow,
        getMoreEvent: state => state.more_event,
        getMoreSubEvent: state => state.more_subevent
    },

    modules: {}
});