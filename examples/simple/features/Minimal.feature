@browser
Feature: Minimal

  @minimal
  Scenario: minimalistic
    Given the minimalism

  @maximal
  Scenario: another one
    Given do something in the maximal way

  @another @slow
  Scenario: another one1
    Given the minimalism

  @browser
  Scenario: the last one
    Given the minimalism

  Scenario Outline: Cucumber Data Table
    Given Table with example
      | FirstName  | <FirstName>  |
      | MiddleName | <MiddleName> |
      | LastName   | <LastName>   |

    Examples:
      | FirstName | MiddleName | LastName |
      | Daniel    | D          | Biehl    |
      | Philip    | K          | Dick     |
