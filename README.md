# Ransomware Simulation Project

## 📋 Description

This is a client-server ransomware simulation that demonstrates:
- File encryption using hybrid cryptography (RSA + AES-GCM)
- Remote command and control
- Persistence mechanisms
- File decryption capabilities

## 🏗️ Architecture

The project consists of several modules:

- **Client.py** - The client agent that runs on the target machine
- **Server.py** - Command and control server
- **Encrypt.py** - File encryption module using AES-GCM
- **Decrypt.py** - File decryption module
- **Rsa.py** - RSA key pair generation
- **Database.py** - SQLite database for storing encryption keys
- **Note.py** - Ransom note display functionality
- **Run.py** - Server startup script

## 🔐 Encryption Details

- **Asymmetric Encryption**: RSA-2048 with OAEP padding (SHA-256)
- **Symmetric Encryption**: AES-256-GCM
- **Key Storage**: SQLite database indexed by MAC address

### Encryption Process:
1. Generate random 256-bit AES key
2. Encrypt file content with AES-GCM
3. Encrypt AES key with RSA public key
4. Store encrypted key + IV + tag + ciphertext
5. Rename file with `.lolo` extension

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Start the Server:
```bash
python Run.py
```

### Run the Client:
```bash
python Client.py
```

### Available Commands:
- `encrypt` - Encrypt files in the target directory
- `decrypt` - Decrypt encrypted files
- `get mac` - Get the machine's MAC address
- `help` - Display available commands
- `exit` - Close the connection

## 📁 Project Structure

```
.
├── Client.py           # Client agent
├── Server.py           # C&C server
├── Encrypt.py          # Encryption module
├── Decrypt.py          # Decryption module
├── Rsa.py              # RSA key generation
├── Database.py         # Key storage
├── Note.py             # Ransom note
├── Run.py              # Server launcher
├── requirements.txt    # Dependencies
└── README.md           # This file
```

## 🔧 Configuration

Default settings:
- **Host**: 127.0.0.1 (localhost)
- **Port**: 12345
- **Target Directory**: `C://Users//<username>//Desktop//test`
- **File Extensions**: `.txt`
- **Database**: `rsa_keys.db`

## 🛡️ Security Considerations

This simulation demonstrates several security vulnerabilities:
1. Arbitrary command execution
2. Hardcoded paths and configurations
3. No authentication mechanism
4. Unencrypted private key storage
5. Bare exception handlers

See `CODE_IMPROVEMENTS.md` for detailed security recommendations.

## 🧪 Testing Environment

**IMPORTANT**: Only test this software in isolated, controlled environments:
- Virtual machines (VMware, VirtualBox)
- Sandboxed environments
- Test directories with non-critical files
- Never on production systems or real user data

## 📚 Educational Resources

This project can be used to learn about:
- Cryptography (RSA, AES-GCM)
- Socket programming
- Client-server architecture
- Malware analysis and defense
- Cybersecurity best practices

## 🤝 Contributing

Contributions for educational improvements are welcome:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is provided as-is for educational purposes. Use responsibly and ethically.

## ⚖️ Ethical Guidelines

- Never use this software without explicit permission
- Only test in controlled environments
- Respect privacy and data protection laws
- Use knowledge gained for defensive purposes
- Report vulnerabilities responsibly

## 📞 Contact
khalaf.hamza.email@gmail.com
