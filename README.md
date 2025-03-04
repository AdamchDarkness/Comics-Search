# ProjectComicsSearch

A full-stack project for managing and searching comics. This project extracts cover images from comics stored on a NAS, indexes comic metadata in Elasticsearch, provides a REST API with Laravel, and features a modern React + TypeScript front-end built with Vite.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)

## Features

- **Cover Extraction**: Automatically extract the first page (cover) from comics in PDF, CBZ, and CBR formats using Python.
- **Elasticsearch Indexing**: Create and index a "comics" index with custom mappings and analyzers to optimize text search.
- **REST API with Laravel**: Query the comics index with optional filters (query, saga, extension, publishing house, run) and serve cover images via HTTP.
- **Modern Front-End**: A search page built with React, TypeScript, and Vite, featuring a search bar, dynamic filters, and result items displaying a larger cover image and comic details.

## Technologies Used

- **Backend Extraction & Indexing**: Python, PyMuPDF, zipfile, rarfile, Elasticsearch, Laravel
- **Front-End**: React, TypeScript, Vite
- **Other Tools**: WinRAR (or standalone UnRAR) for CBR extraction on Windows


## Installation

### Backend Extraction & API

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YourUsername/ProjectComicsSearch.git
   cd ProjectComicsSearch/backend
	```

2. **Python Extraction Script:**
	
	Ensure you have Python 3 installed, then install dependencies:
   ```bash
   pip install PyMuPDF rarfile elasticsearch
	```
	Note: On Windows, ensure that UnRAR.exe is installed and update the path in the script accordingly:
   ```bash
   rarfile.UNRAR_TOOL = r'PATH-TO\UnRAR.exe'
	```

3. **Laravel API:**
	
	Navigate to the Laravel project directory: \
	Install dependencies:
   ```bash
   composer install
	```
	Configure your .env file with your Elasticsearch credentials and other settings.\
	Run migrations and seeders if needed, then start the Laravel server:
	```bash
   php artisan serve
	```
	
### Front-End
	1. **Clone the repository (if not already cloned):**
	2. **Install dependencies:**
   ```bash
   npm install
	```
	3. **Start the development server:**
	```bash
   npm run dev
	```
	The front-end should be accessible on the port specified by Vite (e.g., http://localhost:5173).

## Usage

	- *Search Page*:
		The search page provides a search bar and filters to query comics. It calls the Laravel API endpoint at http://comicssearch.test/api/search to retrieve data from Elasticsearch.
	- *Cover Images:*:
		The front-end builds cover image URLs from the cover_path field and requests them via the Laravel API endpoint /api/covers/{filename}. Make sure your Laravel API can access and serve images from your NAS.
	