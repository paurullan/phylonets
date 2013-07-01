all: test

test:
	python -m unittest discover 

nose:
	#nosetests --processes=2
	nosetests

grafic:
	python _test_grafic.py | dot -Tpng -o a.png

#dot -Tpng xarxa_1_adria.py_2.dot -o xarxa_1_adria.py_2.png

# guia per si vull fer sols un test
hasse:
	python -m unittest tests.test_hasse.TestHasse

edge:
	python -m unittest tests.test_remove_edge

lcsa:
	python -m unittest tests.test_lcsa

newick:
	python -m unittest tests.test_enewick

treechild:
	python -m unittest tests.test_random_treechild.TestTreeChildFromRandom

row:
	python -m unittest tests.test_construct_treechild_bound_row.TestRowProblematic
