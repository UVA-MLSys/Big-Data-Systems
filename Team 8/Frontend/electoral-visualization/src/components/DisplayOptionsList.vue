<template>
  <div class="flex flex-col items-start space-y-4 nav-margin">
    <!-- Iterate over display options and render list items -->
    <div class="flex flex-col flex-1 overflow-y-auto">
      <nav
        class="flex-1 px-2 py-4 nav-background rounded shadow-2xl hover:shadow-xl shadow-inner focus:shadow-xl"
      >
        <a
          href="#"
          @click="renderView(views.HOUSE)"
          class="flex items-center px-4 py-2 hover:nav-background hover:font-bold transition duration-300 shadow-md hover:shadow-xl focus:shadow-xl"
          :class="{
            'text-gray-800': !toggleActiveOption(views.HOUSE),
            'text-purple-700': toggleActiveOption(views.HOUSE),
          }"
        >
          <svg
            class="h-6 w-6 mr-2"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m4 12 8-8 8 8M6 10.5V19a1 1 0 0 0 1 1h3v-3a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3h3a1 1 0 0 0 1-1v-8.5"
            />
          </svg>

          House Data
        </a>
        <a
          href="#"
          @click="renderView(views.FUNDING)"
          class="flex items-center px-4 py-2 mt-2 hover:nav-background hover:font-bold transition duration-300 shadow-md hover:shadow-xl focus:shadow-xl"
          :class="{
            'text-gray-800': !toggleActiveOption(views.FUNDING),
            'text-purple-700': toggleActiveOption(views.FUNDING),
          }"
        >
          <svg
            class="h-6 w-6 mr-2"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 17.345a4.76 4.76 0 0 0 2.558 1.618c2.274.589 4.512-.446 4.999-2.31.487-1.866-1.273-3.9-3.546-4.49-2.273-.59-4.034-2.623-3.547-4.488.486-1.865 2.724-2.899 4.998-2.31.982.236 1.87.793 2.538 1.592m-3.879 12.171V21m0-18v2.2"
            />
          </svg>

          Funding
        </a>
        <a
          href="#"
          @click="renderView(views.CHARTS)"
          class="flex items-center px-4 py-2 mt-2 hover:nav-background hover:font-bold transition duration-300 shadow-md hover:shadow-xl focus:shadow-xl"
          :class="{
            'text-gray-800': !toggleActiveOption(views.CHARTS),
            'text-purple-700': toggleActiveOption(views.CHARTS),
          }"
        >
          <svg
            class="h-6 w-6 mr-2"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 4.5V19a1 1 0 0 0 1 1h15M7 14l4-4 4 4 5-5m0 0h-3.207M20 9v3.207"
            />
          </svg>

          Charts
        </a>
      </nav>
    </div>
  </div>
</template>
  
  
<script>
import { inject, ref } from "vue";
import { views } from "../constants/views";
export default {
  name: "Display Options List",
  setup() {
    // Inject the Event Bus
    const bus = inject("$bus");

    const displayView = ref(views.HOUSE);

    // Get the switch case to redirect to the corresponding pages accordingly
    const renderView = (render) => {
      displayView.value = render; // set this to control the active list option
      bus.emit("renderEvt", render);
    };

    // Toggle the Active state of the Options
    const toggleActiveOption = (activeOption) => {
      return activeOption === displayView.value;
    };
    return { views, displayView, renderView, toggleActiveOption };
  },
};
</script>
  
  <style>
.nav-margin {
  margin-top: -100px !important;
  margin-left: -200px !important;
}

.nav-background {
  background-color: #bfbfbf !important;
}
</style>
  