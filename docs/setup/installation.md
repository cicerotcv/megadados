# Installation

Using a virtual environment is advised.

## 1. Creating a virtual environment

### 1.1 Using `conda`

To create a virtual environment using Anaconda:

```bash
conda create -n megadados python=3.8
```

Then activate:

```bash
conda activate megadados
```

### 1.2 Using `venv`

To create using `venv`:

```bash
python -m venv virtual-env
```

Then activate it:

Unix/macOS:

```bash
source virtual-env/bin/activate
```

Windows:
```powershell
./virtual-env/Scripts/activate
```

## 2. Installing the dependencies

After activating your environment:

```shell
pip install -r requirements.txt
```