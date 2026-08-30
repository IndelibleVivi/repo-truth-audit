# Cedar Tool

Resolve the stable release artifact with an immutable selector:

```bash
python3 selector.py --channel stable --ref v1.0.0
```

Development work uses the separate current channel:

```bash
python3 selector.py --channel development
```

Stable artifacts live under `releases/`; mutable development work lives under
`development/`. Each selected directory carries its own identity record. The
selector verifies that identity and does not provide an implicit default.
