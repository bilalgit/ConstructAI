from recommendations import generate_recommendation


result = generate_recommendation(
    activity_name="Electrical Rough-in",
    delay_reason="Material shortage",
    delay_days=3,
    project_impact=3
)


print("\n")
print("CONSTRUCTAI DELAY RECOMMENDATION")
print("================================")


for key, value in result.items():

    print(f"{key}: {value}")