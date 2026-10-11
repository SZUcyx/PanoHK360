"use strict";

const config = window.PANOHK360_CONFIG || {};
const authors = config.authors || [];
const authorLine = document.querySelector(".authors");
if (authors.length) {
  authorLine.replaceChildren();
  authors.forEach((author, index) => {
    if (index) authorLine.append(document.createTextNode(" ⋅ "));
    const node = document.createElement(author.url ? "a" : "span");
    node.className = "author";
    node.textContent = author.name;
    if (author.url) {
      node.href = author.url;
      node.target = "_blank";
      node.rel = "noopener noreferrer";
    }
    if (author.corresponding) {
      const marker = document.createElement("sup");
      marker.textContent = "*";
      marker.title = "Corresponding author";
      marker.setAttribute("aria-label", "Corresponding author");
      node.append(marker);
    }
    authorLine.append(node);
  });
  document.querySelector(".corresponding-note").hidden = !authors.some((author) => author.corresponding);
}

const affiliation = document.querySelector(".affiliation");
affiliation.textContent = config.affiliation || "";
affiliation.hidden = !config.affiliation;
const venue = document.querySelector(".venue");
if (config.venueUrl) {
  const link = document.createElement("a");
  link.textContent = config.venue || "NeurIPS 2026";
  link.href = config.venueUrl;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  venue.replaceChildren(link);
} else if (config.venue) {
  venue.textContent = config.venue;
}

document.querySelectorAll("[data-resource]").forEach((node) => {
  const url = config.links?.[node.dataset.resource];
  if (!url) return;
  const link = document.createElement("a");
  link.className = "link-btn";
  link.dataset.resource = node.dataset.resource;
  link.href = url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.innerHTML = node.innerHTML;
  node.replaceWith(link);
});

const bibtex = document.querySelector("#bibtex");
if (authors.length) {
  const authorNames = authors.map((author) => author.name).join(" and ");
  bibtex.textContent = bibtex.textContent.replace(/author\s*=\s*\{[^}]*\}/, `author    = {${authorNames}}`);
}

const copyButton = document.querySelector("#copy-citation");
copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(bibtex.textContent.trim());
    copyButton.textContent = "Copied!";
    document.querySelector("#copy-status").textContent = "Citation copied to clipboard.";
    setTimeout(() => { copyButton.textContent = "Copy BibTeX"; }, 2000);
  } catch {
    const range = document.createRange();
    range.selectNodeContents(bibtex);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    document.querySelector("#copy-status").textContent = "Citation selected. Press Ctrl+C or Command+C to copy.";
  }
});

document.querySelectorAll(".system-overview-wrapper").forEach((wrapper) => {
  wrapper.addEventListener("wheel", (event) => {
    if (event.shiftKey && wrapper.scrollWidth > wrapper.clientWidth) {
      event.preventDefault();
      wrapper.scrollLeft += event.deltaY + event.deltaX;
    }
  }, { passive: false });
});
