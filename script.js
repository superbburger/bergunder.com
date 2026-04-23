function createDivsFromJson(data, containerId) {
  const container = document.getElementById(containerId);
  //   find the container

  data.forEach(createItems);
  //   loop through each portfolio item of the array

  function createItems(item) {
    console.log("Creating items...");
    const div = document.createElement("div");
    div.classList.add(`item`);
    // create a new div.item

    const info = document.createElement("div");
    info.classList.add(`info`);

    const title = document.createElement("div");
    title.classList.add(`title`);
    title.innerHTML = item.title;
    info.appendChild(title);

    const tags = document.createElement("div");
    tags.classList.add(`tags`);
    item.category.forEach((tag) => {
      const badge = document.createElement("div");
      badge.classList.add(`badge`);
      badge.innerHTML = tag;
      tags.appendChild(badge);
    });
    info.appendChild(tags);

    const project = document.createElement("div");
    project.classList.add(`project`);
    project.innerHTML = item.project;
    info.appendChild(project);

    const releaseDate = document.createElement("div");
    releaseDate.classList.add(`date`);
    releaseDate.innerHTML =
      `<a href="` + item.link + `" target="_blank">` + item.date + `</a>`;
    info.appendChild(releaseDate);

    const description = document.createElement("div");
    description.classList.add(`description`);
    description.innerHTML = `<p>` + item.description + `</p>`;
    info.appendChild(description);

    const credits = document.createElement("div");
    credits.classList.add(`credits`);
    credits.innerHTML = `<p class="small">` + item.credits + `</p>`;
    info.appendChild(credits);

    div.appendChild(info);

    const imageContainer = document.createElement("div");
    imageContainer.classList.add("image-container");
    const featImg = document.createElement("img");
    featImg.classList.add(`image`);
    featImg.setAttribute("src", item.image);
    featImg.setAttribute("loading", "lazy");
    imageContainer.appendChild(featImg);
    div.appendChild(imageContainer);
    // container.appendChild(div);
    document.body.appendChild(div);
  }
}

function pickAHeading(phraseArray) {
  let rand = Math.floor(Math.random() * phraseArray.length);

  const heading = document.getElementById("headingPhrase");
  heading.innerHTML = String(phraseArray[rand]);
}

fetch("content.json")
  .then((response) => response.json())
  .then((data) => {
    createDivsFromJson(data, "container");

    document.dispatchEvent(new Event("dataLoaded"));
  })
  .catch((error) => console.error("Error:", error));

fetch("phrases.json")
  .then((response) => response.json())
  .then((phrases) => pickAHeading(phrases))
  .catch((error) => console.error("Error:", error));

document.addEventListener("dataLoaded", () => {
  const items = document.querySelectorAll(".item");
  console.log("items:", items);
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          // Optional: stop observing once it has appeared
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1, // triggers when 10% of the element is visible
    }
  );
  console.log("items found:", items.length);
  items.forEach((item) => {
    observer.observe(item);
  });
});
