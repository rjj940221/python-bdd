Feature: Calls out to the protected section of the api for open orders

  Scenario:
    Given valid api keys
    And a valid 2FA key
    And a valid nonce
    When account open orders are requested with a singed request
    Then a valid JSON response is returned
    And the response has no error messages
    And the response has 0 or more orders

  Scenario:
    Given valid api keys
    And a valid 2FA key
    And a valid nonce
    And account open orders are requested with a singed request
    When the request is repeated
    Then a valid JSON response is returned
    And the response has the error messages "EAPI:Invalid nonce"
  
  Scenario:
    Given valid api keys
    And a valid nonce
    And a random 2FA key
    When account open orders are requested with a singed request
    Then a valid JSON response is returned
    And the response has the error messages "EAPI:Invalid signature"

  Scenario:
    Given random api keys
    And a valid nonce
    And a valid 2FA key
    When account open orders are requested with a singed request
    Then a valid JSON response is returned
    And the response has the error messages "EAPI:Invalid key"

  Scenario:
    Given a random api public keys
    And a valid api private keys
    And a valid nonce
    And a valid 2FA key
    When account open orders are requested with a singed request
    Then a valid JSON response is returned
    And the response has the error messages "EAPI:Invalid key"

  Scenario:
    Given a random api private keys
    And a valid api public keys
    And a valid nonce
    And a valid 2FA key
    When account open orders are requested with a singed request
    Then a valid JSON response is returned
    And the response has the error messages "EAPI:Invalid key"

  Scenario:
    When account open orders are requested
    Then a valid JSON response is returned
    And the response has the error messages "EAPI:Invalid key"