# Fast PDF Heading Extractor 📄

Ultra-fast tool: Upload PDF → Get JSON with headings in under 10 seconds

## Quick Start

**Single file:**

```bash
python fast_extract.py file01.pdf
```

**Batch process:**

```bash
python batch_process.py
```

## Performance

- Processes 5 files in ~0.13 seconds
- Average: 0.027 seconds per file
- Well under 10-second requirement

## Output Format

```json
{
	"title": "Document Title",
	"outline": [
		{
			"text": "1. Introduction",
			"level": "H1",
			"page": 1
		}
	]
}
```

That's it! 🚀
