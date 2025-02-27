<template>
  <NavBar @fetchData="fetchCourseContents"/>
  <div class="course-page">
    <!-- Sidebar (20%) -->
    <div class="sidebar">
      <h2>Course Contents</h2>
      <ul>
        <li v-for="week in weeks" :key="week.week">
          <div class="week-header" @click="toggleWeek(week.week)">
            <span>Week {{ week.week }}</span>
            <span class="arrow" :class="{ rotated: activeWeek === week.week }"></span>
          </div>
          <ul v-show="activeWeek === week.week" class="content-list">
            <li 
              v-for="content in week.contents" 
              :key="content.id" 
              class="content-item"
            >
              <span @click="selectVideo(content.video_link, content.title)" class="content-title">
                {{ content.title }}
              </span>
              <button class="delete-btn" @click="deleteCourseContent(content.id, week.week, content.title)">🗑️</button>
            </li>
          </ul>
        </li>
      </ul>
    </div>

    <!-- Content Section (80%) -->
    <div class="content">
      <h2 v-if="selectedTitle">{{ selectedTitle }}</h2>
      <div class="video-container" v-if="selectedVideo">
        <iframe 
          :src="embedVideo(selectedVideo)" 
          frameborder="0" 
          allowfullscreen
        ></iframe>
      </div>
      <p v-else class="placeholder-text">Select a course content to start Learning...!</p>
    </div>
  </div>
</template>

<script>
import api from '@/utils/auth';
import NavBar from '@/components/icons/NavBar.vue';

export default {
  name: "CourseContent",
  components: { NavBar },
  data() {
    return {
      weeks: [],
      activeWeek: null,
      selectedVideo: null,
      selectedTitle: "",
    };
  },
  methods: {
    fetchCourseContents() {
  this.weeks = this.groupByWeek([
    { id: 1, week: 1, title: "Introduction to Course", video_link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ" },
    { id: 2, week: 1, title: "Course Objectives", video_link: "https://www.youtube.com/watch?v=3JZ_D3ELwOQ" },
    { id: 3, week: 2, title: "Deep Dive into Basics", video_link: "https://www.youtube.com/watch?v=5qap5aO4i9A" },
    { id: 4, week: 2, title: "Hands-on Example", video_link: "https://www.youtube.com/watch?v=8ZcmTl_1ER8" },
    { id: 5, week: 3, title: "Advanced Concepts", video_link: "https://www.youtube.com/watch?v=BtN-goy9VOY" },
  ]);
},

    async deleteCourseContent(contentId, week, title) {
      if (!confirm(`Are you sure you want to delete "${title}" from Week ${week}?`)) {
        return;
      }

      try {
        const response = await api.delete('/delete_course_content', {
          data: { 
            course_id: this.$route.query.id, 
            week, 
            title 
          }
        });
        alert(response.data.message);
        this.fetchCourseContents();
      } catch (error) {
        console.error("Error deleting content:", error.response?.data?.message || error);
        alert(error.response?.data?.message || "Failed to delete content.");
      }
    },
    groupByWeek(contents) {
      const weeksMap = {};
      contents.forEach((content) => {
        if (!weeksMap[content.week]) weeksMap[content.week] = [];
        weeksMap[content.week].push(content);
      });
      return Object.keys(weeksMap)
        .map((week) => ({
          week: Number(week),
          contents: weeksMap[week],
        }))
        .sort((a, b) => a.week - b.week);
    },
    toggleWeek(weekNumber) {
      this.activeWeek = this.activeWeek === weekNumber ? null : weekNumber;
    },
    selectVideo(videoLink, title) {
      this.selectedVideo = videoLink;
      this.selectedTitle = title;
    },
    embedVideo(videoLink) {
      return videoLink.replace("watch?v=", "embed/");
    },
  },
  watch: {
    '$route.query': {
      handler() {
        this.fetchCourseContents();
      },
      immediate: true
    }
  }
};
</script>

<style scoped>
@import '@/assets/dashboardBody.css';
@import '@/assets/card.css';

.course-page {
  display: flex;
  height: 91vh;
  width: 100%;
  background: linear-gradient(120deg, #A9F1DF, #FFBBBB);
  color: #333;
  font-family: 'Arial', sans-serif;
}

/* Sidebar */
.sidebar {
  width: 20%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  color: white;
  padding: 20px;
  overflow-y: auto;
}

.sidebar h2 {
  margin-bottom: 15px;
  text-align: center;
  font-size: 20px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 5px;
}

.week-header {
  padding: 12px;
  background: #495057;
  cursor: pointer;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.week-header:hover {
  background: #6c757d;
}

.arrow {
  transition: transform 0.3s ease;
}

.rotated {
  transform: rotate(180deg);
}

/* Dropdown animation */
.content-list {
  background: linear-gradient(90deg, #667eea, #764ba2);
  padding: 10px;
  border-radius: 5px;
  margin-top: 5px;
}

.content-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #868e96;
  border-radius: 5px;
  padding: 8px;
  margin-bottom: 5px;
}

.content-title {
  cursor: pointer;
  flex-grow: 1;
  transition: background 0.3s ease;
}

.content-title:hover {
  background: #adb5bd;
}

/* Delete button */
.delete-btn {
  background: red;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.delete-btn:hover {
  background: darkred;
}

/* Content Section */
.content {
  width: 80%;
  padding: 20px;
  text-align: center;
}

.content h2 {
  font-size: 24px;
  margin-bottom: 15px;
}

.video-container {
  margin-top: 20px;
}

.video-container iframe {
  width: 100%;
  height: 500px;
  border-radius: 10px;
}

.placeholder-text {
  font-size: 18px;
  color: #777;
  margin-top: 50px;
}
</style>
