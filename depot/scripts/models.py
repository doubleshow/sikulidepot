from django.db import models

import sikulihelper as sh
import short_url as surl

STATIC_ROOT = '/home/ec2-user/static'
STATIC_URL  = '/static'


class Script(models.Model):
	basename = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	mod_date = models.DateTimeField('date modifiled')
   	pub_date = models.DateTimeField('date published')
  	text = models.TextField()
	
	def __unicode__(self):
		return self.title

	def highlighted_text(self):
		return sh.highlight(self.text,"/static/p/%s" % self.url())

	def url(self):
		return surl.encode_url(self.id)

	def image_url(self):
		return "p/%s" % self.url()

	def download_url(self):
		return "skl/%s/%s.skl" % (self.url(), self.basename)

	@staticmethod
	def get_id_from_url(url):
		return surl.decode_url(url)

class PatternImage(models.Model):
	script = models.ForeignKey(Script)
	basename = models.CharField(max_length=200)

	def __unicode__(self):
		return self.basename

	def url(self):
		urlstring = surl.encode_url(self.script_id)
		return "%s/%s" % (self.script.image_url(), self.basename)

import datetime

import re
import os.path
import os
import shutil

def extract_image_references(text):
	return re.findall('[\'\"](.*\.png)[\'\"]',text)


import subprocess
def skl2sikuli(skl, outdir):
	"""Decompres .skl and save the output in <outdir>, return
	 the path to the .sikuli bundle, which should be a sub-directory
	 in <outdir>, It is the caller's responsiblity to ensure 
	 <outdir> is unique and the content is cleared up afterward
	"""
	(p,ext) = os.path.splitext(skl)
	name = os.path.basename(p)
	dest = "%s/%s.sikuli" % (outdir, name)
	cmd = ['unzip','-o',skl,'-d',dest]
	subprocess.call(cmd)
	return dest

import tempfile
import shutil
def import_skl(skl):
	# create a temp directory to store the extracted .skl content
	tmpdir = tempfile.mkdtemp()
	sikulidir = skl2sikuli(skl, tmpdir)	
	script = create_script(sikulidir)
	shutil.rmtree(tmpdir)
	
	return script

def create_script(inputdir):
	"""Take a sikuli directory (e.g., apple.sikuli) and create a 
	database record for this script"""
	basename = re.findall("\/([^\/]*?)\.sikuli\/*$", inputdir)[0]
	
	# TODO: change to finding the only .py in the bundle
	pyfile = "%s/%s.py" % (inputdir, basename)
	f = open(pyfile,'r')
	text = f.read()

	script = Script()
	script.basename = basename
	script.title = "untitled"
	script.pub_date = datetime.datetime.now()
	script.mod_date = datetime.datetime.now()
	script.text = text
	script.save()

	# create a static directory to hold the images of this script
	destdir = '%s/%s' % (STATIC_ROOT, script.image_url())
	os.mkdir(destdir)

	# extract all image references
	imgrefs = re.findall('[\'\"](.*?\.png)[\'\"]',text)
	
	for imgref in imgrefs:
		print "> " + imgref
		imgref_path = "%s/%s" % (inputdir, imgref)

		# check if a referred image can be fond in the dir
		if os.path.exists(imgref_path):
			# if so, create a new patternimage record
			ptnimage = PatternImage.objects.create(script = script,
				basename = imgref)
			
			# move image to static directory
			shutil.move(imgref_path, destdir)
			print ptnimage

	return script

def import_script_from_uploaded_file(f):
	# save the uploaded file in a tmp folder
	tmpdir = tempfile.mkdtemp()
	skl = tmpdir + '/' + f.name

	destination = open(skl, 'wb+')	
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()

	script = import_skl(skl)

	# move the uploaded skl file to static file locations
	skl_dest = '%s/%s' % (STATIC_ROOT, script.download_url())
	os.mkdir(os.path.dirname(skl_dest))
	#cmd  = ['mv',skl,skl_dest]
	#subprocess.call(cmd)
	shutil.move(skl,skl_dest)
	os.rmdir(tmpdir)

	return script


def import_script_from_directory(directory):
	print directory
	print "test1"
	print "tx"
	s = Script()
	s.basename = "test"
	s.title = "A test script"
	s.mod_date = datetime.datetime.now()
	s.pub_date = datetime.datetime.now()
	s.content = "click('test.png')"
	s.save()
