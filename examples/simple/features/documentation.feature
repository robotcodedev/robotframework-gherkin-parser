Feature: Scenario Outline with a docstring
This is a documentation for the feature file.

it can be more than one line long.

  Scenario Outline: Greetings come in many forms
    this is the documentation for the scenario

    it can be more than one line long.

    and it can contain <placeholder> that will be replaced by the examples.

    Given this file:
      """<type>
      Greeting:<content>
      """

    Examples:
      | type | content |
      | en   | Hello   |
      | fr   | Bonjour |
