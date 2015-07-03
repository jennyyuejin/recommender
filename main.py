import sys

import recsys.algorithm
recsys.algorithm.VERBOSE = True

from recsys.algorithm.factorize import SVD, SVDNeighbourhood
from recsys.datamodel.data import Data
from recsys.evaluation.prediction import RMSE, MAE


#Evaluation using prediction-based metrics
def evaluate(_svd, _testData):
    global rmse, mae, rating, item_id, user_id, pred_rating
    rmse = RMSE()
    mae = MAE()
    for rating, item_id, user_id in _testData.get():
        try:
            pred_rating = _svd.predict(item_id, user_id)
            rmse.add(rating, pred_rating)
            mae.add(rating, pred_rating)

            # print item_id, user_id, rating, pred_rating
        except KeyError as e:
            print 'ERROR occurred:', e.message

    print 'RMSE=%s' % rmse.compute()
    print 'MAE=%s' % mae.compute()


if __name__ == '__main__':

    #Dataset
    PERCENT_TRAIN = 50
    data = Data()
    data.load('/Users/jennyyuejin/recommender/Data/movieData/u.data',
              sep='\t',
              format={'col':0, 'row':1, 'value':2, 'ids':int})
    # About format parameter:
    #   'row': 1 -> Rows in matrix come from column 1 in ratings.dat file
    #   'col': 0 -> Cols in matrix come from column 0 in ratings.dat file
    #   'value': 2 -> Values (Mij) in matrix come from column 2 in ratings.dat file
    #   'ids': int -> Ids (row and col ids) are integers (not strings)

    #Train & Test data
    train, test = data.split_train_test(percent=PERCENT_TRAIN, shuffle_data=True)
    print len(train), 'training data points;', len(test), 'testing data points'

    #Create SVD
    K=100
    # svd = SVDNeighbourhood()
    svd = SVD()
    svd.set_data(train)
    svd.compute(k=K, min_values=5, pre_normalize=None, mean_center=True, post_normalize=True)

    # save
    # svd.set_data(None)  # clear data before saving
    # pickle.dump(svd, open('./model/svd.obj', 'w'))
    svd.save_model('./model/svd.obj.zip',
        {'k': K, 'min_values': 5,
         'pre_normalize': None, 'mean_center': True, 'post_normalize': True})


    print '------ evaluating original'
    evaluate(svd, test)

    # svd_pred = SVDNeighbourhood()
    svd_pred = SVD()
    svd_pred.load_model('./model/svd.obj.zip')

    print '------ evaluating copy'
    evaluate(svd_pred, test)



