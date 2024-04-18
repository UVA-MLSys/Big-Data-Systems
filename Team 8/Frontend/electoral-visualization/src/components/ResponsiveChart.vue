<template>
  <Bar
    id="third-chart-id"
    :key="chartKey"
    class="cursor-pointer"
    :options="chartOptions"
    :data="chartData"
  />
</template>
  
  <script>
import axios from "axios";
import { inject, computed, ref, reactive, watch } from "vue";
import { urls } from "../constants/urls";
import { views } from "../constants/views";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

export default {
  name: "ResponsiveChart",
  components: { Bar },
  setup() {
    const bus = inject("$bus");

    // Define the BASE API URL for our AWS API Gateway
    const url = urls.BASE_API;

    // Initial Party we use the LIBERAL
    const party = ref("LIBERAL");

    // Listen for party selection Event from Display Chart Selection component
    bus.on("partyChartSelectionEvt", (partySelected) => {
      party.value = partySelected;
    });

    // Fetch New data when party is selected
    watch(party, () => {
      fetchData(party.value);
    });

    const chartOptions = computed(() => ({
      responsive: true,
      plugins: {
        legend: {
          position: "right",
        },
        title: {
          display: true,
          text: party.value, // "Third Party Chart",
        },
      },
    }));

    // On Mount populate with the LIBERAL data
    const chartData = reactive({
      labels: [
        1976, 1978, 1980, 1982, 1984, 1986, 1988, 1990, 1992, 1994, 1996, 1998,
        2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022,
      ],
      datasets: [
        {
          label: "Fusion States (NY and CT)",
          data: [
            4663124, 3441664, 4189066, 2899280, 2914730, 1524270, 2728290, 0,
            3613523, 2445962, 3553168, 2832819, 3001917, 1744157, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0,
          ],
          backgroundColor: "#3b82f6",
        },
        {
          label: "All Other States",
          data: [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0,
          ],
          backgroundColor: "#ef4444",
        },
      ],
    });

    const chartKey = ref(0); // Key to force re-render

    const fetchData = (party) => {
      // Define the URL and query parameters
      const params = {
        view: views.CHARTS,
        party: party,
      };

      // Make the GET request using Axios
      axios
        .get(url, { params })
        .then((response) => {
          // Clear existing data arrays
          chartData.labels = [];
          chartData.datasets[0].data = [];
          chartData.datasets[1].data = [];

          // Iterate over the response objects and populate the reactive datasets
          response.data.forEach((obj) => {
            // Populate labels array with year values
            chartData.labels.push(obj.year);

            // Populate fusion_states data array
            chartData.datasets[0].data.push(obj.fusion_states.total_votes);

            // Populate rest_states data array
            chartData.datasets[1].data.push(obj.rest_states.totalvotes);
          });

          // Update the chart key to trigger a re-render
          chartKey.value += 1;

          bus.emit("triggerLoadingStateEvt", false);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    };

    return { chartKey, chartData, chartOptions };
  },
};
</script>