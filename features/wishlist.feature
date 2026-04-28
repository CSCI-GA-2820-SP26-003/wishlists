Feature: Wishlist UI landing page
  As a developer
  I need a BDD environment with behave and Selenium
  So that I can verify the Wishlist UI is reachable and renders expected content

  Scenario: Open the wishlist landing page
    Given the Wishlist service is running
    When I visit the home page
    Then I should see "Wishlist Service is Up"
    And I should see "These are the routes we serve"

  Scenario: Create a wishlist from the web UI
    Given I am on the "Home Page"
    When I set the "wishlist name" to "Gaming Setup"
    And I set the "customer id" to "12345"
    And I set the "wishlist description" to "PC and peripherals"
    And I press the "Create" button
    Then I should see the message "Success"
    And I should see the newly created wishlist details

  Scenario: Create then search for the new wishlist
    Given I am on the "Home Page"
    When I create a wishlist with valid details
    And I press the "Search" button
    Then I should see the new wishlist in the results

  Scenario: Create requires a wishlist name
    Given I am on the "Home Page"
    When I press the "Create" button without entering a wishlist name
    Then I should see an error message indicating the name is required

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

  Scenario: Update a wishlist name from the web UI
    Given I am on the "Home Page"
    And a wishlist exists
    When I retrieve the wishlist by ID
    And I set the "wishlist name" to "Outdoor Essentials"
    And I press the "Update" button
    Then I should see the message "Success"
    And the wishlist name should be updated to "Outdoor Essentials"

  Scenario: Update a wishlist description from the web UI
    Given I am on the "Home Page"
    And a wishlist exists
    When I retrieve the wishlist by ID
    And I set the "wishlist description" to "Updated wishlist description"
    And I press the "Update" button
    Then I should see the message "Success"
    And the wishlist description should be updated to "Updated wishlist description"

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

  Scenario: Make an existing wishlist private from the web UI
    Given I am on the "Home Page"
    And a wishlist exists
    When I retrieve the wishlist by ID
    And I press the "Make Private" button
    Then I should see the message "Success"
    And the wishlist should show a private status

  Scenario: Retrieve wishlist after making it private
    Given I am on the "Home Page"
    And a wishlist exists
    When I make the wishlist private from the web UI
    And I retrieve that wishlist again
    Then I should see that "is_private" is true

  Scenario: Make Private without a valid wishlist ID
    Given I am on the "Home Page"
    When I press the "Make Private" button
    Then I should see an error message indicating the wishlist ID is required or invalid

  Scenario: Make Private for a wishlist that does not exist
    Given I am on the "Home Page"
    When I enter a wishlist ID that does not exist
    And I press the "Make Private" button
    Then I should see an error message indicating the wishlist was not found
