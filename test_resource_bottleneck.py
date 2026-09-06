from resource_bottleneck import get_resource_bottleneck


PROJECT_ID = 3


result = get_resource_bottleneck(PROJECT_ID)


print()
print("CONSTRUCTAI RESOURCE BOTTLENECK ANALYSIS")
print("=========================================")


if "error" in result:

    print(result["error"])

else:

    print(f"Project: {result['Project']}")

    print(
        f"Bottleneck Count: "
        f"{result['Bottleneck Count']}"
    )

    if result["Bottleneck Count"] == 0:

        print()
        print(
            "No significant resource bottlenecks found."
        )

    else:

        print()
        print("Potential Bottlenecks:")

        for item in result["Potential Bottlenecks"]:

            print()
            print(
                f"ID: {item['Activity ID']}"
            )

            print(
                f"Activity: {item['Activity']}"
            )

            print(
                f"Category: {item['Category']}"
            )

            print(
                f"Quantity: {item['Quantity']} "
                f"{item['Unit']}"
            )

            print(
                f"Progress: {item['Progress']}%"
            )

            print(
                f"Planned Duration: "
                f"{item['Planned Duration']} days"
            )

            print(
                f"Total Float: "
                f"{item['Total Float']} days"
            )

            print(
                f"Critical: {item['Critical']}"
            )

            print(
                f"Bottleneck Score: "
                f"{item['Bottleneck Score']}"
            )

            print(
                f"Risk Level: "
                f"{item['Risk Level']}"
            )

            print("Reasons:")

            for reason in item["Reasons"]:
                print(f" - {reason}")

    print()
    print("Recommendation:")
    print(result["Recommendation"])