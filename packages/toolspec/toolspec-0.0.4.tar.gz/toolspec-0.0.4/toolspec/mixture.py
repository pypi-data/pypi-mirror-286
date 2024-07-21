# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
from tqdm import tqdm
import pandas as pd
import numpy as np

class Concurrent:
    def __init__(self, n_pro, func, *args):
        self.n_pro = n_pro
        self.q_in = Queue(maxsize=-1)
        self.q_out = Queue(maxsize=-1)
        self.counter = 0
        self.p_list = []
        for i in range(self.n_pro):
            p = Process(func, self.q_in, self.q_out, *args, daemon=True)
            self.p_list.append(p)
            p.start()
    def put(self, input_list):
        for input in input_list:
            self.q_in.put(input)
            self.counter += 1
    def get(self):
        while self.check():
            try:
                output = self.q_out.get(timeout=1)
                self.counter -= 1
                return output
            except:
                continue
    def check(self):
        if sum([0 if p.alive() else 1 for p in self.p_list]) > 0:
            self.exit()
            raise('RuntimeError')
        return True
    def empty(self):
        return True if self.counter == 0 else False
    def overload(self):
        return True if self.counter >= self.n_pro else False
    def exit(self):
        self.q_out.close()
        for p in self.p_list:
            p.terminate()
            p.join()
    def __del__(self):
        self.exit()

def feature_processing(data, var_list , min_value=0, max_value=1, fill_else=np.nan, decimal=3):
    def limit(x):
        return x if x >= min_value and x <= max_value else fill_else
    for var in tqdm(var_list):
        data[var] = data[var].astype('float').apply(limit).round(decimal)

def target_processing(data, target_region, fill_na=0, fill_else=np.nan):
    for target in tqdm(list(target_region.keys())):
        data[target].fillna(fill_na,inplace=True)
        data.loc[~data.query(target_region[target]).index, target] = fill_else

def define_index(data, cnt_field, target_list, sample_weight):
    index_list = ['cnt']
    data['cnt'] = (data[cnt_field] >= 0) * 1
    for target in target_list:
        index_list += ['cnt_%s' % target, 'sum_%s' % target]
        if target in sample_weight.keys():
            weight = sample_weight[target]
            if type(weight) == str:
                data['cnt_%s' % target] = (data[target] >= 0) * data[weight]
                data['sum_%s' % target] = (data[target] >= 0) * data[weight] * data[target]
            else:
                data['cnt_%s' % target] = (data[target] >= 0) * data[weight[0]]
                data['sum_%s' % target] = (data[target] >= 0) * data[weight[1]] * data[target]
        else:
            data['cnt_%s' % target] = (data[target] >= 0) * 1
            data['sum_%s' % target] = (data[target] >= 0) * data[target]
    return index_list

def evaluate_gap(data, target_list, target_min_dict, target_max_dict, target_weight, method):
    for target in target_list:
        data['avg_%s' % target] = data['sum_%s' % target] / data['cnt_%s' % target]
        data['gap_%s' % target] = 0
        if target in target_min_dict.keys():
            data['gap_%s' % target] += (data['avg_%s' % target] - target_min_dict[target]) * (data['avg_%s' % target] > target_min_dict[target])
        if target in target_max_dict.keys():
            data['gap_%s' % target] += (target_max_dict[target] - data['avg_%s' % target]) * (data['avg_%s' % target] < target_max_dict[target])
        data['gap_%s' % target] = data['gap_%s' % target] * (target_weight[target] if target in target_weight.keys() else 1)
    data['gap'] = data[['gap_%s' % target for target in target_list]].apply(method, axis=1)
    return data['gap']

def single_cutting(data, var, cnt_field, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None):
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    index_list = define_index(data, cnt_field, target_list, sample_weight)
    data['value'] = data.eval(var).round(3)
    grouped = data.groupby(by='value',as_index=False)[index_list].sum()
    ascending_list = [ascending] if ascending else [True, False]
    result = pd.DataFrame()
    for ascending in ascending_list:
        temp = grouped.sort_values(by='value',ascending=ascending)
        temp['direction'] = '<' if ascending == True else '>'
        temp['cutoff'] = (temp['value'] + temp['value'].shift(-1)) / 2
        temp[index_list] = temp[index_list].cumsum()
        temp['gap'] = evaluate_gap(temp, target_list, target_min_dict, target_max_dict, target_weight, method)
        result = result.append(temp,ignore_index=True)
    result = result[result['cnt'] >= cnt_req].sort_values(by='cnt',ascending=True).drop_duplicates(subset='direction',keep='first')
    result = result[-np.isnan(result['cutoff'])]
    cutoff = result.sort_values(by='gap',ascending=True).iloc[:1]
    cutoff['var'] = var
    return cutoff

def couple_cutting(data, var_couple, cnt_field, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None, pct_single=0):
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    index_list = define_index(data, cnt_field, target_list, sample_weight)
    var1, var2 = var_couple[1], var_couple[2]
    data['value1'] = data.eval(var1).round(3)
    data['value2'] = data.eval(var2).round(3)
    mesh = pd.merge(data[['cnt','value1']].drop_duplicates(), data[['cnt','value2']].drop_duplicates(), how='inner', on=['cnt'])[['value1','value2']]
    grouped = mesh.merge(data.groupby(by=['value1','value2'],as_index=False)[index_list].sum(), how='left', on=['value1','value2']).fillna(0)
    ascending_list = [(ascending,ascending)] if ascending else [(True,True),(True,False),(False,True),(False,False)]
    result = pd.DataFrame()
    for ascending in ascending_list:
        temp = grouped.sort_values(by='value1',ascending=ascending[0])
        temp['direction1'] = '<' if ascending[0] == True else '>'
        temp['direction2'] = '<' if ascending[1] == True else '>'
        temp['cutoff1'] = (temp['value1'] + temp.groupby(by='value2')['value1'].shift(-1)) / 2
        temp[index_list] = temp.groupby(by='value2')[index_list].cumsum()
        temp = temp.sort_values(by='value2',ascending=ascending[1])
        temp['cutoff2'] = (temp['value2'] + temp.groupby(by='value1')['value2'].shift(-1)) / 2
        temp[index_list] = temp.groupby(by='value1')[index_list].cumsum()
        temp['gap'] = evaluate_gap(temp, target_list, target_min_dict, target_max_dict, target_weight, method)
        result = result.append(temp,ignore_index=True)
    result = result.merge(grouped.groupby(by='value1',as_index=False)['cnt'].sum(), how='inner', on='value1', suffixes=('','_1'))
    result = result.merge(grouped.groupby(by='value2',as_index=False)['cnt'].sum(), how='inner', on='value2', suffixes=('','_2'))
    result['pct_1'] = (result['cnt_2'] - result['cnt']) / (grouped['cnt'].sum() - result['cnt'])
    result['pct_2'] = (result['cnt_1'] - result['cnt']) / (grouped['cnt'].sum() - result['cnt'])
    result = result[result['cnt'] >= cnt_req].sort_values(by='cnt',ascending=True).drop_duplicates(subset=['direction1','direction2','value1'],keep='first')
    result = result[(-np.isnan(result['cutoff1'])) & (-np.isnan(result['cutoff2']))]
    result = result[(result['pct_1'] >= pct_single) & (result['pct_2'] >= pct_single)]
    cutoff = result.sort_values(by='gap',ascending=True).iloc[:1]
    cutoff['var1'] = var1
    cutoff['var2'] = var2
    return cutoff

def multiple_cutting(data, var_list, cnt_field, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None, pct_single=0, var_min=5, var_max=10, min_gain=0, n_pro=30):
    def subtask(q_in, q_out, data, var_cutoff, cnt_field, cnt_req, cnt_tol, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, pct_single, var_min, var_max):
        while 1:
            try:
                input = q_in.get(timeout=1)
            except:
                continue
            data['flag'] = 1
            for var in var_cutoff.keys():
                if var not in input:
                    direciton, cutoff = var_cutoff[var]
                    data['flag'] = data['flag'] * ((data[var] < cutoff) if direction == '<' else (data[var] > cutoff))
            if len(input) == 1:
                var = input[0]
                cutoff = single_cutting(data.query('flag == 1'), var, cnt_field, cnt_req, target_min_dict= target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending)
            else:
                var_couple = (input[0],input[1])
                cutoff = couple_cutting(data.query('flag == 1'), var_couple, cnt_field, cnt_req, target_min_dict= target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending, pct_single=pct_single)
            var_num = len(set(list(var_cutoff.keys()+input)))
            cutoff['gap_adj'] = cutoff['gap'] + 10 * (cutoff['cnt'] - cnt_req) / cnt_tol + 100 * (var_min - var_num) * (var_num < var_min) + 100 * (var_num - var_max) * (var_num > var_max)
            q_out.put(cutoff)
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    _ = define_index(data, cnt_field, target_list, sample_weight)
    cnt_tol = data['cnt'].sum()
    var_cutoff = {}
    def calculate(input_list):
        con = Concurrent(n_pro, subtask, data, var_cutoff, cnt_field, cnt_req, cnt_tol, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, pct_single, var_min, var_max)
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        con.exit()
        return result
    gap_min = np.inf
    while 1:
        if len(var_cutoff) == 0:
            input_list = [(var,) for var in var_list]
        else:
            input_list = []
            var_list_1 = list(var_cutoff.keys())
            for i,var1 in enumerate(var_list_1):
                input_list += [(var1,var2) for j,var2 in enumerate(var_list_1) if j > i]
                input_list += [(var1,var2) for var2 in var_list if var2 not in var_list_1]
        result = calculate(input_list)
        if not result.empty:
            opt = result.sort_values(by='gap_adj',ascending=True).iloc[0]
            if opt['gap_adj'] > gap_min-min_gain:
                break
            gap_min = opt['gap_adj']
            if 'var' in opt.index:
                var_cutoff[opt['var']] = (opt['direction'],opt['cutoff'])
            else:
                var_cutoff[opt['var1']] = (opt['direction1'],opt['cutoff1'])
                var_cutoff[opt['var2']] = (opt['direction2'],opt['cutoff2'])
        else:
            break
    result = []
    for var in var_cutoff.keys():
        data['cnt1'] = data['cnt']
        for i in var_cutoff.keys():
            if i != var:
                direction, cutoff = var_cutoff[i]
                data['cnt1'] = data['cnt1'] * ((data[i] < cutoff) if direction == '<' else (data[i] > cutoff))
        direction, cutoff = var_cutoff[var]
        data['cnt2'] = data['cnt'] * (data[var] < cutoff) if direction == '<' else (data[var] > cutoff)
        pct_self = (data['cnt'].sum() - data['cnt2'].sum()) / (data['cnt'].sum() - data.eval('cnt1*cnt2').sum())
        pct_gain = (data['cnt1'].sum() - data.eval('cnt1*cnt2').sum()) / (data['cnt'].sum() - data.eval('cnt1*cnt2').sum())
        result.append([var,direction,cutoff,pct_self,pct_gain])
    var_cutoff = pd.DataFrame(columns=['var','direction','cutoff','pct_self','pct_gain'], data=result).sort_values(by='pct_gain',ascending=False).reset_index(drop=True)
    return var_cutoff

def multiple_grouping(data, var_list, cnt_field, tab_conf, sample_weight={}, target_weight={}, method='sum', ascending=False, pct_single=0, var_min=5, var_max=10, min_gain=0, reverse=False, n_pro=30):
    target_min_list = [column.replace('min_','') for column in tab_conf.columns if 'min_' in column]
    target_max_list = [column.replace('max_','') for column in tab_conf.columns if 'max_' in column]
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    tab_copy = tab_conf.sort_values(by='id',ascending=True)
    if reverse == True:
        index_list = [column for column in tab_copy.columns if 'min_' in column or 'max_' in column]
        tab_copy[index_list] = tab_copy[index_list] * tab_copy['pct']
        tab_copy[index_list] = tab_copy[index_list].cumsum()
        tab_copy['pct'] = tab_copy['pct'].cumsum()
        tab_copy[index_list] = tab_copy[index_list] / tab_copy['pct']
        tab_copy.sort_values(by='id',ascending=False,inplace=True)
    index_list = define_index(data, cnt_field, target_list, sample_weight)
    cnt_tol = data['cnt'].sum()
    data_choice = data.copy()
    result = pd.DataFrame()
    for i in range(tab_copy.shape[0]):
        value = tab_copy.iloc[i]
        cnt_req = int(cnt_tol*value['pct'])
        target_min_dict = {}
        for target in target_min_list:
            target_min_dict[target] = value['min_%s' % target]
        target_max_dict = {}
        for target in target_max_list:
            target_max_dict[target] = value['max_%s' % target]
        var_cutoff = multiple_cutting(data_choice, var_list, cnt_field, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending, pct_single=pct_single, var_min=var_min, var_max=var_max, min_gain=min_gain, n_pro=n_pro)
        data_choice['flag'] = 1
        for var in var_cutoff.keys():
            direction, cutoff = var_cutoff[var]
            data_choice['flag'] = data_choice['flag'] * ((data_choice[var] < cutoff) if direction == '<' else (data_choice[var] > cutoff))
        if reverse == True:
            data_choice = data_choice.query('flag == 1')
        else:
            data_choice = data_choice.query('flag == 0')
        result = result.append(var_cutoff,ignore_index=True)
    cross_tab = pd.pivot_table(result, index='id', columns='var', values='cutoff')
    if reverse == True:
        cross_tab.sort_index(ascending=False,inplace=True)
        cross_tab = cross_tab.cummin() if ascending == True else cross_tab.cummax()
    cross_tab['region'] = cross_tab.apply(lambda x : ' and '.join(['%s %s %f' % (column,'<' if ascending == True else '>',x[column]) for column in cross_tab.columns if x[column] > 0]))
    cross_tab = cross_tab.reset_index().sort_values(by='id',ascending=True)
    data['id'] = 0
    for i in range(cross_tab.shape[0]):
        value = cross_tab.iloc[i]
        data.loc[(data['id'] == 0) & (data.index.isin(data.query(value['region']).index)), 'id'] = value['id']
    grouped = data.groupby(by='id',as_index=False)[index_list].sum()
    grouped['pct_group'] = grouped['cnt'] / cnt_tol
    for target in target_list:
        grouped['avg_%s' % target] = grouped['sum_%s' % target] / grouped['cnt_%s' % target]
    result = tab_conf.merge(cross_tab, how='left', on='id').merge(grouped[['id','pct_group']+['avg_%s' % target for target in target_list]], how='left', on='id')
    return result

def merge_cutting(data, var_list, cnt_field, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None, var_min=5, var_max=10, min_gain=0, max_weight=1, step_list=[], n_pro=30):
    def subtask(q_in, q_out, data, var_list, cnt_field, cnt_req, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, var_min, var_max, max_weight):
        while 1:
            try:
                var_weight = q_in.get(timeout=1)
            except:
                continue
            formula = ' + '.join(['%s * %f' % (var_list[i],weight) for i,weight in enumerate(var_weight) if weight > 0])
            data['value'] = data.eval(formula).round(3)
            cutoff = single_cutting(data, 'value', cnt_field, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending)
            var_num = len([1 for weight in var_weight if weight > 0])
            gap_add = sum([(weight-max_weight) for weight in var_weight if weight > max_weight])
            cutoff['gap_adj'] = cutoff['gap'] + 10 * gap_add + 100 * (var_min - var_num) * (var_num < var_min) + 100 * (var_num - var_max) * (var_num > var_max)
            cutoff[var_list] = var_weight
            q_out.put(cutoff[['gap_adj']+var_list])
    con = Concurrent(n_pro, subtask, data, var_list, cnt_field, cnt_req, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, var_min, var_max, max_weight)
    def calculate(input_list):
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        return result
    input_list = [[(1 if i == var else 0) for i in var_list] for var in var_list]
    result_all = calculate(input_list)
    opt = result_all.sort_values(by='gap_adj',ascending=True).iloc[0]
    var_weight_best = list(opt[var_list])
    gap_min = opt['gap_adj']
    for step in step_list:
        while 1:
            var_sub_1 = [var_list[i] for i,weight in enumerate(var_weight_best) if weight > max_weight]
            var_sub_2 = [var_list[i] for i,weight in enumerate(var_weight_best) if weight >= step]
            var_sub = var_sub_1 if len(var_sub_1) > 0 else var_sub_2
            var_add = [var_list[i] for i,weight in enumerate(var_weight_best) if round(weight+step,2) <= max_weight]
            var_weight_cand = []
            for var1 in var_sub:
                for var2 in var_add:
                    if var1 != var2:
                        var_weight = var_weight_best.copy()
                        var_weight[var_list.index(var1)] = round(var_weight[var_list.index(var1)]-step,2)
                        var_weight[var_list.index(var2)] = round(var_weight[var_list.index(var2)]+step,2)
                        var_weight_cand.append(var_weight)
            var_weight_cand = list(pd.concat([result_all.eval('flag=1'), pd.DataFrame(columns=var_list, data=var_weight_cand).eval('flag=0')], axis=0).drop_duplicates(subset=var_list,keep='first').query('flag=0')[var_list])
            var_weight_cand = [list(var_weight) for var_weight in var_weight_cand]
            result = calculate(var_weight_cand)
            result_all = result_all.append(result,ignore_index=True)
            if not result.empty:
                opt = result.sort_values(by='gap_adj',ascending=True).iloc[0]
                if opt['gap_adj'] > gap_min-min_gain:
                    break
                gap_min = opt['gap_adj']
                var_weight_best = list(opt[var_list])
    con.exit()
    var_choice = [var_list[i] for i,weight in enumerate(var_weight_best) if weight > 0]
    var_weight = [weight for weight in var_weight_best if weight > 0]
    return var_choice, var_weight

def grid_cutting(data, var_couple, cnt_field, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=False, min_gain=0):
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    index_list = define_index(data, cnt_field, target_list, sample_weight)
    var_x, var_y = var_couple[0], var_couple[1]
    data['bin_x'] = data[var_x].round(3)
    data['bin_y'] = data[var_y].round(3)
    bin_x = list(data['bin_x'].drop_duplicates().sort_values(ascending=ascending))
    bin_y = list(data['bin_y'].drop_duplicates().sort_values(ascending=ascending))
    mesh = pd.merge(pd.DataFrame({'bin_x':bin_x,'flag':1}), pd.DataFrame({'bin_y':bin_y,'flag':1}), how='inner', on='flag')[['bin_x','bin_y']]
    mesh = mesh.merge(data.groupby(by=['bin_x','bin_y'],as_index=False)[index_list].sum(), how='left', on=['bin_x','bin_y']).fillna(0)
    mesh.set_index(['bin_x','bin_y'])
    mesh['flag'] = 0
    choice = {}
    for index in index_list:
        choice[index] = 0
    border = []
    gap_min = np.inf
    while 1:
        if len(border) > 0:
            point_cand = []
            for i,j in enumerate(border):
                if i == 0 and j < len(var_y):
                    point_cand.append((i+1,j+1))
                elif i > 0 and j < border[i-1]:
                    point_cand.append((i+1,j+1))
            else:
                if i < len(bin_x) - 1:
                    point_cand.append((i+2,1))
        else:
            point_cand = [(1,1)]
        if len(point_cand) == 0:
            break
        cand = mesh.loc[[(bin_x[p[0]-1],bin_y[p[1]-1]) for p in point_cand]].reset_index()
        for index in index_list:
            cand[index] += choice[index]
        cand['gap'] = evaluate_gap(cand, target_list, target_min_dict, target_max_dict, target_weight, method)
        opt = cand.sort_values(by='gap',ascending=True).iloc[0]
        if min_gain >= 0 and opt['gap'] > gap_min-min_gain:
            break
        point_x = bin_x.index(opt['bin_x']) + 1
        point_y = bin_y.index(opt['bin_y']) + 1
        if point_x <= len(border):
            border[point_x-1] = point_y
        else:
            border.append(point_y)
        for index in index_list:
            choice[index] = opt[index]
        mesh.loc[(opt['bin_x'],opt['bin_y']), 'flag'] = 1
        if min_gain < 0 and opt['cnt'] >= cnt_req:
            break
    cross_tab = pd.pivot_table(mesh, index='bin_x', columns='bin_y', values='flag')
    return cross_tab

def grid_grouping(data, var_couple, cnt_field, tab_conf, sample_weight={}, target_weight={}, method='sum', ascending=False, reverse=False, min_gain=0):
    target_min_list = [column.replace('min_','') for column in tab_conf.columns if 'min_' in column]
    target_max_list = [column.replace('max_','') for column in tab_conf.columns if 'max_' in column]
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    tab_copy = tab_conf.sort_values(by='id',ascending=True)
    if reverse:
        index_list = [column for column in tab_copy.columns if 'min_' in column or 'max_' in column]
        tab_copy[index_list] = tab_copy[index_list] * tab_copy['pct']
        tab_copy[index_list] = tab_copy[index_list].cumsum()
        tab_copy['pct'] = tab_copy['pct'].cumsum()
        tab_copy[index_list] = tab_copy[index_list] / tab_copy['pct']
        tab_copy.sort_values(by='id',ascending=False,inplace=True)
    index_list = define_index(data, cnt_field, target_list, sample_weight)
    cnt_tol = data['cnt'].sum()
    var_x, var_y = var_couple[0], var_couple[1]
    data['bin_x'] = data[var_x].round(3)
    data['bin_y'] = data[var_y].round(3)
    bin_x = list(data['bin_x'].drop_duplicates().sort_values(ascending=ascending))
    bin_y = list(data['bin_y'].drop_duplicates().sort_values(ascending=ascending))
    mesh = pd.merge(pd.DataFrame({'bin_x':bin_x,'flag':1}), pd.DataFrame({'bin_y':bin_y,'flag':1}), how='inner', on='flag')[['bin_x','bin_y']]
    mesh = mesh.merge(data.groupby(by=['bin_x','bin_y'],as_index=False)[index_list].sum(), how='left', on=['bin_x','bin_y']).fillna(0)
    mesh.set_index(['bin_x','bin_y'])
    mesh['id'] = 0
    border = []
    for i in range(tab_copy.shape[0]):
        value = tab_copy.iloc[i]
        id = value['id']
        cnt_req = int(cnt_tol*value['pct'])
        target_min_dict = {}
        for target in target_min_list:
            target_min_dict[target] = value['min_%s' % target]
        target_max_dict = {}
        for target in target_max_list:
            target_max_dict[target] = value['max_%s' % target]
        choice = {}
        for index in index_list:
            choice[index] = 0
        gap_min = np.inf
        while 1:
            if len(border) > 0:
                point_cand = []
                for i,j in enumerate(border):
                    if i == 0 and j < len(bin_y):
                        point_cand.append((i+1,j+1))
                    elif i > 0 and j < border[i-1]:
                        point_cand.append((i+1,j+1))
                else:
                    if i < len(bin_x) - 1:
                        point_cand.append((i+2,1))
            else:
                point_cand = [(1,1)]
            if len(point_cand) == 0:
                break
            cand = mesh.loc[[(bin_x[p[0]-1],bin_y[p[1]-1]) for p in point_cand]].reset_index()
            for index in index_list:
                cand[index] += choice[index]
            cand['gap'] = evaluate_gap(cand, target_list, target_min_dict, target_max_dict, target_weight, method)
            opt = cand.sort_values(by='gap',ascending=True).iloc[0]
            if min_gain >= 0 and opt['gap'] > gap_min-min_gain:
                break
            point_x = bin_x.index(opt['bin_x']) + 1
            point_y = bin_y.index(opt['bin_y']) + 1
            if point_x <= len(border):
                border[point_x-1] = point_y
            else:
                border.append(point_y)
            for index in index_list:
                choice[index] = opt[index]
            mesh.loc[(opt['bin_x'],opt['bin_y']), 'id'] = id
            if min_gain < 0 and opt['cnt'] >= cnt_req:
                break
    cross_tab = pd.pivot_table(mesh, index='bin_x', columns='bin_y', values='id')
    grouped = mesh.groupby(by='id',as_index=False)[index_list].sum()
    grouped['pct_group'] = grouped['cnt'] / cnt_tol
    for target in target_list:
        grouped['avg_%s' % target] = grouped['sum_%s' % target] / grouped['cnt_%s' % target]
    grouped = tab_conf.merge(grouped[['id','pct_group']+['avg_%s' % target for target in target_list]], how='left', on='id')
    return grouped, cross_tab

######################################################################################################################################################################################################











def attr_single_cutting(data1, data2, var, target, prefix=None, ascending=None):
    data = pd.concat([data1.eval('src = 1'), data2.eval('src = 2')], axis=0)
    index_list = ['cnt_1','cnt_2','sum_1','sum_2']
    data['cnt_1'] = (data['src'] == 1) * (data[target] >= 0) * 1
    data['cnt_2'] = (data['src'] == 2) * (data[target] >= 0) * 1
    data['sum_1'] = (data['src'] == 1) * (data[target] >= 0) * data[target]
    data['sum_2'] = (data['src'] == 2) * (data[target] >= 0) * data[target]
    avg_tol_1 = data['sum_1'].sum() / data['cnt_1'].sum()
    avg_tol_2 = data['sum_2'].sum() / data['cnt_2'].sum()
    gap_tol =  avg_tol_1 - avg_tol_2
    ascending_list = [ascending] if ascending else [True,False]
    result = pd.DataFrame()
    for ascending in ascending_list:
        data['value'] = data.eval(var)
        if prefix:
            data.loc[~data.index.isin(data.query(prefix).index),'value'] = np.nan
        data.fillna(data['value'].max() if ascending == True else data['value'].min(),inplace=True)
        grouped = data.groupby(by='value',as_index=False)[index_list].sum()
        grouped.sort_values(by='value',ascending=ascending)
        grouped['cutoff'] = (grouped['value'] + grouped['value'].shift(-1)) / 2
        grouped[index_list] = grouped[index_list].cumsum()
        grouped['pct_cnt_1'] = grouped['cnt_1'] / grouped['cnt_1'].max()
        grouped['pct_cnt_2'] = grouped['cnt_2'] / grouped['cnt_2'].max()
        grouped['pct_sum_1'] = grouped['sum_1'] / grouped['sum_1'].max()
        grouped['pct_sum_2'] = grouped['sum_2'] / grouped['sum_2'].max()
        grouped['avg_tgt_1'] = grouped['sum_1'] / grouped['cnt_1']
        grouped['avg_tgt_2'] = grouped['sum_2'] / grouped['cnt_2']
        grouped['pct_gap'] = (grouped['avg_tgt_1'] * grouped['pct_cnt_1'] - grouped['avg_tgt_2'] * grouped['pct_cnt_2']) / gap_tol
        grouped['diff'] = grouped['pct_gap'] - grouped['pct_cnt_2']
        grouped['direction'] = '<' if ascending == True else '>'
        grouped['var'] = var
        result = result.append(grouped,ignore_index=True)
    columns = ['diff','var','direction','cutoff','pct_gap','gap_tol','avg_tol_1','avg_tol_2','pct_cnt_1','pct_cnt_2','pct_sum_1','pct_sum_2','avg_tgt_1','avg_tgt_2']
    cutoff = result[columns].sort_values(by='diff',ascending=False).iloc[:1]
    return cutoff



def attr_double_cutting(data1, data2, var1, var2, target, prefix=None, ascending=None):
    data = pd.concat([data1.eval('src = 1'), data2.eval('src = 2')], axis=0)
    index_list = ['cnt_1','cnt_2','sum_1','sum_2']
    data['cnt_1'] = (data['src'] == 1) * (data[target] >= 0) * 1
    data['cnt_2'] = (data['src'] == 2) * (data[target] >= 0) * 1
    data['sum_1'] = (data['src'] == 1) * (data[target] >= 0) * data[target]
    data['sum_2'] = (data['src'] == 2) * (data[target] >= 0) * data[target]
    avg_tol_1 = data['sum_1'].sum() / data['cnt_1'].sum()
    avg_tol_2 = data['sum_2'].sum() / data['cnt_2'].sum()
    gap_tol =  avg_tol_1 - avg_tol_2
    ascending_list = [(ascending,ascending)] if ascending else [(True,True),(True,False),(False,True),(False,False)]
    result = pd.DataFrame()
    for ascending in ascending_list:
        data['value1'] = data.eval(var1)
        data['value2'] = data.eval(var2)
        if prefix:
            data.loc[~data.index.isin(data.query(prefix).index),'value'] = np.nan
        data['value1'].fillna(data['value1'].max() if ascending[0] == True else data['value1'].min(),inplace=True)
        data['value2'].fillna(data['value2'].max() if ascending[1] == True else data['value2'].min(),inplace=True)
        data['flag'] = 1
        mesh = pd.merge(data[['flag','value1']].drop_duplicates(), data[['flag','value2']].drop_duplicates(), how='inner', on='flag')[['value1','value2']]
        grouped = mesh.merge(data.groupby(by=['value1','value2'],as_index=False)[index_list].sum(), how='left', on=['value1','value2']).fillna(0)
        grouped.sort_values(by='value1',ascending=ascending[0])
        grouped['cutoff1'] = (grouped['value1'] + grouped.groupby(by='value2')['value1'].shift(-1)) / 2
        grouped[index_list] = grouped.groupby(by='value2')[index_list].cumsum()
        grouped.sort_values(by='value2',ascending=ascending[1])
        grouped['cutoff2'] = (grouped['value2'] + grouped.groupby(by='value1')['value2'].shift(-1)) / 2
        grouped[index_list] = grouped.groupby(by='value1')[index_list].cumsum()
        grouped['pct_cnt_1'] = grouped['cnt_1'] / grouped['cnt_1'].max()
        grouped['pct_cnt_2'] = grouped['cnt_2'] / grouped['cnt_2'].max()
        grouped['pct_sum_1'] = grouped['sum_1'] / grouped['sum_1'].max()
        grouped['pct_sum_2'] = grouped['sum_2'] / grouped['sum_2'].max()
        grouped['avg_tgt_1'] = grouped['sum_1'] / grouped['cnt_1']
        grouped['avg_tgt_2'] = grouped['sum_2'] / grouped['cnt_2']
        grouped['pct_gap'] = (grouped['avg_tgt_1'] * grouped['pct_cnt_1'] - grouped['avg_tgt_2'] * grouped['pct_cnt_2']) / gap_tol
        grouped['diff'] = grouped['pct_gap'] - grouped['pct_cnt_2']
        grouped['direction1'] = '<' if ascending[0] == True else '>'
        grouped['direction2'] = '<' if ascending[1] == True else '>'
        grouped['var1'] = var1
        grouped['var2'] = var2
        result = result.append(grouped,ignore_index=True)
    columns = ['diff','var1','direction1','cutoff1','var2','direction2','cutoff2','pct_gap','gap_tol','avg_tol_1','avg_tol_2','pct_cnt_1','pct_cnt_2','pct_sum_1','pct_sum_2','avg_tgt_1','avg_tgt_2']
    cutoff = result[columns].sort_values(by='diff',ascending=False).iloc[:1]
    return cutoff



def rules_mining_single(data, var_list, target_list, cnt_min=100, pct_min=0.05, weight=None, ascending=False, reverse=False):
    index_list = []
    for target in target_list:
        index_list += ['Total_%s' % target, 'Bad_%s' % target, 'Good_%s' % target]
        if weight:
            data['Total_%s' % target] = (data[target] >= 0) * data[weight]
            data['Bad_%s' % target] = (data[target] >= 0) * data[weight] * data[target]
        else:
            data['Total_%s' % target] = (data[target] >= 0) * 1
            data['Bad_%s' % target] = (data[target] >= 0) * data[target]
        data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
    columns = ['iv','var','direction','cutoff']
    for target in target_list:
        columns += ['%s_%s' % (index,target) for index in ['+Total','+PctTotal','+Badrate','-Total','-PctTotal','-Badrate']]
    result = pd.DataFrame(columns=columns)
    for var in var_list:
        data['value'] = data.eval(var)
        grouped = data.groupby(by='value',as_index=False)[index_list].sum()
        grouped.sort_values(by='value',ascending=True)
        grouped['cutoff'] = (grouped['value'] + grouped['value'].shift(-1)) / 2
        grouped[['%s_1' % index for index in index_list]] = grouped[index_list].cumsum()
        for index in index_list:
            grouped['%s_2' % index] = grouped[index].sum() - grouped['%s_1' % index]
        for target in target_list:
            grouped['PctTotal_%s_1' % target] = grouped['Total_%s_1' % target] / grouped['Total_%s' % target].sum()
            grouped['PctTotal_%s_2' % target] = grouped['Total_%s_2' % target] / grouped['Total_%s' % target].sum()
            grouped['PctBad_%s_1' % target] = grouped['Bad_%s_1' % target] / grouped['Bad_%s' % target].sum()
            grouped['PctBad_%s_2' % target] = grouped['Bad_%s_2' % target] / grouped['Bad_%s' % target].sum()
            grouped['PctGood_%s_1' % target] = grouped['Good_%s_1' % target] / grouped['Good_%s' % target].sum()
            grouped['PctGood_%s_2' % target] = grouped['Good_%s_2' % target] / grouped['Good_%s' % target].sum()
            grouped['Badrate_%s_1' % target] = grouped['Bad_%s_1' % target] / grouped['Total_%s_1' % target]
            grouped['Badrate_%s_2' % target] = grouped['Bad_%s_2' % target] / grouped['Total_%s_2' % target]
            grouped['iv_%s_1' % target] = (grouped['PctBad_%s_1' % target] - grouped['PctGood_%s_1' % target]) * np.log(grouped['PctBad_%s_1' % target] / grouped['PctGood_%s_1' % target])
            grouped['iv_%s_2' % target] = (grouped['PctBad_%s_2' % target] - grouped['PctGood_%s_2' % target]) * np.log(grouped['PctBad_%s_2' % target] / grouped['PctGood_%s_2' % target])
            grouped['iv_%s' % target] = grouped['iv_%s_1' % target] + grouped['iv_%s_2' % target]
        grouped['iv'] = grouped[['iv_%s' % target for target in target_list]].apply(max,axis=1)
        grouped = grouped[(grouped['iv'] > 0) & (grouped['iv'] < np.inf)]
        for target in target_list:
            if ascending == True:
                grouped = grouped[grouped['Badrate_%s_1' % target] < grouped['Badrate_%s_2' % target]]
            else:
                grouped = grouped[grouped['Badrate_%s_1' % target] > grouped['Badrate_%s_2' % target]]
        grouped['direction'] = '<' if ascending == reverse else '>'
        for target in target_list:
            grouped['+Total_%s' % target] = grouped['Total_%s_1' % target] * (grouped['direction'] == '<') + grouped['Total_%s_2' % target] * (grouped['direction'] == '>')
            grouped['-Total_%s' % target] = grouped['Total_%s_1' % target] * (grouped['direction'] == '>') + grouped['Total_%s_2' % target] * (grouped['direction'] == '<')
            grouped['+PctTotal_%s' % target] = grouped['PctTotal_%s_1' % target] * (grouped['direction'] == '<') + grouped['PctTotal_%s_2' % target] * (grouped['direction'] == '>')
            grouped['-PctTotal_%s' % target] = grouped['PctTotal_%s_1' % target] * (grouped['direction'] == '>') + grouped['PctTotal_%s_2' % target] * (grouped['direction'] == '<')
            grouped['+Badrate_%s' % target] = grouped['Badrate_%s_1' % target] * (grouped['direction'] == '<') + grouped['Badrate_%s_2' % target] * (grouped['direction'] == '>')
            grouped['-Badrate_%s' % target] = grouped['Badrate_%s_1' % target] * (grouped['direction'] == '>') + grouped['Badrate_%s_2' % target] * (grouped['direction'] == '<')
            grouped = grouped[(grouped['+Total_%s' % target] >= cnt_min) & (grouped['+PctTotal_%s' % target] >= pct_min)]
        if not grouped.empty:
            opt = grouped.sort_values(by='iv',ascending=False).iloc[0]
            opt['var'] = var
            result = result.append(opt,ignore_index=True)
    result = result.sort_values(by='iv',ascending=False).reset_index(drop=True)[columns]
    return result


def rules_mining_deep(data, var_list, target_list, benchmark, target_lift, initial_point=[], max_depth=3, cnt_min=100, pct_min=0.05, weight=None, ascending=False, reverse=False, n_pro=30):
    def subtask(q_in, q_out, data, var_list):
        while 1:
            try:
                wher_str = q_in.get(timeout=1)
            except:
                continue
            result = rules_mining_single(data.query(wher_str) if where_str else data, var_list, target_list, cnt_min=100, pct_min=0.05, weight=None, ascending=False, reverse=False)
            for i,target in enumerate(target_list):
                result['lift_%s' % target] = result['Badrate_%s' % target] / benchmark[i]
            result['lift'] = result[['lift_%s' % target]].apply(np.mean,axis=1)
            result['flag'] = (result['lift'] <= target_lift) * (reverse == True) + (result['lift'] >= target_lift) * (reverse == False)
            result['rule'] = result['var'] + result['direction'] + result['cutoff'].astype('str')
            q_out.put(result)
    con = Concurrent(n_pro, subtask, data)
    def calculate(input_list):
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        return result
    initial_point = [None] if len(initial_point) == 0 else initial_point
    detail = pd.DataFrame()
    for point in initial_point:
        input_list = [point]
        depth = 0
        result = pd.DataFrame()
        while depth < max_depth and len(input_list) > 0:
            depth += 1
            con.put(input_list)
            output = calculate(input_list)
            choice = output.query('flag == 1')
            result = result.append(choice,ignore_index=True)
            input_list = list(output['rule'])
        detail = detail.append(result,ignore_index=True)
    con.exit()
    rule_set = list(detail['rule'])
    return rule_set, detail


def rules_filter(data_oot, data_app, rule_set, target_list, benchmark, target_lift, cnt_oot_min=100, pct_oot_min=0.05, cnt_app_min=100, weight=None, reverse=False, mode='risk', n_pro=30):
    def subtask(q_in, q_out, data_oot, data_app):
        while 1:
            try:
                rule = q_in.get(timeout=1)
            except:
                continue
            hit_oot = data_oot.query(rule)[index_list].sum()
            cnt_app_hit = data_app.query(rule).shape[0]
            if min([hit_oot['+Total_%s' % target] for target in target_list]) >= cnt_oot_min and min([hit_oot['+PctTotal_%s' % target] for target in target_list]) >= pct_oot_min and cnt_app_hit >= cnt_app_min:
                lift = np.mean([hit_oot['+Badrate_%s' % target]/benchmark[i] for i,target in enumerate(target_lift)])
                lift = (1 / lift) if reverse == True else lift
                if lift > 1:
                    if mode == 'pct':
                        lift = cnt_app_hit / cnt_app_min
                else:
                    lift = 0
            else:
                lift = 0
            q_out.put([rule,lift])
    oot_remain = data_oot.copy()
    app_remain = data_app.copy()
    rule_choice = []
    rule_remain = rule_set.copy()
    while len(rule_remain) > 0:
        con = Concurrent(n_pro, subtask, oot_remain, app_remain)
        con.put(rule_remain)
        result = []
        for i in tqdm(rule_remain):
            output = con.get()
            result.append(output)
        con.exit()
        result = pd.DataFrame(columns=['rule','lift'], data=result)
        opt = result.sort_values(by='lift',ascending=False).iloc[0]
        if opt['lift'] <= 1:
            break
        rule = opt['rule']
        oot_remain = oot_remain.loc[~oot_remain.index.isin(oot_remain.query(rule).index)]
        app_remain = app_remain.loc[~app_remain.index.isin(app_remain.query(rule).index)]
        rule_choice.append(rule)
        rule_remain = list(result.query('lift > 1')['rule'])
    return rule_choice









