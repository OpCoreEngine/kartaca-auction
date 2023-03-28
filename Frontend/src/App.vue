<template>
  <div class="h-100">
    <div class="form-wrapper">
      <div class="container vh-100 vw-100 d-flex">
        <div v-if="!isLoggedIn" class="w-100 row mt-auto mb-auto justify-content-center">
          <div class="col-12 col-md-3">
            <LoginForm @login="onLogin"/>
          </div>
          <div class="col-12 col-md-3">
            <RegisterForm/>
          </div>
        </div>
        <div v-if="isLoggedIn" class="container">
          <div class="row pt-5">
            <ProductList/>
            <div class="w-100">
              <button @click="onLogout" class="btn btn-danger col-12 mt-2">Çıkış Yap</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import LoginForm from "./components/LoginComponent.vue";
import RegisterForm from "./components/RegisterComponent.vue";
import ProductList from "./components/ProductsComponent.vue";

export default {
  name: "App",
  components: {
    LoginForm,
    RegisterForm: RegisterForm,
    ProductList
  },
  data() {
    return {
      isLoggedIn: false
    };
  },
  created() {
    const storedLoginStatus = localStorage.getItem("isLoggedIn");
    if (storedLoginStatus === "true") {
      this.isLoggedIn = true;
    }
  },
  methods: {
    onLogin() {
      this.isLoggedIn = true;
      localStorage.setItem("isLoggedIn", "true");
    },
    onLogout() {
      this.isLoggedIn = false;
      localStorage.removeItem("isLoggedIn");
      localStorage.removeItem("authToken");
      this.$router.push("/login");
    }
  }
};
</script>
