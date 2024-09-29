this website/tool works by importing the questions.txt in the resources folder. 
Html NEEDS to run in a web server environment to be able to import files like this. 
if you want to run the quiz OFFLINE i recommend using this simple web server: https://simplewebserver.org/
it creates a very basic web server, you can select the folder with index.html in it and click the blue link and the quiz should open.
NOTE: reloading the webpage reset's the quiz


----------------------------------------
editing or adding questions

when you click any button for the first time it reloads the questions.txt so you don't have to reload the page when answering questions.

editing or adding questions can easily be done by changing the questions.txt file in the resources folder.
we use the :: as a separator (so only use it as such).
the structure consists out of an arbitrary amount of 

::keyword::text

where keyword ìs a specified word in the list below and text is just some text (including next-lines/enters)
for text you can put something in between two ` to make it a code block. 
You can use:
<img nameOfImage.png the (optional) description go's here>
to import images placed in the /resources/images/ folder. (does not have to be .png , .jpeg etc. will work fine)

[link url text to be displayed]

[download {name of file in /resources/files/} text to be displayed]

list of keywords:
::text:: text is just some text it is used to give information.

::question:: question is like test but is to be used when asking a question and had a slightly different colour to signal this.

::wrong:: wrong should be after either a question or a correct. this is a clickable button that will be used for wrong answers. you can have as many of these as you want.

::correct:: correct should be after either a question or a wrong. this is used for correct answers if clicked it will turn green and reveal the next question. each question needs one and only one correct answer.

::exact:: use this instead of ::correct:: will create a textbox for the user to input something will be correct if it matches exactly what follows. (ignores spaces on the start and end, is not case sensitive) it will also accept the word "skip" to skip questions
----------------------------------------
Editing overview text.

You can edit the overview text (top box on the overview page) by changing the overview.txt.
It has the same parsing as the text from the questions section (codeblocks and images).
I don't know why you would want to change it but i didn't want to hardcode it.