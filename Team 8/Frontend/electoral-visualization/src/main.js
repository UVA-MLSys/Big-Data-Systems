import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import mitt from "mitt";

const eventBus = mitt();

const app = createApp(App);

// Provide the event bus to all components
app.provide("$bus", eventBus);

app.mount("#app");
