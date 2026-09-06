from delayed_activities import get_delayed_activities


PROJECT_ID = 3


result = get_delayed_activities(PROJECT_ID)


print()
print("CONSTRUCTAI DELAYED ACTIVITIES")
print("==============================")

if "error" in result:

    print(result["error"])

else:

    print(f"Project: {result['Project']}")

    print(
        f"Delayed Activity Count: "
        f"{result['Delayed Activity Count']}"
    )

    if result["Delayed Activity Count"] == 0:

        print()
        print("No delayed activities found.")

    else:

        print()
        print("Delayed Activities:")

        for activity in result["Delayed Activities"]:

            print()
            print(
                f"ID: {activity['Activity ID']}"
            )

            print(
                f"Activity: {activity['Activity']}"
            )

            print(
                f"Planned Start: "
                f"{activity['Planned Start']}"
            )

            print(
                f"Planned Finish: "
                f"{activity['Planned Finish']}"
            )

            print(
                f"Actual Start: "
                f"{activity['Actual Start']}"
            )

            print(
                f"Actual Finish: "
                f"{activity['Actual Finish']}"
            )

            print(
                f"Delay: "
                f"{activity['Delay Days']} days"
            )

            print(
                f"Reason: "
                f"{activity['Delay Reason']}"
            )

            print(
                f"Total Float: "
                f"{activity['Total Float']} days"
            )

            print(
                f"Critical: "
                f"{activity['Critical']}"
            )