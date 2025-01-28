import logging
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from services.model import evaluate_model
from config import RED, BLUE

def _get_feature_importance(model):
    """
    Calculate feature importance using built-in feature importance of sklearn models.
    """

    # check if the model has feature_importances_ attribute
    importance_values = model.feature_importances_
    logging.info(f"Feature importance values extracted successfully.")

    # if feature_names is not provided, get it from the model
    feature_names = model.feature_names_in_
    logging.info(f"Feature names extracted from the model.")

    # create DataFrame with feature importance
    feature_importance = pd.DataFrame({
        'feature': list(feature_names), 
        'importance': importance_values
    })
    logging.info(f"Feature importance DataFrame created successfully.")

    return feature_importance

def visualize_feature_importance(model):
    """
    Visualize feature importance using built-in feature importance of sklearn models.
    """

    # get feature importance data
    feature_importance = _get_feature_importance(model)

    # sort feature importance by absolute value in descending order
    sorted_feature_importance = feature_importance.reindex(feature_importance['importance'].abs().sort_values(ascending=False).index)

    # assign rank based on importance
    sorted_feature_importance['rank'] = range(1, len(sorted_feature_importance) + 1)

    # display feature importance
    with st.expander("**Feature Importance**", expanded=True):

        # allow user to select range of values to show
        num_features = st.slider('Number of Features', min_value=1, max_value=len(sorted_feature_importance), value=max(1, len(sorted_feature_importance) // 3))
        sorted_feature_importance = sorted_feature_importance.head(num_features)
        logging.info(f"Top {num_features} feature importance displayed successfully.")

        # create bar chart
        fig = go.Figure(data=go.Bar(
            x=sorted_feature_importance['rank'],
            y=sorted_feature_importance['importance'],
            marker_color=RED,
            textposition='auto',
            hovertemplate='Rank: %{x}<br>Feature: %{customdata}<br>Importance: %{y:.4f}<extra></extra>',
            customdata=sorted_feature_importance['feature']
        ))

        # update layout
        fig.update_layout(
            title='',
            xaxis_title='Rank',
            yaxis_title='Importance',
            margin=dict(l=20, r=20, t=20, b=20),
            height=600,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
        logging.info("Feature importance displayed successfully.")

def _define_intervals(X_test, feature_index=0, num_intervals=10):
    """
    Define intervals for a given feature.
    """

    min_val = X_test.iloc[:, feature_index].min()
    max_val = X_test.iloc[:, feature_index].max()
    intervals = np.linspace(min_val, max_val, num_intervals+1)

    return intervals

def _interval_importance(model, X_test, y_test, feature_index=0, num_intervals=10):
    """
    Use transform_left parameter to map both to the left interval limit or the right interval limit.
    """

    # get original evaluation metrics
    accuracy = st.session_state.accuracy
    precision = st.session_state.precision
    recall = st.session_state.recall
    f1 = st.session_state.f1

    # define intervals
    intervals = _define_intervals(X_test, feature_index, num_intervals)
    
    # initialize lists to store the differences in error metrics
    accuracy_diffs = []
    precision_diffs = []
    recall_diffs = []
    f1_diffs = []

    # iterate over each interval
    for i in range(len(intervals) - 1):

        # create a copy of X_test
        X_test_transformed_left = X_test.copy()
        X_test_transformed_right = X_test.copy()
        
        # transform the interval to the left   
        cut_series = pd.cut(X_test.iloc[:, feature_index], bins=[intervals[i], intervals[i+1]], labels=[intervals[i]], include_lowest=True)
        cut_series = cut_series.astype('float')
        cut_series.fillna(X_test.iloc[:,0], inplace=True)
        X_test_transformed_left.iloc[:, feature_index] = cut_series

        # transform the interval to the right
        cut_series = pd.cut(X_test.iloc[:, feature_index], bins=[intervals[i], intervals[i+1]], labels=[intervals[i+1]], include_lowest=True)
        cut_series = cut_series.astype('float')
        cut_series.fillna(X_test.iloc[:,0], inplace=True)
        X_test_transformed_right.iloc[:, feature_index] = cut_series

        # merge the transformed dataframes
        X_test_transformed = pd.concat([X_test_transformed_left, X_test_transformed_right], axis=0)

        # predict using the transformed test set
        y_pred_transformed = model.predict(X_test_transformed)
        
        # evaluate the model
        y_test_transformed = pd.concat([y_test, y_test], axis=0)
        accuracy_transformed, precision_transformed, recall_transformed, f1_transformed = evaluate_model(y_test_transformed, y_pred_transformed)
        
        # calculate the differences in error metrics
        accuracy_diff = accuracy - accuracy_transformed
        precision_diff = precision - precision_transformed
        recall_diff = recall - recall_transformed
        f1_diff = f1 - f1_transformed
        
        # append the differences to the lists
        accuracy_diffs.append(accuracy_diff)
        precision_diffs.append(precision_diff)
        recall_diffs.append(recall_diff)
        f1_diffs.append(f1_diff)

    accuracy_diffs = np.array(accuracy_diffs)
    precision_diffs = np.array(precision_diffs)
    recall_diffs = np.array(recall_diffs)
    f1_diffs = np.array(f1_diffs)
    
    return accuracy_diffs, precision_diffs, recall_diffs, f1_diffs

def visualize_interval_importance(model, X_test, y_test, feature_index=0, num_intervals=10):
    """
    Visualize interval importance using transform_left parameter.
    """

    # ensure X_test and y_test are DataFrames
    if not isinstance(X_test, pd.DataFrame):
        X_test = pd.DataFrame(X_test)
        logging.info(f"X_test and y_test converted to DataFrames successfully.")
    if not isinstance(y_test, pd.DataFrame):
        y_test = pd.DataFrame(y_test)
        logging.info(f"X_test and y_test converted to DataFrames successfully.")

    # get differences in error metrics
    accuracy_diffs, precision_diffs, recall_diffs, f1_diffs = _interval_importance(model, X_test, y_test, feature_index, num_intervals)
    logging.info(f"Differences in error metrics calculated successfully: {accuracy_diffs}, {precision_diffs}, {recall_diffs}, {f1_diffs}")

    # define intervals
    intervals = _define_intervals(X_test, feature_index, num_intervals)

    # check if all differences are zero
    if np.all(accuracy_diffs == 0):
        st.warning("The differences in error metrics are too small to display meaningful charts. Try a different feature or larger dataset.")
        logging.warning("The differences in error metrics are too small to display meaningful charts. Try a different feature or larger dataset.")
        return

    # create line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=intervals[1:], y=accuracy_diffs, mode='lines+markers', name='Accuracy', 
        line=dict(color='blue'),
        hovertemplate='Interval: %{x}<br>Accuracy Difference: %{y:.4f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=intervals[1:], y=precision_diffs, mode='lines+markers', name='Precision', 
        line=dict(color='green'),
        hovertemplate='Interval: %{x}<br>Precision Difference: %{y:.4f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=intervals[1:], y=recall_diffs, mode='lines+markers', name='Recall', 
        line=dict(color='red'),
        hovertemplate='Interval: %{x}<br>Recall Difference: %{y:.4f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=intervals[1:], y=f1_diffs, mode='lines+markers', name='F1', 
        line=dict(color='purple'),
        hovertemplate='Interval: %{x}<br>F1 Difference: %{y:.4f}<extra></extra>'
    ))

    # update layout
    fig.update_layout(
        title='',
        xaxis_title='Intervals',
        yaxis_title='Difference in Error Metric',
        margin=dict(l=20, r=20, t=20, b=20),
        height=600,
        showlegend=True,
    )

    # display feature importance
    st.plotly_chart(fig, use_container_width=True)
    logging.info("Interval importance displayed successfully.")

    # bar chart for accuracy_diffs
    fig = go.Figure(data=go.Bar(
        x=intervals[1:],
        y=accuracy_diffs,
        marker_color=RED,
        textposition='auto',
        hovertemplate='Interval: %{x}<br>Accuracy Difference: %{y:.4f}<extra></extra>'
    ))

    # update layout
    fig.update_layout(
        title='',
        xaxis_title='Intervals',
        yaxis_title='Difference in Accuracy',
        margin=dict(l=20, r=20, t=20, b=20),
        height=600,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    logging.info("Accuracy differences displayed successfully.")

def get_feature_selection_inputs(feature_importance_df, feature_names):
    """
    Create input controls for feature selection
    """

    col1, col2 = st.columns(2)
    
    # sort features by importance
    sorted_features = feature_importance_df.sort_values(by='importance', ascending=False)['feature']

    with col1:
        # select first feature
        selected_feature1 = st.selectbox( 
            "Select First Feature", 
            sorted_features,
            index=0,
            key='joint_importance_feature1'
        )
        feature1_index = list(feature_names).index(selected_feature1)

    with col2:
        # select second feature
        remaining_features = [f for f in sorted_features if f != selected_feature1]
        selected_feature2 = st.selectbox(
            "Select Second Feature",
            remaining_features,
            index=0,
            key='joint_importance_feature2'
        )
        feature2_index = list(feature_names).index(selected_feature2)
        
    # number of intervals for features
    num_intervals = st.slider(
        f'Number of Intervals', 
        min_value=1, 
        max_value=20, 
        value=3,
        key='joint_importance_intervals'
    )
    
    return selected_feature1, selected_feature2, feature1_index, feature2_index, num_intervals, num_intervals

def _joint_interval_importance(model, X_test, y_test, feature_1_index, feature_2_index,
                             num_intervals1, num_intervals2):
    """
    calculate importance for different intervals of two features.
    """
    # get feature values
    feature1_values = X_test.iloc[:, feature_1_index].values
    feature2_values = X_test.iloc[:, feature_2_index].values
    
    # get baseline predictions and metrics
    base_pred = model.predict(X_test)
    base_metrics = {
        'accuracy': accuracy_score(y_test, base_pred),
        'precision': precision_score(y_test, base_pred, average='weighted', zero_division=0),
        'recall': recall_score(y_test, base_pred, average='weighted', zero_division=0),
        'f1': f1_score(y_test, base_pred, average='weighted', zero_division=0)
    }
    
    # create evenly distributed intervals
    feature1_min, feature1_max = np.min(feature1_values), np.max(feature1_values)
    feature2_min, feature2_max = np.min(feature2_values), np.max(feature2_values)
    
    # add a small offset to ensure all data points are included
    epsilon = 1e-10
    feature1_min -= epsilon
    feature1_max += epsilon
    feature2_min -= epsilon
    feature2_max += epsilon
    
    intervals_1 = np.linspace(feature1_min, feature1_max, num_intervals1 + 1)
    intervals_2 = np.linspace(feature2_min, feature2_max, num_intervals2 + 1)
    
    # create result matrices
    accuracy_diffs = np.zeros((num_intervals2, num_intervals1))
    precision_diffs = np.zeros((num_intervals2, num_intervals1))
    recall_diffs = np.zeros((num_intervals2, num_intervals1))
    f1_diffs = np.zeros((num_intervals2, num_intervals1))
    
    # calculate importance for each interval combination
    for i in range(num_intervals2):
        for j in range(num_intervals1):
            X_modified = X_test.copy()
        
            value1 = (intervals_1[j] + intervals_1[j + 1]) / 2
            value2 = (intervals_2[i] + intervals_2[i + 1]) / 2
       
            X_modified.iloc[:, feature_1_index] = value1
            X_modified.iloc[:, feature_2_index] = value2
            
            # get modified predictions and metrics
            modified_pred = model.predict(X_modified)
            modified_metrics = {
                'accuracy': accuracy_score(y_test, modified_pred),
                'precision': precision_score(y_test, modified_pred, average='weighted', zero_division=0),
                'recall': recall_score(y_test, modified_pred, average='weighted', zero_division=0),
                'f1': f1_score(y_test, modified_pred, average='weighted', zero_division=0)
            }
            
            # calculate differences and ensure no zero values
            accuracy_diffs[i, j] = max(abs(modified_metrics['accuracy'] - base_metrics['accuracy']), 1e-10)
            precision_diffs[i, j] = max(abs(modified_metrics['precision'] - base_metrics['precision']), 1e-10)
            recall_diffs[i, j] = max(abs(modified_metrics['recall'] - base_metrics['recall']), 1e-10)
            f1_diffs[i, j] = max(abs(modified_metrics['f1'] - base_metrics['f1']), 1e-10)
    
    # ensure no zero values in matrices
    accuracy_diffs[accuracy_diffs < 1e-10] = 1e-10
    precision_diffs[precision_diffs < 1e-10] = 1e-10
    recall_diffs[recall_diffs < 1e-10] = 1e-10
    f1_diffs[f1_diffs < 1e-10] = 1e-10
    
    return accuracy_diffs, precision_diffs, recall_diffs, f1_diffs, intervals_1, intervals_2

def visualize_joint_importance(model, X_test, y_test, feature_1_index, feature_2_index,
                             num_intervals1, num_intervals2):
    """
    visualize the joint importance of two features using heatmaps for different metrics.
    """
    # get feature names
    feature_names = list(model.feature_names_in_)
    feature1_name = feature_names[feature_1_index]
    feature2_name = feature_names[feature_2_index]
    
    # get difference matrices
    accuracy_diffs, precision_diffs, recall_diffs, f1_diffs, intervals_1, intervals_2 = _joint_interval_importance(
        model, X_test, y_test, feature_1_index, feature_2_index,
        num_intervals1, num_intervals2
    )
    
    # create interval labels
    x_labels = [f'{intervals_1[i]:.9f}-{intervals_1[i+1]:.9f}' for i in range(len(intervals_1)-1)]
    y_labels = [f'{intervals_2[i]:.9f}-{intervals_2[i+1]:.9f}' for i in range(len(intervals_2)-1)]
    
    # create metrics dictionary
    metrics = {
        'Accuracy': accuracy_diffs,
        'Precision': precision_diffs,
        'Recall': recall_diffs,
        'F1 Score': f1_diffs
    }
    
    # add metric selection
    selected_metrics = st.multiselect(
        'Select Metrics to Display',
        options=list(metrics.keys()),
        default=['Accuracy'],
        key='joint_importance_metrics'
    )
    
    if not selected_metrics:
        st.warning('Please select at least one metric to display')
        return
    
    # create heatmap for each selected metric
    for metric_name in selected_metrics:
        metric_values = metrics[metric_name]
        
        # ensure all values are greater than zero
        metric_values = np.maximum(metric_values, 1e-10)
        
        # create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=metric_values,
            x=x_labels,
            y=y_labels,
            colorscale='RdYlBu_r',
            zmin=np.min(metric_values),
            zmax=np.max(metric_values),
            colorbar=dict(
                title=f"{metric_name} Difference",
                titleside="right",
                tickformat='.9f'
            ),
            text=[[f"{val:.9f}" for val in row] for row in metric_values],
            texttemplate='%{text}',
            textfont={"size": 10, "color": "black"},
            showscale=True,
            hovertemplate=(
                f"{feature1_name}: %{{x}}<br>" +
                f"{feature2_name}: %{{y}}<br>" +
                f"{metric_name} Difference: %{{text}}<extra></extra>"
            )
        ))
        
        # add grid lines
        for i in range(num_intervals1 + 1):
            fig.add_shape(
                type='line',
                x0=i - 0.5,
                x1=i - 0.5,
                y0=-0.5,
                y1=num_intervals2 - 0.5,
                line=dict(color='black', width=1)
            )
        
        for i in range(num_intervals2 + 1):
            fig.add_shape(
                type='line',
                x0=-0.5,
                x1=num_intervals1 - 0.5,
                y0=i - 0.5,
                y1=i - 0.5,
                line=dict(color='black', width=1)
            )
        
        # update layout
        fig.update_layout(
            title={
                'text': f'Joint Feature Importance ({metric_name}): {feature1_name} & {feature2_name}',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title=feature1_name,
            yaxis_title=feature2_name,
            height=600,
            width=800,
            xaxis={
                'side': 'bottom',
                'tickangle': 45,
                'showgrid': False,
                'range': [-0.5, num_intervals1 - 0.5]
            },
            yaxis={
                'autorange': 'reversed',
                'showgrid': False,
                'range': [-0.5, num_intervals2 - 0.5]
            },
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)