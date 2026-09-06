from project_control_summary import get_project_control_summary


PROJECT_ID = 3


result = get_project_control_summary(
    PROJECT_ID
)


print()
print("CONSTRUCTAI PROJECT CONTROL SUMMARY")
print("====================================")


if "error" in result:

    print(result["error"])

else:

    print(
        f"Project: {result['Project']}"
    )

    print(
        f"Project Control Status: "
        f"{result['Project Control Status']}"
    )

    print(
        f"Project Finish: "
        f"{result['Project Finish']}"
    )

    print(
        f"Total Activities: "
        f"{result['Total Activities']}"
    )

    print(
        f"Critical Activities: "
        f"{result['Critical Activities']}"
    )

    print(
        f"Non-Critical Activities: "
        f"{result['Non-Critical Activities']}"
    )

    print(
        f"Zero Float Activities: "
        f"{result['Zero Float Activities']}"
    )

    print(
        f"Delayed Activities: "
        f"{result['Delayed Activities']}"
    )

    print(
        f"Critical Delayed Activities: "
        f"{result['Critical Delayed Activities']}"
    )

    print()
    print(
        f"Risk Score: "
        f"{result['Risk Score']}"
    )

    print(
        f"Overall Risk: "
        f"{result['Overall Risk']}"
    )

    print()
    print("Highest Risk Activities:")

    for item in result["Highest Risk Activities"]:

        print(
            f" - ID {item['Activity ID']}: "
            f"{item['Activity']} "
            f"(Risk Score: {item['Risk Score']})"
        )

    print()
    print("Delayed Activities:")

    if not result["Delayed Activities"]:

        print(" - None")

    else:

        for item in result["Delayed Activities"]:

            print(
                f" - ID {item['Activity ID']}: "
                f"{item['Activity']} "
                f"({item['Delay Days']} days)"
            )

    print()
    print("Recommendations:")

    for recommendation in result["Recommendations"]:

        print(
            f" - {recommendation}"
        )

    print()
    print("Overall Action:")
    print(result["Overall Action"])