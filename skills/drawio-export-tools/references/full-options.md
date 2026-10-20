# Full Option Lists

## CLI Options (Full List)

**Load this section ONLY if user asks: "what are all the CLI options?" or "show me all flags"**

```text
Format: -f pdf|png|svg|jpg|vsdx|xml
Output: -o <path>
Quality: -t (transparent), --scale <n>, -q <n> (jpeg quality), --border <n>
Pages: -a (all), -p <n> (index), --page-range <range>
Advanced: --embed-diagram, --crop, --uncompressed, -r (recursive)
Validation: --check
```

## GitHub Action Options (Full List)

**Load this section ONLY if user asks for "all action options" or "complete configuration"**

```yaml
format: pdf                   # adoc, md, jpg, pdf, png, svg, xml
path: diagrams/
output: exports               # folder created next to each source file
action-mode: auto             # auto, recent, all, reference
since-reference: main         # only with action-mode: reference
transparent: true
scale: 2
width: 800
height: 600
quality: 100                  # JPEG only (default 90)
border: 10
crop: true
all-pages: true               # PDF only
embed-diagram: true
embed-svg-images: true
embed-svg-fonts: true         # default true
svg-theme: light              # light, dark
svg-links-target: auto        # auto, new-win, same-win
uncompressed: true
enable-plugins: true
remove-page-suffix: true
```
