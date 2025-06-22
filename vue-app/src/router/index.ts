import {createRouter, createWebHistory} from 'vue-router'

import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Register from "../pages/Register.vue";
import Login from "../pages/Login.vue";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/about',
        name: 'About',
        component: About,
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
