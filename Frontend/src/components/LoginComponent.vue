<template>
  <div class="card">
    <div class="card-header">Giriş Yap</div>
    <div class="card-body">
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="loginUsername">Kullanıcı Adı</label>
          <input
              type="text"
              class="form-control"
              id="loginUsername"
              placeholder="Kullanıcı Adı"
              v-model="username"
              required
          />
        </div>
        <div class="form-group">
          <label for="loginPassword">Şifre</label>
          <input
              type="password"
              class="form-control"
              id="loginPassword"
              placeholder="Şifre"
              v-model="password"
              required
          />
        </div>
        <button type="submit" class="btn btn-primary mt-2">Giriş Yap</button>
        <div v-if="error_message" class="alert alert-danger mt-2" role="alert">
          {{ error_message }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Vue_Login",
  data() {
    return {
      username: "",
      password: "",
      error_message: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await this.$axios.post("/login", {
          username: this.username,
          password: this.password,
        });
        if (response.data.status === "success") {
          localStorage.setItem("authToken", response.data.token);
          this.$router.replace("/");
          this.$emit("login");
        } else {
          this.error_message = response.data.message;
        }
      } catch (error) {
        console.error(error);
      }
    },


  },
};
</script>
