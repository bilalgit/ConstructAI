from recovery_impact import calculate_recovery_impact


ACTIVITY_ID = 3
RECOVERY_DAYS = 2


result = calculate_recovery_impact(
    ACTIVITY_ID,
    RECOVERY_DAYS
)


print("\n")
print("CONSTRUCTAI RECOVERY IMPACT")
print("===========================")


for key, value in result.items():

    print(f"{key}: {value}")