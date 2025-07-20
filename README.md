# PDF Heading Extractor 📄

Simple tool: Upload PDF → Get JSON with headings

## Usage

1. **Install:**

```bash
pip install -r requirements.txt
```

2. **Extract headings:**

```bash
python extract.py your_file.pdf
```

3. **Get output:** `your_file_headings.json`

## Output Format

```json
{
	"title": "Document Title",
	"outline": [
		{
			"text": "Introduction",
			"level": "H1",
			"page": 1
		}
	]
}
```

That's it! �
