"use strict";
const data = JSON.parse(document.querySelector("#site-data").textContent);
const menu = document.querySelector(".menu"),
  nav = document.querySelector(".nav-links");
menu.addEventListener("click", () => {
  const open = menu.getAttribute("aria-expanded") !== "true";
  menu.setAttribute("aria-expanded", String(open));
  menu.textContent = open ? "Schließen −" : "Menü +";
  nav.classList.toggle("open", open);
});
nav.querySelectorAll("a").forEach((a) =>
  a.addEventListener("click", () => {
    menu.setAttribute("aria-expanded", "false");
    menu.textContent = "Menü +";
    nav.classList.remove("open");
  }),
);
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    menu.setAttribute("aria-expanded", "false");
    nav.classList.remove("open");
    menu.textContent = "Menü +";
  }
});
const cards = [...document.querySelectorAll(".project")];
document.querySelectorAll(".filter").forEach((button) =>
  button.addEventListener("click", () => {
    document
      .querySelectorAll(".filter")
      .forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
    cards.forEach(
      (c) =>
        (c.hidden =
          button.dataset.filter !== "Alle" &&
          c.dataset.category !== button.dataset.filter),
    );
    document.querySelector(".no-results").hidden = cards.some((c) => !c.hidden);
  }),
);
const dialog = document.querySelector("#detail-dialog"),
  content = document.querySelector("#dialog-content");
function openDialog(title, text) {
  content.replaceChildren();
  const h = document.createElement("h2");
  h.id = "dialog-title";
  h.textContent = title;
  const p = document.createElement("p");
  p.textContent = text;
  content.append(h, p);
  dialog.showModal();
}
function mediaUrl(value) {
  try {
    const u = new URL(value, location.origin);
    return ["https:", "http:"].includes(u.protocol) ? u.href : null;
  } catch {
    return null;
  }
}
document.querySelectorAll("[data-project]").forEach((b) =>
  b.addEventListener("click", () => {
    const p = data.projects[Number(b.dataset.project)];
    openDialog(p.title, p.description);
    if (p.image && mediaUrl(p.image)) {
      const i = document.createElement("img");
      i.src = mediaUrl(p.image);
      i.alt = p.image_alt || p.title;
      i.className = "dialog-image";
      content.append(i);
    }

if (Array.isArray(p.gallery) && p.gallery.length) {
    const gallery = document.createElement('div');
    gallery.className = 'dialog-gallery';

    p.gallery.forEach(item => {
        if (!item.image || !mediaUrl(item.image)) return;

        const image = document.createElement('img');
        image.src = mediaUrl(item.image);
        image.alt = item.alt || p.title;
        image.loading = 'lazy';

        gallery.append(image);
    });

    content.append(gallery);
}

    if (p.video && mediaUrl(p.video)) {
      const v = document.createElement("video");
      v.src = mediaUrl(p.video);
      v.controls = true;
      v.preload = "none";
      v.playsInline = true;
      v.className = "dialog-video";
      content.append(v);
    }
  }),
);
document
  .querySelector(".close")
  .addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (e) => {
  if (e.target === dialog) {
    const r = dialog.getBoundingClientRect();
    if (
      e.clientX < r.left ||
      e.clientX > r.right ||
      e.clientY < r.top ||
      e.clientY > r.bottom
    )
      dialog.close();
  }
});
dialog.addEventListener("close", () => {
  dialog.querySelectorAll("video").forEach((v) => v.pause());
});
document
  .querySelectorAll("[data-legal]")
  .forEach((b) =>
    b.addEventListener("click", () =>
      openDialog(
        b.dataset.legal === "imprint" ? "Impressum" : "Datenschutz",
        data[b.dataset.legal] ||
          "Diese Seite ist ein unveröffentlichter Entwurf. Die Angaben werden vor dem öffentlichen Start ergänzt.",
      ),
    ),
  );

  document.querySelector(".contact-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const form = e.currentTarget;
  const status = document.querySelector(".form-status");
  const button = form.querySelector('button[type="submit"]');

  const originalButtonText = button.innerHTML;

  button.disabled = true;
  button.textContent = "Wird gesendet …";
  status.textContent = "";

  try {
    const formData = new FormData(form);

    formData.set("form-name", form.getAttribute("name"));

    const response = await fetch("/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams(formData).toString(),
    });

    if (!response.ok) {
      throw new Error("Formular konnte nicht gesendet werden.");
    }

    form.reset();

    status.textContent =
      "Danke! Deine Anfrage wurde erfolgreich gesendet. Ich melde mich bei dir.";

  } catch (error) {
    console.error(error);

    status.textContent =
      "Das hat leider nicht funktioniert. Bitte versuche es noch einmal.";

  } finally {
    button.disabled = false;
    button.innerHTML = originalButtonText;
  }
});