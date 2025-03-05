<template>
  <div class="body">
    <NavBar :courses="courses" @fetchData="fetchData"/>
    <AddCourseContents :course="course" :isVisible="isAddCourseContentVisible"  @close="isAddCourseContentVisible = false" />

    <div class="container mx-auto p-6">
      <h3>Welcome, {{ user.name }}</h3>
<br><br>
      <!-- Pending Student Enrollment Approvals -->
      <div v-if="pendingEnrollments.length != 0" class="box">
        <h1>Pending Student Enrollment Approvals</h1>
        <div class="table-container"> 
          <table class="styled-table">
            <thead >
              <tr>
                <th     >Name</th>
                <th     >Email</th>
                <th     >Course</th>
                <th     >Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="enrollment in pendingEnrollments" :key="enrollment.student_id"  >
                <td     >{{ enrollment.student_name }}</td>
                <td     >{{ enrollment.student_email }}</td>
                <td     >{{ enrollment.course_name }}</td>
                <td     >
                  <button @click="manageEnrollments(enrollment.student_id, enrollment.course_id, 'approve')" class="button">Approve</button>
                  <button @click="manageEnrollments(enrollment.student_id, enrollment.course_id, 'reject')" class="button">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <p v-else class="box">No pending enrollment approvals.</p>
      <br><br><br>
      <!-- Support Staff Courses -->
      <div class="box">
        <h1>All Courses</h1>
        <div v-if="supportCourses.length > 0" class="stats-container">
          <div v-for="course in supportCourses" :key="course.id" class="stat-card" >
            <div class="stat-icon clr-b"><button @click="openAddCourseContent(course)">➕  </button> 
            </div>
            <h2 class="stat-value" @click="goToCourse(course)">{{ course.name }}</h2>
            <p class="stat-description" @click="goToCourse(course)">Proffessor name: {{ course.prof }}</p>
          </div>
        </div>
        <p v-else class="box">No courses found.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/auth';
import NavBar from "@/components/icons/NavBar.vue";
import AddCourseContents from "@/components/icons/AddCourseContents.vue";

export default {
  name: "SupportStaffDashboard",
  components: { NavBar, AddCourseContents },
  data() {
    return {
      course:{},
      isAddCourseContentVisible: false,
      user: JSON.parse(localStorage.getItem('user')) || { name: "Support Staff" },
      pendingEnrollments: [],
      courses: [],
      supportCourses: [],
    };
  },
  methods: {openAddCourseContent(course) {
      this.course = course;
      this.isAddCourseContentVisible = true;
    },
    async fetchData() {
      try {
        const response = await api.get('/dashboard/support_staff');
        this.courses = response.data.courses;
        this.supportCourses = response.data.support_courses;
        this.pendingEnrollments = response.data.pendingEnrollments;
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        alert("Failed to load dashboard data. Please try again later.");
      }
    },
    async manageEnrollments(student_id, course_id, action) {
      await api.put('/approve/course_enrollment', { student_id, course_id, action });
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

</style>
