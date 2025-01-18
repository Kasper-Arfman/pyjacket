



files = {
    0.1: ['exp1'],
    1: ['exp2'],
    2: ['exp3', 'exp5'],
    5: ['exp4'],
}


x = [0.1, 1, 2, 5]
y = []
for key in x:

    file_names = files[key]  # e.g. ['exp3', 'exp5']

    outputs = []
    for file in file_names:
        output = run_analysis_here(...)
        outputs.append(output)

    average = average_output_here(...)

    y.append(average)

