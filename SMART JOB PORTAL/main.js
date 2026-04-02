const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");
const menuBtnIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", (e) => {
  navLinks.classList.toggle("open");

  const isOpen = navLinks.classList.contains("open");
  menuBtnIcon.setAttribute("class", isOpen ? "ri-close-line" : "ri-menu-line");
});

navLinks.addEventListener("click", (e) => {
  navLinks.classList.remove("open");
  menuBtnIcon.setAttribute("class", "ri-menu-line");
});

const scrollRevealOption = {
  distance: "50px",
  origin: "bottom",
  duration: 1000,
};

ScrollReveal().reveal(".header__container h2", {
  ...scrollRevealOption,
});
ScrollReveal().reveal(".header__container h1", {
  ...scrollRevealOption,
  delay: 500,
});
ScrollReveal().reveal(".header__container p", {
  ...scrollRevealOption,
  delay: 1000,
});
ScrollReveal().reveal(".header__btns", {
  ...scrollRevealOption,
  delay: 1500,
});

ScrollReveal().reveal(".steps__card", {
  ...scrollRevealOption,
  interval: 500,
});

ScrollReveal().reveal(".explore__card", {
  duration: 1000,
  interval: 500,
});

// --- NEW FUNCTIONALITY ---

// Dark Mode Toggle
const themeToggle = document.getElementById("theme-toggle");
const body = document.body;
const themeIcon = themeToggle.querySelector("i");

const currentTheme = localStorage.getItem("theme");
if (currentTheme === "dark") {
  body.classList.add("dark-mode");
  themeIcon.classList.replace("ri-moon-fill", "ri-sun-fill");
}

themeToggle.addEventListener("click", () => {
  body.classList.toggle("dark-mode");
  const isDark = body.classList.contains("dark-mode");
  localStorage.setItem("theme", isDark ? "dark" : "light");
  themeIcon.setAttribute("class", isDark ? "ri-sun-fill" : "ri-moon-fill");
});

// Modal Logic
const registerBtn = document.getElementById("register-btn");
const modalOverlay = document.getElementById("register-modal");
const modalClose = document.getElementById("modal-close");

registerBtn.addEventListener("click", () => {
  modalOverlay.classList.add("show");
});

modalClose.addEventListener("click", () => {
  modalOverlay.classList.remove("show");
});

modalOverlay.addEventListener("click", (e) => {
  if (e.target === modalOverlay) {
    modalOverlay.classList.remove("show");
  }
});

// Dynamic Jobs & Filtering
const jobs = [
  {
    company: "Figma",
    logo: "assets/figma.png",
    location: "USA",
    title: "Senior Product Engineer",
    description: "Lead the development of innovative product solutions.",
    positions: "12 Positions",
    type: "Full Time",
    salary: "$1,45,000/Year",
    category: "engineering"
  },
  {
    company: "Google",
    logo: "assets/google.png",
    location: "USA",
    title: "Project Manager",
    description: "Manage project timelines and budgets to ensure successful delivery.",
    positions: "2 Positions",
    type: "Full Time",
    salary: "$95,000/Year",
    category: "management"
  },
  {
    company: "LinkedIn",
    logo: "assets/linkedin.png",
    location: "Germany",
    title: "Full Stack Developer",
    description: "Develop and maintain components of web applications.",
    positions: "10 Positions",
    type: "Full Time",
    salary: "$35,000/Year",
    category: "development"
  },
  {
    company: "Amazon",
    logo: "assets/amazon.png",
    location: "USA",
    title: "Front-end Developer",
    description: "Design and implement user interfaces using HTML, CSS, and JS.",
    positions: "20 Positions",
    type: "Full Time",
    salary: "$1,01,000/Year",
    category: "development"
  },
  {
    company: "Twitter",
    logo: "assets/twitter.png",
    location: "USA",
    title: "ReactJS Developer",
    description: "Specialize in building dynamic and interactive user interfaces.",
    positions: "6 Positions",
    type: "Full Time",
    salary: "$98,000/Year",
    category: "development"
  },
  {
    company: "Microsoft",
    logo: "assets/microsoft.png",
    location: "USA",
    title: "Python Developer",
    description: "Develop scalable and efficient backend systems.",
    positions: "9 Positions",
    type: "Full Time",
    salary: "$80,000/Year",
    category: "development"
  }
];

const jobGrid = document.getElementById("job-grid");
const searchInput = document.getElementById("job-search");
const categorySelect = document.getElementById("job-category");

function displayJobs(jobsToDisplay) {
  jobGrid.innerHTML = "";
  if (jobsToDisplay.length === 0) {
    jobGrid.innerHTML = "<p style='grid-column: 1 / -1; text-align: center; color: var(--text-light); padding: 2rem;'>No jobs found matching your criteria.</p>";
    return;
  }
  
  jobsToDisplay.forEach(job => {
    const jobCard = document.createElement("div");
    jobCard.classList.add("job__card");
    jobCard.innerHTML = `
      <div class="job__card__header">
        <img src="${job.logo}" alt="job" />
        <div>
          <h5>${job.company}</h5>
          <h6>${job.location}</h6>
        </div>
      </div>
      <h4>${job.title}</h4>
      <p>${job.description}</p>
      <div class="job__card__footer">
        <span>${job.positions}</span>
        <span>${job.type}</span>
        <span>${job.salary}</span>
      </div>
    `;
    jobGrid.appendChild(jobCard);
  });

  // Re-initialize ScrollReveal for newly rendered job cards
  ScrollReveal().reveal(".job__card", {
    ...scrollRevealOption,
    interval: 100,
  });
}

function filterJobs() {
  const searchTerm = searchInput.value.toLowerCase();
  const category = categorySelect.value;
  
  const filteredJobs = jobs.filter(job => {
    const matchesSearch = job.title.toLowerCase().includes(searchTerm) || job.company.toLowerCase().includes(searchTerm);
    const matchesCategory = category === "all" || job.category === category;
    return matchesSearch && matchesCategory;
  });
  
  displayJobs(filteredJobs);
}

if (searchInput && categorySelect && jobGrid) {
  searchInput.addEventListener("input", filterJobs);
  categorySelect.addEventListener("change", filterJobs);
  displayJobs(jobs); // Initial load
}

const swiper = new Swiper(".swiper", {
  loop: true,
});
