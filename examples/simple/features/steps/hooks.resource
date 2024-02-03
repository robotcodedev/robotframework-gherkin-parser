*** Keywords ***
before_test
    [Arguments]    ${context}=    ${test}=
    [Tags]    hook:before-test
    Log    before test
    Fail    har har test

before_suite
    [Arguments]    ${context}=    ${suite}=
    [Tags]    hook:before-suite
    Log    hook before suite
    #Fail    hahar suite

before_keyword
    [Arguments]    ${context}=    ${suite}=
    [Tags]    hook:before-keyword
    Log    before keyword
    Fail    blah
    RETURN    after_keyword

after_keyword
    [Arguments]    ${context}=    ${suite}=
    [Tags]    hook:after-step
    Log    after step

before_tag
    [Arguments]    ${context}=    ${suite}=
    [Tags]    hook:before-tag
    Log    before suite


start_browser
    [Arguments]    ${context}=    ${suite}=
    [Tags]    hook:before-tag:browser
    Log    before suite
