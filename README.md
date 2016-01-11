```
  ____           _                    ____                      _     
 / ___|__ _ _ __| |_ ___   ___  _ __ / ___|  ___  __ _ _ __ ___| |__  
| |   / _` | '__| __/ _ \ / _ \| '_ \\___ \ / _ \/ _` | '__/ __| '_ \ 
| |__| (_| | |  | || (_) | (_) | | | |___) |  __/ (_| | | | (__| | | |
 \____\__,_|_|   \__\___/ \___/|_| |_|____/ \___|\__,_|_|  \___|_| |_|
                                                                      
Charlie Hack
The New Yorker Magazine
January 2016
```
Introduction
============
This module is intended to replace the search functionality on The Cartoon Bank search engine. It implements the "Search by Cartoon" feature, which enables the user to select a cartoon and find the most similar cartoons from the ~80,000 cartoons in the collection.

Planned features include search by text and search by image.


Installation
============
```
$ python setup.py install

```
Should suffice to process dependencies.

Usage
=====
```
>>> from cartoonsearch import search_by_id
>>> search_by_id(60005)

[ target cartoon raw text ]
 amy parents are the same way. lots of ostentatious child-rearing,very little direct nurturing.a (two children talking )children,parents,trends,nannies, modern life, psychobabble"my parents are the same way. lots of ostentatious child-rearing, very little direct nurturing." one child in a striller who is being pushed by a nanny says to another who is also being pushed by a nanny.  25370 amy parents are the same way. lots of ostentatious child-rearing, very little direct nurturing.a 8/16/1993

==[ fetching results... ]==
[ result #1 cartoon raw text ]
 amy parents are the same way. lots of ostentatious child-rearing,very little direct nurturing.a (two children talking )children,parents,trends,nannies, modern life, psychobabble"my parents are the same way. lots of ostentatious child-rearing, very little direct nurturing." one child in a striller who is being pushed by a nanny says to another who is also being pushed by a nanny.  25370 amy parents are the same way. lots of ostentatious child-rearing, very little direct nurturing.a 8/16/1993

[ result #2 cartoon raw text ]
 ated was severely edited as a child.a, ted, severely, child ated was severely edited as a child.a 10/17/2011

[ result #3 cartoon raw text ]
 "it isn't that i don't want to take you, but don't you see? we're here and disneyland is way,way over here."(father to his children as he shows than a map of the u.s.)  parents parenting family children kids families family childhood child rearing  travel trip journey vacation holiday  vacation vacations trip journey break  distance far away drs 68805 rde richard decker ait isnat that i donat want to take you, but donat you see? weare here and disneyland is way, way over here.a 9/17/1955

[ result #4 cartoon raw text ]
 children, parenting, modernl lifeaboth of you are rotten and hatefulafrom a kidas perspective.a"both of you are rotten and hateful--from a kid's perspective." child to parents about his messy room.  artkey 29899 aboth of you are rotten and hatefulafrom a kidas perspective.a 1/15/1990

[ result #5 cartoon raw text ]
 79869 dre donald reilly amy father was one of the anest snakes iave ever known.a (one snake to another.)  animal animals another children families family fatherhood grass kids one parenting parents paternity remembrance snake talking amy father was one of the anest snakes iave ever known.a 3/6/1971

[ result #6 cartoon raw text ]
 111712 gpr george price  (children's nurse skipping rope with child on her shoulders.)  boy boys child childhood children children's families family fun game games girl girls housekeeper housekeeping jump jumping kid kids little maid nanny nurse parenting parents play playing rearing rope shoulders skip skipping youth  2/7/1942

[ result #7 cartoon raw text ]
 104700 wst william steig ayou might spend a little time at home!a (tiny boy to parents going out for formal evening.)  attention boy child childhood children dining evening families family formal going kids leaving never out parent parenting parents quality rearing tiny ayou might spend a little time at home!a 4/30/1932

[...]
```

TODO:
=====
- scrape thumbnails from CartoonBank and display
- search by text
- javascript frontend
- hosting