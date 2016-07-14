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
 
    print str(feature_key)[1:-1].replace(' ','').replace('\'','')
    print str(feature_value)[1:-1].replace(' ','')
    return feature_key, feature_value, new_model_file_path 

key=['q_query_click_15d','q_query_ctr_15d','q_query_cvr_15d','q_query_order_15d','q_query_view_15d','qs_query_brand_click_15d','qs_query_brand_order_15d','qs_query_cid3_click_15d','qs_query_cid3_order_15d','qs_query_cid3_view_15d','qs_query_shop_click_15d','qs_query_shop_order_15d','qs_query_wid_click_15d','qs_query_wid_order_15d','s_cid2_click_15d','s_cid2_order_15d','s_cid2_view_15d','s_cid3_click_15d','s_cid3_order_15d','s_cid3_view_15d','s_shop_click_15d','s_shop_order_15d','s_shop_view_15d','sa_wid_addcart','sa_wid_bad_ratio','sa_wid_follow','sa_wid_good_comm','sa_wid_good_ratio','sa_wid_good_ratio_clean','sa_wid_order_stk','text_weight','weight']

value=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1852497.0,277297.0,3197540.0,17884.0,1029.0,60714.0,23146.0,1434.0,111599.0,41.0,0.00865265760197775,119.0,1561.0,0.9647713226205191,0.9641734758013828,5.0,206.0,1432.0]
feature_dict={}
for i in range(len(key)):
    feature_dict[key[i]]=value[i]

data_ready(feature_dict, 'model.text')
