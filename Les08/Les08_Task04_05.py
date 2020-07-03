# 4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
# 5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
from pprint import pprint

from pymongo import MongoClient


def find_followers(username):
    followers_list = []
    client = MongoClient('localhost', 27017)
    db = client['instagram_scrapy']
    instagram = db.users
    user_id = instagram.find_one({'username': username}, {'user_id': 1})['user_id']
    for follower in db[f'{user_id}'].find({'label': 'follower'}):
        followers_list.append(follower)
    client.close()
    return followers_list


def find_followings(username):
    following_list = []
    client = MongoClient('localhost', 27017)
    db = client['instagram_scrapy']
    instagram = db.users
    user_id = instagram.find_one({'username': username}, {'user_id': 1})['user_id']
    for following in db[f'{user_id}'].find({'label': 'following'}):
        following_list.append(following)
    client.close()
    return following_list


username = input('Введите ник пользователя: ')

print(f'Пользователь:{username}\n'
      f'Всего подпиcчиков:{len(find_followers(username))}\n'
      f'Список подписчиков:\n{find_followers(username)}\n')
print(f'Пользователь:{username}\n'
      f'Всего подписок:{len(find_followings(username))}\n'
      f'Список подписок:\n{find_followings(username)}\n')

