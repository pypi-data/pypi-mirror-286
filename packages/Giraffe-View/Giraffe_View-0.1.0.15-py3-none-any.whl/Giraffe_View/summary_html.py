from Giraffe_View.function import *
import pandas as pd
import re
import os
import pathlib

working_path = pathlib.Path().resolve()

def generate_giraffe_data(input_table):
    # Initialize the dictionary structure
    giraffe_data = {
        "samples": [],
        "metrics": {
            "Estimate (average)": {
                "Estimated read accuracy": [],
                "Read length": [],
                "Read GC content": []
            },
            "Observed (average)": {
                "Observed read accuracy": [],
                "Observed read identification": [],
                "Substitution proportion": [],
                "Insertion proportion": [],
                "Deletion proportion": [],
                "Homopolymer accuracy (A)": [],
                "Homopolymer accuracy (T)": [],
                "Homopolymer accuracy (G)": [],
                "Homopolymer accuracy (C)": []
            }
        }
    }

    # Read sample IDs from the input table
    with open(input_table, "r") as ff:
        giraffe_data["samples"] = [line.strip().split()[0] for line in ff]

    # Process the Estimated results
    estimated_file = "Giraffe_Results/1_Estimated_quality/Estimated_information.txt"
    df_estimated = process_in_chunks(estimated_file)
    df_estimated = pd.DataFrame(df_estimated)
    
    for sample in giraffe_data["samples"]:
        sample_df = df_estimated[df_estimated['Group'] == sample]
        giraffe_data["metrics"]["Estimate (average)"]["Estimated read accuracy"].append(round(100*sample_df["Accuracy"].mean(), 2))
        giraffe_data["metrics"]["Estimate (average)"]["Read length"].append(round(sample_df["Length"].mean(), 2))
        giraffe_data["metrics"]["Estimate (average)"]["Read GC content"].append(round(100*sample_df["GC_content"].mean(), 2))

    # Process the Observed results
    observed_file = "Giraffe_Results/2_Observed_quality/Observed_information.txt"
    df_observed = process_in_chunks(observed_file)
    df_observed = pd.DataFrame(df_observed)

    # Calculate proportions
    df_observed["p_ins"] = 100 * df_observed["Ins"] / (df_observed["Ins"] + df_observed["Del"] + df_observed["Sub"] + df_observed["Mat"])
    df_observed["p_del"] = 100 * df_observed["Del"] / (df_observed["Ins"] + df_observed["Del"] + df_observed["Sub"] + df_observed["Mat"])
    df_observed["p_sub"] = 100 * df_observed["Sub"] / (df_observed["Ins"] + df_observed["Del"] + df_observed["Sub"] + df_observed["Mat"])

    for sample in giraffe_data["samples"]:
        sample_df = df_observed[df_observed['Group'] == sample]
        giraffe_data["metrics"]["Observed (average)"]["Observed read accuracy"].append(round(100*sample_df["Acc"].mean(), 2))
        giraffe_data["metrics"]["Observed (average)"]["Observed read identification"].append(100*round(sample_df["Iden"].mean(), 2))
        giraffe_data["metrics"]["Observed (average)"]["Substitution proportion"].append(round(sample_df["p_sub"].mean(), 2))
        giraffe_data["metrics"]["Observed (average)"]["Deletion proportion"].append(round(sample_df["p_del"].mean(), 2))
        giraffe_data["metrics"]["Observed (average)"]["Insertion proportion"].append(round(sample_df["p_ins"].mean(), 2))

    # Process the Homopolymer results
    homopolymer_file = "Giraffe_Results/2_Observed_quality/Homoploymer_summary.txt"
    df_homopolymer = process_in_chunks(homopolymer_file)
    df_homopolymer = pd.DataFrame(df_homopolymer)

    for sample in giraffe_data["samples"]:
        sample_df = df_homopolymer[df_homopolymer['Group'] == sample]
        for base in ["A", "T", "G", "C"]:
            accuracy = sample_df[sample_df['Base'] == base]["Accuracy"].mean() if not sample_df[sample_df['Base'] == base].empty else float('nan')
            giraffe_data["metrics"]["Observed (average)"][f"Homopolymer accuracy ({base})"].append(round(100*accuracy, 2) if not pd.isna(accuracy) else float('nan'))

    return giraffe_data

def generate_giraffe_html(giraffe_data, summary_figures, output_file):
    with open(output_file, 'w') as f:
        f.write("<html>\n<head>\n<title></title>\n")
        f.write("<style>\n")
        f.write("body { font-family: Arial, sans-serif; margin: 0; padding: 0; }\n")
        f.write("header { background-color: #4CAF50; color: white; padding: 10px 0; text-align: center; }\n")
        f.write("nav { background-color: #f2f2f2; padding: 10px; width: 25%; float: left; height: 100vh; box-sizing: border-box; position: fixed; top: 0; left: 0; }\n")
        f.write("main { margin-left: 26%; padding: 10px; }\n")
        f.write("nav a { display: block; margin: 10px 0; text-decoration: none; color: #4CAF50; font-weight: bold; }\n")
        f.write("nav a:hover { text-decoration: underline; }\n")
        f.write("h1, h2, h3, h4 { color: #4CAF50; }\n")
        f.write("table { border-collapse: collapse; width: 650px; margin: 20px auto; }\n")
        f.write("th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }\n")
        f.write("th { background-color: #f2f2f2; }\n")
        f.write(".figure-container { text-align: center; margin: 20px auto; }\n")
        f.write(".figure-container img { width: 650px; height: auto; }\n")
        f.write("</style>\n")
        f.write("</head>\n<body>\n")

        f.write("<header>\n<h1>Giraffe Report</h1>\n</header>\n")

        # Navigation Index
        f.write("<nav>\n")
        f.write("<h2>Giraffe report</h2>\n")
        f.write("<ul>\n")
        
        # Add entry for Statistics first
        f.write("<li><a href='#summary_table'>Statistics</a></li>\n")

        # Add entries for summary figures
        for category, figures in summary_figures.items():
            f.write(f"<li><a href='#summary_{category}'>{category}</a>\n")
            f.write("<ul>\n")
            for figure in figures:
                figure_title = os.path.splitext(os.path.basename(figure))[0].replace('_', ' ').title()
                f.write(f"<li><a href='#{figure_title}'>{figure_title}</a></li>\n")
            f.write("</ul>\n")
            f.write("</li>\n")
        f.write("</ul>\n</nav>\n")

        # Main content area
        f.write("<main>\n")

        # Create table headers
        headers = "<tr><th>Metric</th>"
        for sample in giraffe_data['samples']:
            headers += f"<th>{sample}</th>"
        headers += "</tr>\n"
        
        # Generate table rows
        rows = ""
        for group, metrics in giraffe_data['metrics'].items():
            # Add group header
            rows += f"<tr><td colspan='{len(giraffe_data['samples']) + 1}'><strong>{group}</strong></td></tr>\n"
            for metric, values in metrics.items():
                rows += f"<tr><td>{metric}</td>"
                for value in values:
                    rows += f"<td>{value:.2f}</td>"
                rows += "</tr>\n"
        
        # Combine headers and rows into a table
        f.write("<section id='summary_table'>\n<h2>Statistics</h2>\n")
        f.write("<div style='text-align: center;'>\n")  # Center the table
        f.write("<table>\n")
        f.write(headers)
        f.write(rows)
        f.write("</table>\n")
        f.write("</div>\n")  # End of centering div
        f.write("</section>\n")

        # Summary Section with Figures
        f.write("<section>\n<h2>Figures</h2>\n")
        for category, figures in summary_figures.items():
            f.write(f"<h3 id='summary_{category}'>{category}</h3>\n")
            for figure in figures:
                figure_title = os.path.splitext(os.path.basename(figure))[0].replace('_', ' ').title()
                f.write(f"<div class='figure-container' id='{figure_title}'>\n")
                f.write(f"<h4>{figure_title}</h4>\n")
                # f.write(f"<p>Description for {figure_title}.</p>\n")
                f.write(f"<img src='{figure}' alt='{figure_title}' style='width: 650px; height: auto;'>\n")
                f.write(f"</div>\n")
        f.write("</section>\n")

        f.write("</main>\n")

        f.write("</body>\n</html>\n")

def summarize_giraffe_results(input_data):
    path = f"{working_path}/Giraffe_Results/Summary"
    giraffe_data = generate_giraffe_data(input_data)
    
    summary_figures = {
    "Estimate": [
        f"{path}/1_Read_estimate_accuracy.png",
        f"{path}/2_Read_GC_content.png",
        f"{path}/3_Read_length.png"
    ],
    "Observe": [
        f"{path}/1_Observed_read_accuracy.png",
        f"{path}/2_Observed_mismatch_proportion.png",
        f"{path}/3_Homoploymer_summary.png"
    ],
    "GC bias": [
        f"{path}/1_Bin_distribution.png",
        f"{path}/2_Relationship_normalization.png"
    ]}

    generate_giraffe_html(giraffe_data, summary_figures, "giraffe_report.html")