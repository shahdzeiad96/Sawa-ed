function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("overlay");
  
    // إذا السايدبار ظاهر
    if (sidebar.classList.contains("translate-x-0")) {
      closeSidebar();
    } else {
      openSidebar();
    }
  }
  
  function openSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("overlay");
  
    sidebar.classList.remove("translate-x-full");
    sidebar.classList.add("translate-x-0");
    overlay.classList.remove("hidden");
  }
  
  function closeSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("overlay");
  
    sidebar.classList.remove("translate-x-0");
    sidebar.classList.add("translate-x-full");
    overlay.classList.add("hidden");
  }
  lucide.createIcons();
  function openMessageModal() {
  document.getElementById('messageModal').classList.remove('hidden');
}

function closeMessageModal() {
  document.getElementById('messageModal').classList.add('hidden');
}


function openReviewModal() {
document.getElementById("reviewModal").classList.remove("hidden");
}

function closeReviewModal() {
document.getElementById("reviewModal").classList.add("hidden");
}

let stars = document.querySelectorAll('.star');
let ratingInput = document.getElementById('rating-input');

stars.forEach(star => {
star.addEventListener('click', function() {
let rating = this.getAttribute('data-value');
ratingInput.value = rating;
updateStars(rating); 
});
});

function updateStars(rating) {
stars.forEach(star => {
if (star.getAttribute('data-value') <= rating) {
star.innerHTML = "&#9733;";
} else {
star.innerHTML = "&#9734;";
}
});
}
// chatbot function
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

function appendMessage(sender, text) {
    const messageEl = document.createElement("div");
    messageEl.classList.add("chat-message");
    messageEl.classList.add(sender === "user" ? "user" : "bot");
    messageEl.innerHTML = `<strong>${sender === "user" ? "You" : "Bot"}:</strong> ${text}`;
    chatBox.appendChild(messageEl);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    userInput.value = "";

    fetch(`/chatbot/?message=${encodeURIComponent(message)}`)
        .then(response => response.json())
        .then(data => {
            appendMessage("bot", data.response);
        })
        .catch(error => {
            appendMessage("bot", "⚠️ Error contacting chatbot.");
            console.error("Error:", error);
        });
}

sendButton.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});


  