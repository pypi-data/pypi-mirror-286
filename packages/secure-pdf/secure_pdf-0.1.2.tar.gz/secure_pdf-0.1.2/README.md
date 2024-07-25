# Secure PDF
================

A simple web application to remove passwords from PDF files.

## Table of Contents
-----------------

1. [Introduction](#introduction)
2. [Features](#features)
3. [How it Works](#how-it-works)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction
---------------

Secure PDF is a web application that allows users to upload a PDF file, enter the password, and download the PDF file without the password. This application uses a secure password removal process to ensure the confidentiality and integrity of the PDF file.

## Features
------------

* Remove passwords from PDF files
* Secure password removal process
* Easy to use web interface
* Supports PDF files with RC4 and AES encryption

## How it Works
----------------

1. The user uploads a PDF file to the application.
2. The user enters the password for the PDF file.
3. The application checks the password and add/removes it from the PDF file.
4. The user can then download the PDF file without the password.

## Installation
---------------

To install the Secure PDF application, follow these steps:

    pip install secure_pdf

## Usage
-----
For Usage run following command

    run_secure_pdf

1. Open a web browser and navigate to `http://localhost:8501`
2. Click on the "Upload PDF" button to select a PDF file.
3. Enter the password for the PDF file in the "Password" field.
4. Based on selected radio button if "Remove Password" is selected, then password is removed.
5. if "Add a Password" is selected, then pdf is secured with password.
6. Click on the "Download" button to download the PDF file with/without the password.

## Contributing
------------

Contributions are welcome! If you have any issues or feature requests, please open an issue on the GitHub repository. If you would like to contribute code.

## License
-------

Secure PDF is licensed under the MIT License. See LICENSE for details https://opensource.org/license/mit