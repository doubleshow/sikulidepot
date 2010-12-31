from django.db import models

import sikulihelper as sh

# Create your models here.
class Script(models.Model):
	basename = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	mod_date = models.DateTimeField('date modifiled')
   	pub_date = models.DateTimeField('date published')
  	text = models.TextField()
	
	def __unicode__(self):
		return self.title

	def highlighted_text(self):
		return sh.highlight(self.text,"/static/%d" % self.id)

class PatternImage(models.Model):
	script = models.ForeignKey(Script)
	basename = models.CharField(max_length=200)

	def __unicode__(self):
		return self.basename

	def url(self):
		return "%d/%s" % (self.script_id, self.basename)

import datetime

import re
import os.path
import os
import shutil

def extract_image_references(text):
	return re.findall('[\'\"](.*\.png)[\'\"]',text)

import subprocess
def skl2sikuli(skl, outdir):
	(p,ext) = os.path.splitext(skl)
	name = os.path.basename(p)
	dest = "%s/%s.sikuli" % (outdir, name)
	cmd = ['unzip','-o',skl,'-d',dest]
	print cmd
	subprocess.call(cmd)
	return dest

def import_skl(skl):
	sikuli = skl2sikuli(skl, "tmp")
	return create_script(sikuli)

def create_script(inputdir):
	'Take a sikuli directory (e.g., apple.sikuli) and get the text of the .py file'
	basename = re.findall("\/([^\/]*?)\.sikuli\/*$", inputdir)[0]
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
	destdir = 'static/%d' % script.id
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
			
			# copy image to static directory
			shutil.copy(imgref_path, destdir)
			print ptnimage

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
