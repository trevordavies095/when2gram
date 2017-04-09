"""
Name   : L Trevor Davies
Program: when2gram.py
Date   : April 8th, 2017
"""


import argparse
import imageio
from datetime import datetime
from InstagramAPI import InstagramAPI


def term_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("instagram_credentials", type=str, help=".txt with instagram credentials")
	return parser.parse_args()


def get_credentials(file_name):
	# Local variables
	count = 0
	user = ""
	pswd = ""

	# ******** start get_credentials() ******** #

	# Get keys from file
	f = open(file_name, "r")
	for line in f:
		if line.strip()[0] == "#":
			continue
		elif count == 0:
			user = line.strip()
			count += 1
		elif count == 1:
			pswd= line.strip()
			count += 1
	f.close()

	instagram = InstagramAPI(user, pswd)
	return instagram


def get_feed(instagram):
	# Local variables
	feed = instagram.getTotalSelfUserFeed()
	time_likes = {}
	time_posts = {}
	avg_time   = {}

	# ******** start get_feed() ********#
	
	for ranked_items in feed:

		# Get likes and hour posted
		likes = ranked_items["like_count"]

		# There's probably a much easier way to do this
		utc = str(datetime.utcfromtimestamp(ranked_items["taken_at"]))
		utc = utc.split(" ")
		hour = int(utc[1][0:2])
		if hour < 4:
			hour += 20
		else:
			hour -= 4

		# Update the time:likes dictionary
		if hour in time_likes:
			time_likes[hour] += likes
		else:
			time_likes.update({hour:likes})

		# Update the time:posts dictionary
		if hour in time_posts:
			time_posts[hour] += 1
		else:
			time_posts.update({hour:1})

	# Calculate avg of likes at hours posted, save in avg:time dictionary
	for hour in time_likes:
		avg_time.update({time_likes[hour] / time_posts[hour]:hour})

	# Sort likes in descending order
	avgs = list(avg_time.keys())
	avgs.sort(reverse=True)

	print("Results")
	print("-----------------")
	print("1. " + str(avg_time[avgs[0]]) + ":00, you average " + str(round(avgs[0])) + " likes.")
	print("2. " + str(avg_time[avgs[1]]) + ":00, you average " + str(round(avgs[1])) + " likes.")
	print("3. " + str(avg_time[avgs[2]]) + ":00, you average " + str(round(avgs[2])) + " likes.")
	print("-----------------\n")


def main():
	# Local variables
	args = term_args()

	# ******** start main() ******** #

	instagram = get_credentials(args.instagram_credentials)
	instagram.login()

	get_feed(instagram)


if __name__ == "__main__":
	imageio.plugins.ffmpeg.download()
	main()