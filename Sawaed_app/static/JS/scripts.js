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
window.addEventListener('scroll', function() {
  const ctaContainer = document.querySelector('.cta-container');
  if (window.scrollY > 100) {
      ctaContainer.classList.add('animate-background');
  } else {
      ctaContainer.classList.remove('animate-background');
  }
});