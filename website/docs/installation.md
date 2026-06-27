---
id: installation
title: Installation
sidebar_position: 2
---

# Installation

## Requirements

- Python 3.11 or higher
- pip

## Install

```bash
pip install argus-standards
```

## Verify

```bash
argus --version
```

Expected output: `argus, version 0.1.1` (or newer).

## Upgrade

To upgrade to the latest version:

```bash
pip install --upgrade argus-standards
```

See [Upgrade](./upgrade) for detecting when generated files are out of date after an upgrade.

## Virtual Environments

If your project uses a virtual environment, install Argus inside it:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install argus-standards
argus --version
```

## Next Step

→ [Quick Start](./quick-start)
