# Pending Result Processor

This project is a Streamlit application designed to process multiple Excel files and generate a pending result report automatically.

## Project Structure

```
streamlit-app
├── src
│   ├── main.py
│   ├── processor.py
│   └── center_map.py
├── requirements.txt
└── README.md
```

## Installation

To run this project, you need to have Python installed on your machine. Follow these steps to set up the project:

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies using pip:

   ```
   pip install -r requirements.txt
   ```

## Running the Application

To start the Streamlit application, run the following command in your terminal:

```
streamlit run src/main.py
```

Once the application is running, you can access it in your web browser at `http://localhost:8501`.

## Usage

- Upload multiple Excel files using the provided interface.
- The application will load the files and concatenate them into a single DataFrame for further processing.