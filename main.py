import pandas as pd
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from scipy.stats import norm

import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.inspection import permutation_importance
from sklearn.metrics import r2_score
import random
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.utils import resample
import matplotlib.cm as cm
import matplotlib
import seaborn as sns
# import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 7)
pd.set_option('display.width', 1000)


def one_hot(df, col):
    """One hot encode a given column col"""
    one_hot = pd.get_dummies(df[col])
    df = df.drop(col, axis=1)
    columns = [f"{col}_{i}" for i in range(len(one_hot.columns))]
    one_hot.columns = columns
    df = df.join(one_hot)
    return df


def feature_importance(x, y, model):
    features = x.columns
    model.fit(x, y)

    r = permutation_importance(model, x, y, n_repeats=20, random_state=0)

    for i in r.importances_mean.argsort()[::-1]:
        if r.importances_mean[i] - 2 * r.importances_std[i] > 0:
            print(f"{features[i]:<8}"
                  f"{r.importances_mean[i]:.3f}"
                  f" +/- {r.importances_std[i]:.3f}")


def dimension_reduction(df, dim=3):
    pca = PCA(n_components=dim)
    useful_cols = list(df.columns)
    useful_cols.remove('Rent')
    x = df[useful_cols]
    y = df['Rent']
    df = pd.DataFrame(pca.fit_transform(x))
    df = df.join(y)
    return df


def scale_and_reduce(df):
    """For PCA, some columns need to be scaled"""
    cols_to_keep = list(df.columns)
    cols_to_keep.remove('Rent')
    df_1 = df[cols_to_keep]
    scaled = preprocessing.scale(df_1)
    df_1_s = pd.DataFrame(scaled, columns=cols_to_keep)
    df = df.drop(cols_to_keep, axis=1)
    return df.join(df_1_s)


def bin_rent(df, bin_size=10):
    y = np.array(df['Rent'])
    y_1 = np.sort(y)
    buckets = [np.percentile(y_1, i) for i in range(0, 100, bin_size)]
    y = np.digitize(y, buckets)
    df['Rent'] = y
    return df


# def bin_year(df, bin_size=80):
#     y = np.array(df['Year Built'])
#     y_1 = np.sort(y)
#     buckets = [np.percentile(y_1, i) for i in range(0, 100, bin_size)]
#     y = np.digitize(y, buckets)
#     df['Year Built'] = y
#     return df


def view_pca(df):
    """Generates a 1d,2d or 3d scatter plot of attributes with respect to price"""
    dim = 3
    y = df['Rent']
    df = bin_rent(df)
    df = scale_and_reduce(df)
    df = dimension_reduction(df, dim)

    colors = cm.rainbow(np.linspace(0, 1, 10))

    if dim == 2:
        for index, row in df.iterrows():
            plt.scatter(row[0], row[1], color=colors[int(row['Rent']) - 1])

    elif dim == 3:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for _, row in df.iterrows():
            ax.scatter(row[0], row[1], row[2], color=colors[int(row['Rent']) - 1])

    plt.show()


def get_data():
    rent100 = r"C:\Users\ggoh2\Documents\rent100a.csv"
    rent596 = r"C:\Users\ggoh2\Documents\rent596.csv"

    train_df = pd.read_csv(rent596)
    test_df = pd.read_csv(rent100)

    return train_df, test_df


def regression1(train):
    train_X, train_Y = train[list(set(train.columns) - {'Rent'})], train['Rent']
    # Create linear regression object
    regr = LinearRegression()
    # Train the model using the training sets
    regr.fit(train_X, train_Y)
    return regr


def regression2(train):
    train_X, train_Y = train[list(set(train.columns) - {'Rent'})], train['Rent']
    train['Rent square'] = train['Sq Feet (in 100s)'] ** (2)
    # Create linear regression object
    regr = LinearRegression()
    # Train the model using the training sets
    regr.fit(train_X, train_Y)
    return regr


def eval_model(regressor, test):
    test_X, test_Y = test[list(set(train.columns) - {'Rent'})], test['Rent']

    # Make predictions using the testing set
    pred = regressor.predict(test_X)

    # The coefficients
    print("Coefficients: \n", regressor.coef_)
    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(test_Y, pred))
    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(test_Y, pred))

    # Plot outputs
    # plt.scatter(test_X, test_Y, color="black")
    # plt.plot(test_X, test_Y, color="blue", linewidth=3)

    # plt.xticks(())
    # plt.yticks(())
    #
    # plt.show()


def cross_validate_model(df, model, cv=5):
    x, y = df[list(set(train.columns) - {'Rent'})], df['Rent']
    scores = cross_val_score(model, x, y, cv=cv, scoring='explained_variance')
    print(f"Model has an explained variance score of {np.mean(scores)}")


def manual_cross_validate(df, col1, col2):
    plt.scatter(df[col1], df[col2])
    plt.show()


"""

TODO 

look at variable correlations (remove highly correlated)
 


"""

if __name__ == '__main__':
    train, test = get_data()

    # train = one_hot(train, 'Air Conditioning')
    train['Rent square'] = train['Sq Feet (in 100s)'] ** (1/2)
    train['Year Built'] = train['Year Built'] - min(train['Year Built'])
    feature_importance(train[list(set(train.columns) - {'Rent', 'Air Conditioning', 'Parking'})], train['Rent'], LinearRegression())
    cross_validate_model(train, LinearRegression())
    view_pca(train)

    # for i in train.columns:
    #     print(i, 'Rent')
    #     manual_cross_validate(train, i, 'Rent')
    # plt.figure(figsize=(12, 10))
    # t = train[list(set(train.columns) - {'Rent'})]
    # cor = t.corr()
    # sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
    # plt.show()

    # print(train)
    # regressor = regression1(train)
    # eval_model(regressor, test)
