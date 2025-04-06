// Function to toggle sidebar visibility
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("overlay");

    // Apply sliding effect with transition
    sidebar.classList.toggle("translate-x-0");  // Slide in
    sidebar.classList.toggle("translate-x-full");  // Slide out

    // Add background overlay effect with fade-in/out
    overlay.classList.toggle("opacity-0");
    overlay.classList.toggle("opacity-50");
    overlay.classList.toggle("pointer-events-none");
}

// Function to close sidebar manually
function closeSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("overlay");

    // Slide out sidebar and fade out the overlay
    sidebar.classList.add("translate-x-full");
    overlay.classList.add("opacity-0");
    overlay.classList.add("pointer-events-none");
}
