# Contributing to Telegram Auto Order Bot

Terima kasih atas minat Anda untuk berkontribusi! 🎉

## Cara Berkontribusi

### 1. Melaporkan Bug

Jika menemukan bug:
1. Cek apakah bug sudah dilaporkan di [Issues](https://github.com/yasirarism/telegram-auto-order-bot/issues)
2. Jika belum, buat issue baru dengan detail:
   - Deskripsi bug
   - Langkah untuk reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots (jika ada)
   - Environment (OS, Python version, dll)

### 2. Request Fitur Baru

Untuk request fitur baru:
1. Buat issue dengan label `enhancement`
2. Jelaskan fitur yang diinginkan
3. Jelaskan use case dan benefit
4. Tambahkan mockup atau example (jika ada)

### 3. Pull Request

#### Persiapan
```bash
# Fork repository
# Clone fork Anda
git clone https://github.com/YOUR_USERNAME/telegram-auto-order-bot.git
cd telegram-auto-order-bot

# Tambah upstream remote
git remote add upstream https://github.com/yasirarism/telegram-auto-order-bot.git

# Buat branch baru
git checkout -b feature/nama-fitur
```

#### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env dengan test credentials

# Test changes
python main.py
```

#### Submit PR
```bash
# Commit changes
git add .
git commit -m "Add: deskripsi perubahan"

# Push ke fork
git push origin feature/nama-fitur

# Buat PR di GitHub
```

### 4. Coding Standards

#### Python Style Guide
- Ikuti [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Gunakan 4 spaces untuk indentation
- Maximum line length: 100 characters
- Gunakan docstrings untuk functions dan classes

#### Contoh:
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    # Function implementation
    return True
```

#### Naming Conventions
- Variables & functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private methods: `_leading_underscore`

#### Code Organization
- Satu file untuk satu concern
- Group related functions
- Keep functions small and focused
- Add comments untuk logic yang kompleks

### 5. Commit Messages

Format commit message:
```
Type: Short description

Detailed description (jika diperlukan)

Fixes #issue_number
```

Types:
- `Add:` - Fitur baru
- `Fix:` - Bug fix
- `Update:` - Update code/dependencies
- `Refactor:` - Code refactoring
- `Docs:` - Documentation
- `Test:` - Testing
- `Style:` - Formatting

Contoh:
```
Add: Product pagination feature

Implemented pagination for product catalog to handle
more than 10 products per page.

Fixes #123
```

### 6. Testing

Sebelum submit PR:
- Test manual semua perubahan
- Pastikan tidak ada syntax error
- Pastikan tidak break existing features
- Test dengan berbagai scenarios

### 7. Documentation

Update documentation jika diperlukan:
- README.md - Untuk perubahan major
- USAGE.md - Untuk fitur baru
- DEPLOYMENT.md - Untuk deployment changes
- Docstrings - Untuk functions baru

## Development Setup

### Prerequisites
- Python 3.11+
- MongoDB
- Virtual environment (recommended)

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
# Install MongoDB atau gunakan Docker
docker run -d -p 27017:27017 mongo:7.0

# Setup config
cp .env.example .env
# Edit .env dengan credentials
```

### Project Structure
```
telegram-auto-order-bot/
├── main.py              # Bot entry point
├── config.py            # Configuration
├── database.py          # Database operations
├── handlers.py          # User command handlers
├── admin.py             # Admin command handlers
├── keyboards.py         # Keyboard utilities
├── setup_sample_data.py # Sample data setup
├── test_structure.py    # Structure validation
├── requirements.txt     # Dependencies
├── Dockerfile           # Docker config
├── docker-compose.yml   # Docker Compose config
└── docs/                # Documentation
```

## Code Review Process

1. PR akan di-review oleh maintainer
2. Bisa ada request untuk changes
3. Setelah approved, akan di-merge
4. PR akan otomatis di-close setelah merge

## Questions?

Jika ada pertanyaan:
- Buka discussion di GitHub
- Comment di issue terkait
- Contact maintainer

## License

Dengan berkontribusi, Anda setuju bahwa kontribusi Anda akan dilisensikan di bawah MIT License.

## Code of Conduct

- Be respectful
- Be professional
- Be collaborative
- Be helpful

Terima kasih sudah berkontribusi! 🙏
