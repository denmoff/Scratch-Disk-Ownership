#!/usr/bin/python

########################## volume_ownership.py #######################
#
# Created by Dennis Moffett
# February 1, 2014
# Rutgers University
#
#
# Purpose: This script will check to make sure a secondary scratch 
# disk is set set to 'ignore ownership' and will set it if it is not.
# It will look for internally mounted disks that are hfs formated that
# are not the root volume.
######################################################################

import os, re, sys, subprocess

du_cmd = '/usr/sbin/diskutil'
volumes_path = '/Volumes/'

def ignore_ownership_volume(vol):
	# check to make sure they are attached via sata
	# that it is an hfs partition
	# and that it is not the primary boot volume
	vol_info = volume_dict(vol)		# sets vol_info to a dictionary containing all info from diskutil
	if vol_info:					# only runs if vol_info has info in it
		if vol_info['Type (Bundle)'] == 'hfs' \
		and vol_info['Mount Point'] != '/' \
		and vol_info['Internal'] == 'Yes' \
		and vol_info['Owners'] == 'Enabled':
			print 'Setting volume %s to ignore ownership' % (vol_info['Volume Name'])
			p = subprocess.call([du_cmd, 'disableOwnership', vol], shell=False)
		else:
			pass


def return_list_volumes(dir):
	# given directory, return list of volume names
	# return vol_list
	dir_list = []
	dir_list = os.listdir(dir)
	return dir_list

def volume_dict(vol):
	# gets the info of the volume and returns the dictionary: info.
	info = subprocess.Popen([du_cmd, 'info', vol], \
		stderr=subprocess.PIPE, \
		stdout=subprocess.PIPE, \
		shell=False)
	stdout, stderr = info.communicate()
	info = {}
	for line in stdout.splitlines():
		match = re.search('(\s*)(.+):(\s*)(.+)',line)
		if match and match.group(2) != 'Could not find disk': # sometimes volumes are listed in /Volumes but they are no longer mounted
			info[match.group(2)] = match.group(4)	# builds the dictionary: info.
	return info

def main():
	# get list of volumes to check
	dir_list = return_list_volumes(volumes_path)
	# step thru each volume and set volume to ignore ownership if meets criteria.
	for vol in dir_list:
		ignore_ownership_volume(vol)
		


if __name__ == "__main__":
    main()
