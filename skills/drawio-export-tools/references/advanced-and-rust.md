# Advanced Processing and Rust Library

## Advanced Processing

**When to provide:** User needs custom processing, pre/post hooks, or pipeline integration

**Three approaches:**

1. **Pre-process diagram (modify XML):**

```bash
# Modify .drawio file → Export → Restore
sed -i.bak 's/pattern/replacement/g' diagram.drawio
docker run ... drawio-desktop-headless -x diagram.drawio
mv diagram.drawio.bak diagram.drawio
```

1. **Post-process output:**

```bash
# Export → Transform output → Save
docker run ... drawio-desktop-headless -x diagram.drawio -o temp.pdf
convert temp.pdf [transformations] final.pdf
```

1. **Custom pipeline:**

```bash
#!/bin/bash
preprocess_diagrams()
export_with_custom_logic()
postprocess_outputs()
```

**Offer:** "What specific processing do you need? (watermarks, metadata, format conversion, etc.)"

---

## Rust Library

**When to provide:** User is building a custom tool or needs library integration

**Use drawio-exporter** (Rust library) for:

- Building automation tools
- Service/API integration
- Custom export logic

```rust
use drawio_exporter::Exporter;
// Build your custom export pipeline
```

**Full docs:** <https://github.com/rlespinasse/drawio-exporter>

**Most users should use Docker tools instead.**
