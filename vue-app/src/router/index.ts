import {createRouter, createWebHistory} from 'vue-router'

import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Register from "../pages/Register.vue";
import Login from "../pages/Login.vue";
import AddReview from "../pages/AddReview.vue";
import ManageMovieData from "../pages/ManageMovieData.vue";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/add-review',
        name: 'AddReview',
        component: AddReview,
    },
    {
        path: '/manage-movie-data',
        name: 'ManageMovieData',
        component: ManageMovieData,
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
