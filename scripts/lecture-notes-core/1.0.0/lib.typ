// Templating

/// Document template used for styling lecture notes.
/// Examples:
///   show: doc => template(0, "Introduction", "MATH 144", datetime(year: 2025, month: 9, day: 1), doc)
///
/// - lec_num (int): Number of lecture since beginning
/// - lec_title (str): Title of lecture
/// - course_code (str): Code for the course in the format "[DESIGNATOR] [CODE]" ex. "MATH 144"
/// - creation_date (datetime): Date of creation of the lecture note
/// - doc (content): Content of the document
/// -> content
#let template(
  lec_num,
  lec_title,
  course_code,
  creation_date,
  doc,
) = [
  // Document Settings
  #set document(
    title: lec_title,
  )
  // Text Styling
  #set text(
    font: "New Computer Modern",
  )

  // Page Styling
  #set page(
    header: [
      #text(weight: "black")[ Lecture #lec_num: #lec_title ]
      #h(1fr)
      #emph(course_code)
      #line(length: 100%)
    ],
    numbering: "1",
  )

  // Heading Styling
  #set heading(
    numbering: (..nums) => [#lec_num.#numbering("1.1", ..nums)],
  )

  // Table Styling
  #set table(
    inset: 10pt,
    align: horizon,
  )

  #metadata(lec_num)<start_note> // Label for convenient selecting

  // Labels for metadata querying
  #metadata(lec_title)<title>
  #metadata(creation_date.display())<creation_date>

  // Display all content reminders at the top of the document
  #context {
    let reminders = query(selector(<reminder>).after(here()).before(selector(<end_note>).after(here())))
    if reminders.len() != 0 {
      pad(x: 16pt, bottom: 8pt)[
        *Reminders:*
        #for reminder in reminders {
          [- #reminder.body (Page #reminder.location().page())]
        }
      ]
    }
  }

  #doc
  #counter(heading).update(0)
  #metadata(lec_num)<end_note> // Label for convenient selecting
]

// Colors
#let clr_theorem = rgb("ca9ee6")
#let clr_proof = rgb("74c7ec")
#let clr_reminder = rgb("cba6f7")
#let clr_definition = rgb("89b4fa")
#let clr_example = rgb("f38ba8")
#let clr_solution = rgb("a6e3a1")

// Snippets
/// Highlights given content with purple highlight and a <reminder> label
///
/// - content (content):
/// -> content
#let reminder(content) = [
  #highlight(radius: 2pt, fill: clr_reminder, extent: 2pt)[#content]<reminder>
]

/// Places a block with given content and name as a title with fill
/// of given color. Can be used to create definition, theorem, or example
/// blocks
///
/// - content (content):
/// - name (str):
/// - color (color):
/// ->
#let container(content, name: "", color: clr_theorem) = [
  #block(
    fill: color.lighten(90%),
    radius: 8pt,
    stroke: 2pt + color,
    width: 100%,
    pad(rest: 10pt, [
      #if name != "" [#text(fill: color)[*#name*]]

      #content
    ]),
  )
]

/// Definition Container
#let defn(content) = container(content, name: "Definition", color: clr_definition)
/// Theorem Container
#let thrm(content) = container(content, name: "Theorem", color: clr_theorem)
/// Proof Container
#let proof(content) = container(content, name: "Proof", color: clr_proof)
/// Example Container
#let exmp(content) = container(content, name: "Example", color: clr_example)
/// Solution Container
#let sltn(content) = container(content, name: "Solution", color: clr_solution)

/// Wrap the given content in integral evaluation bars.
///
/// - content (content): Expression to be "evaluated"
/// - lower (content): Lower bound of integral expression
/// - upper (content): Upper bound of integral expression
/// -> content
#let evalbar(content, lower, upper) = [
  $lr((#content )|)^upper_lower$
]
