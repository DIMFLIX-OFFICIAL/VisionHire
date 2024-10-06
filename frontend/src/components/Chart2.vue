<script setup>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  DoughnutController,
} from "chart.js";
import { defineProps, toRef, ref, onMounted, watch } from "vue";

const getColor = (color) =>
  getComputedStyle(document.documentElement.children[1])
    .getPropertyValue(color)
    .trim();

ChartJS.register(Title, Tooltip, Legend, ArcElement, DoughnutController);

const props = defineProps({
  labels: {
    type: Array,
    default: () => ["January", "February", "March"],
  },
  label: {
    type: String,
    default: "Sales",
  },
  data: {
    type: Array,
    default: () => [40, 20, 12],
  },
});
const refProps = toRef(props);

const chartData = {
  labels: refProps.value.labels,
  datasets: [
    {
      label: refProps.value.label,
      backgroundColor: [
        getColor("--green"),
        getColor("--red"),
        getColor("--lavander"),
      ],
      data: refProps.value.data,
    },
  ],
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: refProps.value.label,
      font: {
        size: 20,
        weight: "bold",
        family: "Arial",
      },
      color: getColor("--text"),
    },
    legend: {
      display: false,
      labels: {
        color: getColor("--text"),
        font: {
          size: 14,
        },
      },
    },
    tooltip: {
      enabled: true, // Enable tooltips for pie chart
    },
  },
};

const myChart = ref(null);
let chartInstance = null;

onMounted(() => {
  const ctx = myChart.value.getContext("2d");
  chartInstance = new ChartJS(ctx, {
    type: 'doughnut', // Change to 'pie'
    data: chartData,
    options: chartOptions,
  });
});

watch(
  () => props,
  (n) => {
    chartInstance.destroy();
    const ctx = myChart.value.getContext("2d");
    chartInstance = new ChartJS(ctx, {
      type: 'doughnut', // Change to 'pie'
      data: {
        labels: refProps.value.labels,
        datasets: [
          {
            label: refProps.value.label,
            backgroundColor: [
              getColor("--green"),
              getColor("--red"),
              getColor("--lavander"),
            ],
            data: refProps.value.data,
          },
        ],
      },
      options: chartOptions,
    });
  },
  { deep: true }
);
</script>

<template>
    <canvas class="chart" ref="myChart"></canvas>
</template>

<style scoped>
.chart {
  min-width: 45%;
  height: 400px;
}
</style>
