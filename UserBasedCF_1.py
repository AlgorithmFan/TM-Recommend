#!usr/bin/env python
#coding:utf-8

import numpy as np

class CUserBasedCF:
    def __init__(self):
        pass

    def calSimilarity(self, user_A, user_B):
        '''
        Calculate the similarity between user A and user B.
        '''
        user_A_avr = float(np.sum(user_A))/len(user_A)
        user_B_avr = float(np.sum(user_B))/len(user_B)
        temp_A = user_A-user_A_avr
        temp_B = user_B-user_B_avr
        return float(np.sum(temp_A*temp_B))/np.linalg.norm(temp_A)/np.linalg.norm(temp_B)*temp_B

    def calSubRecommend(self, users_map_items, artistsList, active_user_id):
        '''
        Calculate the recommendation for the active user.
        '''
        recommendation = np.zeros(len(artistsList), 'float')
        for user_id in users_map_items:
            if user_id == active_user_id:
                continue
            recommendation += self.calSimilarity(users_map_items[active_user_id], users_map_items[user_id])

        temp = {}
        for index in range(len(artistsList)):
            if users_map_items[active_user_id][index] > 0: continue
            if recommendation[index]>0:
                temp[index] = recommendation[index]
        return temp

    def preProcess(self, mUserModels, artistsList):
        '''
        Get the average rate of items.
        '''
        artists = np.zeros(len(artistsList), 'float')
        users_map_items = {}
        for user_id in mUserModels:
            temp = np.zeros(len(artistsList), 'int')
            for artist_id in range(artists.shape[0]):
                if mUserModels[user_id].train[:, artist_id].sum()>0:
                    temp[artist_id] = 1.0
            users_map_items[user_id] = temp
            artists += temp
        return users_map_items, artists/len(mUserModels)

    def calRecommend(self, mUserModels, artistsList, top_num):
        '''
        Calculate the recommendation for all users
        '''
        users_map_items, items_avrRate = self.preProcess(mUserModels, artistsList)
        recommendation = {}
        for user_id in mUserModels:
            temp = self.calSubRecommend(users_map_items, artistsList, user_id)
            temp = sorted(temp.iteritems(), key=lambda x:x[1], reverse=True)
            recommendation[user_id] = [item_id for item_id, sim in temp[:top_num]]
        return recommendation