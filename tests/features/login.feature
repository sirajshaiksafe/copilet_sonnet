Feature: User Authentication
  As a user of the application
  I want to be able to log in
  So that I can access my account

  Background:
    Given the application is running
    And I am on the login page

  @smoke @ui
  Scenario: Successful login with valid credentials
    When I enter "valid@example.com" as email
    And I enter "validPassword123" as password
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see a welcome message with my name

  @ui @negative
  Scenario Outline: Failed login attempts
    When I enter "<email>" as email
    And I enter "<password>" as password
    And I click the login button
    Then I should see an error message "<error_message>"

    Examples:
      | email              | password        | error_message                    |
      | invalid@email      | Password123     | Please enter a valid email      |
      | user@example.com   |                 | Password is required            |
      |                    | somepassword    | Email is required               |
      | wrong@example.com  | wrongpass       | Invalid email or password       |

  @api
  Scenario: Login API validation
    When I send a POST request to "/api/login" with valid credentials
    Then the response status code should be 200
    And the response should contain an authentication token
    And the response should contain the user profile