import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [{
        path: "/",
        name: "Home",
        component: Home
    },
    {
        path: '/events',
        name: 'Events',
        component: () =>
            import ('../views/Events.vue')
    },
    {
        path: '/event/:id',
        name: 'SingleEvent',
        component: () =>
            import ('../views/SingleEvent.vue')
    },
    {
        path: '/guests/:id',
        name: 'Guests',
        component: () =>
            import ('../views/Guests.vue')
    },
    {
        path: '/guests_today',
        name: 'GuestsToday',
        component: () =>
            import ('../views/GuestsToday.vue')
    },
    {
        path: '/map',
        name: 'Map',
        component: () =>
            import ('../views/Map.vue')
    },
    {
        path: '/user/:id',
        name: 'User',
        component: () =>
            import ('../views/User.vue')
    },
    {
        path: '/add',
        name: 'Dashboard',
        component: () =>
            import ('../views/Dashboard.vue')
    },
    {
        path: '/howtouse',
        name: 'Info',
        component: () =>
            import ('../views/Info.vue')
    },
    {
        path: '/chief',
        name: 'Chief',
        component: () =>
            import ('../views/Chief.vue')
    },
    {
        path: '/structure',
        name: 'Structure',
        component: () =>
            import ('../views/Structure.vue')
    },
    {
        path: '/scheme',
        name: 'Scheme',
        component: () =>
            import ('../views/Scheme.vue')
    },
    {
        path: '/contacts',
        name: 'Contacts',
        component: () =>
            import ('../views/Contacts.vue')
    },
    {
        path: '/more_event/:id',
        name: 'MoreEvent',
        component: () => import ('../views/MoreEvent.vue')
    }
];

const router = new VueRouter({
    routes
});

export default router;