  document.addEventListener("DOMContentLoaded", function () {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll("aside.sidebar nav ul li");

    menuItems.forEach(item => {
      const link = item.querySelector("a");
      if (link && link.getAttribute("href") === currentPath) {
        item.classList.add("active");
      } else {
        item.classList.remove("active");
      }
    });
  });
