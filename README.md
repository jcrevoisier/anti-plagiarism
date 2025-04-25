# Plagiarism Checker API

This is a simple Flask application that allows users to check for plagiarism by extracting text from a provided URL, preprocessing the text, and then searching for duplicate content using Google Search.

## Features
- **Extract Text from URL**: Given a URL, the app extracts the visible text by removing unnecessary elements like scripts and styles.
- **Text Preprocessing**: The extracted text is tokenized, stopwords are removed, and stemming is applied for efficient comparison.
- **Plagiarism Detection**: It breaks the text into chunks and searches Google for each chunk to detect potential plagiarism.
- **Health Check Endpoint**: To ensure the service is running properly.

## Requirements

- Python 3.6+
- Flask
- nltk
- BeautifulSoup4
- requests
- googlesearch-python

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Download necessary NLTK data:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    ```

## Usage

1. **Run the Flask app**:
    ```bash
    python app.py
    ```

2. **Access the app**:
    - Open a browser and go to `http://localhost:8080/` to see the homepage.
    - You can also interact with the app via the `/check-plagiarism` API endpoint.

### Endpoints

- **GET `/`**: Displays the homepage (requires a template like `index.html`).
- **GET `/health`**: Health check endpoint to verify if the server is running. Returns:
    ```json
    {
        "status": "healthy"
    }
    ```
- **POST `/check-plagiarism`**: Checks for plagiarism. Requires a JSON body with a `url` field.
    
    Example request:
    ```json
    {
        "url": "https://example.com"
    }
    ```

    Example response:
    ```json
    {
        "url": "https://example.com",
        "results": [
            {
                "chunk": "some extracted chunk of text",
                "sources": [
                    "https://source1.com",
                    "https://source2.com"
                ]
            },
            ...
        ]
    }
    ```

## How It Works

1. **Text Extraction**: The app fetches the content of the provided URL and uses BeautifulSoup to remove unnecessary elements such as `<script>` and `<style>`. The visible text is then extracted.

2. **Text Preprocessing**: The text is tokenized (broken into words), stopwords (common words like "and", "the", etc.) are removed, and stemming is applied to reduce words to their root form.

3. **Plagiarism Search**: The text is broken into chunks (default chunk size is 10 words). Each chunk is searched using Google Search. If the chunk matches any content on other web pages, it is considered a potential plagiarism source.

4. **Result Formatting**: For each chunk, the app returns a list of sources (URLs) where similar content was found.

## Error Handling

- If the request is missing the `url` field, the app responds with a `400` error and a message:
    ```json
    {
        "error": "URL is required"
    }
    ```

- If there’s an issue extracting text from the URL, the app responds with an error message.

## Example:

1. **Send a POST request to `/check-plagiarism`**:
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"url": "https://example.com"}' \
    http://localhost:8080/check-plagiarism
    ```

    Response:
    ```json
    {
        "url": "https://example.com",
        "results": [
            {
                "chunk": "Lorem ipsum dolor sit amet",
                "sources": [
                    "https://source1.com",
                    "https://source2.com"
                ]
            },
            ...
        ]
    }
    ```

## Testing the Application

1. You can write unit tests for individual functions like `extract_text_from_url`, `preprocess_text`, etc., using libraries such as `unittest` or `pytest`.
2. For integration testing, you can use Flask’s test client to simulate API requests.

## Deployment

1. **Docker**: You can containerize the app using Docker for easier deployment.

2. **Cloud Deployment**: You can deploy this app to cloud platforms like Heroku, AWS, GCP, or any other platform that supports Python/Flask apps.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
