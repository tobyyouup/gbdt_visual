####### coding=utf-8
####-*- coding: UTF-8 -*-
# coding=utf-8
# this file is used to run the model and select specific features
# run_model.py train_file_dir test_file_dir feature include
# raw version:
#from __future__ import print_function
import sys
import re
import os
import codecs

def data_ready(feature_dict,model_file_path):

    new_model_file_path = model_file_path + '.new'

    feature_key = feature_dict.keys()
    feature_key = sorted(feature_key)
    feature_value = []
    for key in feature_key:
        feature_value.append(feature_dict[key])

    new_model_wirtef = codecs.open(new_model_file_path, 'w')
    for line in open(model_file_path):
        for key in feature_key:
            if key.lower() + '<' in line:
                line = line.replace(key.lower() + '<', 'f' + str(feature_key.index(key)) + '<')
                break
        new_model_wirtef.write(line)
 
    #print feature_key
    #print feature_value
    return feature_key, feature_value, new_model_file_path 


feature_dict = {'price':4078, 'weight':3870, 'text_weight':0, 'is_exp':0, 'is_same_field':1, 'is_click_by_user':0, 'is_order_by_user':0, 'is_follow_by_user':0, 'is_bhp_click_brand':0, 'is_bhp_follow_brand':0, 'is_bhp_order_brand':0, 'is_bhp_click_shop':0, 'is_bhp_order_shop':0, 'is_majorappliances':1, 'is_ltp':0, 'bm25_12':3.28676105, 'bm25_2':3.00811815, 'match_count':1, 'match_ratio':1, 'q_query_view_15d':247038, 'q_query_click_15d':164385, 'q_query_order_15d':3767, 'q_query_ctr_15d':0.665421247, 'q_query_cvr_15d':0.0152526526, 's_wid_view_15d':295487, 's_wid_click_15d':26492, 's_wid_order_15d':319, 's_wid_ctr_15d':0.0896550789, 's_wid_cvr_15d':0.00108295435, 's_cid3_view_15d':2453262, 's_cid3_click_15d':1295364, 's_cid3_order_15d':38771, 's_cid3_ctr_15d':0.528016746, 's_cid3_cvr_15d':0.0158042572, 's_cid2_view_15d':7413996, 's_cid2_click_15d':4497201, 's_cid2_order_15d':241888, 's_cid2_ctr_15d':0.606582522, 's_cid2_cvr_15d':0.0326259919, 's_brand_view_15d':1628405, 's_brand_click_15d':436642, 's_brand_order_15d':6341, 's_brand_ctr_15d':0.268140733, 's_brand_cvr_15d':0.00389460614, 's_shop_view_15d':1278882, 's_shop_click_15d':314403, 's_shop_order_15d':3981, 's_shop_ctr_15d':0.245841876, 's_shop_cvr_15d':0.00311365467, 'qs_query_wid_view_15d':21593, 'qs_query_wid_click_15d':1347, 'qs_query_wid_order_15d':10, 'qs_query_wid_ctr_15d':0.0623784401, 'qs_query_wid_cvr_15d':0.000509400736, 'qs_query_cid3_view_15d':246918, 'qs_query_cid3_click_15d':164196, 'qs_query_cid3_order_15d':3719, 'qs_query_cid3_ctr_15d':0.664979219, 'qs_query_cid3_cvr_15d':0.0150656691, 'qs_query_cid2_view_15d':246974, 'qs_query_cid2_click_15d':164251, 'qs_query_cid2_order_15d':3753, 'qs_query_cid2_ctr_15d':0.665051103, 'qs_query_cid2_cvr_15d':0.0151999192, 'qs_query_brand_view_15d':220963, 'qs_query_brand_click_15d':53624, 'qs_query_brand_order_15d':374, 'qs_query_brand_ctr_15d':0.24268207, 'qs_query_brand_cvr_15d':0.00169710908, 'qs_query_shop_view_15d':208417, 'qs_query_shop_click_15d':48942, 'qs_query_shop_order_15d':340, 'qs_query_shop_ctr_15d':0.234826162, 'qs_query_shop_cvr_15d':0.00163613504, 'sa_wid_pv':114209, 'sa_wid_order_stk':1733, 'sa_wid_cvr':0.0151738031, 'sa_brand_pv':3525201, 'sa_brand_order_stk':52152, 'sa_brand_cvr':0.0147940461, 'sa_shop_pv':2212401, 'sa_shop_order_stk':33554, 'sa_shop_cvr':0.0151663218, 'sa_wid_follow':2519, 'sa_wid_addcart':7784, 'sa_wid_good_comm':687, 'sa_wid_good_ratio':0.970339, 'sa_wid_good_ratio_clean':0.967987776, 'sa_wid_bad_ratio':0.0197740104, 'sa_brand_follow':439274, 'sa_brand_addcart':1305757, 'sa_brand_good_comm':223091, 'sa_brand_good_ratio':0.954457164, 'sa_brand_good_ratio_clean':0.953700244, 'sa_brand_bad_ratio':0.0266454462, 'sa_shop_follow':332905, 'sa_shop_addcart':874482, 'sa_shop_good_comm':166868, 'sa_shop_good_ratio':0.960905671, 'sa_shop_good_ratio_clean':0.960129619, 'sa_shop_bad_ratio':0.0217900798, }

feature_dict['price'] = 1899

feature_key = feature_dict.keys()
feature_key = sorted(feature_key)
feature_value = []
for key in feature_key:
    feature_value.append(feature_dict[key])
#print str(feature_key)[1:-1].replace(' ','').replace('\'','')
#print str(feature_value)[1:-1].replace(' ','')
