# Menumaker — Project Setup Screens

Static HTML/CSS prototype of the Project Setup screens, built from the
[Figma comps](https://www.figma.com/design/fVl7BGfMaH18ZOX1tqvC5t/PROJECT-SETUP-SCREEN?node-id=26-6132).

## Pages

One file per tab. Open `index.html` and use the tab bar.

| File | Tab |
| --- | --- |
| `index.html` | General Info |
| `renderings.html` | Renderings |
| `library.html` | Library |
| `data.html` | Data |
| `templates.html` | Templates |
| `default-modifiers.html` | Default Modifiers |
| `styles.html` | Styles |
| `configuration.html` | Configuration › Access |
| `configuration-approval.html` | Configuration › Approval |

## Structure

```
css/styles.css   all styles, one file, sectioned (see header comment)
js/app.js        prototype interactions only
build.py         regenerates the 9 pages from one shared shell
```

`build.py` exists so the app bar, tab bar and footer are authored once instead
of nine times. Edit the page bodies there and run `python3 build.py` — or just
edit the generated HTML directly if you prefer; the output is plain,
hand-readable markup.

## Conventions

- **Colors** are CSS custom properties in `:root` (`--color-*`). Nothing
  hard-codes a hex value outside that block, except the two icon swatches on
  the Data tab, which are per-record data.
- **Type / space / shape** are also tokenized (`--font-size-*`, `--space-*`,
  `--radius-*`) so the scale stays consistent.
- **Fonts**: Roboto via Google Fonts (400 / 500 / 700).
- **Icons**: Font Awesome kit `da08280601`.
- **Reuse over duplication**: `.control`, `.input`, `.textarea`,
  `.select__native` and `.combo__field` share one control surface rule, so
  every field is the same height, border and radius by construction.
- **Checkboxes and radios** are wrapped in `.choice`, a `<label>` — the whole
  row, label text included, is the touch target.

## Custom controls

`.combo` is the shared shell for the two existing custom elements:

- `[data-combo="multiselect"]` — chips (`.chip`) plus a typeahead input.
- `[data-combo="typeahead"]` — single-value input, "Select an Option".

Markup is static here; wire these to the real components when integrating.

## Known placeholders

- **Date picker** is generic on purpose. Fields render as `mm/dd/yyyy` text
  inputs to match the comps; the calendar button momentarily swaps the input to
  a native `type="date"` and calls `showPicker()`. Swap in the real picker
  later — the hook is `[data-date-trigger]` in `js/app.js`.
- **Style Preview** thumbnails on the Styles tab are placeholder boxes; no
  image assets were exported from the comps.
- Table row actions, pagination, and the `+ Rendering` sub-tab are inert.
- Two comp labels were corrected: "Search Corpoate Contacts" → "Search
  Corporate Contacts", and the Configuration › Access search placeholder
  "Search Styles" → "Search Access Rules".
