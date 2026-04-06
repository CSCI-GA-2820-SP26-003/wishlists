Feature: Wishlist UI landing page
	As a developer
	I need a BDD environment with behave and Selenium
	So that I can verify the Wishlist UI is reachable and renders expected content

	Scenario: Open the wishlist landing page
		Given the Wishlist service is running
		When I visit the home page
		Then I should see "Wishlist Service is Up"
		And I should see "These are the routes we serve"
