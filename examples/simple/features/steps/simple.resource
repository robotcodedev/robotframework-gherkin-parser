*** Settings ***
Library     step_impls.py


*** Keywords ***
the minimalism
    Log    yeah

Table with example
    [Tags]    gherkin:step
    [Arguments]    ${rows}

    FOR    ${index}    ${row}    IN ENUMERATE    @{rows}
        Log    ${index} ${{", ".join((c["value"] for c in $row["cells"]))}}
    END

    FOR    ${row}    IN    @{rows}
        FOR    ${cell}    IN    @{row}[cells]
            Log    ${cell["value"]}
        END
    END

a blog post named "${name}" with Markdown body
    [Tags]    gherkin:step
    [Arguments]    ${body}

    Log    ${name}
    Log    ${body}

this file:
    [Tags]    gerkin:step
    [Arguments]    ${content}    ${mediaType}=

    Log    ${content}
    Log    ${mediaType}
