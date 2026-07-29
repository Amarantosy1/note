/*
 * Typing model adapted from Termynal by Ines Montani.
 * https://github.com/ines/termynal
 *
 * MIT License
 * Copyright (c) 2017 Ines Montani
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

(() => {
  "use strict";

  const root = document.querySelector("[data-home-terminal]");
  if (!root || root.dataset.terminalInitialized === "true") return;

  const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (motionPreference.matches) return;

  const command = root.querySelector('[data-ty="input"]');
  const logo = root.querySelector("[data-terminal-logo]");
  const rows = [...root.querySelectorAll("[data-terminal-row]")];
  const ready = root.querySelector("[data-terminal-ready]");
  if (!command || !logo || !rows.length || !ready) return;

  const finalCommand = command.textContent;
  const finalRows = rows.map((row) => row.textContent);
  let cancelled = false;
  let visibilityVersion = 0;

  document.addEventListener("visibilitychange", () => {
    visibilityVersion += 1;
  });

  root.dataset.terminalInitialized = "true";
  root.dataset.terminalState = "running";
  command.textContent = "";
  command.setAttribute("data-ty-cursor", "▋");
  rows.forEach((row) => {
    row.textContent = "";
  });

  const wait = (duration) =>
    new Promise((resolve) => {
      let elapsed = 0;
      let previousTime = null;
      let previousVisibilityVersion = visibilityVersion;

      const advance = (currentTime) => {
        if (cancelled) {
          resolve(false);
          return;
        }

        if (
          document.visibilityState !== "visible" ||
          previousVisibilityVersion !== visibilityVersion
        ) {
          previousTime = null;
          previousVisibilityVersion = visibilityVersion;
          requestAnimationFrame(advance);
          return;
        }

        if (previousTime !== null) elapsed += currentTime - previousTime;
        previousTime = currentTime;

        if (elapsed >= duration) {
          resolve(true);
          return;
        }

        requestAnimationFrame(advance);
      };

      requestAnimationFrame(advance);
    });

  const showFinalState = () => {
    command.textContent = finalCommand;
    command.removeAttribute("data-ty-cursor");
    rows.forEach((row, index) => {
      row.textContent = finalRows[index];
    });
    root.dataset.terminalState = "complete";
  };

  const typeCommand = async () => {
    for (const character of finalCommand) {
      if (!(await wait(character === " " ? 24 : 46))) return false;
      command.textContent += character;
    }
    return true;
  };

  const renderLogoFrame = (settledColumns, phase) => {
    const frontCharacters = ["░", "▒", "▓"];

    rows.forEach((row, rowIndex) => {
      const target = finalRows[rowIndex];
      let frame = target.slice(0, settledColumns);

      for (let column = settledColumns; column < settledColumns + 2; column += 1) {
        const character = target[column];
        if (character === undefined) break;
        if (character === " ") {
          frame += " ";
          continue;
        }
        frame += frontCharacters[(phase + rowIndex + column) % frontCharacters.length];
      }

      row.textContent = frame;
    });
  };

  const revealLogo = async () => {
    const width = Math.max(...finalRows.map((row) => row.length));

    for (let column = 0; column < width; column += 2) {
      for (let phase = 0; phase < 3; phase += 1) {
        renderLogoFrame(column, phase);
        if (!(await wait(18))) return false;
      }
    }

    rows.forEach((row, index) => {
      row.textContent = finalRows[index];
    });
    return true;
  };

  const handleMotionChange = (event) => {
    if (!event.matches) return;
    cancelled = true;
    showFinalState();
  };
  motionPreference.addEventListener("change", handleMotionChange, { once: true });

  const start = async () => {
    if (!(await wait(420))) return;
    if (!(await typeCommand())) return;
    command.removeAttribute("data-ty-cursor");
    if (!(await wait(260))) return;
    if (!(await revealLogo())) return;
    if (!(await wait(180))) return;
    root.dataset.terminalState = "complete";
  };

  start();
})();
