from bottleneck import analyze_bottlenecks


PROJECT_ID = 1


results = analyze_bottlenecks(PROJECT_ID)


print("\n")
print("CONSTRUCTAI BOTTLENECK ANALYSIS")
print("===============================")


if isinstance(results, dict):

    print(results)

else:

    for result in results:

        print(
            f"\nActivity: {result['Activity']}"
        )

        print(
            f"Float: {result['Float']} days"
        )

        print(
            f"Critical: {result['Critical']}"
        )

        print(
            f"Risk: {result['Risk']}"
        )