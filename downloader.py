#!/usr/bin/env python3

import os
import sys
import requests
from multiprocessing.dummy import Pool
import json
seqnum = 0


def _download_image(args):
	img_url = args[0]
	seq = args[1]
	seq_count = args[2]
	filename = img_url
	global seqnum

	r = requests.get('https://images.mapillary.com/{}/thumb-2048.jpg'.format(img_url))
	with open('downloads/%s/%04.f.jpg' % (seq, seq_count), 'wb') as f:

		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
		seqnum += 1   
		sys.stdout.write("\rDownloaded {} images of {}".format(seqnum, args[3]))
		sys.stdout.flush()
def download_sequence(sequence_id, client_id):
	os.makedirs("downloads/%s" % sequence_id, exist_ok=True)

	image_list = []
	sequence_count = 0

	print("Downloading sequence information from mapillary...")
	r = requests.get('https://a.mapillary.com/v3/sequences/{}?client_id={}'.format(sequence_id, client_id))
	if "not found" in r:
		print("Invalid sequence ID!")
		return
	elif "client_id_invalid" in r:
		print("Invalid client ID!")
		return
	data = r.json()
	data2 = data['properties']
	data3 = data2['coordinateProperties']
	data4 = data3['image_keys']
	for h in data3['image_keys']:
		image_list.append((h, sequence_id, sequence_count, len(data3['image_keys'])))

		sequence_count += 1

	print("Starting download of %s images" % sequence_count)
	download_pool = Pool(4)
	download_pool.map(_download_image, image_list)
	download_pool.close()
	download_pool.join()
	print("Downloaded images into downloads/%s" % sequence_id)



sqid = input("What is your sequence ID?")
clid = input("What is your client ID?")
seqnum = 0
download_sequence(sqid, clid)
