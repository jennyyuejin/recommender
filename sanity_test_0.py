import sys

import recsys.algorithm
recsys.algorithm.VERBOSE = True

from recsys.algorithm.factorize import SVD, SVDNeighbourhood
from recsys.datamodel.item import Item
from recsys.datamodel.user import User
from recsys.datamodel.data import Data
from recsys.evaluation.prediction import RMSE, MAE


#Evaluation using prediction-based metrics
def evaluate(_svd, _testData, verbose=False):
    global rmse, mae, rating, item_id, user_id, pred_rating
    rmse = RMSE()
    mae = MAE()
    for rating, item_id, user_id in _testData.get():
        try:
            pred_rating = _svd.predict(item_id, user_id, MIN_VALUE=0, MAX_VALUE=10)
            rmse.add(rating, pred_rating)
            mae.add(rating, pred_rating)

            if verbose:
                print item_id, user_id, rating, pred_rating
        except Exception as e:
            print 'ERROR occurred:', e.message

    print 'RMSE=%s' % rmse.compute()
    print 'MAE=%s' % mae.compute()


if __name__ == '__main__':

    #Dataset
    PERCENT_TRAIN = 100
    data = Data()
    data.load('/Users/jennyyuejin/recommender/Data/test_0/userProd.data',
              sep='\t',
              format={'col':0, 'row':1, 'value':2, 'ids':int})

    #Train & Test data
    train, test = data.split_train_test(percent=PERCENT_TRAIN, shuffle_data=True)
    print len(train), 'training data points;', len(test), 'testing data points'

    itemId = 0
    item = Item(itemId)
    item.add_data({'name': 'project0',
                   'popularity': 0.5,
                   'tags': [0, 0, 1]
    })

    itemId = 1
    item2 = Item(itemId)
    item2.add_data({'name': 'project1',
                   'popularity': 0.9,
                   'tags': [0, 0, 1]
    })




    #Create SVD
    K=100
    svd = SVD()
    svd.set_data(train)
    svd.compute(k=K, min_values=None, pre_normalize=None, mean_center=True, post_normalize=True)

    # save
    # svd.set_data(None)  # clear data before saving
    # pickle.dump(svd, open('./model/svd.obj', 'w'))
    svd.save_model('./model/svd.obj.zip',
                   {'k': K, 'min_values': 5,
                    'pre_normalize': None, 'mean_center': True, 'post_normalize': True})


    # similarity between items x and y
    print '-------- SIMILARITIES:'
    for prodid1 in [0, 1, 3, 4]:
        for prodid2 in [0, 1, 3, 4]:
            print prodid1, prodid2, svd.similarity(prodid1, prodid2)

    # similar to item x
    # svd.similar(1)
    #
    # # predict ratings
    # evaluate(svd, test, True)
    #
    # # recommend products to a user
    # for userid in [0, 1, 2]:
    #     print 'User #', userid
    #     print svd.recommend(userid, is_row=False, only_unknowns=True)
    #
    # # which users should use a given product?
    # for prodid in [0, 1, 3, 4]:
    #     print 'Product #', prodid
    #     print svd.recommend(prodid, only_unknowns=True)