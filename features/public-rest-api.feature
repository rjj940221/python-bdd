Feature: Calls out to the public section of the api 

  Scenario: check that the server time and local time are in a margin of error
    When the server time is requested
    Then a valid JSON response is returned
    And the response is not cached
    And the response has no error messages
    And the system time is in a margin of 1 sec
    And the unixtime field corresponds with the rfc1123
  
  Scenario: Get the market info for a trading pair
    When the asset pair "XXBTZUSD" is requested
    Then a valid JSON response is returned
    And the response has no error messages
    And the the response has a "XXBTZUSD" section
    And the the response "XXBTZUSD" section is valid

