# PutToWeb a Static Site Generator. 
## Introduction
Markdown is an awesome way to format text in a texteditor and can be interpreted easily by humaneye. On the otherhand, HTML seams simple with its tags approach but can be quite unintuive to write. To allow me to create an a static website based on markdown text this project was concoured. if you inspect the [content](https://github.com/LS-2ednar/PutToWeb/tree/main/content) and its subdirectories you can see the markdown that was written. Glories stuff about LoTR!!! Id you inspect the [docs](https://github.com/LS-2ednar/PutToWeb/tree/main/docs) directory you can see the html code which was generated to host my first webpage on Github which you can reach with this [Link](https://ls-2ednar.github.io/PutToWeb/).

Another cool thing about this project is that there are 76 unittests which hopefully did catch all edgecases for my codebase.

## How to use this codebase
1. `gitclone https://github.com/LS-2ednar/PutToWeb`
2. Write your content and store it in your content directory
3. Using `./main.sh` you can create a locally hosted version of your static site when checking out `https://localhost:8888/`
4. When you are ready to push your website to the web, `./build.sh`
5. On Github in your repo go to `Settings` -> `Pages` -> at the source select `main` and `docs` as this is where src/main.py will save the html for your webpage. 

## Used libraries
- os
- sys
- Unittest for Unittests

## Future improvements
- Add documentation on how to host pages on another domain