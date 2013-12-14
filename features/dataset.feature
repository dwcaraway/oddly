Feature: The dataset resources

  Background:
    Given podserve is running

  Scenario: All endpoints are discoverable from /
    When I get the 'root' resource
    Then I should see a link to the 'organization' resource
    And I should see a link to the 'user' resource
    And I should see a link to the 'dataset' resource
    And I should see a link to the 'schema' resource
