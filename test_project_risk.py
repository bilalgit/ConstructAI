from project_risk_analysis import get_project_risk_analysis


PROJECT_ID = 3


result = get_project_risk_analysis(PROJECT_ID)


print()
print("CONSTRUCTAI PROJECT RISK ANALYSIS")
print("=================================")


if "error" in result:

    print(result["error"])

else:

    print(f"Project: {result['Project']}")
    print(f"Project Finish: {result['Project Finish']}")
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
    print(f"Risk Score: {result['Risk Score']}")
    print(f"Overall Risk: {result['Overall Risk']}")

    print()
    print("Highest Risk Activities:")

    if not result["Highest Risk Activities"]:

        print(" - None")

    else:

        for item in result["Highest Risk Activities"]:

            print()
            print(
                f"ID: {item['Activity ID']}"
            )

            print(
                f"Activity: {item['Activity']}"
            )

            print(
                f"Risk Score: {item['Risk Score']}"
            )

            print(
                f"Critical: {item['Critical']}"
            )

            print(
                f"Total Float: {item['Total Float']}"
            )

            print("Reasons:")

            for reason in item["Reasons"]:
                print(f" - {reason}")

    print()
    print("Recommendations:")

    for recommendation in result["Recommendations"]:

        print(f" - {recommendation}")