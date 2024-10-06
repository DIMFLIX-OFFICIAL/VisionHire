<script setup>
import { logout } from "@/modules/auth";
import { getAccountInfo, getTasks } from "@/modules/api";
import Footer from "@/components/Footer.vue";
import { onMounted, ref, toRaw } from "vue";
import Header from "@/components/Header.vue";
import Chart from "@/components/Chart.vue";
import Chart2 from "@/components/Chart2.vue";
import List from "@/components/List.vue";
import Modal from "@/components/Modal.vue";
import Filter from "@/assets/svg/Filter.vue";
import { candidates } from "@/stubs/Candidats.stubs";
import { todos as td } from "@/stubs/Todos.stubs";
import { getMetrNewCandidates } from "@/modules/api";
// import {todos} from "@/stubs/Todos.stubs";

const name = ref("");
const todos = ref([]);
const todoDATA = ref([]);

onMounted(async () => {
  let user = await getAccountInfo();

  if (user !== null) {
    name.value = user.name;
    let result = await getTasks();
    // console.log(result["tasks"]);

    // Set todoDATA with proxied tasks
    todoDATA.value = result["tasks"];

    // Accessing raw data
    todos.value = toRaw(todoDATA.value)
    console.log(toRaw(todoDATA.value), 'todos.value'); // Accessing the first item as a raw object
  } else {
    logout();
  }
});
const dataDictionary = [
  { title: "Соотношение отказов к приглашениям", data: [30, 50, 60] },
  { title: "Процент заполненных вакансий", data: [100, 200, 150] },
];

const chartLabels = ref(["2024-10-07", "2024-10-08", "2024-10-09"]);
const chartData = ref([30, 50, 60]);
const chartLabel = ref("Соотношение отказов к приглашениям");

const isModalVisible = ref(false);
const startDate = ref("");
const endDate = ref("");
const selectedData = ref(dataDictionary[0].title);

const chartLabels2 = ref(["2024-10-07", "2024-10-08", "2024-10-09"]);
const chartData2 = ref([30, 50, 60]);
const chartLabel2 = ref("Соотношение отказов к приглашениям");
const isModalVisible2 = ref(false);
const startDate2 = ref("");
const endDate2 = ref("");
const selectedData2 = ref(dataDictionary[0].title);

const openModalFilterBar = () => {
  isModalVisible.value = true;
};
const closeModalFilterBar = () => {
  isModalVisible.value = false;
};

const applyFilter = async () => {
  const start = new Date(startDate.value);
  const end = new Date(endDate.value);
  const dateArray = [];

  for (let d = start; d <= end; d.setDate(d.getDate() + 1)) {
    dateArray.push(new Date(d).toISOString().split("T")[0]); // Формат YYYY-MM-DD
  }

  const filteredData = dataDictionary.find(
    (item) => item.title === selectedData.value
  );

  chartLabels.value = dateArray; // Массив дат для графика
  chartData.value = await getMetrNewCandidates(`${start}`, `${end}`); //filteredData.data; // Данные для графика
  chartLabel.value = filteredData.title; // Название графика

  console.log(chartLabels.value);
  console.log(chartData.value);

  closeModalFilterBar();
};
const openModalFilterBar2 = () => {
  isModalVisible2.value = true;
};

const closeModalFilterBar2 = () => {
  isModalVisible2.value = false;
};

const applyFilter2 = () => {
  const start2 = new Date(startDate2.value);
  const end2 = new Date(endDate2.value);
  const dateArray2 = [];

  for (let d = start2; d <= end2; d.setDate(d.getDate() + 1)) {
    dateArray2.push(new Date(d).toISOString().split("T")[0]); // Формат YYYY-MM-DD
  }

  const filteredData2 = dataDictionary.find(
    (item) => item.title === selectedData2.value
  );

  chartLabels2.value = dateArray2; // Массив дат для графика
  chartData2.value = filteredData2.data; // Данные для графика await getMetr(`${start}`, `${end}`);
  chartLabel2.value = filteredData2.title; // Название графика

  console.log(chartLabels2.value);
  console.log(chartData2.value);

  closeModalFilterBar2();
};
</script>

<template>
  <Header page="main" />
  <div class="home">
    <div class="lists">
      <List type="cand" title="Кандидаты" :list="candidates" class="cand" />
      <List type="todo" title="TODO" :list="td" class="todo" />
    </div>

    <div class="charts">
      <div class="chart">
        <Chart :labels="chartLabels" :label="chartLabel" :data="chartData" />
        <button class="filter" @click="openModalFilterBar">
          <Filter />
        </button>
        <Modal class="graph-modal" :modelValue="isModalVisible" @update:modelValue="isModalVisible = $event">
          <div class="content">
            <p class="title">Фильтр графиков</p>

            <div class="inps">
              <div class="inp">
                <label for="startDate">Начальная дата:</label>
                <input class="selector" type="date" id="startDate" v-model="startDate" />
              </div>

              <div class="inp">
                <label for="endDate">Конечная дата:</label>
                <input class="selector" type="date" id="endDate" v-model="endDate" />
              </div>

              <div class="inp">
                <label for="dataSelect">Выберите данные:</label>
                <select class="selector" id="dataSelect" v-model="selectedData">
                  <option v-for="item in dataDictionary" :key="item.title" :value="item.title">
                    {{ item.title }}
                  </option>
                </select>
              </div>
            </div>


            <button @click="applyFilter" class="apply-filter-btn">Применить фильтр</button>
          </div>
        </Modal>
      </div>
      <div class="chart">
        <Chart2 :labels="chartLabels2" :label="chartLabel2" :data="chartData2" />
        <button class="filter" @click="openModalFilterBar2">
          <Filter />
        </button>
        <Modal class="graph-modal" :modelValue="isModalVisible2" @update:modelValue="isModalVisible2 = $event">
          <div class="content">
            <p class="title">Фильтр графиков</p>

            <div class="inps">
              <div class="inp">
                <label for="startDate2">Начальная дата:</label>
                <input class="selector" type="date" id="startDate2" v-model="startDate2" />
              </div>

              <div class="inp">
                <label for="endDate2">Конечная дата:</label>
                <input class="selector" type="date" id="endDate2" v-model="endDate2" />
              </div>

              <div class="inp">
                <label for="dataSelect2">Выберите данные:</label>
                <select class="selector" id="dataSelect2" v-model="selectedData2">
                  <option v-for="item in dataDictionary" :key="item.title" :value="item.title">
                    {{ item.title }}
                  </option>
                </select>
              </div>
            </div>

            <button @click="applyFilter2" class="apply-filter-btn">Применить фильтр</button>
          </div>
        </Modal>
      </div>

    </div>

    <Modal class="graph-modal" :modelValue="isModalVisible" @update:modelValue="isModalVisible = $event">
      <div class="content">
        <p class="title">Фильтр графиков</p>

        <div class="inps">
          <div class="inp">
            <label for="startDate">Начальная дата:</label>
            <input class="selector" type="date" id="startDate" v-model="startDate" />
          </div>

          <div class="inp">
            <label for="endDate">Конечная дата:</label>
            <input class="selector" type="date" id="endDate" v-model="endDate" />
          </div>

          <div class="inp">
            <label for="dataSelect">Выберите данные:</label>
            <select class="selector" id="dataSelect" v-model="selectedData">
              <option v-for="item in dataDictionary" :key="item.title" :value="item.title">
                {{ item.title }}
              </option>
            </select>
          </div>
        </div>


        <button @click="applyFilter" class="apply-filter-btn">Применить фильтр</button>
      </div>
    </Modal>

    <img src="/api/protected/my_avatar" v-if="false" />
    <Footer />
  </div>
</template>

<style scoped lang="scss">
.home {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-content: center;
  gap: 50px;
  min-height: 100vh;
  width: 100%;

  .lists {
    display: flex;
    justify-content: space-between;

    .cand {
      width: 50%;
    }

    .todo {
      width: 40%;

    }
  }

  .charts {
    margin: 100px 0 100px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-around;
    padding: 0 150px;
    gap: 50px;

    .chart {
      display: flex;
      position: relative;

      .filter {
        position: absolute;
        top: 0px;
        right: 0px;
        background: var(--sbg);
        color: var(--text);
        border-radius: 50px;
        padding: 0;
        width: 50px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
      }
    }
  }

  .title {
    font-size: 40px;
    margin-bottom: 0;
  }

  .description {
    margin-bottom: 30px;
    font-size: 16px;
    color: var(--text);
  }

  .logout-btn {
    background: var(--lavander);
    border-radius: 15px;
    border: none;
    width: 30%;
    max-width: 500;
    height: 60px;
    color: var(--hinted-text);
    font-weight: 600;
    font-size: 18px;
  }
}

.graph-modal {
  .content {
    display: flex;
    flex-direction: column;

    .title {
      font-size: 35px;
      margin-bottom: 20px;
    }

    .inps {
      display: flex;
      flex-direction: column;
      gap: 20px;
      margin-bottom: 30px;

      .inp {
        display: flex;
        gap: 20px;
        white-space: nowrap;
        height: 50px;
        align-items: center;

        .selector {
          width: 100%;
          background-color: var(--sbg-light);
          border: none;
          border-radius: 10px;
          color: var(--text);
          outline: none;
          height: 100%;
        }
      }
    }

    .apply-filter-btn {
      background: var(--lavander);
      border-radius: 15px;
      border: none;
      width: 100%;
      height: 60px;
      color: var(--hinted-text);
      font-weight: 600;
      font-size: 18px;
    }
  }

}
</style>
