from flowo import Flow, Type


def main():
    flow = Flow()
    flow.name("TheUltimateQuestion").authors("yuvlian").about(
        "An example usage of Flowo"
    )

    with flow.function("Main"):
        # 1. Declare variables and 1D Arrays
        flow.declare("n, i, j, tempMath, tempScience", Type.INTEGER)
        flow.declare("tempAvg", Type.REAL)
        flow.declare("tempName, tempGrade", Type.STRING)

        # 2. Do-While loop to ensure positive student count
        with flow.do_("n <= 0"):
            flow.output('"Enter number of students (must be > 0):"')
            flow.input("n")

        # Declare arrays dynamically based on size
        flow.declare("names", Type.STRING, array=True, size="n")
        flow.declare("math", Type.INTEGER, array=True, size="n")
        flow.declare("science", Type.INTEGER, array=True, size="n")
        flow.declare("averages", Type.REAL, array=True, size="n")
        flow.declare("grades", Type.STRING, array=True, size="n")

        # 3. For loop for data entry
        with flow.for_("i", "0", "n - 1"):
            flow.output('"Enter name for student " & (i + 1) & ":"')
            flow.input("names[i]")
            flow.output('"Enter math score:"')
            flow.input("math[i]")
            flow.output('"Enter science score:"')
            flow.input("science[i]")

            # 4. Call function (stored in assign since Flowgorithm uses Call for void, and Assign for function return mapping)
            flow.assign("averages[i]", "CalculateAverage(math[i], science[i])")

            # 5. If cascade for grades
            with flow.if_("averages[i] >= 90"):
                flow.assign("grades[i]", '"A"')
            with flow.else_():
                with flow.if_("averages[i] >= 80"):
                    flow.assign("grades[i]", '"B"')
                with flow.else_():
                    with flow.if_("averages[i] >= 70"):
                        flow.assign("grades[i]", '"C"')
                    with flow.else_():
                        flow.assign("grades[i]", '"D"')

        # 6. Comment and Breakpoint testing
        flow.comment(
            "Data entry complete. Starting Bubble Sort by average score descending."
        )
        flow.breakpoint()

        # 7. While loop implementing Bubble Sort
        flow.assign("i", "0")
        with flow.while_("i < n - 1"):
            flow.assign("j", "0")
            with flow.while_("j < n - i - 1"):
                # Sort descending
                with flow.if_("averages[j] < averages[j + 1]"):
                    # Swap averages
                    flow.assign("tempAvg", "averages[j]")
                    flow.assign("averages[j]", "averages[j + 1]")
                    flow.assign("averages[j + 1]", "tempAvg")
                    # Swap names
                    flow.assign("tempName", "names[j]")
                    flow.assign("names[j]", "names[j + 1]")
                    flow.assign("names[j + 1]", "tempName")
                    # Swap math
                    flow.assign("tempMath", "math[j]")
                    flow.assign("math[j]", "math[j + 1]")
                    flow.assign("math[j + 1]", "tempMath")
                    # Swap science
                    flow.assign("tempScience", "science[j]")
                    flow.assign("science[j]", "science[j + 1]")
                    flow.assign("science[j + 1]", "tempScience")
                    # Swap grades
                    flow.assign("tempGrade", "grades[j]")
                    flow.assign("grades[j]", "grades[j + 1]")
                    flow.assign("grades[j + 1]", "tempGrade")

                flow.assign("j", "j + 1")
            flow.assign("i", "i + 1")

        # 8. For loop outputting the leaderboard
        flow.output('"\\n--- CLASS LEADERBOARD ---"')
        with flow.for_("i", "0", "n - 1"):
            flow.comment(
                "Explicit Call statement testing (e.g. built-in void procedure)"
            )
            flow.call("PrintStudent(names[i], averages[i], grades[i])")

    # Function returning a value
    with (
        flow.function("CalculateAverage", Type.REAL, "result")
        .parameter("math", Type.INTEGER)
        .parameter("science", Type.INTEGER)
    ):
        flow.assign("result", "(math + science) / 2.0")

    # Function returning nothing (void)
    with (
        flow.function("PrintStudent", Type.NONE)
        .parameter("name", Type.STRING)
        .parameter("avg", Type.REAL)
        .parameter("grade", Type.STRING)
    ):
        flow.output('name & " - Avg: " & avg & " [Grade: " & grade & "]"')

    flow.to_fprg("UltimateQuestion.fprg")


if __name__ == "__main__":
    main()
