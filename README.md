# Password Manager

## Description
Password Manager is a simple tool used to securely store and manage your passwords.

## Motivation
The goal behind this project was to store account information in a single, local solution that would allow me to view all of my account information in one place -- by simply scrolling through account names. At the same time, I realized this project would give me practical experience working with databases, creating a simple python backend, and designing a lightweight GUI.

## Getting Started

#### Installation
- Downloadand unzip file from GitHub
- initialize a python virtual environment:
    ```
    python3 -m venv /path/to/new/virtual/environment
    ```
- Activate virtual environment:
    ```
    source <venv_name>/bin/activate
    ```
- Install requirements:
    ```
    python3 install -r requirements.txt
    ```
- Create your secret key by typing the following in the command line or terminal:
    ```
    python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"
    ```
- Copy and paste the output in your virtual environment activate script:
    ```
    export MY_SUPER_SECRET_SECRET="<secret_key_string>"
    ```
#### Executing the program
- Simply run the following in your command line or terminal:
    ```
    python3 ./main.py
    ```

 