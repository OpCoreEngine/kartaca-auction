<template>
  <div class="card">
    <div class="card-header">Kayıt Ol</div>
    <div class="card-body">
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="registerUsername">
            Kullanıcı Adı
          </label>
          <input
              type="text"
              class="form-control"
              id="registerUsername"
              placeholder="Kullanıcı Adı"
              v-model="username"
              required
          />
        </div>
        <div class="form-group">
          <label for="registerPassword">Şifre</label>
          <input
              type="password"
              class="form-control"
              id="registerPassword"
              placeholder="Password"
              v-model="password"
              required
          />
        </div>
        <button type="submit" class="btn btn-primary mt-2">Kayıt ol</button>
        <div v-if="error_message" class="alert alert-danger mt-2" role="alert">
          {{ error_message }}
        </div>
        <div v-if="success_message" class="alert alert-success mt-2" role="alert">
          {{ success_message }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Vue_Register",
  data() {
    return {
      username: "",
      password: "",
      error_message: "",
      success_message: "",
    };
  },
  methods: {
    async register() {
      try {
        const response = await this.$axios.post("/register", {
          username: this.username,
          password: this.password,
        });
        if (response.data.status === "success") {
          this.success_message = response.data.message;
          this.error_message = "";
          await this.$router.push("/login");
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
