#  AI Video Assistant

An AI-powered backend application that transforms long-form audio and video into structured, searchable knowledge. The system automates transcription, meeting analysis, information extraction, and context-aware question answering using Retrieval-Augmented Generation (RAG).

Designed with a modular architecture, the project combines local speech recognition, cloud-based language models, vector search, and an interactive interface to process meeting recordings, lectures, interviews, podcasts, and other spoken content efficiently.

---

## Key Features

* Upload local audio/video files or process YouTube videos directly.
* Automatic audio preprocessing and chunking for long recordings.
* Dual transcription pipeline using **OpenAI Whisper** and **Sarvam AI**.
* AI-generated meeting titles and concise summaries.
* Automatic extraction of:

  * Action Items
  * Key Decisions
  * Open Questions
* Retrieval-Augmented Generation (RAG) for transcript-based question answering.
* ChromaDB vector store with HuggingFace sentence embeddings.
* Interactive chat interface for querying processed transcripts.
* Modern Streamlit-based user interface.

---

## Tech Stack

| Category           | Technologies                      |
| ------------------ | --------------------------------- |
| Language           | Python                            |
| LLM                | Mistral AI                        |
| Speech Recognition | OpenAI Whisper, Sarvam AI         |
| RAG                | LangChain, ChromaDB               |
| Embeddings         | HuggingFace Sentence Transformers |
| Vector Search      | Chroma                            |
| Frontend           | Streamlit                         |
| Audio Processing   | yt-dlp, PyDub, FFmpeg             |
| Environment        | Python Dotenv                     |

---

## Repository

```bash
git clone https://github.com/JAINSID02/AI-VIDEO-ASSISTANT.git

cd AI-VIDEO-ASSISTANT
```

## System Architecture

The application follows a modular pipeline where each component has a single responsibility. This separation makes the codebase easier to maintain, extend, and test while allowing individual modules to evolve independently.

```text
Input (YouTube URL / Local File)
               │
               ▼
      Audio Processing
(Download → Convert → Chunk)
               │
               ▼
        Speech-to-Text
   Whisper / Sarvam AI
               │
               ▼
      Complete Transcript
               │
     ┌─────────┴─────────┐
     ▼                   ▼
AI Analysis          Vector Database
(Summary, Title,     (ChromaDB +
Action Items,         Embeddings)
Decisions,
Questions)               │
     │                   ▼
     └────────────► RAG Pipeline
                        │
                        ▼
             Interactive Q&A Chat
```

---

## Backend Workflow

### 1. Audio Processing

The pipeline accepts either a YouTube URL or a local media file.

For YouTube videos, audio is downloaded automatically using **yt-dlp**. Local media files are converted into a standardized WAV format, ensuring compatibility across the transcription pipeline.

To efficiently process lengthy recordings, audio is divided into fixed-duration chunks before transcription.

---

### 2. Speech Transcription

The project supports two transcription engines depending on the selected language.

* **Whisper** performs local transcription for English recordings.
* **Sarvam AI** handles Hinglish audio and automatically translates the output into English.

Since the Sarvam API accepts short audio segments, the backend automatically splits recordings into smaller pieces, processes them sequentially, and merges the results into a single transcript.

---

### 3. AI-Powered Meeting Analysis

Once transcription is complete, the transcript is passed through multiple independent LLM pipelines powered by **Mistral AI**.

The backend generates:

* Professional meeting title
* Concise meeting summary
* Action items
* Key decisions
* Open questions requiring follow-up

Each task is implemented as an isolated processing chain, making the system modular and easy to extend with additional analysis features.

---

### 4. Retrieval-Augmented Generation (RAG)

Instead of sending the complete transcript to the language model for every question, the project implements a Retrieval-Augmented Generation pipeline.

The transcript is:

* Split into semantic chunks
* Converted into vector embeddings
* Stored in a local ChromaDB vector database
* Retrieved using similarity search for every user query

Only the most relevant transcript sections are supplied to the language model, improving response quality while reducing unnecessary context.

---

### 5. Interactive Question Answering

After the vector database is created, users can interact with the processed recording through a conversational interface.

Questions are answered using only the retrieved transcript context, helping reduce hallucinations and keeping responses grounded in the original meeting content.

## Project Structure

```text
AI-VIDEO-ASSISTANT/
│
├── core/
│   ├── extractor.py          # Extracts action items, decisions and questions
│   ├── rag_engine.py         # Retrieval-Augmented Generation pipeline
│   ├── summarize.py          # Meeting summarization and title generation
│   ├── transcriber.py        # Whisper & Sarvam transcription
│   └── vector_store.py       # ChromaDB vector database
│
├── utils/
│   └── audio_processor.py    # Audio download, conversion and chunking
│
├── vector_db/                # Persisted Chroma vector database
├── downloades/               # Downloaded audio files
│
├── app.py                    # Streamlit frontend
├── main.py                   # Backend pipeline entry point
├── requirements.txt
├── .env
└── .gitignore
```

---

# Backend Modules

### `audio_processor.py`

Responsible for preparing media before transcription.

**Responsibilities**

* Downloads audio from YouTube videos.
* Converts local media files into WAV format.
* Normalizes audio for speech recognition.
* Splits long recordings into manageable chunks.
* Provides a unified processing pipeline for both online and local sources.

---

### `transcriber.py`

Implements the complete speech-to-text pipeline.

**Responsibilities**

* Loads Whisper only when required.
* Supports multiple transcription backends.
* Routes requests based on selected language.
* Automatically handles Sarvam API duration limits.
* Combines chunk-level transcripts into a single document.

---

### `summarize.py`

Processes transcripts using Mistral AI.

**Responsibilities**

* Generates a concise meeting summary.
* Produces a professional meeting title.
* Uses a map-reduce style summarization strategy for long transcripts.

---

### `extractor.py`

Extracts structured information from meeting transcripts.

**Outputs**

* Action Items
* Key Decisions
* Open Questions

Each extraction task runs independently, making it easy to extend the pipeline with additional analysis modules.

---

### `vector_store.py`

Creates and manages the knowledge base used by the RAG pipeline.

**Responsibilities**

* Splits transcripts into semantic chunks.
* Generates sentence embeddings.
* Stores embeddings inside ChromaDB.
* Creates retrievers for similarity search.

---

### `rag_engine.py`

Implements transcript-aware question answering.

Instead of relying solely on the language model, this module retrieves the most relevant transcript sections from the vector database before generating an answer. This keeps responses grounded in the original meeting content.

---

### `main.py`

Acts as the backend orchestrator.

It coordinates every stage of the pipeline:

1. Audio Processing
2. Speech Transcription
3. Title Generation
4. Meeting Summarization
5. Information Extraction
6. Vector Database Creation
7. Interactive Question Answering

Each stage is executed sequentially, producing a complete AI-powered analysis of the input recording.

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/JAINSID02/AI-VIDEO-ASSISTANT.git

cd AI-VIDEO-ASSISTANT
```

---

## 2. Create a Virtual Environment

**Windows**

```bash
python -m venv aivenv

aivenv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv aivenv

source aivenv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install FFmpeg

This project relies on **FFmpeg** for audio conversion.

After installing FFmpeg, make sure it is available in your system PATH.

---

## 5. Configure Environment Variables

Create a `.env` file in the project root and add the following variables:

```env
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key

WHISPER_MODEL=small
SARVAM_STT_MODEL=saaras:v2.5
```

---

# Running the Application

Start the Streamlit interface:

```bash
streamlit run app.py
```

The application allows users to:

* Process YouTube videos.
* Upload local media files.
* Generate meeting summaries.
* Extract action items, decisions, and questions.
* Chat with processed transcripts using RAG.

---

# Technologies Used

| Category               | Technologies              |
| ---------------------- | ------------------------- |
| Programming Language   | Python                    |
| UI Framework           | Streamlit                 |
| LLM                    | Mistral AI                |
| Speech Recognition     | OpenAI Whisper, Sarvam AI |
| AI Framework           | LangChain (LCEL)          |
| Vector Database        | ChromaDB                  |
| Embedding Model        | all-MiniLM-L6-v2          |
| Audio Processing       | yt-dlp, PyDub, FFmpeg     |
| HTTP Requests          | Requests                  |
| Environment Management | Python Dotenv             |

---

# Engineering Highlights

This project focuses on building an end-to-end AI backend rather than simply integrating an LLM.

Some implementation details include:

* Modular processing pipeline with clear separation of responsibilities.
* Language-aware transcription using multiple speech recognition engines.
* Automatic handling of API limitations through audio segmentation.
* Retrieval-Augmented Generation to improve answer quality.
* Persistent local vector database for transcript retrieval.
* Map-reduce based summarization for processing long recordings.
* Reusable LangChain LCEL pipelines for multiple AI tasks.
* Interactive conversational interface backed by transcript retrieval instead of direct prompting.


# Future Improvements

Although the current implementation provides a complete AI-powered meeting analysis pipeline, there are several enhancements that could further improve scalability and user experience.

* Speaker diarization for identifying individual speakers.
* Support for additional languages and multilingual transcription.
* Batch processing of multiple videos or meetings.
* Streaming transcription for live meetings.
* Integration with cloud storage providers such as Google Drive or Dropbox.
* Export reports in Markdown, PDF, and DOCX formats.
* REST API for third-party integrations.
* Docker support for simplified deployment.
* Authentication and user-specific transcript management.

---

# Contributing

Contributions are welcome.

If you have ideas for improving the project, fixing bugs, or adding new features, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a feature branch.

```bash id="mlyd6x"
git checkout -b feature/new-feature
```

3. Commit your changes.

```bash id="lk6q8s"
git commit -m "Add new feature"
```

4. Push the branch.

```bash id="jms6ch"
git push origin feature/new-feature
```

5. Open a Pull Request.

---

# Contact

**Sidharth Jain**

* **GitHub:** https://github.com/JAINSID02
* **LinkedIn:** https://linkedin.com/in/jisidharthjain

If you have questions, suggestions, or would like to collaborate on AI or Machine Learning projects, feel free to connect.

---

# Acknowledgements

This project builds upon several excellent open-source libraries and APIs.

* LangChain
* Mistral AI
* OpenAI Whisper
* ChromaDB
* HuggingFace Sentence Transformers
* Streamlit
* yt-dlp
* PyDub

A big thanks to the maintainers and contributors of these projects for making AI application development more accessible.

---

## Project Status

This project is actively maintained and serves as a practical demonstration of building a modular AI application that combines speech recognition, large language models, vector databases, and Retrieval-Augmented Generation into a single end-to-end workflow.

If you found this project useful, consider giving the repository a ⭐ to support its development.
