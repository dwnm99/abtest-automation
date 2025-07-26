Flow Chart:
<img width="573" height="976" alt="image" src="https://github.com/user-attachments/assets/6cd1923b-0b99-4606-a684-3ffd75128a80" />

- Assignment table: 
  The assignment table is a table that contains users' populations for experiments. The format of the table must include: date, user_id, experiment_id, experiment_name, variant_id, and variant_name.

- Fact table: 
  A fact table is a table that contains users' performance on experiments. The format of the table must include: date, user_id, device_name, tribe_name, metrics_dimension_name, metrics_dimension_value, metrics_name, and metrics_amount.

- New Flow Automation Experiment: 
  We need to modify the flow when creating the fact table by renaming the identifier to a new identifier that can be reused for further experiments without having to redefine all metrics in EPPO.

- Impact Quantifying: 
  In a single experiment, at least 7 metrics must be assessed for significance, and for each metric, we must specify which page or widget the experiment is run on. This process is repeated for each experiment as the experiments are conducted on different pages or widgets, which means the DA team needs to create at least 7 new metrics in EPPO when each experiment is started.
  <img width="933" height="492" alt="image" src="https://github.com/user-attachments/assets/f79c0076-1e6b-4b3b-b942-a5825505d617" />
  With the new flow, where the original identifier is renamed with the new identifier, we can create metrics that can be reused in different experiments. We only need to create metrics in the first experiment; there is no need to repeat the creation of metrics for the next experiments.

- Cost Estimation: 
  By implementing EPPO, we can reduce cost queries. Below is the estimated cost using EPPO vs. a manual query. Discovery will reduce by $13 (-72%) monthly.

- Rules:
  1.	Fill in all identifiers maximum 1 day before the experiment starts.
  2.	Page-level performance: Fill the sheet: experiment_page with the following criteria:
  - sub_discovery_page_name is filled with the discovery page identifier (url), and all page experiments need to be listed in the sheet.
  - eppo_page_name is filled with the value provided (experiment 1/.../experiment 10); there cannot be the same value with another experiment on the same experiment day.
  - start_date is filled with the date the experiment started.
  - end_date is filled with the date the experiment ended.
  - is_active is a flag of whether an experiment is active (1) or not (0); if it is active, then choose a different eppo_page_name from the active eppo_page_name. The value is using a function, so to fill this column, you need to copy and paste the above value.
  3.	Widget-level performance (optional): Fill the sheet: widget_list with the following criteria:
  - sub_discovery_page_name is filled with the eppo_page_name on page-level sheet.
  - creative_name is filled with the widget identifier (intools: Tracker Name)
  - eppo_widget_name is filled with new widget identifier {eppo_page_name}_{widget_identifier}, which is the combination of new page name like experiment1/…/experiment10 with the widget1/widget2/…/widget5. If you need to aggregate the performance of several widgets, you can list down the creative name and fill the eppo_creative_name with the same value.
  - start_date is filled with the date the experiment started.
  - end_date is filled with the date the experiment ended.

- Add discovery page metrics on EPPO: 
  To add discovery page metrics on EPPO, find the metrics that starts with Discovery followed by the eppo_page_name that has been defined on sheet.
