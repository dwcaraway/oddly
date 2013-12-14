Feature: The dataset resources

  Background:
    Given podserve is running

  Scenario: All endpoints are discoverable from /
    When I get '/'
    Then the response should link to 'ep:organization'
    And the response should link to 'ep:user'
    And the response should link to 'ep:dataset'
    And the response should link to 'ep:schema'
