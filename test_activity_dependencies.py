from activity_dependencies import get_activity_dependencies


PROJECT_ID = 3
ACTIVITY_ID = 33


result = get_activity_dependencies(
    PROJECT_ID,
    ACTIVITY_ID
)


print()
print("CONSTRUCTAI ACTIVITY DEPENDENCIES")
print("================================")


if "error" in result:

    print(result["error"])

else:

    print(f"Project: {result['Project']}")
    print(f"Activity ID: {result['Activity ID']}")
    print(f"Activity: {result['Activity']}")

    print()
    print(
        f"Predecessor Count: "
        f"{result['Predecessor Count']}"
    )

    print("Predecessors:")

    if result["Predecessor Count"] == 0:

        print(" - None")

    else:

        for item in result["Predecessors"]:

            print(
                f" - ID {item['Activity ID']}: "
                f"{item['Activity']} "
                f"({item['Dependency Type']}, "
                f"lag {item['Lag Days']} days)"
            )

    print()
    print(
        f"Successor Count: "
        f"{result['Successor Count']}"
    )

    print("Successors:")

    if result["Successor Count"] == 0:

        print(" - None")

    else:

        for item in result["Successors"]:

            print(
                f" - ID {item['Activity ID']}: "
                f"{item['Activity']} "
                f"({item['Dependency Type']}, "
                f"lag {item['Lag Days']} days)"
            )