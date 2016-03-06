# stest
## install/uninstall
	#install
		sudo python setup.py bdist_egg
		sudo python ./setup.py install --record install.txt

	#uninstall
		sudo cat install.txt | xargs rm -rf

	#run
		stest
		"stest -h" for help


  #参考资料：
  	https://docs.python.org/2/distutils/setupscript.html
    http://yansu.org/2013/06/07/learn-python-setuptools-in-detail.html
# cmd


# contact

	email: byonecry@qq.com for more help
	blog:wongming.cn
