# B.C. Design System alignment — deferred work

Companion to the EPIC.engage colour/font alignment work. That change moved the application's
foundational styling onto a local design-token file transcribed from the B.C. Design System, and
upgraded [`@bcgov/bc-sans`](https://www.npmjs.com/package/@bcgov/bc-sans) to v2. This document
records what was deliberately left out, and why, so it can be picked up as separate work.

**Tokens are local, not an npm dependency.** Values live in `met-web/src/styles/designTokens.ts`
(and `_tokens.scss` for the two stylesheets that need them), transcribed from
[`@bcgov/design-tokens`](https://www.npmjs.com/package/@bcgov/design-tokens) v5.0.0 with the upstream
names preserved so the two can be diffed. This was chosen over the package so colours can be tuned
without waiting on an upstream release — the greens in particular are under design review. The
trade-off is that upstream changes no longer arrive automatically; someone has to re-diff against
v5.0.0 periodically.

Hardcoded colour literals in `met-web/src` went from **204 occurrences (91 unique)** to **77**. Every
remaining one is in a file listed below.

Guard command — should only ever return files named in this document:

```
grep -rlE "#[0-9a-fA-F]{3,8}\b" met-web/src --include=*.ts --include=*.tsx
```

## 1. Domain colour palettes — need design input, not a token swap

These are not UI chrome. The B.C. Design System does not define equivalents, so mapping them onto
tokens would be inventing a design rather than aligning to one.

| File | Literals | What it is |
| --- | ---: | --- |
| `met-web/src/models/engagementPhases.tsx` | 26 | The 7-phase project colour system (`#54858D`, `#DA6D65`, `#043673`, `#4D95D0`, `#E7A913`, `#6A54A3`, `#A6BB2E`) plus matching pastel accordion and "learn more" backgrounds. |
| `met-web/src/components/admin/MetMap/index.tsx` | 23 | ArcGIS / maplibre map styling — feature fills, strokes, markers. |
| `met-web/src/components/shared/analytics/constants.ts` | 13 | Categorical chart palette for the recharts dashboards. |
| `met-web/src/components/shared/analytics/charts/SurveyBar/TreemapLabel.tsx` | 2 | Treemap label stroke/fill. |

**Follow-up needed:** the chart palette in particular should get an accessible-contrast pass — a
categorical palette needs to hold up for colour-vision deficiency and against both light backgrounds
and the treemap fills it sits on. That is a design exercise with its own acceptance criteria.

## 2. Phases widget visual language

| File | Literals |
| --- | ---: |
| `met-web/src/components/public/engagement/view/widgets/PhasesWidget/ForumIcon.tsx` | 6 |
| `met-web/src/components/public/engagement/view/widgets/PhasesWidget/IconBox.tsx` | 5 |
| `.../PhasesWidget/PhasesWidgetMobile/PhaseBoxMobile.tsx` | 1 |
| `.../PhasesWidget/PhasesWidgetMobile/EngagementPhaseMobile.tsx` | 1 |

Teal `#458686` / pale cyan `#9BE2DF` / `#F5FCFC`, plus an inline SVG illustration with its own
palette. This is the same visual system as `engagementPhases.tsx` above and should move with it, in
one design decision rather than two.

## 3. Form.io and Bootstrap

`met-web/src/components/shared/form/FormBuilder/formio.scss` and `formio-bootstrap.scss` pull in the
whole of Bootstrap 5, Bootstrap Icons and Font Awesome 4, then override `met-formio` / `@formio/js`
component styles by selector. The font stack in that file now reads from the design-token SCSS
variable, but the colours, spacing and control styling are still Bootstrap's.

Re-theming the form builder means either restyling against formio's own theming hooks or replacing
the dependency. Either is a ticket in its own right, with survey-rendering regression risk that this
change deliberately avoided.

Related: `font-awesome` and `bootstrap-icons` exist in `package.json` **only** for this file — there
are zero `FontAwesomeIcon` or `fa-` references in any `.tsx`. `react-svg` is installed and never
imported at all. Worth dropping.

## 4. MUI `CssBaseline`

The original plan proposed replacing the hand-rolled reset in `met-web/src/App.scss` with MUI's
`CssBaseline`. **Not done.** `App.scss` now reads its font and body colour from design tokens, so the
conflict it was meant to fix (body `#494949` vs theme `#2D2D2D`) is resolved without it.

`CssBaseline` was held back because it applies a global normalize — `box-sizing: border-box` on every
element, body margin and background resets — on top of an app that also loads full Bootstrap CSS
(§3), spans 1,185 raw `<Grid>` usages, and has no visual regression coverage (§6). The upside was
cosmetic; the downside was silent layout shifts nobody would catch. Revisit once §3 and §6 are done.

## 5. Accessibility baseline

Measured across 351 `.tsx` files:

| | Count |
| --- | ---: |
| `aria-*` attributes | 55 |
| `role=` | 8 |
| `tabIndex` | 1 |
| Focus management (`.focus()`, `autoFocus`, `focusVisible`) | 2 |
| Skip links | 0 |
| `alt=` on images | 3 |
| axe / a11y tooling | none |

The alignment work added visible focus rings and validation-state colours via theme
`styleOverrides`, which helps. It does not amount to an accessibility pass. No skip navigation, no
focus management on modals or drawers, no screen-reader-only text utility, and no way to measure any
of it. This deserves its own ticket with WCAG 2.1 AA as the acceptance bar.

## 6. Test coverage for styling

There is no visual, snapshot, or accessibility test coverage, and `jest.config.cjs` maps
`\.(css|scss)$` to a stub — **styles are not exercised by any test**. The 69 existing suites prove
functional behaviour only.

Deliberately not added here, per the agreed approach for this ticket (manual review at supported
breakpoints). If styling is going to keep changing, the highest-value additions are `jest-axe`
against a handful of representative screens, then Playwright screenshots at the supported widths.

## 7. Component duplication

Not styling, but it makes every future restyle land two to five times:

- **~24 bespoke `<Modal>` implementations**, each `<Modal>` + `<Grid sx={{ ...modalStyle }}>`. Only one
  is the shared `NotificationModal`. `<Dialog>` is used zero times.
- **`modalStyle`** (`met-web/src/components/shared/common/Layouts.tsx`) sets `left: '48%'` with a
  `translate(-50%, -50%)`, so **all 24 modals sit 2% left of centre**. One-line fix, but it changes
  every modal at once and wanted its own verification pass.
- **`ActionsDropDown.tsx` exists five times** — under engagement form user management, user management
  listing, user details, survey listing, and engagement listing.
- **`InvalidTokenModal.tsx` exists twice**, verbatim, in the admin and public trees.
- **`Uploader.tsx` exists twice**, under `imageManagement` and `shared/common/FileUpload`.
- The admin widget editors (`admin/engagement/form/EngagementWidgets/*`) and public widget renderers
  (`public/engagement/view/widgets/*`) are parallel implementations of the same seven widgets.
- Dead code: `ModalSubtitle` (0 uses), `BannerWithoutImage` (never rendered).

## 8. Adopting the official component library

`@bcgov/design-system-react-components` (0.8.1) was **not** adopted. It is built on React Aria and is
still pre-1.0; running it beside MUI 5.18 would mean two focus models, two styling systems and a
larger bundle. That is a component-library migration, not colour and font alignment.

If it is ever taken on, note the peer dependency `@bcgov/bc-sans ^2.1.0` — already satisfied by this
change.

## 9. Smaller notes

- `@bcgov/bc-sans` v2 ships a **Light (300)** weight that v1 did not. Nothing uses it yet.
- `met-web/src/styles/designTokens.ts` and `_tokens.scss` hold the same values in two places. Only
  two SCSS variables are duplicated (font family, primary text colour), so a generator would be more
  machinery than the problem deserves — but keep them in step.
- `met-web/index.html` still loads a Font Awesome kit from a CDN, with a `TODO: Remove` comment
  already next to it.
