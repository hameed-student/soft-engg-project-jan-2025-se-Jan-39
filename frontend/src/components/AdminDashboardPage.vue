<template>
  <div class="body">
    <NavBar @fetchData="fetchData"/>
    <AddCourseContents :course="course" :isVisible="isAddCourseContentVisible"  @close="isAddCourseContentVisible = false;course={}" />
    <div class="container">
      <h3>Welcome Admin</h3>
      <br><br>
      <!-- Pending Support Staff Approvals -->
      <div v-if="pendingApprovals.length != 0" class="box">
        <h1>Pending Support Staff Approvals</h1>
        <div class="table-container">
          <table class="styled-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Course</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="staff in pendingApprovals" :key="staff.staff_id" class="hover:bg-gray-50">
                <td>{{ staff.staff_name }}</td>
                <td>{{ staff.staff_email }}</td>
                <td>{{ staff.course_name }}</td>
                <td>
                  <button @click="manageApprovals(staff.staff_id, staff.course_id, 'approve')" class="button">Approve</button>
                  <button @click="manageApprovals(staff.staff_id, staff.course_id, 'reject')" class="button">Reject</button>
                </td>
              </tr>
              
            </tbody>
          </table>
        </div>
      </div>
      <p v-else class="box">No approvals pending for support staff.</p>
      <br><br><br>
      <!-- Pending Student Enrollment Approvals -->
      <div v-if="pendingEnrollments.length != 0" class="box">
        <h1>Pending Student Enrollment Approvals</h1>
        <div class="table-container">
          <table class="styled-table">
            <thead  >
              <tr>
                <th    >Name</th>
                <th    >Email</th>
                <th    >Course</th>
                <th    >Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="enrollment in pendingEnrollments" :key="enrollment.student_id"  >
                <td    >{{ enrollment.student_name }}</td>
                <td    >{{ enrollment.student_email }}</td>
                <td    >{{ enrollment.course_name }}</td>
                <td    >
                  <button @click="manageEnrollments(enrollment.student_id, enrollment.course_id, 'approve')" class="button">Approve</button>
                  <button @click="manageEnrollments(enrollment.student_id, enrollment.course_id, 'reject')" class="button">Reject</button>
                </td>
              </tr>
              
            </tbody>
          </table>
        </div>
      </div>
      <p v-else class="box">No approvals pending for student enrollments.</p>
      <br><br><br>
      <!--app stats-->
      
      <div class="box">
        <h1>Dashboard Overview</h1>
        <div class="stats-container">
            <!-- Course Card -->
            <div class="stat-card">
                <div class="stat-icon clr-b">📚</div>
                <p class="stat-title">TOTAL COURSES</p>
                <h2 class="stat-value">42</h2>
                <p class="stat-description">12 new courses this month</p>
            </div>

            <!-- Students Card -->
            <div class="stat-card">
                <div class="stat-icon clr-b">👨‍🎓</div>
                <p class="stat-title">TOTAL STUDENTS</p>
                <h2 class="stat-value">1,200</h2>
                <p class="stat-description">87 new enrollments this week</p>
            </div>

            <!-- Teachers Card -->
            <div class="stat-card">
                <div class="stat-icon clr-b">👨‍🏫</div>
                <p class="stat-title">TOTAL SUPPORT STAFF</p>
                <h2 class="stat-value">18</h2>
                <p class="stat-description">2 joined this month</p>
            </div>

            <!-- weeks Card -->
            <div class="stat-card">
                <div class="stat-icon clr-b">⏳</div>
                <p class="stat-title">TOTAL WEEKS</p>
                <h2 class="stat-value">123</h2>
                <p class="stat-description">+15% from last month</p>
            </div>
        </div>
    </div>

<br><br><br>
      <!-- All Courses Section -->
      <div class="box">
        <h1>All Courses</h1>
        <div v-if="courses.length > 0" class="stats-container">
          <div v-for="course in courses" :key="course.id" class="stat-card">
            <div class="button-container">
              <div class="stat-icon clr-b" ><button @click="openAddCourseContent(course)">➕  </button>  </div><p> - </p>
                <div class="stat-icon clr-b"><button @click="deleteCourse(course.id)">  ❌</button></div>
            </div>
            <h2 class="stat-value" @click="goToCourse(course)" >{{ course.name }}</h2>
            <p class="stat-description" @click="goToCourse(course)">Professor name: {{ course.prof }}</p>
          </div>
        </div>
        <p v-else class="box">No courses found.</p>
      </div>
      
    </div>
    <br><br><br>
<Dashboard/>
  </div>
</template>

<script>
import api from '@/utils/auth';
import NavBar from "@/components/icons/NavBar.vue";
import Dashboard from '../assets/charts.vue';
import AddCourseContents from "@/components/icons/AddCourseContents.vue";

export default {
  
  name: "AdminDashboard",
  components: { NavBar, Dashboard, AddCourseContents },
  data() {
    return {
      user: JSON.parse(localStorage.getItem('user')) || { name: "Admin" },
      pendingApprovals: [],
      pendingEnrollments: [],
      courses: [],
      course:{},
      isAddCourseContentVisible: false,
    };
  },
  methods: {
    async deleteCourse(course_id) {
      if (confirm("Are you sure you want to delete this course?")) {
        try {
          await api.delete("/delete", {
            headers: {
              'Content-Type': 'application/json'
            },
            data: {
              id: course_id
            }
          });
          this.fetchData();
        } catch (error) {
          console.error("Error deleting course:", error);
        }
      }
    },
    openAddCourseContent(course) {
      this.course = course;
      this.isAddCourseContentVisible = true;
    },
    async fetchData() {
      try {
        const response = await api.get('/dashboard/admin');
        Object.assign(this, response.data);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    },
    async manageEnrollments(student_id, course_id, action) {
      await api.put('/approve/course_enrollment', { student_id, course_id, action });
      this.fetchData();
    },
    async manageApprovals(staff_id, course_id, action) {
      await api.put('/approve/support_staffs', { staff_id, course_id, action });
      this.fetchData();
    },
    goToCourse(course) {
      this.$router.push({ name: "courseContent", query: { id: course.id, name: course.name }});
    }
  },
  created() {
    this.fetchData();
  },
};
</script>

<style scoped>
@import '@/assets/dashboardBody.css';
@import '@/assets/card.css';
@import '@/assets/table.css';

.cardBack {
    background: linear-gradient(90deg, #667eea, #764ba2);
}
.button-container {
  display: flex;
  justify-content: left;
}

</style>
