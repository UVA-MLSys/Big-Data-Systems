<template>
  <div class="relative" @mouseenter="showTooltip" @mouseleave="hideTooltip">
    <div v-show="displayTooltip" class="bg-gray-500">
      <span
        class="align-middle text-sm font-bold text-white bg-gray-500 bg-opacity-80 px-2 py-1 rounded-md tooltip"
      >
        The Transaction Amount contributed in Dollars. Please select the range.
      </span>
    </div>

    <div class="flex gap-4">
      <h3>Transaction Amount</h3>
      <svg
        class="w-6 h-6 text-gray-800 dark:text-white"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9.529 9.988a2.502 2.502 0 1 1 5 .191A2.441 2.441 0 0 1 12 12.582V14m-.01 3.008H12M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
        />
      </svg>
    </div>
  </div>

  <div class="grid grid-cols-12 gap-4 content-start items-center">
    <div class="col-span-6">
      <input
        type="range"
        class="mr-4 cursor-pointer"
        :min="minValue"
        :max="maxValue / 2"
        :step="stepValue"
        v-model="minSliderValue"
      />
    </div>
    <div class="col-span-6 pl-4">
      <input
        type="range"
        class="mr-4 cursor-pointer"
        :min="maxValue / 2 + 1"
        :max="maxValue"
        :step="stepValue"
        v-model="maxSliderValue"
      />
    </div>

    <div class="mr-2 col-span-6">
      Min:
      <input
        id="min-slider"
        type="text"
        inputmode="numeric"
        v-model="formattedMinSliderValue"
        @input="handleMinInput"
        class="w-24 mx-2 py-1 border rounded-md"
      />
    </div>
    <div class="ml-8 col-span-6">
      Max:
      <input
        id="max-slider"
        type="text"
        inputmode="numeric"
        v-model="formattedMaxSliderValue"
        @input="handleMaxInput"
        class="w-24 mx-2 py-1 border rounded-md"
      />
    </div>

    <div class="col-span-12 ml-12">
      <button
        v-if="searching"
        :disabled="searching"
        type="button"
        class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-md shadow-md transition duration-300 ease-in-out"
      >
        <svg
          aria-hidden="true"
          role="status"
          class="inline mr-3 w-4 h-4 text-white animate-spin"
          viewBox="0 0 100 101"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
            fill="#E5E7EB"
          ></path>
          <path
            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
            fill="currentColor"
          ></path>
        </svg>
        Searching...
      </button>
      <button
        v-if="!searching"
        class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-md shadow-md transition duration-300 ease-in-out"
        @click="searchEvent"
      >
        Search
      </button>
    </div>
  </div>
</template>
  
  <script>
import { inject, ref, computed, watch } from "vue";

export default {
  setup() {
    const bus = inject("$bus");

    // Listen to the Loading state start and stop from Map and chart Component
    // to stop the searching bar
    bus.on("triggerLoadingStateEvt", (loadingState) => {
      if (!loadingState) {
        searching.value = loadingState; // sets to false
      }
    });

    const minValue = 25;
    const maxValue = 2800000;
    const stepValue = 1;
    const displayTooltip = ref(false);
    const searching = ref(false);

    const minSliderValue = ref(100);
    const maxSliderValue = ref(1000);

    const showTooltip = () => {
      displayTooltip.value = true;
    };

    const hideTooltip = () => {
      displayTooltip.value = false;
    };

    // Define a computed property to format minSliderValue
    const formattedMinSliderValue = computed({
      get() {
        return minSliderValue.value
          .toString()
          .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      },
      set(newValue) {
        // Remove commas before setting the value
        const newMinValueWithoutCommas = newValue.replace(/,/g, "");
        minSliderValue.value = parseInt(newMinValueWithoutCommas);
      },
    });

    const handleMinInput = (event) => {
      let newValue = event.target.value.replace(/\D/g, ""); // Remove non-numeric characters
      if (newValue === "" || isNaN(newValue)) {
        newValue = 0;
      }
      if (newValue > maxValue / 2) {
        minSliderValue.value = maxValue / 2;
      } else {
        minSliderValue.value = parseInt(newValue);
      }
    };

    // Handle Max sliders
    const formattedMaxSliderValue = computed({
      get() {
        return maxSliderValue.value
          .toString()
          .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      },
      set(newValue) {
        // Remove commas before setting the value
        const newMaxValueWithoutCommas = newValue.replace(/,/g, "");
        maxSliderValue.value = parseInt(newMaxValueWithoutCommas);
      },
    });

    const handleMaxInput = (event) => {
      let newValue = event.target.value.replace(/\D/g, ""); // Remove non-numeric characters
      if (newValue === "" || isNaN(newValue)) {
        newValue = 0;
      }
      if (newValue > maxValue) {
        maxSliderValue.value = maxValue;
      } else {
        maxSliderValue.value = parseInt(newValue);
      }
    };

    watch(minSliderValue, () => {
      if (parseInt(minSliderValue.value) > parseInt(maxSliderValue.value)) {
        maxSliderValue.value = (maxValue / 2 + 1).toString();
      }
    });

    // Search Event propagated to the Responsive Funding component
    const searchEvent = () => {
      const sliderValues = {
        min: minSliderValue.value,
        max: maxSliderValue.value,
      };
      searching.value = true;
      bus.emit("searchFundingDataEvt", sliderValues);
    };

    return {
      minValue,
      maxValue,
      stepValue,
      minSliderValue,
      maxSliderValue,
      showTooltip,
      hideTooltip,
      displayTooltip,
      searching,
      searchEvent,
      handleMinInput,
      handleMaxInput,
      formattedMinSliderValue,
      formattedMaxSliderValue,
    };
  },
};
</script> 