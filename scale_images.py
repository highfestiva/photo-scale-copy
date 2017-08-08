#!/usr/bin/env python2.7


import PIL.Image
import os
import shutil
import sys


img_extensions = set([".JPG", ".jpg"])
imgcnt = 0
w = 320
h = 240
imgindex = 0


def filterout(path):
	path = path.upper()
	if "\\." in path or "/." in path or "ORIGINALS" in path:
		return True
	return False


def walk_count_files(_, dirname, names):
	if filterout(dirname):
		return
	for n in names:
		if n[-4:] in img_extensions:
			global imgcnt
			imgcnt += 1
			# print(dirname, n, imgcnt)
	sys.stdout.write("\rCounting: %i images." % imgcnt)
	#print dirname, names


def countfiles(sourcedir):
	imgcnt = 0
	for root, dirs, files in os.walk(sourcedir):
		walk_count_files(None, root, files)
	print()


def walk_scale_files(targetdir, dirname, names):
	# print('yes!')
	# print(targetdir, dirname, names)
	if filterout(dirname):
		return
	for n in names:
		if n[-4:] in img_extensions:
			global w
			global h
			global imgindex
			global imgcnt
			sys.stdout.write("\r%s (%.1f %%)                     \n" % (os.path.join(dirname, n), imgindex*100.0/imgcnt))
			try:
				im = PIL.Image.open(os.path.join(dirname, n))
				ratio = min(w/float(im.size[0]), h/float(im.size[1]))
				#print
				#print "Previous size:", im.size, "ratio:", ratio
				im = im.resize(tuple(int(x*ratio) for x in im.size), PIL.Image.ANTIALIAS)
				subdir = os.path.join(targetdir, "%3.3i" % (imgindex//100))
				if not os.path.exists(subdir):
					os.mkdir(subdir)
				outname = "%i.jpg" % imgindex
				fullname = os.path.join(subdir, outname)
				im.save(fullname, "JPEG", quality=98)
			except Exception as e:
				print()
				print(e)
				sys.exit(1)
			imgindex += 1


def scalefiles(sourcedir, targetdir, width, height):
	global w
	global h
	w = width
	h = height
	global imgindex
	imgindex = 0
	for root, dirs, files in os.walk(sourcedir):
		walk_scale_files(targetdir, root, files)
	print()


def main():
	if len(sys.argv) == 5:
		srcdir = sys.argv[1]
		tgtdir = sys.argv[2]
		width = int(sys.argv[3])
		height = int(sys.argv[4])
		countfiles(srcdir)
		try:
			shutil.rmtree(tgtdir)
		except:
			pass
		try:
			os.mkdir(tgtdir)
		except:
			pass
		scalefiles(srcdir, tgtdir, width, height)
	else:
		print("Usage: %s <src dir> <tgt dir> <width> <height>" % sys.argv[0])
		print(sys.argv)
		sys.exit(1)


if __name__ == "__main__":
	main()
