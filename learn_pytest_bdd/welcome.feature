Feature: Welcome Page Form

  Background:
    Given the user is on the Welcome page

  Scenario: Page renders correctly
    Then the page title should be "Welcome"
    And the subtitle should be "Fill in the details below to continue"
    And the "Full name" input field is visible
    And the "Email address" input field is visible
    And the "Submit" button is visible
    And the "Cancel" button is visible

  Scenario: Submit navigates to the dashboard with a personalised message
    When the user enters "Jane Smith" in the "Full name" field
    And the user enters "jane@example.com" in the "Email address" field
    And the user clicks the "Submit" button
    Then the user should be on the Dashboard page
    And the welcome message should be "Welcome, Jane Smith! Choose an option below to get started."

  Scenario: Submit without a name shows a generic welcome message
    When the user enters "" in the "Full name" field
    And the user enters "jane@example.com" in the "Email address" field
    And the user clicks the "Submit" button
    Then the user should be on the Dashboard page
    And the welcome message should be "Welcome! Choose an option below to get started."

  Scenario: Cancel clears the form fields
    When the user enters "Jane Smith" in the "Full name" field
    And the user enters "jane@example.com" in the "Email address" field
    And the user clicks the "Cancel" button
    Then the "Full name" field should be empty
    And the "Email address" field should be empty
    And the user should remain on the Welcome page

  Scenario: Cancel does not navigate away
    When the user clicks the "Cancel" button
    Then the user should remain on the Welcome page
    And the "Submit" button is visible
