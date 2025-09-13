# Ambavia scripts
Scripts for https://github.com/fadaaszhi/ambavia to make it easier to use. 

## extract_latex.py
Use this to extract the equations from yuor graph. Go to your graph, do Calc.getExpressions(), copy object, and save it into a file. Then do `python extract_latex.py <input.json> <output.txt>`. Output file will be contain all equations seperated by a newline.

## line_sender.py
Use this to write the output of `extract_latex.py` into ambavia. Run `extract_latex.py` and then open your ambavia build. Run `python line_sender.py <input.txt> -d`. Select the ambavia window from the options, focus the ambavia gui, and put your cursor on the first line. It is **HIGHLY** encourage to disable debug logging in `src\compiler.rs:213`, if you dont ambavia will probably freeze. `-d` for delay between pasting each line.
