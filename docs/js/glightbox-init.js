(() => {
  "use strict";

  let lightbox = null;

  const destroy = () => {
    if (!lightbox) return;
    lightbox.destroy();
    lightbox = null;
  };

  const initialize = () => {
    destroy();

    const trigger = document.querySelector(
      ".glightbox[data-glightbox-options]",
    );
    if (!trigger || typeof window.GLightbox !== "function") return;

    try {
      const options = JSON.parse(trigger.dataset.glightboxOptions);
      lightbox = window.GLightbox({
        ...options,
        selector: ".glightbox[data-glightbox-options]",
      });
    } catch (error) {
      console.error("Unable to initialize GLightbox", error);
    }
  };

  if (typeof document$ !== "undefined") {
    document$.subscribe(initialize);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();
