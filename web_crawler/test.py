#coding=utf-8
import facebookapi as fbapi

dataset = fbapi.get_json_from_cloud(date='0322')
print(dataset)
# single_post_info= fbapi.get_posts_by_post_id(dataset=dataset, post_id=13)
# print(single_post_info)
# userid_list = fbapi.get_all_user_ids(dataset)
# print(userid_list)
# post_list = fbapi.get_all_posts_by_type(dataset=dataset, type='Q&A')
# print(post_list)
# comment_list = fbapi.get_all_main_comments_by_post_id_user_id(dataset=dataset, post_id=1, user_id='Nicolas Hei')
# print(comment_list)
# comment_list=fbapi.get_all_below_comments_by_post_id_user_id(dataset=dataset, post_id=1, user_id='Nicolas Hei')
# print(comment_list)
# emoji_list = fbapi.get_post_emojis_by_post_id(dataset=dataset, post_id=1)
# print(emoji_list)
# user_emojitimes = fbapi.get_all_posts_emojis_times_by_user_id(dataset=dataset, user_id='Jason Chen')
# print(user_emojitimes)
# data = fbapi.get_all_posts_all_user_comments_times(dataset=dataset)
# print(data)
# allemojitimes = fbapi.get_user_emoji_times_by_user_id(dataset=dataset, user_id='Jason Chen')
# print(allemojitimes)
# date_list=fbapi.get_fine_dataset_date()
# print(date_list)
# print(dataset["member_info"])
