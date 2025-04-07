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
  