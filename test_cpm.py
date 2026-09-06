from cpm import calculate_cpm


PROJECT_ID = 3


results = calculate_cpm(PROJECT_ID)


print("\n")
print("CONSTRUCTAI CPM ANALYSIS")
print("========================")


for result in results:

    print(f"\nActivity: {result['Activity']}")
    print(f"Early Start:  {result['Early Start']}")
    print(f"Early Finish: {result['Early Finish']}")
    print(f"Late Start:   {result['Late Start']}")
    print(f"Late Finish:  {result['Late Finish']}")
    print(f"Total Float:  {result['Total Float']} days")
    print(f"Critical:     {result['Critical']}")