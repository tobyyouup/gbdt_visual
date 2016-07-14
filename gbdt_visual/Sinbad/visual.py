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
if not "../" in sys.path:
    sys.path.append("../")
if not 'BinaryTree' in sys.modules:
    from BinaryTree import *

import pygraphviz as pgv
from data_ready import *
import uuid

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
    return elem_list, len(trees)

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



if len(sys.argv) != 3:
    print 'usage:<model_file><sample>'
    exit(1)
else:
    model_file, feature_dict = sys.argv[1:]
    feature_dict = eval(feature_dict)


feature_list, sample, model_file_path = data_ready(feature_dict, '../../model_file/' + model_file)
#print feature_list
#print sample





node_list, num_tree = dump_txt(model_file_path)
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


for i in range(1, num_tree):
    btree = BinaryTree()
    tree_id = i
    node_id = 0
    btree.root = get_tree(tree_id, node_map[str(tree_id)+'_'+str(node_id)], feature_list, sample, 1)

