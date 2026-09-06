from project_status import get_project_status


PROJECT_ID = 3


result = get_project_status(PROJECT_ID)


print("\n")
print("CONSTRUCTAI PROJECT STATUS")
print("==========================")

if "error" in result:

    print(result["error"])

else:

    print(
        f"\nProject: "
        f"{result['Project']}"
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

    print("\nCritical Path:")

    for activity in result["Critical Path"]:

        print(f" → {activity}")

    print("\nHighest Risk Activities:")

    for activity in result[
        "Highest Risk Activities"
    ]:

        print(f" - {activity}")