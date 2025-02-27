<template>
  <div class="chat-overlay">
    <div class="chat-container">
      <!-- Chat History Sidebar -->
      <div class="chat-sidebar">
        <h3>Chat History</h3>
        <ul>
          <li v-for="(chat, index) in chatHistory" :key="index">{{ chat }}</li>
        </ul>
      </div>
      
      <!-- Chat Window -->
      <div class="chat-window">
        <div class="chat-header">
          <h2>AI Chatbot!</h2>
          <button @click="$emit('closeChat')" class="close-btn">✖</button>
        </div>
        
        <div class="chat-messages">
          <p v-for="(msg, index) in messages" :key="index" class="message">{{ msg }}</p>
        </div>
        
        <div class="chat-input">
          <input v-model="newMessage" placeholder="Type your message..." @keyup.enter="sendMessage" />
          <button @click="sendMessage">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: ["Hello! How can I assist you?"],
      newMessage: "",
      chatHistory: ["Chat 1", "Chat 2", "Chat 3"]
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() !== "") {
        this.messages.push(this.newMessage);
        this.newMessage = "";
      }
    }
  }
};
</script>

<style scoped>
.chat-overlay {
  position: fixed;
  top: 5%;
  left: 5%;
  width: 90%;
  height: 90%;
  z-index: 2000;
  background: rgb(30, 27, 27);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 20px;
}

.chat-container {
  display: flex;
  width: 85%;
  height: 85%;
  background: #222;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.chat-sidebar {
  width: 25%;
  background: #111;
  color: white;
  padding: 20px;
  overflow-y: auto;
}

.chat-sidebar h3 {
  margin-bottom: 15px;
}

.chat-sidebar ul {
  list-style: none;
  padding: 0;
}

.chat-sidebar li {
  padding: 10px;
  border-bottom: 1px solid #333;
  cursor: pointer;
}

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #333;
  color: white;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  background: #636364;
  color: white;
}

.close-btn {
  background: transparent;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

.chat-messages {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
}

.message {
  background: #444;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.chat-input {
  display: flex;
  padding: 15px;
  border-top: 1px solid #555;
  background: #222;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background: #555;
  color: white;
}

.chat-input button {
  background: #2b3540;
  color: white;
  border: none;
  padding: 10px;
  margin-left: 10px;
  cursor: pointer;
  border-radius: 5px;
}
</style>
