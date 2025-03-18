# junpilot

## Project Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/Junnyjun/junpilot.git
    cd junpilot
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the Django development server:
    ```sh
    python manage.py runserver
    ```

## Running the Project using Docker

1. Build the Docker image:
    ```sh
    docker build -t junpilot .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 8000:8000 junpilot
    ```

## Running the Project using an Executable File

1. Create the executable file using PyInstaller:
    ```sh
    pyinstaller --onefile manage.py
    ```

2. Run the executable file:
    ```sh
    ./dist/manage
    ```
