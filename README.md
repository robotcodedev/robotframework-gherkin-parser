# **Robot Framework Gherkin Parser**: Quick Overview

The **Robot Framework Gherkin Parser** enables seamless integration of Gherkin feature files with the **Robot Framework**, facilitating behavior-driven development (BDD) with ease. This integration not only allows for the flexible execution of Gherkin feature files alongside **Robot Framework** test files but also highlights the complementary strengths of both approaches. Gherkin feature files, with their less technical and more scenario-focused syntax, emphasize the behavioral aspects of what is being tested, rather than the how. In contrast, **Robot Framework** test files tend to be more technical, focusing on the step-by-step implementation of test scenarios through keyword sequences.

Utilizing a slightly modified version of the official [Cucumber Gherkin Parser](https://github.com/cucumber/gherkin), this custom parser implementation ensures the direct execution of Gherkin scenarios within the **Robot Framework** environment. This supports efficient transitions to and from BDD practices, catering to both technical and non-technical stakeholders by bridging the gap between business requirements and technical implementation.

The **Robot Framework Gherkin Parser** simplifies test step implementation, allowing technical testers to implement test steps in the **Robot Framework**'s keyword-driven language. This is particularly beneficial when compared to the traditional BDD approach, which might require complex programming skills for step definitions in languages such as Java or C#. The parser thereby reduces the barrier to BDD test creation and maintenance, making it more accessible.

## Core Features

- **Focus on Behavioral Testing**: Gherkin feature files allow for specifying test scenarios in a less technical, more narrative form, focusing on what needs to be tested rather than how it is to be tested. This complements the more technically oriented **Robot Framework** test files, providing a balanced approach to defining and executing tests.
- **User-Friendly Test Implementation**: Technical testers can easily implement test steps in the **Robot Framework**'s intuitive language, avoiding the complexity of traditional programming languages for BDD step definitions.
- **Efficient Execution and Porting**: Enables direct execution and easy porting of Gherkin feature files, bridging the gap between Gherkin's scenario-focused syntax and the **Robot Framework**'s technical implementation.
- **Seamless Development Environment**: The inclusion of a plugin/extension for [RobotCode](https://robotcode.io) enhances the development and testing process within Visual Studio Code, offering integrated tools tailored for both BDD and automated testing.

Designed for teams leveraging the **Robot Framework** and looking to integrate or enhance their BDD methodology, the **Robot Framework Gherkin Parser** facilitates a comprehensive testing strategy. It encourages a collaborative testing environment by simplifying the creation of BDD tests and improving testing efficiency and flexibility.

Explore the subsequent sections for details on integrating this parser into your testing strategy, optimizing its usage, and contributing to its development.

## Requirements

Only the Parser

* Python 3.8 or above
* Robotframework 7.0 and above

For Support in VSCode

* VSCode version 1.82 and above

## Installation

The **Robot Framework Gherkin Parser** can be installed using the following methods:

- **Pip**: The parser can be installed using pip, the Python package manager. Run the following command to install the parser:

  ```bash
  pip install robotframework-gherkin-parser
  ```

If you are using the [RobotCode](https://marketplace.visualstudio.com/items?itemName=d-biehl.robotcode) extension for VSCode as your IDE, you can install the [**RobotCode GherkinParser Support** extension](https://marketplace.visualstudio.com/items?itemName=d-biehl.robotcode-gherkin) from the VSCode Marketplace.


## Usage

## On command line

To execute `.feature` files using the **Robot Framework Gherkin Parser** on command line, you need to use the `robot` command line option `--parser` to specify the parser to be used. The following command demonstrates how to execute a `.feature` file using the **Robot Framework Gherkin Parser**:

```bash
robot --parser GherkinParser path/to/your/feature/file.feature
```

## IDE

### Visual Studio Code with [RobotCode](https://marketplace.visualstudio.com/items?itemName=d-biehl.robotcode) extension

If the plugin-extension for [**RobotCode GherkinParser Support** extension](https://marketplace.visualstudio.com/items?itemName=d-biehl.robotcode-gherkin) is installed in VSCode

By creating a `robot.toml` file in your project root and adding the following configuration:

```toml
[parsers]
GherkinParser=[]
```

NOT IMPLEMENTED YET: ~~You can enable the GherkinParser by the VSCode Setting: `robotcode.robot.parsers`~~

## Examples

The following example demonstrates a simple Gherkin feature file that can be executed using the **Robot Framework Gherkin Parser**:

Create a folder named `features` in your project root.
Create a file named `calculator.feature` in the folder `features` with the following content:

```gherkin
Feature: Calculator
  As a user
  I want to use a calculator
  So that I can perform basic arithmetic operations

  Scenario: Add two numbers
    Given I have entered 50 into the calculator
    And I have entered 70 into the calculator
    When I press add
    Then the result should be 120 on the screen
```

To execute the `calculator.feature` file using the **Robot Framework Gherkin Parser** on command line, run the following command:

```bash
robot --parser GherkinParser features/calculator.feature
```

If your are using VSCode + RobotCode + RobotCode GherkinParser Support, you can run the test by clicking on the play buttons in the feature file.



## Contributing

TODO
