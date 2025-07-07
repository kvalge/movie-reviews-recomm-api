import {createRouter, createWebHistory} from 'vue-router'

import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Register from "../views/Register.vue";
import Login from "../views/Login.vue";
import AddReview from "../views/AddReview.vue";
import ManageMovieData from "../views/ManageMovieData.vue";

import {useAuthStore} from '../stores/authStore'
import {storeToRefs} from 'pinia'

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
        meta: {requiresAdmin: true}
    },
    {
        path: '/manage-movie-data',
        name: 'ManageMovieData',
        component: ManageMovieData,
        meta: {requiresAdmin: true}
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

router.beforeEach((to, _, next) => {
    const auth = useAuthStore()
    const {isAuthenticated, user} = storeToRefs(auth)

    if (to.meta.requiresAdmin) {
        if (!isAuthenticated.value || user.value?.username !== 'admin') {
            return next('/login')
        }
    }

    next()
})


export default router
