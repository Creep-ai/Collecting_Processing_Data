# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    following_id = scrapy.Field()
    following_name = scrapy.Field()
    following_nick = scrapy.Field()
    following_photo = scrapy.Field()
    user_id = scrapy.Field()
    follower_id = scrapy.Field()
    follower_name = scrapy.Field()
    follower_nick = scrapy.Field()
    follower_photo = scrapy.Field()
    label = scrapy.Field()
    username = scrapy.Field()


# class FollowersItem(scrapy.Item):
#     # define the fields for your item here like:
#     _id = scrapy.Field()
#     user_id = scrapy.Field()
#     follower_id = scrapy.Field()
#     follower_name = scrapy.Field()
#     follower_nick = scrapy.Field()
#     follower_photo = scrapy.Field()
#     label = scrapy.Field()
#
#
# class FollowingItem(scrapy.Item):
#     # define the fields for your item here like:
#     _id = scrapy.Field()
#     following_id = scrapy.Field()
#     following_name = scrapy.Field()
#     following_nick = scrapy.Field()
#     following_photo = scrapy.Field()
#     user_id = scrapy.Field()
#     label = scrapy.Field()
