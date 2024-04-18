<template>
  <div class="relative" @click="toggleDropdown">
    <button
      ref="dropdownButtonRef"
      type="button"
      class="inline-flex justify-between w-56 px-4 py-2 text-sm font-medium text-white bg-gray-800 rounded-md shadow-sm hover:bg-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75"
      aria-haspopup="listbox"
      :aria-expanded="open ? 'true' : 'false'"
    >
      <span>Select Year</span>
      <svg
        class="w-5 h-5 ml-2 -mr-1 text-white"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
        aria-hidden="true"
      >
        <path
          fill-rule="evenodd"
          d="M10 12a1 1 0 01-.707-.293l-4-4a1 1 0 011.414-1.414L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4A1 1 0 0110 12z"
          clip-rule="evenodd"
        />
      </svg>
    </button>

    <div
      ref="dropdownListRef"
      v-show="open"
      class="absolute z-10 w-full mt-1 bg-white shadow-lg"
      style="display: none"
    >
      <ul
        class="py-1 overflow-auto text-base rounded-md ring-1 ring-black ring-opacity-5 max-h-60 focus:outline-none sm:text-sm"
        tabindex="-1"
        role="listbox"
        aria-labelledby="listbox-label"
        aria-activedescendant="listbox-item-3"
      >
        <li
          v-for="year in years"
          :key="year"
          @click="selectYear(year)"
          class="text-gray-900 cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-gray-100"
          role="option"
        >
          <span class="font-normal block truncate">{{ year }}</span>
          <span
            v-if="selectedYear === year"
            class="text-gray-600 absolute inset-y-0 right-0 flex items-center pr-4"
          >
            <!-- Heroicon name: check -->
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
                d="M8.5 11.5 11 14l4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
              />
            </svg>
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>
  
  <script>
import { inject, ref, onMounted, watch } from "vue";

export default {
  setup() {
    const bus = inject("$bus");

    const open = ref(false);
    const selectedYear = ref(null);
    const years = ref([]);
    const dropdownButtonRef = ref(null);
    const dropdownListRef = ref(null);

    const toggleDropdown = () => {
      open.value = !open.value;
    };

    const generateYears = () => {
      // 2024 - 2 = 2022 // because that is the data we have
      // generic approach to handle Odd and Even years
      const currentYear =
        new Date().getFullYear() % 2 == 0
          ? new Date().getFullYear() - 2
          : new Date().getFullYear() - 1;
      const startYear = 1976;
      years.value = Array.from(
        { length: (currentYear - startYear) / 2 + 1 },
        (_, i) => startYear + i * 2
      );
    };

    const selectYear = (year) => {
      selectedYear.value = year;
      bus.emit("yearSelectionEvt", year);
      open.value = false;
    };

    onMounted(() => {
      generateYears();
    });

    // Watch for changes in the dropdown's visibility and adjust button width
    watch(open, () => {
      if (open.value) {
        const buttonWidth = dropdownButtonRef.value.offsetWidth;
        dropdownListRef.value.style.width = buttonWidth + "px";
      }
    });

    return {
      open,
      selectedYear,
      years,
      toggleDropdown,
      selectYear,
      dropdownButtonRef,
      dropdownListRef,
    };
  },
};
</script>
  
  <style>
/* Add your custom styles here */
</style>
  