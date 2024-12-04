import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go

# streamlit app
st.set_page_config(page_title="VisA Dashboard", layout="wide")
st.title("VisA Dashboard")

# sidebar for user inputs
st.sidebar.header("Model Parameters")
max_depth = st.sidebar.slider('Max Depth', min_value=1, max_value=20, value=14)
n_estimators = st.sidebar.slider('Number of Estimators', min_value=10, max_value=500, value=384)
data_percentage = st.sidebar.slider('Percentage of Data to Use', min_value=1, max_value=100, value=1)
normalize_cm = st.sidebar.checkbox('Normalize Confusion Matrix', value=True)

# spinner while loading
with st.spinner('Preparing the data...'):
    # load the data
    df_target = pd.read_csv('app/lucas_organic_carbon/target/lucas_organic_carbon_target.csv')
    df_training = pd.read_csv('app/lucas_organic_carbon/training_test/lucas_organic_carbon_training_and_test_data.csv')
    df_combined = pd.merge(df_training, df_target, left_index=True, right_index=True)

    # sample the data
    sample_size = int(len(df_combined) * (data_percentage / 100))
    df_sampled = df_combined.sample(n=sample_size, random_state=42)

    # prepare the data
    predictors = df_sampled.columns[:-1]
    target = df_sampled.columns[-1]
    X = df_sampled[predictors]
    y = df_sampled[target]

    # encode categorical target
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# spinner while loading
with st.spinner('Training the model...'):
    # train model
    rf_classifier = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators)
    rf_classifier.fit(X_train, y_train)
    y_pred = rf_classifier.predict(X_test)

# spinner while loading
with st.spinner('Evaluating the model...'):
    ### overall metrics

    # compute metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    # display metrics (in columns)
    st.subheader("Overall Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", f"{accuracy:.2f}")
    col2.metric("Precision", f"{precision:.2f}")
    col3.metric("Recall", f"{recall:.2f}")
    col4.metric("F1 Score", f"{f1:.2f}")

    ### confusion matrix

    # actual label names
    unique_labels = label_encoder.classes_

    # compute confusion matrix
    if normalize_cm:
        cm = confusion_matrix(y_test, y_pred, labels=range(len(unique_labels)), normalize='true')
    else:
        cm = confusion_matrix(y_test, y_pred, labels=range(len(unique_labels)))

    # display confusion matrix
    st.subheader('Confusion Matrix')
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=[f'Predicted: {label}' for label in unique_labels],
        y=[f'Actual: {label}' for label in unique_labels],
        colorscale='Viridis',
        showscale=True
    ))
    fig.update_layout(
        xaxis_title='Predicted Label',
        yaxis_title='Actual Label',
        xaxis=dict(tickmode='array', tickvals=list(range(len(unique_labels))), ticktext=unique_labels),
        yaxis=dict(tickmode='array', tickvals=list(range(len(unique_labels))), ticktext=unique_labels)
    )
    st.plotly_chart(fig)