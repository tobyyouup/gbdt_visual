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
if not "./" in sys.path:
    sys.path.append("./")
if not 'BinaryTree' in sys.modules:
    from BinaryTree import *

import pygraphviz as pgv

debug = 3


def dump_txt(model_file):
    tmp=''
    flag =0
    for line in open(model_file):
        if flag == 0:
            flag=1
            continue
        line = line.replace('\t', '')
        tmp = tmp + line
    trees = re.split('booster\[\d+\]:', tmp)     
    # split into trees
    if debug==4:
        print('trees:', len(trees))

    node = r'(\d+):\[([\w\d]+)<(.+)\]\s+yes=(\d+),no=(\d+),missing=(\d+)'
    node_matcher = re.compile(node)

    leaf = r'(\d+):leaf=(.*)'
    leaf_matcher = re.compile(leaf)

    feature_name_set = set()
    elem_list = []
    for idx, tree in enumerate(trees):
        elem_list.append((0, idx, None, None, None, None, None, None))  # None to generate tree
        for l in tree.strip('\n').split('\n'):
            if debug==4:
                print(l)
            if l.find('leaf') >= 0:
                nodeid, value = leaf_matcher.search(l).groups()
                # type, treeid, nodeid, feature_name, value, yes, no, missing
                # for leaf
                # type, treeid, nodeid, None, value, next_treeid, None, None
                elem_list.append((1, idx, nodeid, None, value, idx + 1, None, None))
                if debug==4:
                    print("nodeid", nodeid, "value", value)
            else:  # node
                nodeid, feature_name, value, yes_idx, no_idx, missing_idx = node_matcher.search(l).groups()
                if debug==4:
                    print("nodeid", nodeid, "feature_name", feature_name, "value", value, "yes_idx", yes_idx, "no_idx", no_idx, "missing_idx", missing_idx)

                feature_name_set.add(feature_name)
                # type, treeid, feature_name, value, yes, no, missing
                elem_list.append((2, idx, nodeid, feature_name, value, yes_idx, no_idx, missing_idx))
    elem_list.append((0, len(trees), None, None, None, None, None, None))
    return elem_list,len(trees)

def get_tree(tree_id, node_info, feature_list, sample, is_inpath):

    node = Node()
    node.attr = {'color' : '#00FFFF', 'style' : 'filled'}
    node.leftEdgeAttr = {'color' : 'green', 'penwidth' : '2.5', 'label' : 'yes'}
    node.rightEdgeAttr = {'color' : 'green', 'penwidth' : '2.5', 'label' : 'no'}
    if node_info[0] == 1:
		node.attr['shape'] = 'box'
		node.attr['label'] = str(node_info[4])
		if is_inpath:
			node.attr['color'] = 'red'
			print (node.attr['label'])
		return node

    feature_name = feature_list[int(node_info[3][1:])]
    #feature_name = node_info[3]
    label = '%s\l < %s ?'%(feature_name, node_info[4])
    node.attr['label'] = label

    
    if is_inpath:
        l = sample[int(node_info[3][1:])] < float(node_info[4])
        r = 1 - l
        if l:
			#print (sample[int(node_info[3][1:])])
			#print (node_info[3][1:])
			label = '%s\l %f < %s ?'%(feature_name, sample[int(node_info[3][1:])], node_info[4])
			node.attr['label'] = label
			node.attr['color'] = 'red'
			node.leftEdgeAttr['color'] = 'red'
        else:
            label = '%s\l %f < %s ?'%(feature_name, sample[int(node_info[3][1:])], node_info[4])
            node.attr['label'] = label
            node.attr['color'] = 'red'
            node.rightEdgeAttr['color'] = 'red'
    else:
        l = r = 0

    node.left = get_tree(tree_id, node_map[str(tree_id)+'_'+str(node_info[5])], feature_list, sample, l)
    node.right = get_tree(tree_id, node_map[str(tree_id)+'_'+str(node_info[6])], feature_list, sample, r)

    return node

def get_feature(feature_file):
    tmp = ''
    for line in open(feature_file):
        line = line.strip().replace(' ','')
        tmp = tmp + line
    feature_list = [str(i) for i in tmp.split(',')] 
    return feature_list

def get_sample(sample_file):
    
    line = sample_file.strip().replace(' ','')
    sample = [float(i) for i in line.split(',')] 
    return sample



if len(sys.argv) == 4:
    #print 'usage:<model_file><feature_file><sample>'
    #exit(1)
    model_file, feature_file, sample_file = sys.argv[1:]
else:
    model_file=''
    feature_file=''
    sample_file=''
#print len(sys.argv)

if debug==4:
    print model_file + '####'
    print feature_file + '####'
    print sample_file + '####'


if model_file == '':
    model_file_path = '/var/www/html/visual/gbdt_visual/relevanceModelXG_raw.all'
else:
    model_file_path = '/var/www/html/visual/model_file/' + model_file

if feature_file == '':
    feature_list = ['price','weight','IS_CLICK_BY_USER','IS_ORDER_BY_USER','IS_FOLLOW_BY_USER','match_count','match_ratio','q_query_complete_ratio','q_query_ctr','q_query_cvr','q_query_order_stk','q_query_view','qs_query_wid_complete_ratio','qs_query_wid_ctr','qs_query_wid_cvr','qs_query_wid_order_stk','qs_query_wid_view','qs_query_brand_complete_ratio','qs_query_brand_ctr','qs_query_brand_cvr','qs_query_brand_order_stk','qs_query_brand_view','qs_query_cid1_complete_ratio','qs_query_cid1_ctr','qs_query_cid1_cvr','qs_query_cid1_order_stk','qs_query_cid1_view','qs_query_cid2_complete_ratio','qs_query_cid2_ctr','qs_query_cid2_cvr','qs_query_cid2_order_stk','qs_query_cid2_view','qs_query_cid3_complete_ratio','qs_query_cid3_ctr','qs_query_cid3_cvr','qs_query_cid3_order_stk','qs_query_cid3_view','qs_query_shop_complete_ratio','qs_query_shop_ctr','qs_query_shop_cvr','qs_query_shop_order_stk','qs_query_shop_view','s_wid_complete_ratio','s_wid_ctr','s_wid_cvr','s_wid_order_stk','s_wid_view','s_brand_complete_ratio','s_brand_ctr','s_brand_cvr','s_brand_order_stk','s_brand_view','s_cid1_complete_ratio','s_cid1_ctr','s_cid1_cvr','s_cid1_order_stk','s_cid1_view','s_cid2_complete_ratio','s_cid2_ctr','s_cid2_cvr','s_cid2_order_stk','s_cid2_view','s_cid3_complete_ratio','s_cid3_ctr','s_cid3_cvr','s_cid3_order_stk','s_cid3_view','s_shop_complete_ratio','s_shop_ctr','s_shop_cvr','s_shop_order_stk','s_shop_view','sa_wid_follow','sa_wid_addcart','sa_wid_good_comm_clean','sa_wid_good_comm','sa_wid_pv_clean','sa_wid_order_stk_clean','sa_wid_good_comm_ratio_clean','sa_wid_good_comm_ratio','sa_wid_complete_ratio','sa_cid3_follow','sa_cid3_addcart','sa_cid3_good_comm_clean','sa_cid3_good_comm','sa_cid3_pv_clean','sa_cid3_order_stk_clean','sa_cid3_good_comm_ratio_clean','sa_cid3_good_comm_ratio','sa_cid3_complete_ratio','sa_cid2_follow','sa_cid2_addcart','sa_cid2_good_comm_clean','sa_cid2_good_comm','sa_cid2_pv_clean','sa_cid2_order_stk_clean','sa_cid2_good_comm_ratio_clean','sa_cid2_good_comm_ratio','sa_cid2_complete_ratio','sa_cid1_follow','sa_cid1_addcart','sa_cid1_good_comm_clean','sa_cid1_good_comm','sa_cid1_pv_clean','sa_cid1_order_stk_clean','sa_cid1_good_comm_ratio_clean','sa_cid1_good_comm_ratio','sa_cid1_complete_ratio','sa_shop_follow','sa_shop_addcart','sa_shop_good_comm_clean','sa_shop_good_comm','sa_shop_pv_clean','sa_shop_order_stk_clean','sa_shop_good_comm_ratio_clean','sa_shop_good_comm_ratio','sa_shop_complete_ratio','sa_brand_follow','sa_brand_addcart','sa_brand_good_comm_clean','sa_brand_good_comm','sa_brand_pv_clean','sa_brand_order_stk_clean','sa_brand_good_comm_ratio_clean','sa_brand_good_comm_ratio','sa_brand_complete_ratio']
else:
    feature_list = get_feature('/var/www/html/visual/model_file/' + feature_file)          

if sample_file == '':
    sample = [49.0,878,0,0,0,0.0,0.0,0.5886524822695035,0.01007749837144013,8.330999649696521E-5,77.0,996278.0,0.0,0.0,0.0,0.0,0.0,0.512396694214876,0.010821347647939602,9.128211621391228E-5,59.0,679212.0,0.49122807017543857,0.008672298427140695,3.574100028848093E-5,23.0,783413.0,0.5102040816326531,0.009019589332074581,4.720320981826764E-5,20.0,529624.0,0.4883720930232558,0.009337527757216876,7.7720207253886E-5,17.0,270199.0,0.6428571428571429,0.013555787278415016,1.4896469536719798E-4,6.0,60416.0,0.0,0.0,0.0,0.0,0.0,0.5996236179722418,0.012829533477561435,2.827980251844456E-4,2446.0,9013499.0,0.5101328633647141,0.08962641512795905,0.001186184882235155,894498.0,7.72576866E8,0.3285774482822191,0.011157233471238438,8.021888050667894E-5,49685.0,6.22110401E8,0.6334291187739464,0.013352407868228135,2.89453324086701E-4,6446.0,2.2846515E7,0.5171102661596958,0.015564555125725339,2.9358938933407016E-4,124.0,463231.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0,16412.0,98800.0,35145.0,57507.0,1029462.0,35032.0,0.9421257204128133,0.9631378854109096,0.9897149405529294,393344.0,1112266.0,179348.0,357812.0,2.8900747E7,417537.0,0.9238412642813727,0.9594590971008119,1.0573712690860235,3007430.0,9363723.0,1775980.0,3015886.0,2.2344258E8,4096332.0,0.926223621771286,0.9543387491555083,1.050103966891084,410.0,1612.0,274.0,276.0,30090.0,991.0,0.8785942492012779,0.8793650793650793,0.9036511156186613,6126.0,27810.0,7002.0,7237.0,410538.0,15473.0,0.9382368703108253,0.9396339088666753,1.1147477108903177]
else:
    sample = get_sample(sample_file)
    #print sample

#bst = pickle.load(open('result/relevanceModelXG.all', 'rb'))
#node_list = dump_txt(bst, 'result/text_model', feature_list)
node_list, tree_num = dump_txt(model_file_path)
node_map = {}
for elem in node_list:
    tree_id = elem[1]
    node_id = elem[2]
    node_map[str(tree_id)+'_'+str(node_id)]= elem 


btree = BinaryTree()



tree_id = 0
node_id = 0
node = Node()
node.attr = {'color' : 'white', 'shape':'box', 'label':'I am a little decision tree'}
btree.root = node
node.left = get_tree(tree_id, node_map[str(tree_id)+'_'+str(node_id)], feature_list, sample, 1)

if model_file == '':
    os.popen('rm -rf ../png/default')
    os.popen('mkdir ../png/default')      
    png_out = '../png/default'
else:
    os.popen('rm -rf ../png/' + model_file)     
    os.popen('mkdir ../png/' + model_file)      
    png_out = '../png/' + model_file

writer = TreeWriter(btree)
writer.Write(png_out + '/tree0.png')

for i in range(1,tree_num):
    btree = BinaryTree()
    tree_id = i
    node_id = 0
    btree.root = get_tree(tree_id, node_map[str(tree_id)+'_'+str(node_id)], feature_list, sample, 1)
    writer = TreeWriter(btree)
    writer.Write(png_out + '/tree' + str(i) + '.png')



