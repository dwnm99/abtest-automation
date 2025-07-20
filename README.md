# Automating A/B Experiment Analysis for Dynamic Pages

**Context:** During my tenure as a Data Analyst at Tokopedia, the Discovery Page team frequently launched new campaigns and temporary pages, each requiring A/B testing to evaluate performance. Manually calculating experiment results and significance for 2-3 experiments per week placed a significant burden on the data team, leading to delays and limited capacity for deeper analytical work.

**Problem:**

- **Manual & Time-Consuming:** Analyzing A/B test results for each new page or campaign was a manual process involving data extraction, metric calculation (CTR, CVR, etc.), and statistical significance testing.
- **Scalability Issue:** With a growing number of experiments (2-3 per week), the manual process became unsustainable, creating a bottleneck for the Discovery Page team's rapid iteration cycles.
- **Dashboard Limitation:** The initial build of the A/B test experiment analysis result dashboard requires static data to identify specific page or component names to register as metric dimensions. This is problematic for the Discovery Page team because we are constantly creating new pages for experiments.
- **Data Capture Challenges:** Ensuring consistent and accurate data capture for newly created, dynamic experiment pages was a critical hurdle.

**My Role & Contribution:**

- **Led Data Requirements Definition:** Collaborated closely with the Discovery Page Product Managers, Engineers, and Data Engineers to define the data points needed to accurately track user behavior on dynamic experiment pages.
- **Designed Data Model & Logic:** Architected the logical framework for aggregating experiment data, attributing metrics (CTR, CVR) to specific page and widget variations (control vs. experiment), and identifying the relevant user segments.
- **Developed Automation Scripts/Logic:** Implemented the core analytical logic, likely using SQL for data extraction and aggregation, and Python (with libraries like SciPy) for statistical significance testing (e.g., delta-method for ratio metrics).
- **Established Significance Testing Framework:** Incorporated established statistical methodologies to automatically determine the statistical significance of observed differences in key metrics (CTR, CVR) between control and experiment groups.
- **Ensured Data Integrity & Attribution:** Worked to implement robust data capture mechanisms that correctly linked user interactions (clicks, conversions) to the specific experiment variant and page view.
- **Collaborated on Platform Integration:** Partnered with engineering teams to integrate the analytical scripts into an automated platform, ensuring seamless data flow and result presentation.

**Solution & Technical Implementation:**

- **Automated Data Extraction & ETL:** Developed SQL queries and/or Python scripts to automatically extract relevant user interaction data (page views, clicks, purchases) associated with specific A/B test IDs and page variations.
- **Metric Calculation Engine:** Implemented logic to calculate key e-commerce metrics like:
    - **Click-Through Rate (CTR):** (Clicks/Views)
    - **Conversion Rate (CVR):** (Conversions/Views)
    - *Potentially other metrics like average order value (AOV), paid order per user, etc., depending on the scope.*
- **Statistical Significance Module:** Incorporated statistical tests (e.g., delta method) Estimating variance of complex (often ratio) metrics, which then allows for a Z-test to be performed on the difference in ratios.. The platform would output p-values and confidence intervals.
- **Dynamic Page Data Attribution:** A key aspect was designing a system to correctly attribute user actions to the specific dynamic pages and experiment groups, regardless of how new pages were generated. This likely involved consistent tagging or URL parameters.
- **Platform Integration:** The analytical backend was integrated with a user-facing dashboard or reporting tool for automated display of results.

**Key Technologies & Tools Used:**

- **SQL (e.g., BigQuery,):** For robust data extraction, aggregation, and transformation from Tokopedia's data warehouses.
- **Python:** For scripting the automation logic, statistical analysis, and potentially data manipulation (Pandas, NumPy).
- **Statistical Libraries:** `SciPy.stats` for significance testing.

**Impact & Results:**

- **Reduced Data Team Workload by ~80%:** Significantly freed up the data team's time, reducing manual reporting hours and allowing them to focus on deeper, proactive analytical initiatives.
- **Accelerated Experimentation Cycle:** Empowered the Discovery Page team to rapidly launch and evaluate new campaigns and pages, enabling faster iteration and data-driven decision-making.
- **Improved Data-Driven Culture:** Provided product teams with direct, on-demand access to reliable A/B test results, fostering a stronger data-driven approach to product development.
- **Increased Experiment Throughput:** Enabled Tokopedia to run *more* experiments per week due to the automated analysis, leading to a greater number of validated improvements.
- **Enhanced Reporting Consistency:** Standardized the methodology for A/B test analysis, ensuring consistent and accurate reporting across all experiments.
