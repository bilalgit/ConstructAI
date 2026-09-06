from forecast import calculate_project_forecast


PROJECT_ID = 1


result = calculate_project_forecast(PROJECT_ID)


print("\n")
print("CONSTRUCTAI PROJECT FORECAST")
print("============================")


for key, value in result.items():

    print(f"{key}: {value}")
    