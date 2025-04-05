function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("overlay");
    sidebar.classList.toggle("translate-x-full");
    overlay.classList.toggle("hidden");
  }
function closeSidebar() {
    document.getElementById("sidebar").classList.add("translate-x-full");
    document.getElementById("overlay").classList.add("hidden");
  }