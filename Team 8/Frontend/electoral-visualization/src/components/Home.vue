<script>
import { inject, ref, onMounted, onBeforeUnmount, computed } from "vue";
import { views } from "../constants/views";
import DisplayOptionsList from "./DisplayOptionsList.vue";
import ResponsiveHouseMap from "./ResponsiveHouseMap.vue";
import ResponsiveFundingMap from "./ResponsiveFundingMap.vue";
import ResponsiveChart from "./ResponsiveChart.vue";
import DisplaySelectionList from "./DisplaySelectionList.vue";
export default {
  name: "Home",
  components: {
    DisplayOptionsList,
    ResponsiveHouseMap,
    ResponsiveFundingMap,
    ResponsiveChart,
    DisplaySelectionList,
  },
  setup() {
    // Inject the Event Bus
    const bus = inject("$bus");

    // Display view
    const displayView = ref(views.HOUSE);

    // Loading State
    const isLoading = ref(false);

    // Progress Value
    const progressValue = ref(15);

    // Listen for view render Event
    bus.on("renderEvt", (renderEvt) => {
      displayView.value = renderEvt;
    });

    // Listen to the Loading state start and stop from Map and chart Component
    bus.on("triggerLoadingStateEvt", (loadingState) => {
      isLoading.value = loadingState;
      progressValue.value = 15;
      // When the value is true we would like to show the progress values
      if (loadingState) {
        handleLoadingState();
      } else {
        // Reset the progress Value
        progressValue.value = 15;
      }
    });

    const title = ref("Electoral Visualization");
    const description = ref("House Data Visualization");
    const isSmallScreen = ref(window.innerWidth < 1400);

    onMounted(() => {
      window.addEventListener("resize", handleResize);
    });

    onBeforeUnmount(() => {
      window.removeEventListener("resize", handleResize);
    });

    const handleResize = () => {
      isSmallScreen.value = window.innerWidth < 1400;
    };

    const handleDescriptionRender = computed(() => {
      switch (displayView.value) {
        case views.HOUSE:
          return "House Data Visualization";
        case views.FUNDING:
          return "Funding Data Visualization";
        case views.CHARTS:
          return "Total Votes count Visualization";
      }
    });
    const handleLoadingState = () => {
      const interval = 2000; // Interval between increments in milliseconds

      const timer = setInterval(() => {
        if (progressValue.value < 90) {
          if (progressValue.value === 30) {
            progressValue.value = 60;
          } else if (progressValue.value === 60) {
            progressValue.value = 75;
          } else if (progressValue.value === 75) {
            progressValue.value = 90;
          } else {
            progressValue.value += 15;
          }
        } else {
          clearInterval(timer);
        }
      }, interval);
    };

    return {
      views,
      title,
      description,
      displayView,
      isSmallScreen,
      isLoading,
      progressValue,
      handleDescriptionRender,
    };
  },
};
</script>

<template>
  <div id="app">
    <!-- Progress Bar for data loading -->
    <div
      v-if="isLoading"
      class="bg-white rounded-xl shadow-sm overflow-hidden p-1"
    >
      <div class="relative h-6 flex items-center justify-center">
        <div
          class="progress absolute top-0 bottom-0 left-0 rounded-lg"
          :class="{
            'w-[15%] bg-violet-200': progressValue == 15,
            'w-[30%] bg-orange-200': progressValue == 30,
            'w-[60%] bg-sky-500': progressValue == 60,
            'w-[75%] bg-teal-200': progressValue == 75,
            'w-[90%] bg-green-200': progressValue == 90,
          }"
        ></div>
        <div
          class="relative font-medium text-sm"
          :class="{
            'text-violet-900': progressValue == 15,
            'text-orange-900': progressValue == 30,
            'text-sky-900': progressValue == 60,
            'text-teal-900': progressValue == 75,
            'text-green-900': progressValue == 90,
          }"
        >
          {{ progressValue }}%
        </div>
      </div>
    </div>

    <div class="grid grid-cols-12 gap-4 content-start items-center">
      <div
        class="flex justify-center w-full"
        :class="{
          'col-span-1': !isSmallScreen,
          'col-span-12 mt-32': isSmallScreen,
        }"
      >
        <display-options-list />
      </div>

      <!-- The Body that renders the Maps and Chart -->
      <div
        :class="{ 'col-span-8': !isSmallScreen, 'col-span-12': isSmallScreen }"
      >
        <h1>{{ title }}</h1>
        <h2>{{ handleDescriptionRender }}</h2>
        <responsive-house-map v-if="displayView == views.HOUSE" />
        <responsive-funding-map v-if="displayView == views.FUNDING" />
        <responsive-chart v-if="displayView == views.CHARTS" />
      </div>
      <div
        class="flex justify-center ml-12"
        :class="{ 'col-span-3': !isSmallScreen, 'col-span-12': isSmallScreen }"
      >
        <display-selection-list />
      </div>
    </div>
  </div>
</template>


<style>
#app {
  max-width: 1400px !important;
}

.progress {
  animation: progress 1s infinite linear;
}

.left-right {
  transform-origin: 0% 50%;
}
@keyframes progress {
  0% {
    transform: translateX(0) scaleX(0);
  }
  40% {
    transform: translateX(0) scaleX(0.4);
  }
  100% {
    transform: translateX(100%) scaleX(0.5);
  }
}
</style>