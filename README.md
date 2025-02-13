# VisA

Visual analytics app for exploring machine learning classifications.   
Developed as part of course work (and beyond) by students at HU Berlin.

[![Unit Tests](https://github.com/noelkronenberg/hub-visa/actions/workflows/tests.yml/badge.svg)](https://github.com/noelkronenberg/hub-visa/actions/workflows/tests.yml)

## Showcase

The app is live and hosted on the Streamlit Community Cloud: [visa-demo.streamlit.app](https://visa-demo.streamlit.app/)

## Set-up

```bash
git clone https://github.com/noelkronenberg/visa.git # clone repository
cd visa # change directory
pip install -r app/requirements.txt # install dependencies
streamlit run app/app.py # open application
```

## Structure

- ```.github/workflows/``` Directory containing GitHub Actions configurations.
-   - `tests.yml` Configuration for running unit tests on commit.
- ```.streamlit/``` Directory containing Streamlit configurations.
  - `config.toml` Configuration file for Streamlit server settings.
- ```app/``` Directory containing Streamlit application files.
  - `lucas_organic_carbon/` Directory containing data files for the Lucas Organic Carbon dataset [[ESDAC](https://esdac.jrc.ec.europa.eu/projects/lucas)].
      - `target/` Directory containing target data files.
      - `training_test/` Directory containing training and test data files.
  - `services/` Directory containing supporting files.
    - `data.py` Contains functions for loading and preparing data.
    - `error_analysis.py` Contains functions for visualizing error analysis.
    - `feature_importance.py` Contains functions for visualizing feature importance.
    - `model.py` Contains functions for training and evaluating the machine learning model.
  - `__init__.py` Initialization file for the app module.
  - `app.py` Main application file for the Streamlit dashboard.
  - `config.py` Configuration file for general settings used in the app.
  - `requirements.txt` Lists the Python packages required to run the app.
  - `test_app.py` Unit tests for checking the app.
- ```check_env.py``` Script to check if the required environment and packages are installed.
- ```environment.yml``` Conda environment configuration file listing the dependencies.
- ```local-install-instructions.md``` Instructions for setting up the project locally.

## Milestones

> Solved tasks and addressing of milestones.

| ID | Milestone | Solved Tasks | Improvements |
|---|------------|--------------|--------------|
| M1 | Data Exploration | Raw data attributes, overall data distributions, distribution of organic carbon concentration classes, spectral profiles of random soil samples, boxplot of selected wavelengths by carbon concentration class, profiling report. ||
| M2 | Random Forest                      | Label encoding, train-test split (test size = 0.2), grid search as well as randomized search with 3-fold CV on parameter grid (```n_estimators```, ```max_depth```, ```min_samples_split```, ```min_samples_leaf```, ```max_features```), evaluation of different grid search results (plot of score over iterations, confusion matrix, accuracy score, cross-validation score, mean cross-validation score). ||
| M3 | Explorative Error Analysis Concept (*Konzept I*) | [[presentation slides](https://docs.google.com/presentation/d/16qUn8gltr5sOPD6g4-4v1JwBQHDfBOIbRnPZEQq2H_U/edit?usp=sharing)] [[updated wireframe](https://docs.google.com/presentation/d/1CWkKQfMkITK6Dze0oZnR4_OqrqThp5agR9G6SoI4Jhk/edit?usp=sharing)] ||
| M4 | Explorative Error Analysis Prototype (*Komponente I*) | [see *Components*] ||
|M5|Feature Importance Concept (*Konzept II*)|[[presentation slides](https://docs.google.com/presentation/d/1sSXYiWVSzP-jKvBnRYrvyK_wPkAHrHsJ0h6WnJ6E7G0/edit?usp=sharing)]||
|M6|Feature Importance Prototype (*Komponente II*)|[see *Components*]|[see *Improvements*]|
|M7|Model Comparison Concept (*Konzept III*)|[[presentation slides](https://docs.google.com/presentation/d/1NYDmAEd8p7cuZHK_mLCI6-d52McKKU-4vzNwit14Toc/edit?usp=sharing)]||
|M8|Model Comparison Prototype (*Komponente III*)|[see *Components*]||

## Components

> Major components of the VA system and the status of implementation.

| ID  | Component                     | Description                                                                                                     | Status | Milestone |
| --- | ----------------------------- | --------------------------------------------------------------------------------------------------------------- | ------ | --------- |
| C1  | Confusion Matrix              | Allow user to view confusion matrix for a trained model in Streamlit application.                               | done   | M4        |
| C2  | Evaluation Metrics            | Allow user to view specific model evaluation metrics.                                                           | done   | M4        |
| C3  | Data Upload                   | Allow user to upload their own or large dataset.                                                                | done   | M4        |
| C4  | Hosting                       | Allow user to view Streamlit application on a hosted website.                                                   | done   | M4        |
| C5  | Dynamic Model Training        | Allow user to change model parameters to retrain the model dynamically.                                         | done   | M4        |
| C6  | Faster UX                     | Enable faster loading times and improve usability.                                                              | done   | M4        |
| C7  | Class Selection               | Allow users to select a specific target class to view evaluation metrics.                                       | done   | M4        |
| C8  | Overview of Importance Scores | Show importance scores for each feature.                                                                        | done   | M6        |
| C9  | Impact of Intervals           | Show the average impact of intervals.                                                                           | done   | M6        |
| C10 | Impact of 2-D Intervals       | Show the average impact of 2-D intervals.                                                                       | done   | M6        |
| C11 | Improved Division of Tasks    | Allow the user to focus on a single task (e.g. model training, error exploration, investigation of importance). | done   | M6        |
| C12 | Auto Encoded Data    | Allow for selection of auto encoded data. | done   | M8        |
| C13 | Model Comparison    | Allow for the selection of a second model to compare. | done   | M8        |


## Activities

> Major implementation activities for each component.

| ID  | Component                     | Description                                                                 | Status | Point Person               |
| --- | ----------------------------- | --------------------------------------------------------------------------- | ------ | -------------------------- |
| C1  | Confusion Matrix              |                                                                             |        | Noel Kronenberg            |
| A1  |                               | Setting up Streamlit application.                                           | done   | Noel Kronenberg            |
| A2  |                               | Integrating trained model with application.                                 | done   | Noel Kronenberg            |
| A3  |                               | Integrating trained model with Plotly figure.                               | done   | Noel Kronenberg            |
| A4  |                               | Integrating Plotly figure with application.                                 | done   | Noel Kronenberg            |
| C2  | Evaluation Metrics            |                                                                             |        | Noel Kronenberg            |
| A1  |                               | Calculation of evaluation metrics for trained model.                        | done   | Noel Kronenberg            |
| A2  |                               | Displaying of evaluation metrics on Streamlit application.                  | done   | Noel Kronenberg            |
| A3  |                               | Adding a bar chart for the comparison of predicted and actual class counts. | done   | Aodi Chen                  |
| A4  |                               | Adding confusion matrix metrics.                                            | done   | Aodi Chen                  |
| A5  |                               | Adding collapsible sections to hide metrics.                                | done   | Noel Kronenberg            |
| A6  |                               | Preselecting class with lowest accuracy.                                    | done   | Noel Kronenberg            |
| C3  | Data Upload                   |                                                                             |        | Noel Kronenberg            |
| A1  |                               | Adding form for uploading data.                                             | done   | Noel Kronenberg            |
| A2  |                               | Increasing maximum Streamlit upload limit.                                  | done   | Noel Kronenberg            |
| C4  | Hosting                       |                                                                             |        | Noel Kronenberg            |
| A1  |                               | Setting up Streamlit Community Cloud.                                       | done   | Noel Kronenberg            |
| A2  |                               | Making application compatible with hosting.                                 | done   | Noel Kronenberg            |
| C5  | Dynamic Model Training        |                                                                             |        | Noel Kronenberg            |
| A1  |                               | Adding form for adjustment of parameters.                                   | done   | Noel Kronenberg            |
| A2  |                               | Adding function to dynamically train model with new parameters.             | done   | Noel Kronenberg            |
| C6  | Faster UX                     |                                                                             |        | Noel Kronenberg            |
| A1  |                               | Adding caching functionality of data (e.g. uploaded data).                  | done   | Noel Kronenberg            |
| A2  |                               | Adding caching functionality of resources (e.g. trained model).             | done   | Noel Kronenberg            |
| A3  |                               | Adding data loader signs for transparent loading processes.                 | done   | Noel Kronenberg            |
| C7  | Class Selection               |                                                                             |        | Noel Kronenberg            |
| A1  |                               | Adding form for selection of class.                                         | done   | Noel Kronenberg            |
| A2  |                               | Highlighting class in confusion matrix.                                     | done   | Noel Kronenberg            |
| A3  |                               | Adding evaluation metrics for selected class.                               | done   | Noel Kronenberg            |
| A4  |                               | Adding highlight to evaluation metrics for selected class.                  | done   | Noel Kronenberg            |
| C8  | Overview of Importance Scores |                                                                             |        | Aodi Chen                  |
| A1  |                               | Calculating importance scores.                                              | done   | Aodi Chen, Noel Kronenberg |
| A2  |                               | Adding bar chart to plot feature importance.                                | done   | Aodi Chen, Noel Kronenberg |
| A3  |                               | Adding slider to select number of features.                                 | done   | Noel Kronenberg            |
| C9  | Impact of Intervals           |                                                                             |        | Fabian Henning             |
| A1  |                               | Slicing data into desired intervals.                                        | done   | Fabian Henning             |
| A2  |                               | Comparing prediction metrics of transformed and original data.              | done   | Fabian Henning, Noel Kronenberg |
| A3  |                               | Plotting differences of prediction metrics.                                 | done   | Noel Kronenberg            |
| A4  |                               | Adding dropdown and slider for user input (feature selection, number of intervals). | done   | Noel Kronenberg            |
| C10 | Impact of 2-D Intervals       |                                                                             |        | Aodi Chen                  |
| A1  |                               | Expanding functions from C9 to allow for 2-D intervals.                     | done   | Aodi Chen                  |
| A2  |                               | Visualizing 2-D intervals for all metrics.                                   | done   | Aodi Chen, Noel Kronenberg |
| A3  |                               | Adding dropdown and slider for user input (selection of features, number of intervals, selection of metrics). | done   | Aodi Chen, Noel Kronenberg |
| C11 | Improved Division of Tasks    |                                                                             |        | Noel Kronenberg            |
| A1  |                               | Adding of tabs for Explorative Error Analysis and Feature Importance.       | done   | Noel Kronenberg            |
| A2  |                               | Refactoring (e.g. encapsulating) the code to be more readable.              | done   | Noel Kronenberg            |
| C12 | Auto Encoded Data             |                                                                             |        | Noel Kronenberg            |
| A1  |                               | Encoding data locally and upload as an option.                                | done   | Noel Kronenberg            |
| C13 | Model Comparison              |                                                                             |        | Noel Kronenberg, Aodi Chen           |
| A1  |                               | Allowing user to check "Compare Models" and select new model parameters and data. | done   | Noel Kronenberg |
| A2  |                               | Enabling the side-by-side comparison of the selected models in all relevant views. | done   | Noel Kronenberg |

## Improvements

> Large optimizations to the components that are not core to official milestones tasks.

| ID | Improvement | Solved Tasks | Status | Point Person | Milestone |
|----|-------------|--------------|--------|--------------|-----------|
| I1 | Data Exploration Graphs | Bar chart for distribution of organic carbon concentration classes, spectral profiles of random soil samples, boxplot of selected wavelengths by carbon concentration class. | done | Noel Kronenberg | M6 |
| I2 | Model Download | Option to download trained model as a pickle file. | done | Noel Kronenberg | M6 |
| I3 | Demo Datasets | Option to choose from multiple demo datasets. | done | Noel Kronenberg | M6 |
| I4 | Unit Tests | Unit tests to check the app with automation for commits. | done | Noel Kronenberg | M6 |
