let allItems = [];
let itemSlugs = [];

const SITE_TITLE = "Aaron Bergunder";
const DEFAULT_COLS = "2";

/* -------------------- helpers -------------------- */

function slugify(str) {
  return String(str)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-+|-+$)/g, "");
}

function buildSlugs(data) {
  const counts = {};
  return data.map((item) => {
    const base = slugify(item.title) || "untitled";
    counts[base] = (counts[base] || 0) + 1;
    return counts[base] > 1 ? `${base}-${counts[base]}` : base;
  });
}

function parseHash() {
  const match = window.location.hash.match(/^#work\/(.+)$/);
  return match ? decodeURIComponent(match[1]) : null;
}

/* -------------------- grid view -------------------- */

function renderGrid(data, slugs, containerId) {
  const container = document.getElementById(containerId);

  data.forEach((item, i) => {
    const tile = document.createElement("a");
    tile.classList.add("tile");
    tile.href = `#work/${slugs[i]}`;

    const imageContainer = document.createElement("div");
    imageContainer.classList.add("tile-image-container");

    const img = document.createElement("img");
    img.setAttribute("src", item.image);
    img.setAttribute("loading", "lazy");
    img.setAttribute("alt", item.title);
    imageContainer.appendChild(img);
    tile.appendChild(imageContainer);

    const title = document.createElement("div");
    title.classList.add("tile-title");
    title.innerHTML = item.title;
    tile.appendChild(title);

    container.appendChild(tile);
  });
}

function observeTiles() {
  const tiles = document.querySelectorAll(".tile");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );
  tiles.forEach((tile) => observer.observe(tile));
}

/* -------------------- zoom control -------------------- */

function setZoom(cols) {
  document.getElementById("container").style.setProperty("--cols", cols);
  try {
    localStorage.setItem("archiveZoomCols", cols);
  } catch (e) {
    /* localStorage unavailable, ignore */
  }
  document.querySelectorAll(".zoom-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.cols === String(cols));
  });
}

function initZoomControls() {
  document.querySelectorAll(".zoom-btn").forEach((btn) => {
    btn.addEventListener("click", () => setZoom(btn.dataset.cols));
  });

  let saved = DEFAULT_COLS;
  try {
    saved = localStorage.getItem("archiveZoomCols") || DEFAULT_COLS;
  } catch (e) {
    /* localStorage unavailable, ignore */
  }
  setZoom(saved);
}

/* -------------------- detail view -------------------- */

function renderDetail(item) {
  const detailContent = document.getElementById("detailContent");

  const tagsHtml = item.category
    .map((tag) => `<div class="badge">${tag}</div>`)
    .join("");

  detailContent.innerHTML = `
    <div class="item detail-item">
      <div class="info">
        <div class="title">${item.title}</div>
        <div class="tags">${tagsHtml}</div>
        <div class="project">${item.project}</div>
        <div class="date"><a href="${item.link}" target="_blank">${item.date}</a></div>
        <div class="description"><p>${item.description}</p></div>
        <div class="credits"><p class="small">${item.credits}</p></div>
      </div>
      <div class="image-container">
        <img class="image" src="${item.image}" loading="lazy" alt="${item.title}" />
      </div>
    </div>
  `;
}

function updatePrevNext(idx) {
  const prevIdx = (idx - 1 + allItems.length) % allItems.length;
  const nextIdx = (idx + 1) % allItems.length;
  document.getElementById("prevLink").href = `#work/${itemSlugs[prevIdx]}`;
  document.getElementById("nextLink").href = `#work/${itemSlugs[nextIdx]}`;
}

/* -------------------- routing -------------------- */

function showGrid() {
  document.getElementById("gridView").hidden = false;
  document.getElementById("detailView").hidden = true;
  document.getElementById("zoomControls").hidden = false;
  document.title = SITE_TITLE;
  window.scrollTo(0, 0);
}

function showDetail(slug) {
  const idx = itemSlugs.indexOf(slug);
  if (idx === -1) {
    // unknown slug, fall back to the grid
    window.location.hash = "";
    return;
  }
  renderDetail(allItems[idx]);
  updatePrevNext(idx);
  document.getElementById("gridView").hidden = true;
  document.getElementById("detailView").hidden = false;
  document.getElementById("zoomControls").hidden = true;
  document.title = `${allItems[idx].title} — ${SITE_TITLE}`;
  window.scrollTo(0, 0);
}

function route() {
  if (!allItems.length) return; // data not loaded yet
  const slug = parseHash();
  if (slug) {
    showDetail(slug);
  } else {
    showGrid();
  }
}

/* -------------------- heading phrase -------------------- */

function pickAHeading(phraseArray) {
  const rand = Math.floor(Math.random() * phraseArray.length);
  const heading = document.getElementById("headingPhrase");
  heading.innerHTML = String(phraseArray[rand]);
}

/* -------------------- init -------------------- */

fetch("content.json")
  .then((response) => response.json())
  .then((data) => {
    allItems = data;
    itemSlugs = buildSlugs(data);
    renderGrid(allItems, itemSlugs, "container");
    initZoomControls();
    observeTiles();
    route();
  })
  .catch((error) => console.error("Error:", error));

fetch("phrases.json")
  .then((response) => response.json())
  .then((phrases) => pickAHeading(phrases))
  .catch((error) => console.error("Error:", error));

window.addEventListener("hashchange", route);
