# Python File Orginizer
tested for linux


## How to ->
costantly check the download directory.
if i find a new file - given a regular language => i chose where to put it. 
defining the regular language:
 - with some particular uni-prefix (es. (comb|ling|ott|so|reti)-([a-z])-* it need to be inserted in the correct directory path/to/uni/[subject]) =>
    - where [subject] is the first argument
    - and the block [a-z] indicates the sub-directory (by default "lucidi")
 - that works even for the main linux directories: (Documents|Downloads|Music|Pictures|Public|Templates|Videos)-([a-z]|[A-Z]|\d)*
 - if no directories is specified, then it's gonna look for the extencion => ex. \*.pdf => Pictures
 - the only tag nd-\*(no directory) => will specify that it remains in the Downloads
