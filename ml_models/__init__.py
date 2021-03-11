import dill
# from sklearn.pipeline import Pipeline, FeatureUnion
# from sklearn.compose import ColumnTransformer, make_column_selector
# from sklearn.preprocessing import StandardScaler, FunctionTransformer
# from sklearn.linear_models import SGDRegressor
# from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from pythainlp import word_tokenize
import pandas as pd 

from .utility import split_transformer_func

class ModelLoader:
    def __init__(self):
        # print(split_transformer_func)
        self.meta=dill.load(open("ml_models/V1/meta_20210311082244.pkl","rb"))
        self.clf=dill.load(open("ml_models/V1/pipeline_20210311082244.pkl","rb"))

    def get_meta(self):
        return self.meta

    def get_clf(self):
        return self.clf

    def predict(self,input_text):
        test_df=pd.DataFrame(columns=['activity_name'])
        to_append=[input_text]
        test_df.loc[len(test_df)]=to_append
        y_predict=self.clf.predict(test_df)
        return y_predict[0]