Feature: Android Detection System
  As a security officer
  I want to ensure that only humans gain access

  Scenario: A human attempts to gain access
    Given An individual reaches the security checkpoint
    And The individual is a human
    When The detection system is activated
    Then The individual should be granted access

  Scenario: An android attempts to gain access
    Given An individual reaches the security checkpoint
    And The individual is an android
    When The detection system is activated
    Then The individual should be denied access
