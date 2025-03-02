<template>
  <div class="box" style="grid-template-columns: repeat(2,1fr);grid-template-rows: auto auto ;display:grid">
    <h1>Visual statistics</h1> <br>
    <div class="graph-container">
      <!-- First graph: Number of enrolled students vs Course Name (Bar Chart) -->
      <h3>Enrolled Students per Course</h3>
      <div class="chart-wrapper">
        <Bar
          :data="enrollmentData"
          :options="barChartOptions"
        />
      </div>
    </div>

    <div class="graph-container">
      <!-- Second graph: Number of approved students vs unapproved -->
      <h3>Administrative</h3>
      <div class="chart-wrapper">
        <Bar
          :data="approvalData"
          :options="stackedBarOptions"
        />
      </div>
    </div>
    
    <div class="graph-container">
      <!-- Third graph: Number of support staff per course (Line Chart) -->
      <h3>Support Staff per Course</h3>
      <div class="chart-wrapper">
        <Line
          :data="staffData"
          :options="lineChartOptions"
        />
      </div>
    </div>
    
    <div class="graph-container">
      <!-- Fourth graph: Number of weeks vs course name (Pie Chart) -->
      <h3>Course Duration (Weeks)</h3>
      <div class="chart-wrapper pie-wrapper">
        <Pie
          :data="weekData"
          :options="pieChartOptions"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar, Line, Pie } from 'vue-chartjs';

// Register the necessary Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

export default defineComponent({
  name: 'Dashboard',
  components: {
    Bar,
    Line,
    Pie
  },
  data() {
    return {
      // Data for the first bar chart (Enrolled students per course)
      enrollmentData: {
        labels: ['Math', 'Science', 'History', 'Art', 'Music'], // Course names
        datasets: [
          {
            label: 'Enrolled Students',
            data: [100, 150, 90, 70, 120], // Number of enrolled students per course
            backgroundColor: '#42A5F5', // Color for the bars
            borderColor: '#1E88E5',
            borderWidth: 1,
          },
        ],
      },

      // Options for the first bar chart
      barChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Number of Enrolled Students vs Course Name',
            padding: {
              top: 10,
              bottom: 10
            }
          },
          legend: {
            position: 'top',
            labels: {
              boxWidth: 10,
              padding: 10
            }
          },
          tooltip: {
            callbacks: {
              label: function (tooltipItem) {
                return `${tooltipItem.label}: ${tooltipItem.raw} students`;
              },
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              padding: 5
            }
          },
          x: {
            ticks: {
              padding: 5
            }
          }
        },
        layout: {
          padding: {
            bottom: 10
          }
        }
      },

      // Data for the second stacked bar chart (Approved vs Unapproved Students)
      approvalData: {
        labels: ['enrolments', 'support approvals' ],
        datasets: [
          {
            label: 'Approved',
            data: [30, 50, 40, 70, 20], // Approved students
            backgroundColor: '#66BB6A',
            stack: 'approval',
          },
          {
            label: 'Unapproved',
            data: [70, 50, 60, 30, 80], // Unapproved students
            backgroundColor: '#EF5350',
            stack: 'approval',
          },
        ],
      },

      // Options for the second stacked bar chart
      stackedBarOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Approved vs Unapproved',
            padding: {
              top: 10,
              bottom: 10
            }
          },
          legend: {
            position: 'top',
            labels: {
              boxWidth: 15,
              padding: 10
            }
          }
        },
        scales: {
          x: {
            stacked: true,
            ticks: {
              padding: 5
            }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            ticks: {
              padding: 5
            }
          }
        },
        layout: {
          padding: {
            bottom: 10
          }
        }
      },
      
      // Data for the third chart - Line chart showing support staff per course
      staffData: {
        labels: ['Math', 'Science', 'History', 'Art', 'Music'],
        datasets: [
          {
            label: 'Support Staff',
            data: [5, 8, 4, 3, 6],
            fill: false,
            borderColor: '#7E57C2',
            tension: 0.1,
            pointBackgroundColor: '#5E35B1',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 5
          }
        ]
      },
      
      // Options for the line chart
      lineChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Number of Support Staff per Course',
            padding: {
              top: 10,
              bottom: 10
            }
          },
          tooltip: {
            callbacks: {
              label: function(tooltipItem) {
                return `${tooltipItem.dataset.label}: ${tooltipItem.raw} staff`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1,
              padding: 5
            },
            title: {
              display: true,
              text: 'Number of Staff'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Course'
            }
          }
        }
      },
      
      // Data for the fourth chart - Pie chart showing course duration in weeks
      weekData: {
        labels: ['Math', 'Science', 'History', 'Art', 'Music'],
        datasets: [
          {
            data: [12, 16, 10, 8, 14],
            backgroundColor: [
              '#FF7043', 
              '#26C6DA', 
              '#FFA726', 
              '#66BB6A',
              '#9575CD'
            ],
            borderColor: '#ffffff',
            borderWidth: 2
          }
        ]
      },
      
      // Options for the pie chart
      pieChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: {
              padding: 15
            }
          },
          tooltip: {
            callbacks: {
              label: function(tooltipItem) {
                return `${tooltipItem.label}: ${tooltipItem.raw} weeks`;
              }
            }
          }
        }
      }
    };
  },
});
</script>

<style scoped>
@import '@/assets/card.css';
.graph-container {
  margin: 20px;
  padding: 20px;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  background-color: white;
  overflow: hidden; /* Prevent content from spilling out */
  min-width: 80%;
  

}

.chart-wrapper {
  position: relative;
  height: 350px; /* Fixed height for the chart */
  width: 100%;
  margin-bottom: 15px; /* Add space at the bottom */
}

.pie-wrapper {
  height: 400px; /* Slightly taller for the pie chart and its legend */
}

h3 {
  text-align: center;
  margin-bottom: 15px;
  color: #333;
}

@media (min-width: 992px) {
  .graph-container {
    width: calc(50% - 40px);
    
    vertical-align: top;
  }
  .box{
    display:flex;
    justify-content: center;
  }
}
</style>