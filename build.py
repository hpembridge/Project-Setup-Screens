#!/usr/bin/env python3
"""Generates the static Project Setup screens from a single shared shell.

Run:  python3 build.py
Every page is written as plain, readable HTML — the script only exists so the
app bar / tab bar / footer are authored once instead of nine times.
"""

import pathlib

OUT = pathlib.Path(__file__).parent

TABS = [
    ("index.html",             "General Info"),
    ("renderings.html",        "Renderings"),
    ("library.html",           "Library"),
    ("data.html",              "Data"),
    ("templates.html",         "Templates"),
    ("default-modifiers.html", "Default Modifiers"),
    ("styles.html",            "Styles"),
    ("configuration.html",     "Configuration"),
]

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &middot; Project Setup &middot; Menumaker</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
<script src="https://kit.fontawesome.com/da08280601.js" crossorigin="anonymous"></script>
</head>
<body>
<div class="app">

  <header class="app-bar">
    <h1 class="app-bar__title">Project Name</h1>
    <a class="app-bar__action" href="#">
      <i class="fa-regular fa-pen-to-square" aria-hidden="true"></i>
      Edit Default Menu
    </a>
  </header>

  <nav class="tab-bar" aria-label="Project setup sections">
{tabs}
  </nav>
{subtabs}
  <main class="page">
{body}
  </main>

  <footer class="app-footer">
    <button type="button" class="btn">
      <i class="fa-regular fa-circle-xmark" aria-hidden="true"></i> Cancel Edits
    </button>
    <button type="button" class="btn btn--success">
      <i class="fa-solid fa-floppy-disk" aria-hidden="true"></i> Save Project
    </button>
  </footer>

</div>
<script src="js/app.js"></script>
</body>
</html>
"""


def tab_bar(active_href):
    out = []
    for href, label in TABS:
        cls = "tab is-active" if href == active_href else "tab"
        aria = ' aria-current="page"' if href == active_href else ""
        out.append(f'    <a class="{cls}" href="{href}"{aria}>{label}</a>')
    return "\n".join(out)


def subtab_bar(items, active):
    """items: list of (href, label)."""
    if not items:
        return ""
    rows = []
    for href, label in items:
        cls = "subtab is-active" if label == active else "subtab"
        rows.append(f'    <a class="{cls}" href="{href}">{label}</a>')
    return (
        '\n  <nav class="subtab-bar" aria-label="Section views">\n'
        + "\n".join(rows)
        + "\n  </nav>\n"
    )


def indent(text, spaces=4):
    pad = " " * spaces
    return "\n".join(pad + ln if ln.strip() else "" for ln in text.strip("\n").split("\n"))


# ---------------------------------------------------------------- partials ---

def checkbox(label, checked=False, name=None):
    attr = " checked" if checked else ""
    nm = f' name="{name}"' if name else ""
    return (
        f'<label class="choice"><input type="checkbox"{nm}{attr}>'
        f"<span>{label}</span></label>"
    )


def radio(label, group, checked=False):
    attr = " checked" if checked else ""
    return (
        f'<label class="choice"><input type="radio" name="{group}"{attr}>'
        f"<span>{label}</span></label>"
    )


def choice_group(rows):
    return '<div class="choice-group">\n' + "\n".join("  " + r for r in rows) + "\n</div>"


def field(label, control, for_id=None):
    lbl = f'<label class="field__label"{f" for=" + chr(34) + for_id + chr(34) if for_id else ""}>{label}</label>'
    return f'<div class="field">\n  {lbl}\n{indent(control, 2)}\n</div>'


def text_input(value="", placeholder="", disabled=False, iid=None):
    v = f' value="{value}"' if value else ""
    p = f' placeholder="{placeholder}"' if placeholder else ""
    d = " disabled" if disabled else ""
    i = f' id="{iid}"' if iid else ""
    return f'<input type="text" class="input"{i}{v}{p}{d}>'


def date_field(value="", disabled=False):
    d = " disabled" if disabled else ""
    v = f' value="{value}"' if value else ""
    ph = "" if value else ' placeholder="mm/dd/yyyy"'
    return (
        '<div class="date">\n'
        f'  <input type="text" class="input" data-date{v}{ph}{d}>\n'
        f'  <button type="button" class="date__trigger" data-date-trigger'
        f'{d} aria-label="Choose date">'
        '<i class="fa-regular fa-calendar" aria-hidden="true"></i></button>\n'
        "</div>"
    )


def select(options, selected=None):
    opts = []
    for o in options:
        sel = " selected" if o == selected else ""
        opts.append(f'    <option{sel}>{o}</option>')
    return (
        '<div class="select">\n'
        '  <select class="select__native">\n'
        + "\n".join(opts)
        + "\n  </select>\n"
        '  <i class="fa-solid fa-chevron-down select__caret" aria-hidden="true"></i>\n'
        "</div>"
    )


def typeahead(placeholder="Select an Option"):
    """Custom single-value typeahead control."""
    return (
        '<div class="combo" data-combo="typeahead">\n'
        '  <div class="combo__field">\n'
        f'    <input type="text" class="combo__input" placeholder="{placeholder}"'
        ' role="combobox" aria-expanded="false" aria-autocomplete="list">\n'
        "  </div>\n"
        '  <i class="fa-solid fa-caret-down combo__caret" aria-hidden="true"></i>\n'
        "</div>"
    )


def multiselect(chips, placeholder=""):
    """Custom multi-value control: chips plus a typeahead input."""
    chip_html = "\n".join(
        '    <span class="chip">{0}'
        '<button type="button" class="chip__menu" aria-label="Options for {0}">'
        '<i class="fa-solid fa-caret-down" aria-hidden="true"></i></button></span>'.format(c)
        for c in chips
    )
    return (
        '<div class="combo" data-combo="multiselect">\n'
        '  <div class="combo__field">\n'
        + (chip_html + "\n" if chip_html else "")
        + f'    <input type="text" class="combo__input" placeholder="{placeholder}"'
        ' role="combobox" aria-expanded="false" aria-autocomplete="list">\n'
        "  </div>\n"
        '  <i class="fa-solid fa-caret-down combo__caret" aria-hidden="true"></i>\n'
        "</div>"
    )


def search_bar(placeholder, action_label=None, icon="fa-plus"):
    action = ""
    if action_label:
        action = (
            f'\n  <button type="button" class="btn btn--success">'
            f'<i class="fa-solid {icon}" aria-hidden="true"></i> {action_label}</button>'
        )
    return (
        '<div class="search-bar">\n'
        f'  <label class="u-sr-only" for="q">{placeholder}</label>\n'
        f'  <input type="search" id="q" class="input" placeholder="{placeholder}">'
        f"{action}\n"
        "</div>"
    )


def pagination():
    return (
        '<nav class="pagination" aria-label="Pagination">\n'
        '  <a class="pagination__item" href="#">First</a>\n'
        '  <a class="pagination__item" href="#" aria-label="Previous">'
        '<i class="fa-solid fa-angle-left" aria-hidden="true"></i></a>\n'
        '  <a class="pagination__item is-active" href="#" aria-current="page">1</a>\n'
        '  <a class="pagination__item" href="#" aria-label="Next">'
        '<i class="fa-solid fa-angle-right" aria-hidden="true"></i></a>\n'
        '  <a class="pagination__item" href="#">Last</a>\n'
        "</nav>"
    )


ROW_ACTIONS = (
    '<div class="table__actions">\n'
    '  <button type="button" class="btn btn--sm">Edit</button>\n'
    '  <button type="button" class="btn btn--sm btn--danger">Delete</button>\n'
    '  <button type="button" class="btn btn--sm btn--warning">Copy</button>\n'
    "</div>"
)

EDIT_DELETE = (
    '<div class="table__actions">\n'
    '  <button type="button" class="btn btn--sm">Edit</button>\n'
    '  <button type="button" class="btn btn--sm btn--danger">Delete</button>\n'
    "</div>"
)

CHECK = '<i class="fa-solid fa-square-check table__check" aria-label="Yes"></i>'


# ------------------------------------------------------------- 1. General ----

GENERAL_LEFT = "\n".join([
    field("Project Name:", text_input("David Fai")),
    field("Project Description:", '<textarea class="textarea">Mosby HR Training - Graffco</textarea>'),
    '<div class="field">\n'
    '  <span class="field__label">Project Owner:</span>\n'
    '  <div class="entity">\n'
    "    <span>Cleveland Menu Test Account</span>\n"
    '    <button type="button" class="entity__clear" data-clear-entity'
    ' aria-label="Clear project owner">'
    '<i class="fa-solid fa-xmark" aria-hidden="true"></i></button>\n'
    "  </div>\n"
    "</div>",
    field("Sub Project Label:", text_input("Layout")),
    field("Open Date:", date_field("09/14/2026")),
    field("Project Effective Date:", date_field("09/14/2026", disabled=True)),
    field("Close Date:", date_field("11/27/2999")),
])

GENERAL_MID = "\n".join([
    choice_group([
        checkbox("Is Data Collection Project", True),
        checkbox("Enable Background Image Import", True),
        checkbox("Print Comparison Report on Job Ticket", True),
    ]),
    choice_group([
        checkbox("Hide Default Menus"),
        checkbox("Allow Menu Templates"),
        checkbox("Hide Default Menu if Template Assigned"),
    ]),
    choice_group([
        checkbox("Error on 99.99 Prices", True),
        checkbox("Error on '###' Text", True),
        checkbox("Enforce Section Content Type"),
        checkbox("Allow Users To Submit Menus With Broken Rules"),
        checkbox("Images Count In Rule By Default"),
    ]),
])

GENERAL_RIGHT = "\n".join([
    choice_group([
        checkbox("Hide Edit Format Tab"),
        checkbox("Hide Library Tab"),
        checkbox("Hide Pages Pane Option"),
    ]),
    choice_group([
        checkbox("Hide Advanced Tools"),
        checkbox("Hide Cost Calculator"),
        checkbox("Hide Feature Selector"),
        checkbox("Hide Price Tier Selector"),
    ]),
    choice_group([
        checkbox("Hide Menu Eyeball Icon"),
        checkbox("Enable Hiding Calories"),
        checkbox("Enable Hiding Prices"),
    ]),
    choice_group([
        checkbox("CMP Approval"),
        checkbox("Disable Mobile Menu Section Collapse"),
        checkbox("Show Existing Menus on Product Details"),
    ]),
])

GENERAL = f"""
<section class="well">
  <div class="grid grid--3">

    <div class="stack">
{indent(GENERAL_LEFT, 6)}
    </div>

    <div>
{indent(GENERAL_MID, 6)}
    </div>

    <div>
{indent(GENERAL_RIGHT, 6)}
    </div>

    <div class="grid__divider"></div>

    <div class="stack">
{indent(field("Development Status:", select(["", "In Development", "Approved", "Archived"])), 6)}
{indent(field("Default Item Sync Type:", select(["None", "Sync", "Sync and Overwrite"], "None")), 6)}
    </div>

    <div class="stack">
{indent(field("Rendering Display Title:", text_input()), 6)}
{indent(field("Rendering Sync Type:", select(["Sync", "None", "Manual"], "Sync")), 6)}
    </div>

    <div class="stack">
{indent(field("High Res Hi Up Count:", text_input()), 6)}
{indent(field("Publish Online Type:", text_input()), 6)}
    </div>

  </div>
</section>
"""


# ---------------------------------------------------------- 2. Renderings ----

SKIN_ROW = (
    '<div class="row">\n'
    f'{indent(text_input(), 2)}\n'
    f'{indent(text_input(), 2)}\n'
    '  <button type="button" class="btn btn--sm" aria-label="Remove skin">'
    '<i class="fa-regular fa-trash-can" aria-hidden="true"></i></button>\n'
    "</div>"
)

RENDERINGS = f"""
<section class="well">
  <div class="grid grid--2">

    <div class="stack stack--lg">
{indent(field("Name", text_input()), 6)}

      <div class="stack stack--sm">
        <h2 class="section-title">CSS</h2>
        <div class="row">
          <div class="field u-grow">
            <span class="field__label">File Name</span>
{indent(text_input(), 12)}
          </div>
          <button type="button" class="btn btn--info u-mt-4">
            <i class="fa-solid fa-pencil" aria-hidden="true"></i> Edit File
          </button>
          <button type="button" class="btn btn--success u-mt-4">
            <i class="fa-solid fa-plus" aria-hidden="true"></i> Add File
          </button>
        </div>
      </div>

      <div class="stack stack--sm">
        <h2 class="section-title">Autospacing</h2>
{indent(choice_group([
    radio("Manual", "autospacing", True),
    radio("Automatic", "autospacing"),
    radio("Never", "autospacing"),
]), 8)}
      </div>
    </div>

    <div class="stack stack--lg">
      <div class="stack stack--sm">
        <h2 class="section-title">PDF Rendering Options</h2>
{indent(choice_group([
    radio("Render without Validation Success", "validation", True),
    radio("Render with Validation Success", "validation"),
]), 8)}
      </div>

      <div class="grid grid--2">
{indent(field("Web PDF Quality:", typeahead()), 8)}
{indent(field("Low Res PDF Preset:", typeahead()), 8)}
      </div>

      <div class="row">
        <div class="field u-grow">
          <span class="field__label">High Res PDF Preset:</span>
{indent(typeahead(), 10)}
        </div>
        <button type="button" class="btn btn--info u-mt-4">
          <i class="fa-solid fa-pencil" aria-hidden="true"></i> Edit
        </button>
      </div>
    </div>

    <div class="grid__divider"></div>

    <div class="stack">
      <div class="row row--between">
        <h2 class="section-title">Dimensions</h2>
        <div class="u-w-sm">
{indent(typeahead("Select to Add Dimensions"), 10)}
        </div>
      </div>

      <div class="dimensions">
        <div class="preset-list">
          <button type="button" class="preset">
            <span>Print</span>
            <span class="preset__remove" aria-hidden="true">
              <i class="fa-solid fa-xmark"></i>
            </span>
          </button>
          <button type="button" class="preset is-active">Print</button>
          <button type="button" class="preset">Print Preview</button>
        </div>

        <div class="measure-grid">
          <span class="text-sm text-muted"></span>
          <span class="field__label">Measurement</span>
          <span class="field__label">Unit</span>

          <span class="measure-grid__label">Width</span>
{indent(text_input(), 10)}
{indent(select(["points", "inches", "millimeters"], "points"), 10)}

          <span class="measure-grid__label">Height</span>
{indent(text_input(), 10)}
{indent(select(["points", "inches", "millimeters"], "points"), 10)}

          <span class="measure-grid__label">DPI</span>
{indent(text_input(), 10)}
{indent(select(["points", "inches", "millimeters"], "points"), 10)}
        </div>
      </div>
    </div>

    <div class="stack">
      <div class="row row--between">
        <h2 class="section-title">Skins</h2>
        <button type="button" class="btn btn--success">
          <i class="fa-solid fa-plus" aria-hidden="true"></i> Add Skin
        </button>
      </div>

      <div class="stack stack--sm">
        <div class="row">
          <span class="field__label u-grow">Name</span>
          <span class="field__label u-grow">Description</span>
          <span class="u-w-btn"></span>
        </div>
{indent(SKIN_ROW, 8)}
{indent(SKIN_ROW, 8)}
      </div>
    </div>

  </div>
</section>
"""


# ------------------------------------------------------------- 3. Library ----

LIBRARY_ROW = (
    "<tr>\n"
    "  <td>Cleveland Menu Test Food</td>\n"
    "  <td>Healey</td>\n"
    '  <td class="col-actions"><div class="table__actions">'
    '<button type="button" class="btn btn--sm btn--danger">Delete</button>'
    "</div></td>\n"
    "</tr>"
)

LIBRARY = f"""
<section class="well">
  <div class="grid grid--2">

    <div class="stack">
{indent(field("Allowable Libraries", multiselect(["Cleveland Menu Test Food", "Cleveland Menu Test Images"])), 6)}
{indent(field("Library Linking", select(["Always", "Never", "On Import"], "Always")), 6)}
    </div>

    <div class="stack stack--sm">
      <span class="field__label">Allowable Items</span>
{indent(choice_group([
    checkbox("Allow unapproved menu items."),
    checkbox("User can create new items."),
    checkbox("User can create new sizes."),
]), 6)}
    </div>

  </div>
</section>

<section class="well">
  <div class="stack">
    <h2 class="section-title">Available Library Categories</h2>

    <div class="row">
      <div class="field u-grow">
        <span class="field__label">Select a Library</span>
{indent(typeahead(), 8)}
      </div>
      <div class="field u-grow">
        <span class="field__label">Select a Catalog</span>
{indent(typeahead(), 8)}
      </div>
      <button type="button" class="btn btn--success u-mt-4">
        <i class="fa-solid fa-plus" aria-hidden="true"></i> Add
      </button>
    </div>

    <table class="table">
      <thead>
        <tr>
          <th>Library Name</th>
          <th>Category Name</th>
          <th class="col-actions"><span class="u-sr-only">Actions</span></th>
        </tr>
      </thead>
      <tbody>
{indent(LIBRARY_ROW, 8)}
{indent(LIBRARY_ROW, 8)}
      </tbody>
    </table>
  </div>
</section>
"""


# ---------------------------------------------------------------- 4. Data ----

def icon_row(color):
    return (
        "<tr>\n"
        "  <td>0</td>\n"
        "  <td>Favorite Blue</td>\n"
        "  <td></td>\n"
        "  <td>Set By Library (Optional)</td>\n"
        f'  <td><span class="swatch" style="background:{color}"></span></td>\n'
        "  <td>Icon 1</td>\n"
        f'  <td class="col-actions">{ROW_ACTIONS}</td>\n'
        "</tr>"
    )


DATA = f"""
<section class="well">
  <div class="stack">
{indent(search_bar("Search Icons"), 4)}

    <div class="row row--between">
      <h2 class="section-title">Project Icons</h2>
      <button type="button" class="btn btn--success">
        <i class="fa-solid fa-plus" aria-hidden="true"></i> Add Icon
      </button>
    </div>

    <table class="table">
      <thead>
        <tr>
          <th class="col-narrow">Order</th>
          <th>Name</th>
          <th>Org Icon Name</th>
          <th>Icon Usage</th>
          <th class="col-narrow">Icon</th>
          <th>Field Group</th>
          <th class="col-actions"><span class="u-sr-only">Actions</span></th>
        </tr>
      </thead>
      <tbody>
{indent(icon_row("#ee5a5a"), 8)}
{indent(icon_row("#5ec8ef"), 8)}
      </tbody>
    </table>

{indent(pagination(), 4)}
  </div>
</section>
"""


# ----------------------------------------------------------- 5. Templates ----

def template_row(name):
    return (
        "<tr>\n"
        f"  <td>{name}</td>\n"
        f"  <td>{name}</td>\n"
        "  <td>1</td>\n"
        "  <td>Library Item</td>\n"
        f'  <td class="col-actions">{ROW_ACTIONS}</td>\n'
        "</tr>"
    )


TEMPLATES = f"""
<section class="well">
  <div class="stack">
{indent(search_bar("Search Templates", "Add Template"), 4)}

    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Description</th>
          <th>Item Group Count</th>
          <th>Template Type</th>
          <th class="col-actions"><span class="u-sr-only">Actions</span></th>
        </tr>
      </thead>
      <tbody>
{indent(template_row("Standard"), 8)}
{indent(template_row("Header Line Right"), 8)}
      </tbody>
    </table>

{indent(pagination(), 4)}
  </div>
</section>
"""


# ---------------------------------------------------- 6. Default Modifiers ----

def modifier_card(chips):
    return f"""<div class="card">
  <div class="grid grid--4">
{indent(field("Template", typeahead()), 4)}
{indent(field("Match Type", typeahead()), 4)}
{indent(field("Match Field", typeahead()), 4)}
    <div class="row">
      <div class="field u-grow">
        <span class="field__label">Base</span>
{indent(typeahead(), 8)}
      </div>
      <button type="button" class="btn btn--danger u-mt-4">Delete</button>
    </div>
  </div>

  <div class="field u-mt-3">
    <span class="field__label">Modifiers</span>
{indent(multiselect(chips), 4)}
  </div>
</div>"""


DEFAULT_MODIFIERS = f"""
<section class="well">
  <div class="stack">
{indent(search_bar("Search Default Modifiers", "Add Default"), 4)}
{indent(modifier_card(["1 cup", "Cleveland Menu Test Images"]), 4)}
{indent(modifier_card(["Cleveland Menu Test Food", "Cleveland Menu Test Images"]), 4)}
  </div>
</section>
"""


# -------------------------------------------------------------- 7. Styles ----

def style_row(name, digital):
    return (
        "<tr>\n"
        f"  <td>{name}</td>\n"
        f"  <td>{name}</td>\n"
        '  <td><span class="table__thumb">'
        '<i class="fa-regular fa-image" aria-label="Style preview"></i></span></td>\n'
        f"  <td>{CHECK}</td>\n"
        f"  <td>{CHECK if digital else ''}</td>\n"
        f"  <td>{'' if digital else CHECK}</td>\n"
        f'  <td class="col-actions">{EDIT_DELETE}</td>\n'
        "</tr>"
    )


STYLES = f"""
<section class="well">
  <div class="stack">
{indent(search_bar("Search Styles", "Add Style"), 4)}

    <table class="table">
      <thead>
        <tr>
          <th>Style Name</th>
          <th>Rendering Name</th>
          <th>Style Preview</th>
          <th class="col-narrow">Print</th>
          <th class="col-narrow">Digital</th>
          <th class="col-narrow">Default</th>
          <th class="col-actions"><span class="u-sr-only">Actions</span></th>
        </tr>
      </thead>
      <tbody>
{indent(style_row("Limited", False), 8)}
{indent(style_row("Full", True), 8)}
      </tbody>
    </table>

{indent(pagination(), 4)}
  </div>
</section>
"""


# ------------------------------------------------- 8a. Configuration/Access ---

def access_card(applies, more, editors, viewers, approvers, tier, style, override):
    def people(items):
        return "\n".join(f"      <li>{i}</li>" for i in items)

    return f"""<div class="card">
  <div class="card__header">
    <div>
      <span class="field__label">Applies To</span>
      <p class="u-mt-0 u-mb-3 text-sm">{applies} <a href="#">+{more} more</a></p>
    </div>
{indent(EDIT_DELETE, 4)}
  </div>

  <div class="grid grid--2">
    <div class="stack stack--sm">
      <span class="field__label">Editors</span>
      <ul class="people">
{people(editors)}
      </ul>
      <span class="field__label">Viewers</span>
      <ul class="people">
{people(viewers)}
      </ul>
      <span class="field__label">Approvers</span>
      <ul class="people">
{people(approvers)}
      </ul>
    </div>

    <div class="stack stack--sm">
      <span class="field__label">Settings</span>
      <dl class="spec">
        <div class="spec__row">
          <dt>Default Price Tier</dt><dd class="spec__value">{tier}</dd>
        </div>
        <div class="spec__row">
          <dt>Default Style</dt><dd class="spec__value">{style}</dd>
        </div>
        <div class="spec__row">
          <dt>Allow Price Override</dt><dd class="spec__value">{override}</dd>
        </div>
      </dl>
    </div>
  </div>
</div>"""


CONFIG_ACCESS = f"""
<section class="well">
  <div class="stack">
{indent(search_bar("Search Access Rules", "Add Access Rule"), 4)}

    <div class="grid grid--2">
{indent(access_card(
    "Omni Nashville, Omni Austin, Omni Charlotte,", 3,
    ["Jane Smith", "Mike Chen"],
    ["Sarah Lee, Tom Park, Ana Cruz"],
    ['David Kim <span class="badge">Regional</span>',
     'Lisa Wong <span class="badge">GM</span>'],
    "Tier 2", "Standard", "Yes"), 6)}
{indent(access_card(
    "Omni Cancun, Omni Amelia Island, Omni Bar Harbour,", 5,
    ["Rachel Torres", "Brandon Liu", "Kenji Patel"],
    ["Mia Johansson"],
    ['Carlos Mendez <span class="badge">RFC</span>',
     'Nina Okafor <span class="badge">GM</span>'],
    "Tier 1", "Premium", "No"), 6)}
    </div>

{indent(pagination(), 4)}
  </div>
</section>
"""


# ----------------------------------------------- 8b. Configuration/Approval ---

def contact(name, email):
    return (
        '<div class="contact">\n'
        f'  <span class="contact__name">{name}</span>\n'
        f'  <span class="contact__email">{email}</span>\n'
        '  <button type="button" class="btn btn--sm btn--danger">Delete</button>\n'
        "</div>"
    )


CONFIG_APPROVAL = f"""
<section class="well">
  <div class="grid grid--2">

    <div class="stack">
{indent(choice_group([
    checkbox("Allow Organization Administrators Admin Access when Viewing"),
]), 6)}
{indent(choice_group([
    checkbox("This Project Does NOT Require Approval"),
    checkbox("This Project Requires GM Approval (Set at Customer Level)"),
    checkbox("This Project Requires Corporate Approval"),
]), 6)}
{indent(choice_group([
    checkbox("This Project Requires Regional Approval (Set at Customer Level)"),
    checkbox("This Project Requires Regional Approval (Set at Customer Level)"),
    checkbox("Regional Approvers Can Edit"),
    checkbox("Allow Regional Approvers Admin Access when Reviewing"),
]), 6)}

      <div class="field u-w-md">
        <span class="field__label">Hours before Auto-approving Regional Approvals</span>
{indent(text_input(), 8)}
      </div>
    </div>

    <div class="stack stack--lg">
      <div class="stack stack--sm">
        <h2 class="section-title">Corporate View Access to All Menus</h2>
{indent(search_bar("Search Corporate Contacts", "Add"), 8)}
        <div class="contact-list">
{indent(contact("Matt Seller", "mattseiler@remingtonhotels.com"), 10)}
{indent(contact("Another Person", "anotherperson@remingtonhotels.com"), 10)}
        </div>
      </div>

      <div class="stack stack--sm">
        <h2 class="section-title">CC Users on Emails</h2>
        <div class="field field--inline">
          <span class="field__label">CC On Order Receipt</span>
{indent(text_input(), 10)}
        </div>
        <div class="field field--inline">
          <span class="field__label">CC On Approval Email</span>
{indent(text_input(), 10)}
        </div>
        <div class="field field--inline">
          <span class="field__label">CC On Denial Email</span>
{indent(text_input(), 10)}
        </div>
      </div>
    </div>

  </div>
</section>
"""


# ------------------------------------------------------------------ build ----

RENDERING_SUBTABS = [("renderings.html", "Default"), ("#", "+ Rendering")]
CONFIG_SUBTABS = [("configuration.html", "Access"),
                  ("configuration-approval.html", "Approval")]

PAGES = [
    ("index.html",                  "index.html",          "General Info",  GENERAL,          [], None),
    ("renderings.html",             "renderings.html",     "Renderings",    RENDERINGS,       RENDERING_SUBTABS, "Default"),
    ("library.html",                "library.html",        "Library",       LIBRARY,          [], None),
    ("data.html",                   "data.html",           "Data",          DATA,             [], None),
    ("templates.html",              "templates.html",      "Templates",     TEMPLATES,        [], None),
    ("default-modifiers.html",      "default-modifiers.html", "Default Modifiers", DEFAULT_MODIFIERS, [], None),
    ("styles.html",                 "styles.html",         "Styles",        STYLES,           [], None),
    ("configuration.html",          "configuration.html",  "Configuration", CONFIG_ACCESS,    CONFIG_SUBTABS, "Access"),
    ("configuration-approval.html", "configuration.html",  "Configuration", CONFIG_APPROVAL,  CONFIG_SUBTABS, "Approval"),
]

for filename, active_tab, title, body, subs, active_sub in PAGES:
    html = SHELL.format(
        title=title,
        tabs=tab_bar(active_tab),
        subtabs=subtab_bar(subs, active_sub),
        body=indent(body, 4),
    )
    (OUT / filename).write_text(html)
    print("wrote", filename)
