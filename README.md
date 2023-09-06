<h1 align="center">Megadados | FastAPI</h1>

<h4 align="center"> 
	🚧 Megadados | FastAPI 🚧
</h4>

<p align="center" style="font-style:italic;">In summary, this FastAPI project was a learning and experimentation journey to gain expertise in this framework and potentially develop functional applications or APIs along the way.</p>

<!-- related technologies -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=FastAPI&logoColor=white" />
</p>
<p align="center" style="font-style:italic;">
To access the full documentation on how to setup and execute this project, refer to the <a href="https://cicerotcv.github.io/megadados/">mkdocs page</a></p>



## 🚀 Getting started

### ⚠️ Installation Requirements
To set up and run the project, you will need:

- **Python 3.8**;
- **[Optional]** Anaconda for environemnt management;

### 🛠️ Installation Instructions

Follow these steps to install and set up the project:

1. Clone the repository:

    ~~~bash
    git clone https://github.com/cicerotcv/megadados
    ~~~

2. Go to Predictor directory
    ~~~bash
    cd megadados
    ~~~


3. Set up the Python environment

    <details>
      <summary><b>Windows</b></summary>

    1. Make sure you have **python3.8** installed.
    2. Run `python -m venv venv` to create the virtual environment;
    3. Activate the virtual environment `. ./venv/Scripts/activate`;
    4. Install the dependencies: `pip install -r requirements.txt`
    </details>

    <details><summary><b>Unix/macOS</b></summary>

    1. Make sure you have **python3.8** or greater installed.
    2. Run `python3.x -m venv venv` to create the virtual environment;
    3. Activate the virtual environment `source venv/bin/activate`;
    4. Install the dependencies: `pip install -r requirements.txt`

    </details>

    <details><summary><b>Using Anaconda</b></summary>

    1. With conda, run `conda env create -n megadados python=3.8` to create the `megadados` environment;
    2. Activate the virtual environment with `conda activate megadados`
    3. Install the dependencies: `pip install -r requirements.txt`
    </details>

### ➡️ Executing the project

To run the project, execute the following command:

~~~powershell
python -m  uvicorn src.main:app
~~~
