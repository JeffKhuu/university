/// This functions includes the lectures with number min to max
/// from the given path
///
/// - min (int): First lecture to include
/// - max (int): Last lecture to include
/// - path (str): Path to lecture files
/// -> content
#let include_n(min, max, path) = [
  #assert(min <= max, message: "Cannot find lectures in given range, min greater than max.")
  #let n = min
  #while n <= max {
    include path + "lec_" + str(n) + ".typ"
    n += 1
  }
]

#let min = int(sys.inputs.at("min", default: 1))
#let max = int(sys.inputs.at("max", default: 1))
#let path = sys.inputs.at("path", default: "/test-1/fall-2030/stat151/")
#let info = yaml(path + "/info.yaml")

#line(length: 100%)
#block()[
  #pad(y: 2em)[
    #title(info.at("title"))
    #emph(text(size: 24pt)[#info.at("designator") #info.at("code")])
  ]
]
#line(length: 100%)
#v(1fr)
#text(size: 14pt)[#datetime.today().display()]

#pagebreak()
// #show outline.entry.where(element: ): set block(above: 1.2em)
#outline()
#pagebreak()

#include_n(min, max, path)
