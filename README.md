# AURELIA

AURELIA is a small command-line prototype for structured, safety-first problem analysis.

It turns an input problem into:

- a sharper research question
- clearly labeled known constraints
- testable hypotheses
- a recommended pilot
- estimated benefits
- uncertainty notes
- required human review

## Install

```bash
python -m pip install -e .
```

## Usage

```bash
python -m aurelia "How effective is intervention for coastal flooding?"
```

Blank or punctuation-only input is rejected with a CLI usage error.

## Testing

```bash
python -m unittest discover -s tests
```
