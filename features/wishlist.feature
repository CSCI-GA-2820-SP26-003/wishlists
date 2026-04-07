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
