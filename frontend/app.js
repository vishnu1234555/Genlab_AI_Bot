// Adjust these once you expose real HTTP endpoints in Python.
const API_BASE = "http://localhost:8080";

const uploadForm = document.getElementById("upload-form");
const pdfInput = document.getElementById("pdf-file");
const uploadStatus = document.getElementById("upload-status");

const queryForm = document.getElementById("query-form");
const questionInput = document.getElementById("question-input");
const clearBtn = document.getElementById("clear-btn");
const answerStatus = document.getElementById("answer-status");
const answerOutput = document.getElementById("answer-output");

function setUploadStatus(message, variant = "default") {
  uploadStatus.textContent = message;
  uploadStatus.classList.remove("gl-status--success", "gl-status--error");
  if (variant === "success") uploadStatus.classList.add("gl-status--success");
  if (variant === "error") uploadStatus.classList.add("gl-status--error");
}

function setAnswerStatus(message) {
  answerStatus.textContent = message;
}

function setAnswerContent(html) {
  answerOutput.innerHTML = html;
}

uploadForm?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = pdfInput.files?.[0];
  if (!file) {
    setUploadStatus("Please choose a PDF file first.", "error");
    return;
  }

  setUploadStatus("Uploading and indexing…", "default");

  try {
    const formData = new FormData();
    formData.append("file", file);

    // Change `/upload` to match your FastAPI/Flask endpoint.
    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error(`Upload failed (${res.status})`);
    }

    const data = await res.json().catch(() => ({}));
    setUploadStatus(
      data.message || "PDF indexed into Qdrant successfully.",
      "success",
    );
  } catch (err) {
    console.error(err);
    setUploadStatus(
      "Upload/indexing failed. Check backend logs & API_BASE / /upload route.",
      "error",
    );
  }
});

queryForm?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const question = questionInput.value.trim();
  if (!question) {
    setAnswerStatus("Type a question first.");
    return;
  }

  setAnswerStatus("Thinking with GenLab RAG…");
  setAnswerContent('<p class="gl-placeholder">Generating answer…</p>');

  try {
    // Change `/ask` to your actual question endpoint that wraps retrieve.py/llm.
    const res = await fetch(`${API_BASE}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!res.ok) {
      throw new Error(`Request failed (${res.status})`);
    }

    const data = await res.json();
    const answer = data.answer || JSON.stringify(data, null, 2);
    setAnswerStatus("Answered by GenLab assistant");
    setAnswerContent(
      `<p>${answer.replace(/\n/g, "<br>")}</p>`,
    );
  } catch (err) {
    console.error(err);
    setAnswerStatus("Something went wrong.");
    setAnswerContent(
      '<p class="gl-placeholder">Check the backend logs and ensure the /ask endpoint is live.</p>',
    );
  }
});

clearBtn?.addEventListener("click", () => {
  questionInput.value = "";
  setAnswerStatus("");
  setAnswerContent(
    '<p class="gl-placeholder">Responses from your `retrieve.py` endpoint will appear here.</p>',
  );
});

