<template>
  <div class="w-100">
    <div class="card w-100">
      <div class="card-header">Ürünler - Hoşgeldiniz, {{ username }}</div>
      <ul class="list-group list-group-flush">
        <li
            class="list-group-item"
            v-for="product in products"
            :key="product.id"
        >
          <h3>{{ product.name }}</h3>
          <p>{{ product.description }}</p>
          <strong>Şu anki fiyat:</strong> {{ product.price }}
          <br/>
          <strong>En son teklif veren:</strong> {{ product.last_bidder }}
          <br/>
          <div class="form-check form-check-inline">
            <input
                class="form-check-input"
                type="radio"
                :id="product.id + '-10'"
                value="10"
                v-model="product.increment"
                :name="product.id + '-increment-10'"
            />
            <label class="form-check-label" :for="product.id + '-10'">10</label>
          </div>
          <div class="form-check form-check-inline">
            <input
                class="form-check-input"
                type="radio"
                :id="product.id + '-30'"
                value="30"
                v-model="product.increment"
                :name="product.id + '-increment-30'"
            />
            <label class="form-check-label" :for="product.id + '-30'">30</label>
          </div>
          <div class="form-check form-check-inline">
            <input
                class="form-check-input"
                type="radio"
                :id="product.id + '-50'"
                value="50"
                v-model="product.increment"
                :name="product.id + '-increment-50'"
            />
            <label class="form-check-label" :for="product.id + '-50'">50</label>
          </div>
          <div class="form-check form-check-inline">
            <input
                class="form-check-input"
                type="radio"
                :id="product.id + '-100'"
                value="100"
                v-model="product.increment"
                :name="product.id + '-increment-100'"
            />
            <label class="form-check-label" :for="product.id + '-100'">100</label>
          </div>
          <button type="button"
                  class="btn btn-outline-primary"
                  @click="bid(product.id, product.increment)"
          >
            Teklif Ver
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import io from "socket.io-client";

export default {
  name: "VueProducts",
  data() {
    return {
      products: [],
      socket: null,
      username: "",
    };
  },
  async created() {
    this.socket = io("http://127.0.0.1:7003")
    this.socket.on("connect", () => {
      this.socket.emit("join", {room: "products"});
    });
    this.socket.on("update_price", (data) => {
      this.updatePrice(data);
    });
    await this.fetchUsername();
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const token = localStorage.getItem("authToken");
        const response = await axios.get("http://127.0.0.1:7003/products", {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        });
        this.products = response.data.map((p) => {
          p.increment = "10";
          return p;
        });
      } catch (error) {
        console.error("Ürünler alınamadı:", error);
      }
    },
    async bid(productId, increment) {
      try {
        const token = localStorage.getItem("authToken");
        const response = await axios.post(
            `http://127.0.0.1:7003/bid/${productId}`,
            {increment: increment},
            {
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
                Accept: "application/json",
              },
            });

        if (response.data.success) {
          this.socket.emit("bid", {
            product_id: productId,
            new_price: response.data.new_price,
            last_bidder: response.data.last_bidder,
            room: "products",
          });

          const updatedPrice = response.data.new_price;
          const product = this.products.find(p => p.id === productId);

          if (product) {
            product.price = updatedPrice;
            product.last_bidder = response.data.last_bidder;

          }
        } else {
          console.error("Teklif verme başarısız oldu:", response.data.message);
        }
      } catch (error) {
        console.error("Teklif verme başarısız oldu:", error);
      }
    },
    updatePrice(data) {
      const product = this.products.find(p => p.id === data.product_id);
      if (product) {
        product.price = data.new_price;
        product.last_bidder = data.last_bidder;
      }
    }, async fetchUsername() {
      try {
        const token = localStorage.getItem("authToken");
        const response = await axios.get("http://127.0.0.1:7003/get_username", {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        });
        this.username = response.data.username;
      } catch (error) {
        console.error("Kullanıcı adı alınamadı:", error);
      }
    },
  },
  beforeUnmount() {
    this.socket.emit("leave", {room: "products"});
    this.socket.disconnect();
  },
};
</script>
