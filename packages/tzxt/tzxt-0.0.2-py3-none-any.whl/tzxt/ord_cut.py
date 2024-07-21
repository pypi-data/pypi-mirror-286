import numpy as np
import copy
import sklearn.base
import sklearn.utils.validation
import sklearn.utils.multiclass


class BaseOrdinalClassifier(sklearn.base.BaseEstimator, sklearn.base.ClassifierMixin):
  def __init__(self, classifier):
    self.original_classifier = classifier

  def check_classes(self, classes, y):
    for class_i in classes:
        if type(class_i) != int and type(class_i) != float:
            raise ValueError("Classes must be numeric (type int or float).")
        if np.sum(np.isclose(y, np.ones(len(y))*class_i)) == 0:
            raise ValueError(f"No training samples were given of class {class_i}")

  def fit(self, X, y, classes=None, sample_weight=None, classifier_fit_kwargs={}, best_split_threshold=None):
    X, y = sklearn.utils.validation.check_X_y(X, y)
    if classes is None:
        self.classes_ = sklearn.utils.multiclass.unique_labels(y)
    else:
        self.check_classes(classes, y)
        self.classes_ = classes

    self.classes_ = np.sort(np.array(self.classes_))

    # self.thresholds = (self.classes_[:-1] + self.classes_[1:])/2
    self.thresholds = self.classes_[:-1] + (1e-6 * np.abs(self.classes_[:-1])) + 1e-9 # is relative and absolute tolerance necessary?

    # X, X_val, y, y_val = sklearn.model_selection.train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
    self.X_ = X
    self.y_ = y
    self.classifier_objs = np.zeros(len(self.thresholds), dtype=object)
    for i, threshold_i in enumerate(self.thresholds):
      self.classifier_objs[i] = copy.deepcopy(self.original_classifier).fit(X, y > threshold_i, sample_weight=sample_weight, **classifier_fit_kwargs)
    if best_split_threshold is None:
        self.best_split_ind = np.argmin([np.sum(y <= threshold)**2 + np.sum(y > threshold)**2 for threshold in self.thresholds])
    else:
        self.best_split_ind = np.argmin( np.abs(self.thresholds - best_split_threshold) )
    return self

  def predict(self, X, use_predict_proba):
    if use_predict_proba:
      return self.classes_[np.argmax(self.predict_proba(X), axis=1)]
    else:
      scores = np.zeros(X.shape[0], dtype=int)
      for classifier in self.classifier_objs:
        scores += classifier.predict(X)
      return self.classes_[scores]

  def predict_proba(self, X):
    pass



class TreeOrdinalClassifier(BaseOrdinalClassifier):
  def __init__(self, classifier):
    super().__init__(classifier)

  def predict(self, X):
    return super().predict(X, True)

  def predict_proba(self, X):
    sklearn.utils.validation.check_is_fitted(self)
    X = sklearn.utils.validation.check_array(X)

    classifier_probabilities = np.zeros((X.shape[0], len(self.thresholds)))
    leaf_probabilities = np.ones((X.shape[0], len(self.classes_)))
    for i, classifier in enumerate(self.classifier_objs):
      classifier_probabilities[:,i] = classifier.predict_proba(X)[:,1]
    for i in range(self.best_split_ind+1):
      leaf_probabilities[:,0] *= (1 - classifier_probabilities[:,i])
    for i in range(1, self.best_split_ind+1):
      leaf_probabilities[:,i] *= classifier_probabilities[:,i-1]
      for j in range(i, self.best_split_ind+1):
        leaf_probabilities[:,i] *= (1 - classifier_probabilities[:,j])
    for i in range(self.best_split_ind+1, len(self.classes_)-1):
      leaf_probabilities[:,i] *= (1 - classifier_probabilities[:,i])
      for j in range(self.best_split_ind, i):
        leaf_probabilities[:,i] *= classifier_probabilities[:,j]
    for i in range(self.best_split_ind, len(self.classes_)-1):
      leaf_probabilities[:,-1] *= classifier_probabilities[:,i]
    leaf_probabilities = sklearn.preprocessing.normalize(leaf_probabilities, 'l1')

    return leaf_probabilities


class SubtractionOrdinalClassifier(BaseOrdinalClassifier):
  def __init__(self, classifier):
    super().__init__(classifier)

  def predict(self, X):
    return super().predict(X, True)

  def predict_proba(self, X):
    sklearn.utils.validation.check_is_fitted(self)
    X = sklearn.utils.validation.check_array(X)
    classifier_probabilities = np.zeros((X.shape[0], len(self.thresholds)))
    for i, classifier in enumerate(self.classifier_objs):
      classifier_probabilities[:,i] = classifier.predict_proba(X)[:,1]
    classifier_probabilities[:,self.best_split_ind:] = np.minimum.accumulate(classifier_probabilities[:,self.best_split_ind:], axis=1)
    classifier_probabilities[:,:self.best_split_ind+1] = np.flip(np.maximum.accumulate(np.flip(classifier_probabilities[:,:self.best_split_ind+1], axis=1), axis=1), axis=1)
    probabilities = np.zeros((X.shape[0], len(self.classes_)))
    probabilities[:,0] = 1 - classifier_probabilities[:,0]
    probabilities[:,-1] = classifier_probabilities[:,-1]
    probabilities[:,1:-1] = classifier_probabilities[:,:-1] - classifier_probabilities[:,1:]
    assert((probabilities < -1e-8).sum() == 0)
    # assert(not np.isnan(probabilities).any())
    return probabilities



def print_classification_report(true, prediction, weights=None):
  true, prediction = np.array(true), np.array(prediction)
  stats = sklearn.metrics.classification_report(true, prediction, output_dict=True)
  print(f"""F1 score: {sklearn.metrics.f1_score(true, prediction)}
Sensitivity: {stats['True']['recall']}
Specificity: {stats['False']['recall']}
Positive predictive value: {stats['True']['precision']}
Negative predictive value: {stats['False']['precision']}""")
  print("Accuracy (unweighted):", np.mean(true==prediction))
  if weights is not None: print(f"Accuracy (weighted): {np.average((true==prediction).astype(int), weights=weights)}\n")
  else: print(f"Accuracy (weighted by 0/1 class): {0.5*np.average(true[true==1]==prediction[true==1]) + 0.5*np.average(true[true==0]==prediction[true==0])}\n")


def regression_accuracy(true, min_class, max_class, print_=True, allowable_error=0):
  true = copy.deepcopy(true)
  predictions = copy.deepcopy(predictions)

  predictions[predictions < min_class] = min_class
  predictions[predictions > max_class] = max_class

  try:
    for i in allowable_error:
      regression_accuracy(true, predictions, i, mrs90=False)
  except:
    sub = np.abs(true - np.round(predictions))
    accuracy = np.mean(sub <= allowable_error)
    if print_: print(f"regression accuracy (+/-{allowable_error}):", accuracy)
    return accuracy

def find_best_F1(y_true, y_score, print_=False):
  if print_: print("AUC:", sklearn.metrics.roc_auc_score(y_true, y_score))
  precisions, recalls, thresholds = sklearn.metrics.precision_recall_curve(y_true, y_score)
  f1_scores = 2*precisions*recalls/(precisions+recalls)
  best_F1 = np.nanmax(f1_scores)
  best_F1_threshold = thresholds[np.nanargmax(f1_scores)]
  if print:
    print(f"Best F1 score: {best_F1}; threshold: {best_F1_threshold}")
    print_classification_report(y_true, y_score>=best_F1_threshold)
  else: return best_F1, best_F1_threshold