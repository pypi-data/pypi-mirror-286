import polars as pl
import numpy as np
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from xgboost import XGBClassifier, XGBRegressor
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer


class ExtractTime:

    @staticmethod
    def sin_transformer(period):
        return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))

    @staticmethod
    def cos_transformer(period):
        return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))

    @staticmethod
    def trigonometric_features(data, dict_column: dict = None, return_df: bool = True):
        if dict_column is None:
            dict_column = {'month': 12, 'day': 30}
        sin_f = [(f'{i}_sin', ExtractTime.sin_transformer(v), [i]) for i, v in dict_column.items()]
        cos_f = [(f'{i}_cos', ExtractTime.cos_transformer(v), [i]) for i, v in dict_column.items()]
        ct = ColumnTransformer(transformers=sin_f + cos_f)
        col = [i[0] for i in sin_f + cos_f]
        df_trigonometric = pl.DataFrame(ct.fit_transform(data), schema=col)
        if return_df:
            return df_trigonometric
        else:
            return ct

    @staticmethod
    def date_time_features(df: pl.DataFrame, col: str = 'grass_date') -> pl.DataFrame:
        return (
            df
            .with_columns(
                pl.col(col).dt.year().alias('year').cast(pl.Int16),
                pl.col(col).dt.month().alias('month').cast(pl.Int8),
                pl.col(col).dt.day().alias('day').cast(pl.Int8),
                pl.col(col).dt.weekday().alias('weekday').cast(pl.Int8),
            )
            .with_columns(
                (pl.col('month') - pl.col('day')).alias('days_dif_spike')
            )
        )

    @staticmethod
    def trend(df: pl.DataFrame, col: list, index_column: str = 'grass_date', period: str = '3d') -> pl.DataFrame:
        return df.with_columns(
            pl.mean(i).rolling(index_column=index_column, period=period, closed='left').alias(f'trend_{period}_{i}')
            for i in col
        )

    @staticmethod
    def season(df: pl.DataFrame, col: list, period: str = '3d') -> pl.DataFrame:
        return df.with_columns(
            (pl.col(i) - pl.col(f'trend_{period}_{i}')).alias(f'season_{period}_{i}') for i in col
        )

    @staticmethod
    def lag(df: pl.DataFrame, col: list, window: int = 7) -> pl.DataFrame:
        return df.with_columns(
            pl.col(i).shift(window).alias(f'shift_{window}d_{i}') for i in col
        )


class EDA:

    @staticmethod
    def group_by_describe(col: str, percentiles: list = None) -> list:
        """
        Use in polars
        Ex: df.group_by(pl.col('date')).agg(*group_by_describe("a"), *group_by_describe("b"))
        :param col: 'a'
        :param percentiles: [.25, .5]
        :return: list of exp
        """
        if not percentiles:
            percentiles = [.25, .5, .75]
        lst = [
            pl.col(col).count().alias(f"{col}_count"),
            pl.col(col).is_null().sum().alias(f"{col}_null_count"),
            pl.col(col).mean().alias(f"{col}_mean"),
            pl.col(col).std().alias(f"{col}_std"),
            pl.col(col).min().alias(f"{col}_min"),
            pl.col(col).max().alias(f"{col}_max"),
        ]
        lst_quantile = [
            pl.col(col).quantile(i).alias(f"{col}_{int(i*100)}th") for i in percentiles
        ]
        return lst + lst_quantile

    @staticmethod
    def plot_correlation(data, figsize: tuple = (10, 6), save_path: Path = None):
        if isinstance(data, pl.DataFrame):
            data = data.to_pandas()
        fig, ax = plt.subplots(figsize=figsize)
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        sns.heatmap(data.corr(), cmap=cmap, annot=True, linewidths=.5, fmt=",.2f")
        fig.show()
        if save_path:
            fig.savefig(save_path)


class PipelineClassification:
    def __init__(self, x_train, y_train, x_test, y_test, target_names: list = None):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.target_names = target_names

    @staticmethod
    def feature_importance(model_input, all_features: list) -> pl.DataFrame:
        zip_ = zip(all_features, model_input.feature_importances_)
        data = (
            pl.DataFrame(zip_, schema=['feature', 'contribution'])
            .sort('contribution', descending=True)
        )
        return data

    @staticmethod
    def report(y_test, y_pred, target_names: list = None, print_report: bool = True) -> pl.DataFrame:
        if print_report:
            print(classification_report(y_test, y_pred))

        # export report to dataframe
        dict_report = classification_report(y_test, y_pred, output_dict=True, target_names=target_names)
        report_full = pl.DataFrame()
        for _ in dict_report.keys():
            if _ == 'accuracy':
                continue
            tmp = (
                pl.DataFrame(dict_report.get(_))
                .with_columns(pl.lit(_).alias('name'))
            )
            report_full = pl.concat([report_full, tmp])

        col = ['name', 'accuracy', 'f1-score', 'precision', 'recall', 'support']
        report_full = (
            report_full
            .with_columns(pl.lit(dict_report.get('accuracy')).alias('accuracy'))
            .select(col)
        )

        return report_full

    def xgb(
            self,
            report_output: bool = True,
            params: dict = None,
            use_rf: bool = None,
            early_stopping_rounds: int = 50,
    ):
        # params
        if not params:
            params = {
                'objective': 'binary:logistic',
                'metric': 'auc',
                'random_state': 42,
                'device': 'cuda',
            }
        if use_rf:
            params = {
                'colsample_bynode': 0.8,
                'learning_rate': 1,
                'max_depth': 5,
                'num_parallel_tree': 100,
                'objective': 'binary:logistic',
                'subsample': 0.8,
                'tree_method': 'hist',
                'device': 'cuda',
            }
        # train
        self.xgb_model = XGBClassifier(**params)
        self.xgb_model.fit(
            self.x_train, self.y_train,
            eval_set=[(self.x_test, self.y_test)],
            early_stopping_rounds=early_stopping_rounds
        )
        # predict
        self.pred = self.xgb_model.predict(self.x_test)
        # report
        report = None
        if report_output:
            report = self.report(self.y_test, self.pred, target_names=self.target_names)
        return self.xgb_model, report


class PipelineRegression:
    def __init__(self, x_train, y_train, x_test, y_test, target_names: list = None):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.target_names = target_names

    @staticmethod
    def feature_importance(model_input, all_features: list) -> pl.DataFrame:
        zip_ = zip(all_features, model_input.feature_importances_)
        data = (
            pl.DataFrame(zip_, schema=['feature', 'contribution'])
            .sort('contribution', descending=True)
        )
        return data

    def xgb(
            self,
            params: dict = None,
    ):
        # params
        if not params:
            params = {
                'metric': 'mse',
                'random_state': 42,
                'device': 'cuda',
            }
        # train
        self.xgb_model = XGBRegressor(**params)
        self.xgb_model.fit(
            self.x_train, self.y_train,
            eval_set=[(self.x_test, self.y_test)],
        )
        # predict
        self.pred = self.xgb_model.predict(self.x_test)
        # report
        return self.xgb_model
