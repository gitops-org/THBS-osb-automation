@ignore
Feature: oauth 2 test using
    http://brentertainment.com/oauth2

Background:
Given url 'http://brentertainment.com/oauth2/lockdin'

Scenario: oauth 2 flow

Given path 'token'
And  form field grant_type = 'password'
And  form field client_id = 'demoapp'
And  form field client_secret = 'demopass'
And  form field username = 'demouser'
And  form field password = 'testpass'
And  method post
And  status 200
And print response
And  def accessToken = response.access_token

#Given path 'resource'
#And header Authorization = 'Bearer ' + accessToken
# * param access_token = accessToken
#And method get
#And status 200