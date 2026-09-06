from schedule_recovery import get_schedule_recovery


PROJECT_ID = 3
ACTIVITY_ID = 33
DELAY_DAYS = 3


result = get_schedule_recovery(
    PROJECT_ID,
    ACTIVITY_ID,
    DELAY_DAYS
)


print()
print("CONSTRUCTAI SCHEDULE RECOVERY")
print("=============================")


if "error" in result:

    print(result["error"])

else:

    print(f"Project: {result['Project']}")
    print(f"Activity ID: {result['Activity ID']}")
    print(f"Activity: {result['Activity']}")
    print(f"Delay: {result['Delay Days']} days")
    print(f"Total Float: {result['Total Float']} days")
    print(f"Critical: {result['Critical']}")
    print(f"Project Impact: {result['Project Impact']} days")
    print(
        f"Recovery Required: "
        f"{result['Recovery Required']}"
    )

    print()
    print("Recovery Options:")

    for index, option in enumerate(
        result["Recovery Options"],
        start=1
    ):

        print(
            f"{index}. {option['Action']}"
        )

        print(
            f"   Purpose: {option['Purpose']}"
        )

    print()
    print("Recommended Strategy:")
    print(result["Recommended Strategy"])