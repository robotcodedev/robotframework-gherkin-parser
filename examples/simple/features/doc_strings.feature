Feature: Parser Should Support DocStrings

  Scenario: A scenario with a docstring
    Given a blog post named "Random" with Markdown body
      """
      Some Title, Eh?
      ===============
      Here is the first paragraph of my blog post. Lorem ipsum dolor sit amet,
      consectetur adipiscing elit.
      """

  Scenario: A scenario with a docstring and multiple whitespace and vars
    Given a blog post named "Random" with Markdown body
      """
      😂🚲🚓
      (❁´◡`❁)
      (*/ω＼*)
      (^///^)
      this text contains     spaces
      and ${TEST NAME}
      """

  Scenario: A scenario with a backtick in the docstring
    Given a blog post named "Random" with Markdown body
      ```python
      😂🚲🚓
      (❁´◡`❁)
      (*/ω＼*)
      (^///^)
      this text contains     spaces
      and ${TEST NAME}
      ```
