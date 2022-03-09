#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import concurrent.futures
import argparse
from common import aliyunsdk,tencentsdk,wangsusdk,huaweisdk,baidusdk


def main(filename):
	res = []
	black = []
	output = []
	_iplist = open(filename).read().splitlines()



	tencentsdk_executor = concurrent.futures.ThreadPoolExecutor(max_workers=15)
	wangsusdk_executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
	baidusdk_executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
	aliyunsdk_executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

	# huaweisdk_executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

	_tencentsdk = {tencentsdk_executor.submit(tencentsdk.main, ip): ip for ip in _iplist}
	_wangsusdk = {wangsusdk_executor.submit(wangsusdk.main, ip): ip for ip in _iplist}
	_baidusdk = {baidusdk_executor.submit(baidusdk.main, ip): ip for ip in _iplist}
	_aliyunsdk = {aliyunsdk_executor.submit(aliyunsdk.main, ip): ip for ip in _iplist}

	# _huaweisdk = {huaweisdk_executor.submit(huaweisdk.main, ip): ip for ip in _iplist}

	# for future in concurrent.futures.as_completed(_huaweisdk):
	# 	data = future.result()
	# 	print(data)

	for future in concurrent.futures.as_completed(_tencentsdk):
		data = future.result()
		print(data)
		res.append(data)


	for future in concurrent.futures.as_completed(_wangsusdk):
		data = future.result()
		print(data)
		res.append(data)

	for future in concurrent.futures.as_completed(_baidusdk):
		data = future.result()
		print(data)
		res.append(data)

	for future in concurrent.futures.as_completed(_aliyunsdk):
		data = future.result()
		print(data)
		res.append(data)

	for _n in res:
		try:
			if _n.split(',')[0] not in output:

				if _n.split(',')[2].lower() == 'yes' or _n.split(',')[2].lower() == 'true':
					black.append(_n.split(',')[0])

				else:
					if _n.split(',')[0] not in output:
						output.append(_n.split(',')[0])

			else:
				if _n.split(',')[2].lower() == 'yes' or _n.split(',')[2].lower() == 'true':
					black.append(_n.split(',')[0])
			if _n.split(',')[0] in black:
				output.remove(_n.split(',')[0])
			else:
				if _n.split(',')[0] not in output:
					output.append(_n.split(',')[0])
		except:
			pass

	print('*****开始写入原始数据*****')
	with open('res.txt','a+') as file:
		for i in res:
			if i is not None:
				file.write(i+'\n')

	print('*****开始写入真实IP*****')
	with open('real_ip.txt','a+') as rfile:
		for _i in output:
			if _i is not None:
				rfile.write(_i+'\n')

def offline(filename):
	res = []
	output = []
	black = []

	with open(filename,'r') as file:
		for i in file:
			res.append(i.rstrip())

	for _n in res:
		try:
			if _n.split(',')[0] not in output:

				if _n.split(',')[2].lower() == 'yes' or _n.split(',')[2].lower() == 'true':
					black.append(_n.split(',')[0])

				else:
					if _n.split(',')[0] not in output:
						output.append(_n.split(',')[0])

			else:
				if _n.split(',')[2].lower() == 'yes' or _n.split(',')[2].lower() == 'true':
					black.append(_n.split(',')[0])
			if _n.split(',')[0] in black:
				output.remove(_n.split(',')[0])
			else:
				if _n.split(',')[0] not in output:
					output.append(_n.split(',')[0])
		except:
			pass

	print('*****开始写入真实IP*****')
	with open('real_ip_office.txt','a+') as rfile:
		for _i in output:
			if _i is not None:
				rfile.write(_i+'\n')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='查询IP是否使用CDN')
	parser.add_argument("file",help="iplist.txt")
	parser.add_argument("-task", help="online / offline")
	args = parser.parse_args()
	if args.task == 'online':
		main(args.file)
	else:
		offline(args.file)
