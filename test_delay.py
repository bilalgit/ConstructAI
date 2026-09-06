from delay_analysis import analyze_delay


ACTIVITY_ID = 3


result = analyze_delay(ACTIVITY_ID)


print("\n")
print("CONSTRUCTAI DELAY IMPACT ANALYSIS")
print("=================================")


for key, value in result.items():

    print(f"\n{key}:")

    if isinstance(value, list):

        for item in value:
            print(f"  {item}")

    else:

        print(f"  {value}")