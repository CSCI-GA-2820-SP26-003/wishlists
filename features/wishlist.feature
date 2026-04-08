Feature: Wishlist UI landing page
  As a developer
  I need a BDD environment with behave and Selenium
  So that I can verify the Wishlist UI is reachable and renders expected content

  Scenario: Open the wishlist landing page
    Given the Wishlist service is running
    When I visit the home page
    Then I should see "Wishlist Service is Up"
    And I should see "These are the routes we serve"

  Scenario: Retrieve a wishlist by ID from the web UI
    Given I am on the "Home Page"
    And a wishlist exists
    When I retrieve the wishlist by ID
    Then I should see the wishlist details
    And I should see the correct wishlist information

  Scenario: Retrieve with an invalid wishlist ID format
    Given I am on the "Home Page"
    When I set the "wishlist id" to "abc"
    And I press the "Retrieve" button
    Then I should see the message "Wishlist ID must be an integer"

  Scenario: Retrieve a wishlist that does not exist
    Given I am on the "Home Page"
    When I set the "wishlist id" to "0"
    And I press the "Retrieve" button
    Then I should see the message "Wishlist with id '0' not found."

  Scenario: Delete a wishlist by ID from the web UI
    Given I am on the "Home Page"
    And a wishlist exists
    When I delete the wishlist by ID
    Then I should see the message "Success"

  Scenario: Deleted wishlist no longer appears in results
    Given I am on the "Home Page"
    And a wishlist exists
    When I delete the wishlist by ID
    Then I should not see the deleted wishlist in the results

  Scenario: List all wishlists from the web UI
    Given I am on the "Home Page"
    And multiple wishlists exist
    When I press the "Search" button
    Then I should see all wishlists in the results

  Scenario: List returns more than one wishlist in the results
    Given I am on the "Home Page"
    And multiple wishlists exist
    When I search for wishlists
    Then I should see more than one wishlist in the results

  Scenario: Query wishlists by name from the web UI
    Given I am on the "Home Page"
    And multiple wishlists exist
    When I set the "wishlist_name" to "Gaming Setup"
    And I press the "Search" button
    Then I should see "Gaming Setup" in the results
    And I should not see "Travel Gear" in the results