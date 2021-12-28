# CD38_Predictor

To those looking for the specific code, models, summary, and figures from the blood paper or bioRxiv preprint (found [here](https://www.sciencedirect.com/science/article/abs/pii/S0006497121045936) and [here](https://www.biorxiv.org/content/10.1101/2021.08.04.455165v1.full.pdf)) please check the CD38 branch at [CD38](https://github.com/vsarin92/CD38_Predictor/tree/CD38) (also reachable via the UI). 

The main branch will be worked on to make the code more user friendly.

This repository hosts the code (and results) by the [Wiita Lab at UCSF](https://wiitalab.ucsf.edu/) in building and analysing regressor models to predict CD38 expression from a set of 100 Transcription factors found to be co expressed with CD38 by wet lab experiments.

Patient transcriptomic data was from the CoMMpass dataset (Interim Analysis 13, acquired by registering at [MMRF](https://research.themmrf.org/)), that was developed by the Multiple Myeloma Research Foundation. The hundred transcription factors we selected to build our models were determined empirically through other experimental work. Of the 892 patients who had RNA-Seq data available, we filtered to only those that were newly diagnosed. We accepted RNA-Seq data into our model building whether or not it was based off of Bone Marrow (767 patients) or Peripheral Blood (12 patients). All counts were log transformed prior to model building and analysis.

We developed random forest models using the scikit-learn package), and XGBoost models (Extreme Gradient Boosting) using the xgboost package. The code for our analysis is available here and the environment yaml file can be used to recreate the specific anaconda environment (with all the relevant packages) to run the analysis themselves. 

Initially all transcription factors determined to be co expressed were utilized together to build the model.  We used the default hyperparameters for Random Forests used in the scikit-learn package, but chose to use randomized search with cross validation to find the best parameters for the XGBoost models. Specifically we conducted a search over colsample_bytree (subsample ratio of features when constructing each tree), colsample_bylevel (subsample ratio of features for each level), colsample_bynode (subsample ratio of features for each split), gamma (minimum loss reduction to partition a leaf node), learning_rate (how big of a step to take after each iteration), max_depth (maximum tree depth), n_estimators (number of trees), and subsample (subsample ratio of training data). Random combinations of these were used to build a model with 10-fold cross validation, for 50000 iterations, and the hyperparameters that gave the highest cross validation score was what was utilized in further model building.

For both (traditional Random Forests, and XGB) model frameworks, we built three models. One with all transcription factors (as described in the previous paragraph), one with the top twenty most correlated (to CD38 expression) transcription factors, and one using the top twenty transcription factors as determined by permutation importance (which is where each transcription factors value is randomized in turn, and if there is a loss in model performance it is seen as the feature carrying valuable information). Permutation importance analysis was conducted using the eli5 package.

We conducted SHAP analysis on each model built to help describe what affect features have on model predictions using the shap package. Essentially for each patient, a feature is selected to be replaced by a random value from the distribution for that feature. The model's prediction for this simulated patient is compared with the average predictions of all other patients and the difference is attributed to the randomly selected feature. This is repeated for each patient and each feature. Note that SHAP analysis was conducted with only test data.

Model performance was validated by calculating coefficient of determination (R2) and adjusted R2 values (which accounts for the number of observations and the number of features used). This was done for each model. Furthermore, each model underwent 5-fold cross validation with the mean absollute error, R2, and adjusted R2 being reported for each fold and for each model to validate that performance was not dependent on our original choice of training and test data.
