<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeAddCourseContents">
      <div class="container">
        <div class="box">
          <span class="close-button" @click="$emit('close')">&times;</span>
          <h1>Add Course Content</h1>
          <div class="scrollable">
          
          <form @submit.prevent="submitCourseContent">
            
              
              <label for="course_id">Course ID </label>
              <input type="number" id="course_id" v-model="form.course_id"  readonly  />
  
              <label for="week">Week</label>
              <input type="number" id="week" v-model="form.week" min="1" max="52" required />
              
              <label for="title">Title</label>
              <input type="text" id="title" v-model="form.title" required />
  
              <label for="description">Description</label>
              <textarea id="description" v-model="form.description" required></textarea>
  
              <label for="video_link">Video Link</label>
              <input type="url" id="video_link" v-model="form.video_link" required />
              
            
            <button type="submit" class="button">Submit</button>
          </form>
  
          <h3>OR Upload CSV</h3>
          <input type="file" @change="handleFileUpload" accept=".csv" />
          <button @click="uploadCSV" type="submit" class="button">Upload CSV</button>
        </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from '@/utils/auth';
  
  export default {
    data() {
      return {
        form: {
          course_id:null,
          week: '',
          title: '',
          description: '',
          video_link: ''
        },
        csvFile: null
      };
    },
    watch: {
  course: {
    immediate: true,
    handler(newCourse) {
      if (newCourse) {
        this.form.course_id = newCourse.id;
      }
    }
  }
},
    props: {
      isVisible: {
        type: Boolean,
        required: true
      },
      course:{
        type: Object,
        required: true
      }
    },
    methods: {
      closeAddCourseContents() {
        this.$emit('close');
      },
      async submitCourseContent() {
        try {
          await api.post('/add_or_update/course_contents', this.form);
          alert('Course content added successfully!');
          this.form.course_id = '';
          this.form.week = '';
          this.form.title = '';
          this.form.description = '';
          this.form.video_link = '';
          this.closeAddCourseContents();
        } catch (error) {
          alert('Error adding course content: ' + error.response.data.error);
          this.form.course_id = '';
          this.form.week = '';
          this.form.title = '';
          this.form.description = '';
          this.form.video_link = '';
          this.closeAddCourseContents();
        }
      },
      handleFileUpload(event) {
        this.csvFile = event.target.files[0];
      },
      async uploadCSV() {
        if (!this.csvFile) {
          alert('Please select a CSV file.');
          return;
        }
        
        const formData = new FormData();
        formData.append('file', this.csvFile);
        
        try {
          await api.post('/upload_course_contents', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          alert('CSV uploaded successfully!');
          this.csvFile = null
          this.closeAddCourseContents();
        } catch (error) {
          alert('Error uploading CSV: ' + error.response.data.error);
          this.csvFile = null
          this.closeAddCourseContents()
        }
      }
    }
  };
  </script>
  
  <style scoped>
  @import '@/assets/overlay.css';
  @import '@/assets/card.css';
  </style>
  