# skip-scan

Find skipped and focused tests hiding in your codebase.

`skip-scan` walks a repository and reports every test that is skipped, xfailed, or
focused (`.skip`, `xit`, `@pytest.mark.skip`, `t.Skip`, `#[ignore]`, …). It is a
small, dependency-free CLI meant to run in CI so skipped tests stop being
invisible.

## Features

- Detects skip/focus markers across Python, JavaScript/TypeScript, Go, Rust,
  Java, and Ruby.
- Reports file, line number, marker kind, and the offending snippet.
- Text or JSON output for humans or machines.
- CI-friendly exit codes: fail when any skip is found, or above a threshold.
- Ignores common non-source directories (`node_modules`, `.git`, `venv`, …).
- No network access, no paid APIs, no runtime dependencies.

## Install

```bash
git clone https://github.com/your-org/skip-scan.git
cd skip-scan
pip install -e .
```

Or run directly without installing:

```bash
python -m skipscan.cli .
```

## Usage

Scan the current directory:

```bash
skip-scan .
```

JSON output:

```bash
skip-scan . --json
```

Fail the build if any skipped test exists:

```bash
skip-scan . --fail
```

Allow up to 3 skipped tests before failing:

```bash
skip-scan . --fail --threshold 3
```

Scan only certain extensions:

```bash
skip-scan src --include .py,.ts
```

## Example output

```
src/test_user.py:12: @pytest.mark.skip
src/test_user.py:40: @pytest.mark.xfail
tests/foo.test.ts:8: it.skip("...", () => {})
```

## License

MIT
