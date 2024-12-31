# CipherMan

Welcome to **CipherMan**, your friendly neighborhood file encryption and decryption tool! Whether you're securing sensitive files or unlocking them, CipherMan is here to save the day, just like your favorite superhero—but with fewer webs and more ciphers. This document explains everything you need to know to use CipherMan effectively and securely.

---

### Table of Contents:

1. [Introduction](#cipherman-documentation)  
   1.1 [What is CipherMan?](#what-is-cipherman)  
   1.2 [Features](#features)  

2. [How It Works](#how-it-works)  
   2.1 [Encryption](#encryption)  
   2.2 [Decryption](#decryption)  

3. [Installation](#installation)  

4. [Usage](#usage)  
   4.1 [Basic Syntax](#basic-syntax)  
   4.2 [Arguments](#arguments)  
   4.3 [Examples](#examples)  

5. [Walkthrough](#walkthrough)  
   5.1 [Encrypting Files](#1-encrypting-files)  
   5.2 [Decrypting Files](#2-decrypting-files)  

6. [How CipherMan Keeps It Simple Yet Secure](#how-cipherman-keeps-it-simple-yet-secure)  

7. [Known Limitations](#known-limitations)  

8. [Frequently Asked Questions](#frequently-asked-questions)  

9. [Behind the Scenes: Technical Details](#behind-the-scenes-technical-details)  

10. [Final Words](#final-words)  

11. [Collaboration and Contact](#collaboration-and-contact)  

12. [License](#license)  

---

Let me know if you'd like this added to your documentation!
      
---

## What is CipherMan?
CipherMan is a command-line utility designed to encrypt and decrypt files in a specified directory using AES encryption. It ensures your files are safe from prying eyes while giving you full control over their security. CipherMan doesn’t just protect your data; it adds a touch of superhero flair to file security!

---

## Features

- **AES Encryption**: Uses Advanced Encryption Standard (AES) in CBC mode for robust encryption.
- **File-Specific Operations**: Only encrypts files without the `.xo` extension and decrypts files with the `.xo` extension.
- **Password Verification**: Ensures that you confirm your password to prevent typos.
- **Retry on Error**: If the password for decryption is incorrect, CipherMan lets you try again without restarting.
- **Directory Targeting**: Operates only on files within a user-specified directory.

---

## How It Works

CipherMan uses the following workflow for encryption and decryption:

### Encryption:
1. The user specifies a directory containing files to encrypt.
2. CipherMan asks for a password and confirmation.
3. For each file in the directory (excluding those already encrypted with `.xo`):
- Generates a 16-byte salt and an initialization vector (IV).
- Derives a 256-bit encryption key from the password and salt using PBKDF2.
- Pads the file content using PKCS7 and encrypts it with AES.
- Saves the encrypted file with the `.xo` extension and deletes the original.

### Decryption:
1. The user specifies a directory containing `.xo` files to decrypt.
2. CipherMan asks for a password and tries to decrypt each file.
3. If the password is incorrect, it allows the user to re-enter the correct password.
4. Successfully decrypted files are restored to their original state, and the `.xo` files are deleted.

---

## Installation

No fancy installation steps are required! Just download the script, ensure you have Python installed on your system (version 3.6+) and run this command.
```bash
pip install -r requirements.txt
```
---

## Usage

CipherMan operates exclusively via the command line. Here’s how to use it:

### Basic Syntax
```bash
python cipherman.py <mode> --dir <directory>
```

### Arguments

1. **`<mode>`**: Choose the operation mode.
- `encrypt`: Encrypt all files in the directory.
- `decrypt`: Decrypt all `.xo` files in the directory.

2. **`--dir <directory>`**: Specify the path to the directory containing files. This argument is **required**.

### Examples

#### Encrypt Files:
```bash
python cipherman.py encrypt --dir /path/to/directory
```

#### Decrypt Files:
```bash
python cipherman.py decrypt --dir /path/to/directory
```

---

## Walkthrough

### 1. Encrypting Files

#### Step-by-Step:
1. Run CipherMan in `encrypt` mode with the `--dir` argument pointing to the desired directory.
2. Enter a password when prompted.
3. Re-enter the password to confirm.
4. CipherMan processes each file in the directory:
- Files without the `.xo` extension are encrypted.
- Files already encrypted are skipped.

#### Output:
Encrypted files are saved with the `.xo` extension in the same directory. The original files are deleted.

### 2. Decrypting Files

#### Step-by-Step:
1. Run CipherMan in `decrypt` mode with the `--dir` argument pointing to the desired directory.
2. Enter the password for decryption.
3. If the password is incorrect, CipherMan prompts you to try again.
4. Successfully decrypted files are restored to their original format, and `.xo` files are removed.

#### Output:
Decrypted files replace the `.xo` files in the directory.

---

## How CipherMan Keeps It Simple Yet Secure

1. **Hidden Password Input**:
- Passwords are entered securely using the `getpass` module.
- Users confirm their password during encryption to prevent typos.

2. **Retry Mechanism for Decryption**:
- If the password is incorrect, CipherMan catches the error and asks the user to re-enter it until successful.

3. **AES Encryption with PBKDF2**:
- The key is derived using PBKDF2 (Password-Based Key Derivation Function 2), which ensures strong keys even from simple passwords.
- Random salts are used to make each encryption unique.

4. **File-Specific Logic**:
- Only unencrypted files are encrypted.
- Only `.xo` files are decrypted.

---

## Known Limitations

- **Password Recovery**: If the password is lost, the files cannot be decrypted. Ensure you choose a password you can remember or store it securely.
- **File Size Overhead**: Encrypted files are slightly larger due to padding and the inclusion of the IV.

---

## Frequently Asked Questions

### What happens if I forget my password?
Unfortunately, CipherMan does not offer a recovery mechanism. It’s a design choice to ensure maximum security. To mitigate this, consider:
- Writing your password down in a secure location.
- Using a password manager to store it.

### Can I encrypt or decrypt files in nested directories?
Currently, CipherMan only processes files in the specified directory. Nested directories are ignored.

### Is my password stored anywhere?
No. CipherMan does not store or log your password. The key is derived dynamically during the encryption/decryption process.

---

## Behind the Scenes: Technical Details

1. **Encryption Algorithm**:
- Uses AES (Advanced Encryption Standard) in CBC (Cipher Block Chaining) mode.
- Block size: 128 bits.

2. **Key Derivation**:
- PBKDF2 with SHA-256.
- 100,000 iterations for added computational effort.

3. **Padding Scheme**:
- PKCS7 padding ensures input length matches the block size.

4. **Randomization**:
- A unique IV is generated for each file, ensuring ciphertext differs even if plaintext and password are identical.

---

## Final Words
CipherMan is a simple yet powerful tool for protecting your files. Like any superhero, it relies on the user to wield it responsibly. Choose strong passwords, keep them safe, and let CipherMan handle the rest.

Stay secure, and may CipherMan keep your data as safe as Vibranium!

---

## Collaboration and Contact
Have feedback, found a bug, or want to contribute to CipherMan? We’d love to hear from you! Reach out through the following channels:

- **Email**: **kamalhegazi05@gmail.com**
- **GitHub**: [**Here**](https://github.com/KamalHegazi)
- **LinkedIn**: [**Here**](https://www.linkedin.com/in/kamalhegazi/)

---

## License

CipherMan is licensed under the [**MIT License**](https://github.com/KamalHegazi/cipherMan/blob/main/LISENCE). Feel free to use, modify, and distribute it, but don’t forget to give credit where credit is due. Encrypt responsibly!
