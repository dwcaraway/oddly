Feature: The dataset resources

  Background:
    Given podserve is running

  Scenario: All endpoints are discoverable from /
    When I get '/'
    Then the response should link to '/organizations'
