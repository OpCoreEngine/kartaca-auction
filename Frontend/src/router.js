import {createRouter, createWebHistory} from "vue-router";
import ProductList from "./components/ProductsComponent.vue";
import LoginForm from "./components/LoginComponent.vue";
import RegisterForm from "./components/RegisterComponent.vue";
import axios from "axios";

const routes = [
    {
        path: "/",
        name: "ProductList",
        component: ProductList,
        meta: {requiresAuth: true}
    },
    {
        path: "/login",
        name: "LoginForm",
        component: LoginForm,
        meta: {requiresGuest: true}
    },
    {
        path: "/register",
        name: "RegisterForm",
        component: RegisterForm,
        meta: {requiresGuest: true}
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const isLoggedIn = localStorage.getItem("isLoggedIn");
    const authToken = localStorage.getItem("authToken");

    if (authToken) {
        axios.post("/token_validation", {}, {
            headers: {
                Authorization: `Bearer ${authToken}`
            }
        })
    }

    if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
        next("/login");
    } else if (to.matched.some(record => record.meta.requiresGuest) && isLoggedIn) {
        next("/");
    } else {
        next();
    }
});

export default router;
