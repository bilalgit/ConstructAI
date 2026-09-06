from recovery import calculate_recovery


ACTIVITY_ID = 3


result = calculate_recovery(
    ACTIVITY_ID,
    2
)


print("\n")
print("CONSTRUCTAI RECOVERY ANALYSIS")
print("=============================")


for key, value in result.items():

    print(f"{key}: {value}")