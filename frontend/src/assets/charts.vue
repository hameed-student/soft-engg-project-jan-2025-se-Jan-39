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
      <h3>Course Content Duration (Weeks)</h3>
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
  props:{
    courses: Array,
    pendingApprovals: Array,  
    pendingEnrollments: Array,
    data: Object
  },

  components: {
    Bar,
    Line,
    Pie
  },
  data() {
    return {
      

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
  computed: {
    courseLabels1() {
      return this.courses ? this.courses.map(course => course.name) : [];
    },
    students(){
      return this.courses ? this.courses.map(course => course.students) : [];
    },
    enrollmentData() {
      return {
        labels: this.courseLabels1,
        datasets: [
          {
            label: 'Enrolled Students',
            data: this.students, // Number of enrolled students per course
            backgroundColor: '#42A5F5', // Color for the bars
            borderColor: '#1E88E5',
            borderWidth: 1,
          },
        ],
      };
    },
    gpendingApprovals(){
      return this.pendingApprovals.length;
    },
    gpendingEnrollments(){
      return this.pendingEnrollments.length;
    },

    approvalData() {
      return{
        labels: [ 'course approvals for support','student enrolments' ],
        datasets: [
          {
            label: 'Approved',
            
            data: [this.data.approvals-this.gpendingApprovals,this.data.enrolled-this.gpendingEnrollments], // Approved students
            backgroundColor: '#66BB6A',
            stack: 'approval',
          },
          {
            label: 'Pending',
            data: [this.gpendingApprovals,this.gpendingEnrollments], // Unapproved students
            backgroundColor: '#EF5350',
            stack: 'approval',
          },
        ],
      };
    },
    support(){
      return this.courses ? this.courses.map(course => course.support_staff) : [];
    },
    staffData() {return{
        labels: this.courseLabels1,
        datasets: [
          {
            label: 'Support Staff',
            data: this.support, // Number of support staff per course
            fill: false,
            borderColor: '#7E57C2',
            tension: 0.1,
            pointBackgroundColor: '#5E35B1',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 5
          }
        ]
      };},
      // Data for the fourth chart - Pie chart showing course duration in weeks
      weeks(){
        return this.courses ? this.courses.map(course => course.weeks) : [];
      },
      weekData() {return{
        labels: this.courseLabels1,
        datasets: [
          {
            data: this.weeks,
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
      };}


  }
  }
);
</script><style scoped>
@import '@/assets/card.css';

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 20px;
}

.graph-container {
  padding: 20px;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  background-color: white;
}

.chart-wrapper {
  position: relative;
  height: 350px;
  width: 100%;
}

.pie-wrapper {
  height: 400px;
}

h3 {
  text-align: center;
  margin-bottom: 15px;
  color: #333;
}

@media (max-width: 991px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>